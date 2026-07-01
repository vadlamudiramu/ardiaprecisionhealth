# Coding Style — ARDIA PRECISION HEALTH

## HTML/CSS (Current Static Site)

- **No shared stylesheet** — all styles are inline `<style>` blocks per file
- **Branding variables** — always use the exact brand colors (never approximate):
  - Navy: `#0a1628`
  - Teal: `#14b8a6`
  - Blue (Precision Health): `#1d9bd1`
  - Amber: `#f59e0b`
  - Gray (tagline): `#5a6e87`
- **Logo box** — `.logo-icon` always: 52×52px, dark navy gradient, teal border, 6px padding
- **Gradient underline** — always 2px, `linear-gradient(to right,#14b8a6,#f59e0b)`
- **Tagline** — always normal-case (not uppercase), 10px, `#5a6e87`
- **Font** — Sora for brand text, system-ui for body

### Page-category colour system (`.page-category-tag`)

The five core brand colors above are **never** overridden or approximated —
they govern the logo, navbar, and gradient underline on every page, no
exceptions. Separately, each page also carries a small `.page-category-tag`
pill directly under the navbar that colour-codes which part of the site
you're in. This is additive wayfinding, not a rebrand — it must never touch
`.logo-icon`, the navbar links, or the gradient underline.

| Category | Pages | Colour | Hex |
|---|---|---|---|
| Company & Vision | about, ardia-profile, vision, roadmap, _internal-team-details | Violet | `#7c6ee6` |
| Product & Platform | our-product, architecture, how-it-works, how-software-works, mobile-app, plg-sandbox, product-demo, dashboard, solutions | Sky | `#0ea5e9` |
| Clinical & Compliance | security, pama, precision-medicine, case-studies, research | Green | `#22c55e` |
| Investors & Business | investors, contact | Fuchsia | `#d946ef` |
| Internal / non-canonical | email-audit, google-cloud-email-response | none — plain gray `#5a6e87`, no colour badge | — |

Hues are chosen to sit clearly apart from the four brand hues (navy/teal
~173–220°, amber ~38°) on the color wheel — violet ~255°, sky ~199° (kept
distinct from brand blue `#1d9bd1` by lightness/saturation, not hue alone,
since the two both live in the blue family — sky is a wayfinding accent,
brand blue is never replaced by it), green ~142° (clearly separated from
brand teal ~173° so the two are never confused at a glance), fuchsia ~300°.

Markup pattern (insert once per page, immediately after `</nav>` or the
navbar's closing tag, before the hero section):

```html
<div class="page-category-tag" style="display:inline-flex;align-items:center;gap:6px;font:600 11px/1 'Sora',system-ui;letter-spacing:.04em;text-transform:uppercase;color:#7c6ee6;background:rgba(124,110,230,.08);border:1px solid rgba(124,110,230,.3);border-radius:6px;padding:4px 10px;margin:12px 24px 0">Company &amp; Vision</div>
```

Swap the `color`/`background`/`border` rgba values and label text for the
page's category per the table above (background = colour at 8% alpha,
border = colour at 30% alpha, matching the existing pill patterns already
used site-wide, e.g. the "DALLAS-FORT WORTH · FOUNDED JAN 2026" badge on
`index.html`).

### Report severity colours

Audit output (the `run-ardiaprecisionhealth` skill's `vuln-scan` and
`claims-check` commands) uses a separate, fixed severity palette — this is
for terminal/markdown reports only, never applied to site pages:

| Severity | Colour | Hex | Report marker |
|---|---|---|---|
| CRITICAL | Red | `#dc2626` | 🔴 |
| HIGH | Orange | `#ea580c` | 🟠 |
| MEDIUM | Amber (brand) | `#f59e0b` | 🟡 |
| LOW | Blue | `#3b82f6` | 🔵 |
| Verified claim | Green | `#16a34a` | 🟢 |
| Conflicting-source claim | Purple | `#9333ea` | 🟣 |
| Unverified/flagged claim | Amber (brand) | `#f59e0b` | 🟡 |

## Python (Future Backend)

- Type hints on all function signatures
- Pydantic models for all API request/response schemas
- Async/await for all I/O operations
- No bare `except:` — always catch specific exceptions
- Docstrings only where the WHY is non-obvious

## TypeScript/Next.js (Future Frontend)

- Strict mode enabled
- Zod schemas for all external inputs
- No `any` type — use `unknown` and narrow properly
- Components: function declarations, not arrow functions
- CSS: Tailwind utility classes preferred over custom CSS

## General Rules

- No TODO/FIXME comments in committed code — open a GitHub issue instead
- No `console.log` in production code — use structured logger
- No dead code — remove unused functions, variables, imports
- Comments explain WHY, not WHAT — code should be self-documenting
