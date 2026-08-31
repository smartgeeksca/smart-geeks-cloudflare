# Deployment Guide -- Cloudflare Pages

## Why Cloudflare Pages, not Workers Static Assets

This project targets **Cloudflare Pages with Pages Functions**, not Workers
Static Assets, chosen deliberately and implemented consistently:

- `functions/api/contact.js` and `functions/_middleware.js` use the Pages
  Functions file-based routing convention (`functions/` directory,
  `onRequestPost`/`onRequest` exports). That convention is specific to
  Pages -- it is not how a plain Worker with static assets is structured.
- `_headers` and `_redirects` are Pages-specific static configuration files,
  read from the build output directory.
- Pages is also the correct fix for a specific issue found in a prior
  production audit of this business's previous deployment: a `.workers.dev`
  hostname was in use, and `.workers.dev` is documented by Cloudflare as
  exclusive to plain Workers, never Pages -- meaning Pages-only files like
  these never would have activated on that project. Deploying this package
  as an actual Pages project (with a `*.pages.dev` preview domain and the
  real custom domain attached) resolves that mismatch at the root.

## Runtime version

Verified against Cloudflare's current build-image documentation while this
project was built: the Pages v3 build image includes **Python 3.13.3** by
default, so `python3 build.py` runs directly as a Pages build command with
no extra runtime installation. `.python-version` (containing `3.13`) pins
this explicitly. No Node dependencies are required to build the site itself
(Node is only relevant if you later add JS tooling).

## Build command / output directory

| Setting | Value |
|---|---|
| Build command | `python3 build.py` |
| Build output directory | `public` |
| Root directory | `/` (repo root) |

## Three ways to deploy (none require Wrangler)

### Option A -- Connect a Git repository (recommended; no CLI at all)

Cloudflare's own build servers do the work here -- you never install or run
Wrangler, and you never build locally.

1. Push this project to a GitHub/GitLab repository.
2. In the Cloudflare dashboard: **Compute (Workers & Pages) -> Create ->
   Pages -> Connect to Git**, select the repo.
3. Framework preset: **None**. Build command: `python3 build.py`. Build
   output directory: `public`.
4. Add environment variables/secrets (see below) before the first deploy
   that needs the contact form to actually send mail.
5. Deploy. Every push to your production branch rebuilds and redeploys.

This is the only one of the three options where `functions/api/contact.js`
and `functions/_middleware.js` are used exactly as delivered, with no
duplication -- Cloudflare's build system compiles the `functions/`
directory for you.

### Option B -- Dashboard drag-and-drop, static pages only (no CLI, no Git)

The fastest path from this ZIP with nothing to install, but with one real
limitation confirmed against Cloudflare's own documentation while this
project was built: **dashboard drag-and-drop does not compile a
`functions/` directory at all.** That means the contact form's `/api/`
endpoint and the non-production `noindex` middleware will not work with
this option alone -- see Option C if you need those without Git.

1. Build locally: `python3 build.py` (needs only Python 3 -- see
   `.python-version`).
2. In the Cloudflare dashboard: **Compute (Workers & Pages) -> Create
   application -> Pages -> "Get started" -> "Drag and drop your files."**
3. Enter a project name, then drag the entire `public/` folder (not the zip,
   not individual files -- the folder itself; drag-and-drop also accepts a
   zip of it) into the upload area.
4. Select **Deploy site**. Limits: 1,000 files / 25 MiB per file -- this
   project is well under both (see QA-REPORT.md for real measured sizes).
5. Re-run step 1 and re-drag `public/` any time content changes; there's no
   auto-redeploy without Git.

### Option C -- Dashboard drag-and-drop WITH the contact form (Advanced Mode)

Still no Wrangler, still no Git -- this adds back the contact form and the
noindex middleware to Option B by using Cloudflare Pages' "Advanced Mode": a
single `_worker.js` file at the root of the uploaded output, which dashboard
drag-and-drop *does* support (unlike a `functions/` directory).

