/**
 * POST /api/contact
 *
 * Handles the contact form for both the AJAX-enhanced path (src/assets/js/
 * main.js, which sends `Accept: application/json` and expects a JSON body
 * back) and the plain-HTML-POST fallback (no JS: the browser submits the
 * form directly and expects a redirect).
 *
 * Email delivery uses Cloudflare's own currently-supported Email Service
 * REST API (https://developers.cloudflare.com/email-service/), called over
 * plain fetch() -- verified against Cloudflare's documentation while this
 * project was built. This deliberately avoids two problems:
 *   1. MailChannels' free unauthenticated Workers integration, which is not
 *      a currently-guaranteed-available method and should not be depended on.
 *   2. Cloudflare's native `send_email` binding, which at the time this was
 *      written is documented for Workers but is NOT listed among Pages
 *      Functions' supported binding types -- so it may not be available in
 *      a Pages project at all. Calling the REST API over fetch() sidesteps
 *      that binding-availability question entirely, since it works the same
 *      way from any Function.
 * `sendEmail()` below is the ONLY function that knows about Cloudflare
 * Email Service specifically -- swap it for Resend, Postmark, SendGrid, or
 * any other provider's HTTP API without touching validation or routing.
 * See DEPLOYMENT.md for the exact dashboard/DNS setup this requires, and
 * .dev.vars.example for the environment variables it reads.
 */

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
  // Strip control characters and collapse excessive whitespace, then trim
  // to the field's max length so nothing oversized reaches the email body.
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

/**
 * Very small best-effort rate limit: at most one submission per IP every
 * 20 seconds. This ONLY activates if a KV namespace is bound as
 * `RATE_LIMIT_KV` (see wrangler.toml / DEPLOYMENT.md) -- if it isn't bound,
 * this silently skips rate limiting rather than failing the request, and
 * that fact is documented rather than implied to always be active.
 */
async function isRateLimited(env, ip) {
  if (!env.RATE_LIMIT_KV || !ip) return false;
  const key = `contact-rl:${ip}`;
  const last = await env.RATE_LIMIT_KV.get(key);
  if (last) return true;
  await env.RATE_LIMIT_KV.put(key, "1", { expirationTtl: 20 });
  return false;
}

/** The only function that talks to a specific email provider. */
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
      body: JSON.stringify({
        to: env.CONTACT_TO_EMAIL,
        from: env.CONTACT_FROM_EMAIL,
        subject,
        text,
        html,
      }),
    }
  );
  if (!res.ok) {
    return { ok: false, reason: "provider_error", status: res.status };
  }
  return { ok: true };
}

export async function onRequestPost(context) {
  const { request, env } = context;
  const asJson = wantsJson(request);

  let form;
  try {
    form = await request.formData();
  } catch (err) {
    if (asJson) return jsonResponse(400, { ok: false, message: "We couldn't read your submission. Please try again." });
    return redirectResponse("/contact/?error=parse");
  }

  // Honeypot: real visitors never see or fill this field (see .hp-field in
  // style.css). If it's filled, respond as if things went fine so the bot
  // gets no signal, but never actually send an email.
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
    // Never claim success when we didn't actually deliver the message.
    const errMsg =
      "We couldn't send your message right now. Please call or WhatsApp us directly instead -- your message was not delivered.";
    if (asJson) return jsonResponse(502, { ok: false, message: errMsg });
    return redirectResponse("/contact/?error=delivery");
  }

  if (asJson) return jsonResponse(200, { ok: true });
  return redirectResponse("/thank-you/");
}

// Any method other than POST/OPTIONS is not a valid use of this endpoint.
export async function onRequestGet() {
  return jsonResponse(405, { ok: false, message: "Method not allowed." });
}
