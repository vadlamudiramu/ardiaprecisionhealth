---
name: website-security
description: Website security specialist for ARDIA PRECISION HEALTH. Run before any production deployment, after adding new pages or third-party scripts, or when asked to audit security. Covers static site hardening, HIPAA web-layer compliance, OWASP checks, and Vercel configuration.
---

# Website Security Specialist — ARDIA PRECISION HEALTH

This skill audits the 20-page static HTML site and `vercel.json` configuration for security vulnerabilities, HIPAA web-layer risks, and deployment hardening. The audit driver (`audit.sh`) runs locally and exits non-zero when blocking issues are found.

## Run the Audit

```bash
# From repo root:
bash .claude/skills/website-security/audit.sh
```

Exit codes: `0` = approved or warnings only, `1` = blocking issues found.

---

## Real Findings (Baseline — run 2026-06-28)

```
PASS: 14   WARN: 2   FAIL: 7
VERDICT: BLOCKED
```

### FAIL — Must Fix

| # | Issue | File | Fix |
|---|-------|------|-----|
| 1 | `X-Frame-Options` missing | vercel.json | Add `DENY` header |
| 2 | `Content-Security-Policy` missing | vercel.json | Add CSP header |
| 3 | `Strict-Transport-Security` (HSTS) missing | vercel.json | Add HSTS header |
| 4 | `Referrer-Policy` missing | vercel.json | Add `strict-origin-when-cross-origin` |
| 5 | `Permissions-Policy` missing | vercel.json | Restrict camera/mic/geolocation |
| 6 | `_internal-team-details.html` publicly accessible | root | Block in vercel.json or move out of web root |
| 7 | `ui-avatars.com` URL with `name=` param in mobile-app.html | mobile-app.html:355 | Replace with static asset; never pass names in URLs |

### WARN — Review Required

| # | Issue | Detail |
|---|-------|--------|
| 1 | CDN resources without SRI | All 20 pages load Google Fonts, FontAwesome, and chart.js from CDN without `integrity=` attributes |
| 2 | HTML comments in _internal-team-details.html | Contains FOUNDER 1/2 and SHARED CONTACT INFO comment blocks |

---

## Fix: vercel.json Security Headers

Replace current `vercel.json` with this hardened version:

```json
{
  "cleanUrls": true,
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options",    "value": "nosniff" },
        { "key": "X-Frame-Options",           "value": "DENY" },
        { "key": "Referrer-Policy",           "value": "strict-origin-when-cross-origin" },
        { "key": "Permissions-Policy",        "value": "camera=(), microphone=(), geolocation=()" },
        { "key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains; preload" },
        {
          "key": "Content-Security-Policy",
          "value": "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com; font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; img-src 'self' data: https:; connect-src 'self'; frame-ancestors 'none';"
        }
      ]
    },
    {
      "source": "/_internal-team-details",
      "headers": [
        { "key": "X-Robots-Tag", "value": "noindex, nofollow" }
      ]
    }
  ],
  "rewrites": [
    {
      "source": "/_internal-team-details",
      "destination": "/404"
    }
  ]
}
```

**Note on CSP**: The `unsafe-inline` is needed for inline `<style>` blocks present on all 20 pages. When the site migrates to Next.js, replace with nonces.

---

## Fix: Block _internal-team-details.html

The above `vercel.json` redirects `/_internal-team-details` to 404. Also rename the file locally to remove it from the public web root, or prefix with a path not served (e.g., move to a `_private/` folder excluded via `.vercelignore`).

---

## Fix: Subresource Integrity (SRI)

Every CDN-loaded resource needs an `integrity=` attribute. Generate SRI hashes:

```bash
# Get SRI hash for a resource
curl -s https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css \
  | openssl dgst -sha384 -binary | openssl base64 -A

# Then use:
# <link rel="stylesheet" href="..." integrity="sha384-HASH" crossorigin="anonymous">
```

Pre-computed for current versions:
- FontAwesome 6.5.0: available at cdnjs.cloudflare.com with SRI hash shown on the page
- chart.js: use pinned version URL from jsdelivr.com/package/npm/chart.js

---

## HIPAA Web-Layer Compliance

### What must NEVER appear in URLs
- Patient names, IDs, SSNs, DOBs, diagnoses
- `?patient_id=`, `?name=`, `?email=`, `?mrn=` query params
- The `mobile-app.html` demo avatar `ui-avatars.com?name=Alex+Carter` — even fake names in URL params establish a bad pattern to fix before real PHI is added

### localStorage / sessionStorage
Zero usage confirmed on all 20 pages. When adding future auth:
- Auth tokens → httpOnly, Secure, SameSite=Strict cookies only
- Never store any patient-related data in browser storage

### Third-Party Scripts & BAA
Current third-party resources (Google Fonts, FontAwesome CDN, chart.js CDN) handle no PHI — no BAA required for these. Any future addition of analytics (GA, Mixpanel, Segment), chat widgets (Intercom, Drift), or A/B testing scripts that could observe patient-related page content requires a BAA with that vendor before deployment.

### Future Next.js Migration
When adding server-side features:
- Never include PHI in page titles or `<meta>` tags (logged by proxies, CDNs, analytics)
- Add audit logging middleware that fires on every authenticated page render
- Use Next.js middleware to block unauthenticated access to patient-facing routes

---

## OWASP Checks — Static Site

| Threat | Status | Notes |
|--------|--------|-------|
| XSS | Low risk (no dynamic rendering) | Will need DOMPurify when Next.js is added |
| Clickjacking | **FAIL** | Missing X-Frame-Options — add to vercel.json |
| Sensitive data in HTML | WARN | _internal page has contact info |
| Dependency vuln | WARN | CDN resources not pinned with SRI |
| Security misconfiguration | **FAIL** | 5 security headers missing |

---

## Gotchas

- **`wc -l` on macOS vs Linux**: returns `"0\n0"` when piping through multiple greps. Fixed with `tr -d ' '` — don't revert this.
- **`_internal-team-details.html`** is served at `/_internal-team-details` on Vercel (cleanUrls strips `.html`). The rewrite in vercel.json must use the clean URL path, not the filename.
- **CSP and inline styles**: All 20 pages use inline `<style>` blocks. A strict CSP without `unsafe-inline` will break all page styles. Document this debt — resolve when migrating to Next.js with nonce-based CSP.
- **Google Fonts SRI**: Google Fonts dynamically generates CSS responses and doesn't support SRI directly. Use `font-display=swap` and self-host fonts for full SRI compliance (or accept the risk and document it).

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| `integer expression expected` in audit.sh | Caused by `wc -l` returning trailing whitespace — pipe through `tr -d ' '` |
| CSP blocks FontAwesome icons | Add `https://cdnjs.cloudflare.com` to `style-src` and `font-src` |
| `_internal` page still accessible after vercel.json update | Vercel caches headers — wait for fresh deployment or use `--force` redeploy |

---

## Verdict Template

After running `audit.sh`, report findings as:

```
## Website Security Audit — [date]
PASS: X  WARN: X  FAIL: X

### Blocking Issues
[from FAIL lines]

### Warnings
[from WARN lines]

### HIPAA Status
[ ] No PHI in URLs
[ ] No PHI in localStorage
[ ] Third-party scripts reviewed for BAA

### Verdict: APPROVED / BLOCKED
```
