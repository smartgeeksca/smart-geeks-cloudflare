/**
 * OPTIONAL "Advanced Mode" bundle for deploying WITHOUT Wrangler AND
 * without connecting a Git repository -- i.e. the Cloudflare dashboard's
 * "Drag and drop your files" / Direct Upload flow.
 *
 * WHY THIS FILE EXISTS: verified against Cloudflare's own docs while this
 * project was built, dashboard drag-and-drop deployments do NOT compile a
 * `functions/` directory -- only Git-connected builds and Wrangler do that.
 * Drag-and-drop DOES support a single `_worker.js` file at the root of the
 * uploaded output ("Advanced Mode"), so this file reimplements the same
 * two Pages Functions (contact.js + _middleware.js) as one self-contained
 * Worker, for people who specifically want drag-and-drop with no CLI and
 * no Git.
 *
 * HOW TO USE:
 *   1. Run `python3 build.py` as normal.
 *   2. Copy THIS file into public/_worker.js
 *        cp alt-deploy/_worker.js public/_worker.js
 *   3. Drag the whole public/ folder into the Cloudflare dashboard
 *      (Workers & Pages -> Create -> Pages -> Drag and drop your files).
 *   4. Set the same environment variables/secrets described in
 *      DEPLOYMENT.md (Settings -> Environment variables works the same way
 *      for a Direct Upload project as any other Pages project).
 *
 * DO NOT commit this into public/_worker.js permanently if you might
 * switch to Git-connected deploys later -- Advanced Mode with a
 * `_worker.js` present takes over ALL routing (including static assets,
 * handled below via `env.ASSETS.fetch`), which is unnecessary complexity
 * you don't need once Cloudflare's own build system is compiling
 * `functions/` for you. See DEPLOYMENT.md "Deploying without Wrangler" for
 * the full comparison of both no-wrangler paths.
 *
 * MAINTENANCE NOTE: this duplicates functions/api/contact.js and
 * functions/_middleware.js by necessity (drag-and-drop performs no build
 * step, so this file must be fully self-contained -- it cannot `import`
 * from another local file). If you edit either of those two files, port
 * the same change here, then run `python3 scripts/check_worker_sync.py`
 * to confirm the two versions haven't drifted apart on the parts that
 * matter (field names, limits, required fields, the email endpoint, the
 * production hostnames).
 */

// ---- from functions/_middleware.js ----------------------------------------
const PRODUCTION_HOSTNAMES = new Set(["www.smartgeeks.ca", "smartgeeks.ca"]);

function applyNoindex(response, hostname) {
  if (PRODUCTION_HOSTNAMES.has(hostname)) return response;
  const headers = new Headers(response.headers);
  headers.set("X-Robots-Tag", "noindex, nofollow, noarchive");
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers,
  });
}

// ---- from functions/api/contact.js -----------------------------------------
const MAX_LENGTHS = { name: 100, contact: 150, device: 80, message: 1000 };
const REQUIRED_FIELDS = ["name", "contact", "device", "message", "consent"];
const ALLOWED_PREFERRED_CONTACT = new Set(["email", "phone", "whatsapp"]);

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function sanitizeField(value, maxLen) {
  if (typeof value !== "string") return "";
  const cleaned = value.replace(/[\r\n]{3,}/g, "\n\n").replace(/[\x00-\x08\x0B\x0C\x0E-\x1F]/g, "");
  return cleaned.trim().slice(0, maxLen);
}

function jsonResponse(status, body) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8" },
  });
}

function wantsJson(request) {
  const accept = request.headers.get("Accept") || "";
  return accept.includes("application/json");
}

function redirectResponse(location) {
  return new Response(null, { status: 303, headers: { Location: location } });
}

async function isRateLimited(env, ip) {
  if (!env.RATE_LIMIT_KV || !ip) return false;
  const key = `contact-rl:${ip}`;
  const last = await env.RATE_LIMIT_KV.get(key);
  if (last) return true;
  await env.RATE_LIMIT_KV.put(key, "1", { expirationTtl: 20 });
  return false;
}

async function sendEmail(env, { subject, text, html }) {
  if (!env.CF_ACCOUNT_ID || !env.CF_EMAIL_API_TOKEN || !env.CONTACT_TO_EMAIL || !env.CONTACT_FROM_EMAIL) {
    return { ok: false, reason: "not_configured" };
  }
  const res = await fetch(
    `https://api.cloudflare.com/client/v4/accounts/${env.CF_ACCOUNT_ID}/email/sending/send`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${env.CF_EMAIL_API_TOKEN}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ to: env.CONTACT_TO_EMAIL, from: env.CONTACT_FROM_EMAIL, subject, text, html }),
    }
  );
  if (!res.ok) return { ok: false, reason: "provider_error", status: res.status };
  return { ok: true };
}

