---
name: run-ardiaprecisionhealth
description: Build, run, and drive the ARDIA PRECISION HEALTH marketing site. Use when asked to start the site, serve it locally, screenshot a page, check navbar branding or page-category colour-tag consistency, verify a change renders correctly before pushing, or run a HIPAA/OWASP security + hallucination/claims-accuracy audit of the site's content.
---

This is a static HTML/CSS site (no build step, no framework, no
`package.json`) — 23 self-contained `.html` files at the repo root,
each with its own inline `<style>` block. "Running" it means serving
the directory over HTTP and driving a headless Chromium against it.
Drive it via `.claude/skills/run-ardiaprecisionhealth/driver.mjs` —
it starts its own static file server (no separate dev-server step)
and screenshots/inspects pages with Playwright.

All paths below are relative to the repo root (`<unit>/`).

## Prerequisites

Playwright's Chromium is not preinstalled. Install both the npm
package and its browser binary (this is macOS in this environment —
`--with-deps` is a Linux-only no-op here, but harmless to include for
portability):

```bash
npm install --no-save playwright
npx playwright install chromium --with-deps
```

This creates an untracked `node_modules/` at the repo root — already
covered by `.gitignore`. No `package.json` is created or needed;
`--no-save` keeps this a zero-footprint dependency.

## Run (agent path)

The driver is `.claude/skills/run-ardiaprecisionhealth/driver.mjs`.
It boots its own static server (default port 8123, override with
`PORT=`) against the repo root, drives Chromium, and shuts the server
down when done — one command, no separate "start the server" step.

```bash
node .claude/skills/run-ardiaprecisionhealth/driver.mjs check index.html
```

```json
{
  "name": "index.html",
  "status": 200,
  "title": "Ardia Health | Precision Revenue Intelligence",
  "hasLogoIcon": true,
  "hasGradientUnderline": true,
  "consoleErrors": []
}
```