1. Build locally: `python3 build.py`.
2. Copy the pre-written bundle into the build output:
   `cp alt-deploy/_worker.js public/_worker.js`
   (`alt-deploy/_worker.js` reimplements the same two Pages Functions as one
   self-contained file, since drag-and-drop performs no build/import step --
   see that file's header comment for the full explanation, and
   `python3 scripts/check_worker_sync.py` to confirm it hasn't drifted from
   `functions/api/contact.js` / `functions/_middleware.js` before you copy it).
3. Drag the `public/` folder (now including `_worker.js`) into the dashboard
   the same way as Option B, and deploy.
4. Set the same environment variables/secrets as any other path (Settings ->
   Environment variables works identically for a Direct Upload project).

Trade-off to know about: with `_worker.js` present, that one file becomes
responsible for every request, including falling back to serve your static
pages (already handled in the bundle via `env.ASSETS.fetch`) -- so it's a
bit more moving parts than Option A, and every future edit to the contact
form or middleware needs to be ported to `alt-deploy/_worker.js` and
re-copied. Prefer Option A once you're willing to use Git; use Option C only
if avoiding Git specifically is the goal.

## Environment variables and secrets

Set these as **Pages secrets** in the dashboard (project -> Settings ->
Environment variables -> add variable -> mark as **Encrypted**/Secret), not
as plain-text build variables. No CLI is needed for this step -- the
`wrangler pages secret put <NAME>` command does the same thing if you
happen to have Wrangler installed, but the dashboard alone is sufficient:

| Name | Required for | Notes |
|---|---|---|
| `CF_ACCOUNT_ID` | Contact form email delivery | Your Cloudflare account ID |
| `CF_EMAIL_API_TOKEN` | Contact form email delivery | API token scoped to Cloudflare Email Service sending (see below) |
| `CONTACT_TO_EMAIL` | Contact form email delivery | Where form submissions land, e.g. `support@smartgeeks.ca` |
| `CONTACT_FROM_EMAIL` | Contact form email delivery | Must be on a domain verified in Cloudflare Email Service |

Until these four are set, the contact form's client- and server-side
validation, honeypot, and rate-limit logic all still work -- submissions
simply fail safely with an honest "we couldn't send your message, please
call or WhatsApp instead" response rather than silently pretending to succeed.

Optional:

| Name | Purpose |
|---|---|
| KV binding `RATE_LIMIT_KV` | Enables the best-effort per-IP rate limit in `functions/api/contact.js`. No CLI needed: create the namespace in the dashboard (**Storage & Databases -> KV -> Create namespace**), then bind it to this project (project -> Settings -> Functions -> KV namespace bindings -> variable name `RATE_LIMIT_KV`). `wrangler kv namespace create` does the same thing if you have Wrangler installed. Without this binding, that specific check is skipped (documented in code), not silently broken. |

`GA4_MEASUREMENT_ID` / `GOOGLE_ADS_CONVERSION_ID` are **not** environment
variables read at runtime -- they're build-time values in
`src/data/business.py` -> `ANALYTICS_CONFIG`. Set real values there, rebuild,
and redeploy. Leaving them `None` (the shipped default) means no tracking
script loads at all.

## Email delivery setup (Cloudflare Email Service)

`functions/api/contact.js` sends mail through Cloudflare's own,
currently-documented Email Service REST API -- deliberately not MailChannels
(whose free unauthenticated Workers integration is not a dependable,
currently-guaranteed method) and not the native `send_email` Worker binding
(which, as of this build, Cloudflare's own Pages Functions bindings
documentation does not list as a supported Pages binding type -- only the
REST-API-over-fetch approach used here is confirmed to work identically on
Pages).

1. In the Cloudflare dashboard: **Compute -> Email Service -> Email
   Sending**, onboard the sending domain (`smartgeeks.ca`) and let Cloudflare
   add the required DNS records to that zone.
