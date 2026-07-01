---
name: run-ardiaprecisionhealth
description: Build, run, and drive the ARDIA PRECISION HEALTH marketing site. Use when asked to start the site, serve it locally, screenshot a page, check navbar branding consistency across pages, or verify a change renders correctly before pushing.
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