| command | what it does |
|---|---|
| `shot <page.html> [out.png]` | screenshot one page (default out: `/tmp/ardia-shots/<page>.png`) |
| `shot-all [outDir]` | screenshot every top-level `*.html` page (skips `_internal-*.html`) |
| `check <page.html>` | HTTP status, `<title>`, whether a nav logo icon is visible, whether the teal→amber gradient underline is present, and any browser console errors |
| `check-all` | run `check` over every top-level page — the fast way to audit navbar branding consistency (the rule in `.claude/rules/coding-style.md`) across all pages in one shot |
| `tag-check <page.html>` | deterministic check: does this page's `.page-category-tag` pill exist with the colour `.claude/rules/coding-style.md` assigns its category? |
| `tag-check-all` | run `tag-check` over every page — flags any page whose colour tag is missing or wrong after an edit |
| `link-check <page.html>` | clicks every link/button in this page's `<footer>` and reports what actually happened (navigated / no navigation / dead — no href or onclick). Note: a link to the page you're already on correctly shows "no navigation" — that's the browser not reloading, not a bug; only treat it as a finding if the click was supposed to go somewhere else |
| `link-check-all` | run `link-check` over every page — the fast way to find real dead footer links (as opposed to same-page self-links, which will always show as "no navigation" and aren't bugs) |

Screenshots default to `/tmp/ardia-shots/`.

Example — screenshot every page and eyeball the ones that matter:

```bash
node .claude/skills/run-ardiaprecisionhealth/driver.mjs shot-all /tmp/ardia-shots
```

Example — audit branding consistency across all pages after a CSS edit:

```bash
node .claude/skills/run-ardiaprecisionhealth/driver.mjs check-all
```

To drive an already-running server instead of the driver's built-in
one (e.g. `python3 -m http.server 8123`), set `BASE_URL`:

```bash
BASE_URL=http://localhost:8123 node .claude/skills/run-ardiaprecisionhealth/driver.mjs shot dashboard.html
```

## Run (human path)

```bash
python3 -m http.server 8123
# → open http://localhost:8123/index.html in a browser. Ctrl-C to stop.
```

Useless in a headless/agent context — no browser to open. Use the
driver above instead.

## Compliance & Security Audit

Beyond rendering/screenshotting, this skill also runs a healthcare-AI-specific
content and security audit, because this site makes investor- and
customer-facing claims about a HIPAA-regulated product (architecture names,
clinical accuracy stats, compliance certifications) that must stay both
secure (OWASP/HIPAA) and truthful (no AI-hallucinated or drifted claims).
This runs daily via a scheduled trigger (see below) and can also be run
on demand.

**Two independent checks, because they need different tools:**

1. **Colour-tag consistency (deterministic, scriptable)** — `tag-check-all`
   above. Confirms every page still carries its assigned
   `.page-category-tag` in the right colour. Safe to run any time, no LLM
   needed.
2. **Security (OWASP/HIPAA) + claims/hallucination accuracy (needs
   judgment, not scriptable)** — reading HTML for XSS/secret-exposure
   patterns and cross-checking marketing claims against source documents
   requires an agent, not a deterministic script. The process:
   - Read `.claude/skills/run-ardiaprecisionhealth/reference/source-of-truth.md`
     first. It's the canonical grounding data extracted from Ardia's own
     business-plan/whitepaper `.docx` files — it tells you which claims
     are confirmed real IP (e.g. the Neuro-Symbolic Sandwich Architecture,
     the ToxIQ/MolecuIQ/AcoIQ/BehaviorIQ module names — **do not flag
     these as hallucinations**, they're documented company IP grounded in
     the published neuro-symbolic-AI research field) versus claims where
     Ardia's own source documents **disagree with each other** (cloud
     provider, seed raise size, a founder's title, the appeal win rate —
     see that file's "Unresolved conflicts" table).
   - For each page, check for OWASP-relevant issues (exposed secrets/PII in
     HTML comments, mixed content, XSS-risk patterns, missing
     `rel="noopener noreferrer"` on external links, broken internal links)
     and HIPAA-relevant issues (no PHI ever appears in static marketing
     copy — it shouldn't, this is a pre-revenue marketing site with no
     patient data pipeline yet, but check anyway).
   - Cross-check every quantitative/technical claim against the reference
     file's four categories: verified / conflicting-source / unverified /
     fabrication-risk.
   - **Claims policy — flag, never silently rewrite.** Numeric and factual
     claims are never auto-edited, even ones classified
     `fabrication-risk` — only the founders can confirm which of two
     conflicting internal documents (or neither) is current. Only
     mechanical, zero-ambiguity fixes get applied automatically (stray
     `console.log`, missing `rel="noopener"`, a leftover TODO/placeholder).
     This mirrors the `security-review` skill's severity gating but adds a
     4th, content-accuracy dimension specific to this site.
   - Report findings using the severity/status colours in
     `.claude/rules/coding-style.md`'s "Report severity colours" table
     (🔴 CRITICAL / 🟠 HIGH / 🟡 MEDIUM / 🔵 LOW for security; 🟢 verified /
     🟣 conflicting-source / 🟡 unverified for claims).
   - For a repo-wide sweep across all 23 pages in parallel, use the
     `Workflow` tool with one `pipeline()` stage per page doing the audit
     and a second stage applying only the safe/mechanical fixes — that's
     how the initial rollout was done; re-run the same shape for
     subsequent audits rather than reviewing pages one at a time serially.

**Daily schedule.** A Routine (`create_trigger`, cron `0 13 * * *` — 8am
Central) fires into this session daily and re-runs the check above,
reporting any new findings (new pages, new claims, drifted stats). It does
not auto-push or auto-fix content claims — it produces a report for you to
act on. See `list_triggers` for the trigger ID if you need to change the
cadence or disable it.

## Gotchas

- **The gradient underline lives on a `::after` pseudo-element**
  (`.logo-main::after { background: linear-gradient(...) }`), not on a
  real DOM element. `getComputedStyle(el).backgroundImage` on the
  element itself always misses it — you must call
  `getComputedStyle(el, '::after')` (and `::before`, since some pages
  use that instead). The driver's `check` command already does this;
  if you write your own probe, don't repeat the mistake — a naive
  check silently reports `hasGradientUnderline: false` on every page.
- **The navbar logo icon uses different class names on different
  pages** — `.logo-icon` and `.nav-brand-icon` per `CLAUDE.md`, but
  also `.nav-logo-icon` (`our-product.html`) and `.nav-logo-box`
  (`product-demo.html`) in practice. The driver's selector already
  covers all four; if `check` reports `hasLogoIcon: false` on a page
  you believe has branding, inspect that page's actual class name
  before assuming the branding is missing — `grep -o
  'class="[^"]*logo[^"]*"' <page>.html`.
- **`email-audit.html` and `google-cloud-email-response.html` are not
  site pages** — they're internal drafts (an outreach audit and an
  email-response draft), not part of the public 20-page site in
  `CLAUDE.md`'s file map. `check-all` will correctly flag them as
  missing navbar branding; that's expected, not a bug to fix.