2. Create an API token scoped to send email via Email Service, and set it as
   the `CF_EMAIL_API_TOKEN` secret.
3. Set `CONTACT_FROM_EMAIL` to an address on that verified domain (e.g.
   `website@smartgeeks.ca`) and `CONTACT_TO_EMAIL` to where you want
   submissions delivered.
4. To swap providers later (Resend, Postmark, SendGrid, etc.), only
   `sendEmail()` in `functions/api/contact.js` needs to change -- validation,
   sanitization, and routing are provider-independent by design.

## Custom domain setup: `www` and apex behaviour

The production canonical for this build is `https://www.smartgeeks.ca/`.

1. Attach `www.smartgeeks.ca` as a custom domain on the Pages project first.
2. To make `smartgeeks.ca` (no www) redirect to `www`, either:
   - **Also** attach `smartgeeks.ca` as a second custom domain on this same
     Pages project -- `_redirects` already contains the
     `smartgeeks.ca/* -> www.smartgeeks.ca/:splat 301!` rule, or
   - Leave the apex on its existing DNS setup and add a Cloudflare
     **Redirect Rule** at the zone level instead (Rules -> Redirect Rules),
     which works regardless of which product apex traffic is served from.
3. Do not point `smartgeeks.ca` at a *different* unrelated site while also
   trying to canonicalize to it -- confirm what is currently live at both
   hostnames before cutover (see "Owner action: confirm domain ownership"
   in README.md).

## Non-production indexing protection

`functions/_middleware.js` adds `X-Robots-Tag: noindex, nofollow, noarchive`
to every response on any hostname other than `www.smartgeeks.ca` /
`smartgeeks.ca` -- this covers the `*.pages.dev` preview subdomain and any
staging hostname automatically, without needing a separate `robots.txt` per
environment (which isn't possible on Pages anyway, since `robots.txt` is a
single static file shared by every hostname the project serves). Production
itself is never blocked: `robots.txt` ships permissive (`Allow: /`) and is
only affected by the per-hostname header, not by file content.

## Cache headers

`_headers` sets long-lived `Cache-Control: public, max-age=31536000,
immutable` on `/assets/css/*`, `/assets/js/*`, and `/assets/icons/*`. This is
safe because `build.py` appends a content-hash query string
(`?v=<hash>`) to the CSS/JS URLs referenced in every page -- a content
change produces a new URL rather than silently reusing a stale cached one.
Rerun `python3 build.py` and redeploy any time source assets change; do not
hand-edit files inside `public/` directly, since it's fully regenerated.

## Rollback procedure

Cloudflare Pages keeps a deployment history. To roll back:

- **Dashboard:** Compute -> Pages -> smart-geeks -> Deployments -> find the
  last known-good deployment -> **Rollback to this deployment**.
- **CLI:** `wrangler pages deployment list --project-name=smart-geeks`, then
  redeploy the desired historical build, or revert the Git commit that
  triggered the bad deploy and push again (Option A) / rebuild and
  `wrangler pages deploy public` from that earlier state (Option B).

## Post-deploy verification checklist

After every deploy, confirm (this is exactly what the prior deployment
forensics audit found was NOT true of the previous deployment, so it's
worth checking explicitly rather than assuming):

1. `https://www.smartgeeks.ca/` serves the CURRENT build -- spot-check a
   piece of copy that only exists in this version.
2. View source on 2-3 pages and confirm a `<script type="application/ld+json">`
   block is present (the previous production deployment had none).
3. `https://www.smartgeeks.ca/robots.txt` is reachable and permissive.
4. Submit the contact form for real and confirm an email arrives, or -- if
   secrets aren't configured yet -- confirm it fails with the honest error
   message rather than a silent false "sent" confirmation.
5. Load the site on a non-production hostname (a `*.pages.dev` preview URL)
   and check the response headers for `X-Robots-Tag: noindex`.
