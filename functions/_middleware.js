/**
 * Cloudflare Pages Functions middleware.
 *
 * Responsibility: keep every non-production hostname (the *.pages.dev
 * preview subdomain, any staging/demo hostname, or the site being reached
 * before a custom domain is fully cut over) out of search indexes, while
 * leaving the real production hostname untouched.
 *
 * Static, hostname-independent security headers live in `_headers` instead
 * of here, since a static file is applied to every asset (including cached
 * ones) without invoking a Function on each request -- this middleware only
 * does the one thing that genuinely needs to be dynamic.
 */

// Canonical production hostnames. Keep this in sync with src/data/business.py.
const PRODUCTION_HOSTNAMES = new Set(["www.smartgeeks.ca", "smartgeeks.ca"]);

export async function onRequest(context) {
  const { request, next } = context;
  const url = new URL(request.url);
  const response = await next();

  if (PRODUCTION_HOSTNAMES.has(url.hostname)) {
    return response;
  }

  // Any other hostname (preview deploys, *.pages.dev, a staging domain,
  // localhost during `wrangler pages dev`) gets a hard noindex, regardless
  // of what any individual page's <meta name="robots"> tag says.
  const headers = new Headers(response.headers);
  headers.set("X-Robots-Tag", "noindex, nofollow, noarchive");
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers,
  });
}