- **No build step to forget.** There's no bundler, no `npm run build`
  — editing an `.html` file's `<style>` block is the whole change.
  The driver's server reads files straight off disk on every request,
  so edits are visible on the very next `shot`/`check` with no restart.
- **The company's own source documents disagree with each other.**
  `Ardia_Health_White_Paper_Business_Plan.docx` and
  `Ardia_Health_Business_Plan_2026_v2.docx` give different numbers for
  the seed raise ($3.5M vs. $500K–$750K), different cloud providers
  (AWS vs. GCP), different appeal win rates (89% vs. 50–83%, and the
  whitepaper contradicts itself internally between its own sections),
  and different founder titles for Ram Vadlamudi (unnamed CTO-to-hire
  vs. named Founder/Product Designer vs. an investor-email template
  calling him "Founder & CEO"). See
  `reference/source-of-truth.md`'s "Unresolved conflicts" table — do
  not resolve these yourself by picking whichever number looks more
  current; they need founder sign-off.
- **`link-check`'s "no navigation" result is a false positive for same-page links.** Every page's footer links to itself (e.g. `about.html`'s "Why Ardia" link points to `about.html`) — clicking a link to the page you're already on doesn't reload, so `link-check` correctly reports "no navigation," but that's normal browser behavior, not a bug. The one exception found so far: `contact.html`'s own "Book a Demo" button used to show this same false-positive-shaped result, except it actually was a real bug — `contact.html` was a byte-for-byte duplicate of `security.html` (fixed 2026-07-01, see `reference/audit-2026-07-01.md`), so clicking "Book a Demo" *looked* like a self-link and got treated as one. When triaging `link-check` output, verify the page's actual content matches its nav-link label before dismissing a "no navigation" result as a false positive.
- **`.page-category-tag` is additive wayfinding, not a rebrand.** It
  must never replace or approximate the five locked brand colors on
  `.logo-icon` / the navbar / the gradient underline — see
  `.claude/rules/coding-style.md`. If `tag-check-all` and `check-all`
  disagree about a page's branding, trust `check-all` for the core
  brand elements; `tag-check-all` only validates the newer category
  pill.

## Troubleshooting

- **`Cannot find package 'playwright'`**: the `npm install --no-save
  playwright` step under Prerequisites wasn't run (or was run in a
  different directory). Node resolves `import 'playwright'` from
  `driver.mjs`'s location upward through parent directories — the
  install must land in a `node_modules/` that's an ancestor of
  `.claude/skills/run-ardiaprecisionhealth/`, i.e. run the install
  from the repo root.
- **`browserType.launch: Executable doesn't exist`**: `npx playwright
  install chromium` wasn't run after installing the npm package — the
  package and the browser binary are separate downloads.
