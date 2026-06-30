---
name: linkedin-eb1a-scanner
description: Scan LinkedIn saved posts, activity, articles, and profile data for EB-1A Extraordinary Ability and EB-2 NIW immigration evidence. Use when asked to check LinkedIn activity, find publication/judging/press evidence for immigration petitions, or analyze saved posts for Ram Vadlamudi or Manasa Jampani.
---

# LinkedIn EB-1A / NIW Evidence Scanner

Scans LinkedIn data for evidence matching all 10 EB-1A criteria and the EB-2 NIW Dhanasar framework. Works two ways: (1) processing LinkedIn's downloadable data export ZIP, or (2) live scraping with a session cookie.

Driver: `.claude/skills/linkedin-eb1a-scanner/scanner.py`
All paths relative to repo root: `/home/user/ardiaprecisionhealth/`

## Prerequisites

```bash
pip install playwright -q
# Chromium already at /opt/pw-browsers/chromium-1194/chrome-linux/chrome
```

## Run (agent path) — Option A: LinkedIn Data Export

**This is the reliable path.** LinkedIn data exports contain all posts, articles, comments, reactions, honors, certifications, and profile data.

### Step 1: Download your LinkedIn export (do this manually in browser)
1. Go to linkedin.com → **Me** → **Settings & Privacy**
2. **Data Privacy** → **Get a copy of your data**
3. Select: **Posts**, **Articles**, **Comments**, **Reactions**, **Profile**, **Honors & Awards**, **Certifications**, **Publications**, **Recommendations**
4. Click **Request archive** — email arrives in ~10 minutes to ~24 hours
5. Download the ZIP file — name looks like `Basic_LinkedInDataExport_06-30-2026.zip`

### Step 2: Drop the ZIP into the project folder and run

```bash
cd /home/user/ardiaprecisionhealth

# Copy the export ZIP here first, then:
python3 .claude/skills/linkedin-eb1a-scanner/scanner.py \
  --export Basic_LinkedInDataExport_06-30-2026.zip
```

Output: color-coded findings per EB-1A criterion + JSON results file.

---

## Run (agent path) — Option B: Live Scrape with Session Cookie

Scrapes your live LinkedIn profile, recent activity, posts, saved items. Requires your `li_at` session cookie.

### Get your session cookie (30 seconds):
1. Open linkedin.com in Chrome → logged in
2. Press **F12** → **Application** tab → **Cookies** → `https://www.linkedin.com`
3. Find `li_at` → copy its **Value**

### Run the live scraper:

```bash
cd /home/user/ardiaprecisionhealth

python3 .claude/skills/linkedin-eb1a-scanner/scanner.py \
  --cookie "li_at=AQEDATxxxxxxxxxxxxxx" \
  --profile-url "https://www.linkedin.com/in/ram-vadlamudi-b69097175/" \
  --screenshot-dir /tmp/linkedin-screenshots
```

Screenshots saved to `/tmp/linkedin-screenshots/`:
- `profile.png` — profile page
- `posts.png` — recent activity / posts
- `saved_posts.png` — saved posts
- `saved_articles.png` — saved articles

---

## What the Scanner Finds

Scans every piece of text against this EB-1A keyword taxonomy:

| Criterion | What it looks for |
|-----------|-------------------|
| **1 — Awards/Prizes** | award, prize, winner, recognition, honor, fellowship, excellence |
| **2 — Membership** | member, fellow, elected, HIMSS, AMIA, IEEE, Forbes Council, advisory board |
| **3 — Press** | featured in, Forbes, TechCrunch, Becker's, Modern Healthcare, interview, quoted |
| **4 — Judging** | judge, reviewer, peer review, panelist, hackathon judge, review committee |
| **5 — Contributions** | invented, designed, architecture, novel, proprietary, neuro-symbolic, FHIR, RCM |
| **6 — Publications** | published, paper, JAMA, NEJM, JAMIA, arXiv, research, authored, white paper |
| **8 — Leadership** | founder, CEO, CTO, co-founder, Ardia, ardiahealthlabs |
| **NIW** | PAMA, molecular diagnostic, denial rate, precision medicine, clinical laboratory |

---

## Sample Output (verified working — run against test data 2026-06-30)

```
══════════════════════════════════════════════
EVIDENCE SUMMARY
══════════════════════════════════════════════
Total EB-1A/NIW relevant items found: 12

  ⚠️  Criterion 1 — Awards/Prizes: 1 items
  ⚠️  Criterion 2 — Membership: 2 items
  ❌ Criterion 3 — Press: 0 items  ← GAP
  ⚠️  Criterion 4 — Judging: 2 items
  ✅ Criterion 5 — Contributions: 9 items
  ✅ Criterion 6 — Publications: 5 items
  ✅ Criterion 8 — Leadership: 3 items
  ✅ NIW — National Importance: 11 items
```

---

## Gotchas

- **LinkedIn blocks headless browsers** from this container (ERR_TUNNEL_CONNECTION_FAILED) — use the export ZIP method or provide a session cookie from your local machine
- **Export format varies** — LinkedIn sometimes names files `Posts.csv`, sometimes `posts.csv` — the scanner handles both
- **Session cookies expire** in ~1 year but may expire sooner if LinkedIn detects automation — if scraping fails, get a fresh `li_at` value
- **Export only covers public + your own content** — it will NOT include posts you've merely saved/reacted to if they're from other people (those appear in Reactions.csv with limited metadata)

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `KeyError: 'Posts'` | Export ZIP has unexpected file names — check `Files in export:` output and adjust |
| `playwright._errors.Error: net::ERR_TUNNEL_CONNECTION_FAILED` | Container can't reach LinkedIn — use `--export` mode instead |
| `No module named 'playwright'` | Run `pip install playwright -q` |
| Cookie scrape loads login page | Session cookie expired — get fresh `li_at` from browser DevTools |
| 0 findings on real export | Add more posts/articles to your LinkedIn profile — the scanner only finds what's there |
