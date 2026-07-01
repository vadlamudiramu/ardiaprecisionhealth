// Driver for the ARDIA PRECISION HEALTH static site.
// Serves the repo root over HTTP and drives pages with Playwright.
//
// Usage:
//   node driver.mjs shot <page.html> [out.png]     screenshot one page
//   node driver.mjs shot-all [outDir]               screenshot every top-level page
//   node driver.mjs check <page.html>               print title, console errors, nav-brand check
//   node driver.mjs check-all                       run `check` over every top-level page
//
// Env:
//   PORT       port for the static server (default 8123)
//   BASE_URL   skip the built-in server and hit an already-running one

import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFile, readdir, mkdir } from 'node:fs/promises';
import { extname, join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..', '..', '..');
const PORT = process.env.PORT || 8123;

const MIME = { '.html': 'text/html', '.css': 'text/css', '.js': 'application/javascript',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.json': 'application/json' };

async function startServer() {
  if (process.env.BASE_URL) return { base: process.env.BASE_URL, close: () => {} };
  const server = createServer(async (req, res) => {
    try {
      const path = decodeURIComponent(req.url.split('?')[0]);
      const file = join(ROOT, path === '/' ? 'index.html' : path);
      const data = await readFile(file);
      res.writeHead(200, { 'Content-Type': MIME[extname(file)] || 'application/octet-stream' });
      res.end(data);
    } catch {
      res.writeHead(404);
      res.end('not found');
    }
  });
  await new Promise((resolve) => server.listen(PORT, resolve));
  return { base: `http://localhost:${PORT}`, close: () => server.close() };
}

async function listPages() {
  const files = await readdir(ROOT);
  return files.filter((f) => f.endsWith('.html') && !f.startsWith('_')).sort();
}

async function checkPage(page, base, name) {
  const errors = [];
  const onErr = (msg) => errors.push(typeof msg.text === 'function' ? msg.text() : String(msg));
  page.on('pageerror', onErr);
  const consoleHandler = (msg) => { if (msg.type() === 'error') errors.push(msg.text()); };
  page.on('console', consoleHandler);

  const resp = await page.goto(`${base}/${name}`, { waitUntil: 'networkidle', timeout: 20000 });
  const status = resp ? resp.status() : null;
  const title = await page.title();
  const hasLogoIcon = await page.locator('.logo-icon, .nav-brand-icon, .logo-mark, .nav-logo-icon, .nav-logo-box').first().isVisible().catch(() => false);
  // The gradient underline is drawn on a ::before/::after pseudo-element in
  // every page (e.g. `.logo-main::after`), not on a real element — plain
  // getComputedStyle(el) always misses it. Must pass the pseudo-element name.
  const hasGradientUnderline = await page.evaluate(() => {
    const isTealAmberGradient = (bg) =>
      bg.includes('linear-gradient') && bg.includes('20, 184, 166') && bg.includes('245, 158, 11');
    for (const el of document.querySelectorAll('*')) {
      if (isTealAmberGradient(getComputedStyle(el).backgroundImage)) return true;
      if (isTealAmberGradient(getComputedStyle(el, '::before').backgroundImage)) return true;
      if (isTealAmberGradient(getComputedStyle(el, '::after').backgroundImage)) return true;
    }
    return false;
  }).catch(() => false);

  page.off('pageerror', onErr);
  page.off('console', consoleHandler);
  return { name, status, title, hasLogoIcon, hasGradientUnderline, consoleErrors: errors };
}

async function main() {
  const [, , cmd, arg1, arg2] = process.argv;
  const { base, close } = await startServer();
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });

  try {
    if (cmd === 'shot') {
      const name = arg1 || 'index.html';
      const out = arg2 || `/tmp/ardia-shots/${name.replace('.html', '')}.png`;
      await mkdir(dirname(out), { recursive: true });
      await page.goto(`${base}/${name}`, { waitUntil: 'networkidle', timeout: 20000 });
      await page.screenshot({ path: out });
      console.log(JSON.stringify({ name, screenshot: out }));
    } else if (cmd === 'shot-all') {
      const outDir = arg1 || '/tmp/ardia-shots';
      await mkdir(outDir, { recursive: true });
      const pages = await listPages();
      const results = [];
      for (const name of pages) {
        const out = join(outDir, `${name.replace('.html', '')}.png`);
        await page.goto(`${base}/${name}`, { waitUntil: 'networkidle', timeout: 20000 });
        await page.screenshot({ path: out });
        results.push({ name, screenshot: out });
      }
      console.log(JSON.stringify(results, null, 2));
    } else if (cmd === 'check') {
      const name = arg1 || 'index.html';
      console.log(JSON.stringify(await checkPage(page, base, name), null, 2));
    } else if (cmd === 'check-all') {
      const pages = await listPages();
      const results = [];
      for (const name of pages) results.push(await checkPage(page, base, name));
      console.log(JSON.stringify(results, null, 2));
    } else {
      console.error('Usage: node driver.mjs <shot|shot-all|check|check-all> [args]');
      process.exitCode = 1;
    }
  } finally {
    await browser.close();
    close();
  }
}

main();
