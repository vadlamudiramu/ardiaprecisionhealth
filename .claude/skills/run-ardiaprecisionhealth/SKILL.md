---
name: run-ardiaprecisionhealth
description: Run, screenshot, and visually verify the ARDIA PRECISION HEALTH website. Use when asked to run the app, take a screenshot, verify a change looks correct, check a page, or preview any of the 20 HTML pages locally.
---

# Run ARDIA PRECISION HEALTH

Static HTML/CSS site — no build step. Served locally with Python's built-in HTTP server and driven headlessly with Chromium. All 20 pages are available instantly.

All paths below are relative to the repo root: `/home/user/ardiaprecisionhealth/`

## Prerequisites

These were verified working in this container:

```bash
# Python 3 (built-in http.server) — already available
python3 --version   # Python 3.x

# Chromium — already installed at:
/opt/pw-browsers/chromium-1194/chrome-linux/chrome --version
```

No `apt-get` installs needed. Both tools are pre-installed.

## Run (agent path) — screenshot any page

Start the server, screenshot a page, stop the server:

```bash
# 1. Start server (background)
cd /home/user/ardiaprecisionhealth
python3 -m http.server 8099 --directory . &
SERVER_PID=$!
sleep 1

# 2. Screenshot a page (replace PAGE with: index, dashboard, investors, etc.)
PAGE=index
CHROME=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
OUT=/tmp/screenshot-${PAGE}.png

$CHROME \
  --headless=new \
  --no-sandbox \
  --disable-gpu \
  --disable-dev-shm-usage \
  --screenshot="$OUT" \
  --window-size=1440,900 \
  "http://localhost:8099/${PAGE}.html" 2>/dev/null

echo "Screenshot: $OUT ($(du -h $OUT | cut -f1))"

# 3. Stop server
kill $SERVER_PID 2>/dev/null
```

## Screenshot all 20 pages

```bash
cd /home/user/ardiaprecisionhealth
python3 -m http.server 8099 --directory . &
SERVER_PID=$!
sleep 1

CHROME=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
OUTDIR=/tmp/ardia-screenshots
mkdir -p "$OUTDIR"

for page in index about architecture ardia-profile case-studies contact \
            dashboard how-it-works how-software-works investors mobile-app \
            our-product pama plg-sandbox precision-medicine research \
            roadmap security solutions vision; do
  $CHROME \
    --headless=new --no-sandbox --disable-gpu --disable-dev-shm-usage \
    --screenshot="$OUTDIR/${page}.png" \
    --window-size=1440,900 \
    "http://localhost:8099/${page}.html" 2>/dev/null
  echo "  done: ${page}.png"
done

kill $SERVER_PID 2>/dev/null
ls -lh "$OUTDIR/"
```

## Check a specific element (DOM / HTML content)

```bash
cd /home/user/ardiaprecisionhealth
python3 -m http.server 8099 --directory . &
SERVER_PID=$!
sleep 1

CHROME=/opt/pw-browsers/chromium-1194/chrome-linux/chrome

# Dump DOM text of a page
$CHROME \
  --headless=new --no-sandbox --disable-gpu --disable-dev-shm-usage \
  --dump-dom \
  "http://localhost:8099/index.html" 2>/dev/null | grep -A2 "logo-icon\|nav-brand"

kill $SERVER_PID 2>/dev/null
```

## Run (human path)

```bash
cd /home/user/ardiaprecisionhealth
python3 -m http.server 8099
# Open http://localhost:8099/index.html in browser
# Ctrl-C to stop
```

## Page map

| Slug | File |
|------|------|
| `index` | Homepage |
| `dashboard` | Analytics dashboard (chart.js, live activity feed) |
| `investors` | Investor relations |
| `about` | About Ardia |
| `architecture` | Technical architecture |
| `ardia-profile` | Company profile |
| `case-studies` | Clinical case studies |
| `contact` | Contact |
| `how-it-works` | Platform walkthrough |
| `how-software-works` | Technical deep-dive |
| `mobile-app` | Mobile app page |
| `our-product` | Product overview |
| `pama` | PAMA compliance |
| `plg-sandbox` | PLG sandbox |
| `precision-medicine` | Precision medicine |
| `research` | Research & publications |
| `roadmap` | Product roadmap |
| `security` | Security & compliance |
| `solutions` | Solutions hub |
| `vision` | Company vision |

## Gotchas

- **SSL handshake errors in Chromium stderr** — these come from Google Fonts / CDN calls that fail in the sandboxed container. They are noise — the page renders correctly regardless. Suppress with `2>/dev/null`.
- **chart.js charts render blank** — chart.js requires canvas + a real event loop tick to paint. In headless screenshots the chart areas appear empty. This is expected; charts render fine in a real browser.
- **Port 8099 already in use** — kill with `kill $(lsof -ti:8099)` before restarting.
- **`--headless` (old) vs `--headless=new`** — use `--headless=new` (Chrome 112+). Old `--headless` produces smaller screenshots with rendering issues.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `Address already in use` on port 8099 | `kill $(lsof -ti:8099)` |
| Screenshot file is 0 bytes | Add `sleep 1` after starting server before screenshotting |
| Page shows raw HTML (no styles) | Confirm server is serving from repo root, not a subdirectory |
| `chrome: error while loading shared libraries` | Pre-installed at `/opt/pw-browsers` — use full path, not `which chromium` |