async function handleContactPost(request, env) {
  const asJson = wantsJson(request);

  let form;
  try {
    form = await request.formData();
  } catch (err) {
    if (asJson) return jsonResponse(400, { ok: false, message: "We couldn't read your submission. Please try again." });
    return redirectResponse("/contact/?error=parse");
  }

  const honeypot = (form.get("website") || "").toString();
  if (honeypot) {
    if (asJson) return jsonResponse(200, { ok: true });
    return redirectResponse("/thank-you/");
  }

  const ip = request.headers.get("CF-Connecting-IP");
  if (await isRateLimited(env, ip)) {
    const message = "Too many submissions from this connection recently. Please wait a moment and try again, or call/WhatsApp us directly.";
    if (asJson) return jsonResponse(429, { ok: false, message });
    return redirectResponse("/contact/?error=rate");
  }

  const raw = {
    name: form.get("name"),
    contact: form.get("contact"),
    device: form.get("device"),
    message: form.get("message"),
    preferred_contact: form.get("preferred_contact"),
    consent: form.get("consent"),
    page: form.get("page"),
  };

  const missing = REQUIRED_FIELDS.filter((f) => !raw[f] || String(raw[f]).trim() === "");
  if (missing.length) {
    const message = "Please fill in all required fields, including consent, and try again.";
    if (asJson) return jsonResponse(400, { ok: false, message, missing });
    return redirectResponse("/contact/?error=validation");
  }

  const name = sanitizeField(raw.name, MAX_LENGTHS.name);
  const contact = sanitizeField(raw.contact, MAX_LENGTHS.contact);
  const device = sanitizeField(raw.device, MAX_LENGTHS.device);
  const message = sanitizeField(raw.message, MAX_LENGTHS.message);
  const preferredContact = ALLOWED_PREFERRED_CONTACT.has(String(raw.preferred_contact))
    ? String(raw.preferred_contact)
    : "unspecified";
  const sourcePage = sanitizeField(raw.page || "", 200) || "unknown page";

  if (!name || !contact || !device || !message) {
    const errMsg = "Please fill in all required fields with valid values and try again.";
    if (asJson) return jsonResponse(400, { ok: false, message: errMsg });
    return redirectResponse("/contact/?error=validation");
  }

  const looksLikeEmail = contact.includes("@");
  const looksLikePhone = /^[0-9()+\-.\s]{7,}$/.test(contact);
  if (!looksLikeEmail && !looksLikePhone) {
    const errMsg = "Please enter a valid email address or phone number.";
    if (asJson) return jsonResponse(400, { ok: false, message: errMsg });
    return redirectResponse("/contact/?error=validation");
  }

  const subject = `Website contact form: ${name}`;
  const text = [
    `New message from the Smart Geeks contact form (${sourcePage})`,
    "",
    `Name: ${name}`,
    `Email or phone: ${contact}`,
    `Preferred contact method: ${preferredContact}`,
    `Device: ${device}`,
    "",
    "Message:",
    message,
  ].join("\n");
  const html = `
    <p>New message from the Smart Geeks contact form (${escapeHtml(sourcePage)})</p>
    <table>
      <tr><td><strong>Name</strong></td><td>${escapeHtml(name)}</td></tr>
      <tr><td><strong>Email or phone</strong></td><td>${escapeHtml(contact)}</td></tr>
      <tr><td><strong>Preferred contact method</strong></td><td>${escapeHtml(preferredContact)}</td></tr>
      <tr><td><strong>Device</strong></td><td>${escapeHtml(device)}</td></tr>
    </table>
    <p><strong>Message:</strong></p>
    <p>${escapeHtml(message).replace(/\n/g, "<br>")}</p>
  `;

  let result;
  try {
    result = await sendEmail(env, { subject, text, html });
  } catch (err) {
    result = { ok: false, reason: "exception" };
  }

  if (!result.ok) {
    const errMsg = "We couldn't send your message right now. Please call or WhatsApp us directly instead -- your message was not delivered.";
    if (asJson) return jsonResponse(502, { ok: false, message: errMsg });
    return redirectResponse("/contact/?error=delivery");
  }

  if (asJson) return jsonResponse(200, { ok: true });
  return redirectResponse("/thank-you/");
}

// ---- entry point ------------------------------------------------------------
export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/api/contact") {
      if (request.method === "POST") {
        const res = await handleContactPost(request, env);
        return applyNoindex(res, url.hostname);
      }
      return applyNoindex(jsonResponse(405, { ok: false, message: "Method not allowed." }), url.hostname);
    }

    // Everything else: fall through to the static assets Cloudflare
    // uploaded alongside this Worker (the rest of public/). Advanced Mode
    // requires this explicit forward -- see DEPLOYMENT.md.
    const assetResponse = await env.ASSETS.fetch(request);
    return applyNoindex(assetResponse, url.hostname);
  },
};
