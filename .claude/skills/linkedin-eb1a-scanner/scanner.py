#!/usr/bin/env python3
"""
LinkedIn EB-1A/NIW Evidence Scanner
Usage:
  python3 scanner.py --export linkedin_export.zip   # process downloaded export
  python3 scanner.py --cookie "li_at=XXXXX"          # live scrape with session cookie
  python3 scanner.py --profile-url URL --cookie "..."  # scrape specific profile
"""

import argparse
import csv
import io
import json
import os
import re
import sys
import zipfile
from pathlib import Path

# ── EB-1A keyword taxonomy ────────────────────────────────────────────────────
CRITERIA = {
    "criterion_1_awards": [
        "award", "prize", "winner", "recognition", "honor", "fellowship",
        "grant", "scholarship", "distinguished", "excellence award",
    ],
    "criterion_2_membership": [
        "member", "fellow", "elected", "association", "society", "HIMSS",
        "AMIA", "IEEE", "ACM", "Forbes Council", "YPO", "advisory board",
    ],
    "criterion_3_press": [
        "featured in", "covered by", "interview", "quoted", "press",
        "article about", "profile in", "Forbes", "TechCrunch", "STAT News",
        "Becker's", "Modern Healthcare", "Health Affairs", "MedCity",
        "mentioned in", "news", "media",
    ],
    "criterion_4_judging": [
        "judge", "reviewer", "peer review", "panelist", "evaluate",
        "hackathon judge", "pitch competition", "review committee",
        "advisory", "mentor", "demo day",
    ],
    "criterion_5_contributions": [
        "invented", "developed", "built", "created", "designed",
        "architecture", "novel", "proprietary", "patent", "innovation",
        "neuro-symbolic", "FHIR", "HL7", "EDI", "clinical AI",
        "denial prevention", "RCM", "revenue cycle", "MolDX",
    ],
    "criterion_6_publications": [
        "published", "paper", "article", "journal", "preprint", "arXiv",
        "JAMIA", "NEJM", "JAMA", "research", "study", "white paper",
        "citation", "co-author", "wrote", "authored",
    ],
    "criterion_8_leadership": [
        "founder", "CEO", "CTO", "co-founder", "president", "director",
        "lead", "head of", "VP", "chief", "built company",
        "Ardia", "ardiahealthlabs",
    ],
    "niw_national_importance": [
        "healthcare", "clinical laboratory", "independent lab", "PAMA",
        "precision medicine", "pharmacogenomics", "NGS", "molecular diagnostic",
        "denial rate", "revenue recovery", "appeal", "HIPAA",
        "national", "US healthcare", "policy", "CMS", "Medicare",
    ],
}

EB1A_CRITERIA_LABELS = {
    "criterion_1_awards":         "Criterion 1 — Awards/Prizes",
    "criterion_2_membership":     "Criterion 2 — Membership in Distinguished Associations",
    "criterion_3_press":          "Criterion 3 — Press/Published Material About You",
    "criterion_4_judging":        "Criterion 4 — Judging Others' Work",
    "criterion_5_contributions":  "Criterion 5 — Original Contributions of Major Significance",
    "criterion_6_publications":   "Criterion 6 — Scholarly Articles / Publications",
    "criterion_8_leadership":     "Criterion 8 — Leading/Critical Role in Distinguished Org",
    "niw_national_importance":    "NIW — National Importance / Merit",
}


def score_text(text):
    """Score a piece of text against all EB-1A criteria. Returns matched criteria."""
    text_lower = text.lower()
    matches = {}
    for criterion, keywords in CRITERIA.items():
        hits = [kw for kw in keywords if kw.lower() in text_lower]
        if hits:
            matches[criterion] = hits
    return matches


def print_finding(item_type, content, matches, url=""):
    label = EB1A_CRITERIA_LABELS
    criteria_hit = [label[c] for c in matches if c in label]
    if not criteria_hit:
        return
    print(f"\n{'─'*70}")
    print(f"[{item_type}]")
    if url:
        print(f"URL: {url}")
    snippet = content[:300].replace("\n", " ")
    print(f"Content: {snippet}...")
    print(f"EB-1A/NIW relevance: {', '.join(criteria_hit)}")
    for crit, keywords in matches.items():
        print(f"  Keywords matched ({crit}): {', '.join(keywords[:5])}")


# ── Export ZIP processor ──────────────────────────────────────────────────────

def process_export(zip_path):
    print(f"\n{'═'*70}")
    print(f"LINKEDIN EXPORT ANALYSIS — {zip_path}")
    print(f"{'═'*70}")

    findings = []

    with zipfile.ZipFile(zip_path, 'r') as zf:
        files = zf.namelist()
        print(f"\nFiles in export: {len(files)}")
        for f in sorted(files):
            print(f"  {f}")

        # ── Posts / Shares ───────────────────────────────────────────────────
        for fname in ["Posts.csv", "Shares.csv", "Articles.csv"]:
            if fname in files:
                print(f"\n{'─'*70}")
                print(f"SCANNING: {fname}")
                data = zf.read(fname).decode("utf-8-sig", errors="ignore")
                reader = csv.DictReader(io.StringIO(data))
                for row in reader:
                    content = " ".join(str(v) for v in row.values())
                    matches = score_text(content)
                    if matches:
                        url = row.get("ShareLink", row.get("URL", ""))
                        print_finding(fname.replace(".csv",""), content, matches, url)
                        findings.append({"type": fname, "content": content[:500], "criteria": list(matches.keys())})

        # ── Comments ─────────────────────────────────────────────────────────
        for fname in ["Comments.csv"]:
            if fname in files:
                print(f"\n{'─'*70}")
                print(f"SCANNING: {fname}")
                data = zf.read(fname).decode("utf-8-sig", errors="ignore")
                reader = csv.DictReader(io.StringIO(data))
                for row in reader:
                    content = " ".join(str(v) for v in row.values())
                    matches = score_text(content)
                    if matches:
                        print_finding("Comment", content, matches)
                        findings.append({"type": "Comment", "content": content[:500], "criteria": list(matches.keys())})

        # ── Reactions / Saved items ──────────────────────────────────────────
        for fname in ["Reactions.csv", "SavedJobs.csv"]:
            if fname in files:
                print(f"\n{'─'*70}")
                print(f"SCANNING: {fname}")
                data = zf.read(fname).decode("utf-8-sig", errors="ignore")
                reader = csv.DictReader(io.StringIO(data))
                for i, row in enumerate(reader):
                    content = " ".join(str(v) for v in row.values())
                    matches = score_text(content)
                    if matches:
                        print_finding(fname.replace(".csv",""), content, matches)
                        findings.append({"type": fname, "content": content[:500], "criteria": list(matches.keys())})
                    if i > 500:
                        break

        # ── Profile (Education, Experience, Skills) ──────────────────────────
        for fname in ["Profile.csv", "Education.csv", "Certifications.csv",
                      "Honors.csv", "Publications.csv", "Languages.csv"]:
            if fname in files:
                print(f"\n{'─'*70}")
                print(f"SCANNING: {fname}")
                data = zf.read(fname).decode("utf-8-sig", errors="ignore")
                reader = csv.DictReader(io.StringIO(data))
                for row in reader:
                    content = " ".join(str(v) for v in row.values())
                    matches = score_text(content)
                    print_finding(fname.replace(".csv",""), content, matches)
                    findings.append({"type": fname, "content": content[:500], "criteria": list(matches.keys())})

        # ── Messages (look for expert/media contacts) ────────────────────────
        for fname in ["messages.csv", "Messages.csv"]:
            if fname in files:
                print(f"\nSCANNING: {fname} (checking for press/expert contacts)")
                data = zf.read(fname).decode("utf-8-sig", errors="ignore")
                reader = csv.DictReader(io.StringIO(data))
                for i, row in enumerate(reader):
                    content = " ".join(str(v) for v in row.values())
                    matches = score_text(content)
                    if matches and ("criterion_3_press" in matches or "criterion_4_judging" in matches):
                        print_finding("Message (potential press/judge contact)", content, matches)
                    if i > 1000:
                        break

    # ── Summary report ────────────────────────────────────────────────────────
    print(f"\n{'═'*70}")
    print("EVIDENCE SUMMARY")
    print(f"{'═'*70}")
    total = len(findings)
    print(f"Total EB-1A/NIW relevant items found: {total}")
    print()

    criteria_counts = {}
    for f in findings:
        for c in f["criteria"]:
            criteria_counts[c] = criteria_counts.get(c, 0) + 1

    for crit, label in EB1A_CRITERIA_LABELS.items():
        count = criteria_counts.get(crit, 0)
        bar = "█" * min(count, 20)
        status = "✅" if count >= 3 else "⚠️ " if count >= 1 else "❌"
        print(f"  {status} {label}: {count} items  {bar}")

    # Save JSON output
    outfile = Path(zip_path).stem + "_eb1a_analysis.json"
    with open(outfile, "w") as f:
        json.dump({"total_findings": total, "criteria_counts": criteria_counts,
                   "findings": findings}, f, indent=2)
    print(f"\nFull results saved to: {outfile}")
    return findings


# ── Live Chromium scraper (with session cookie) ───────────────────────────────

def scrape_live(profile_url, cookie_string, screenshot_dir="/tmp/linkedin-screenshots"):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: pip install playwright first")
        sys.exit(1)

    os.makedirs(screenshot_dir, exist_ok=True)
    chrome = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

    # Parse cookie string like "li_at=XXXXX; JSESSIONID=YYYY"
    cookies = []
    for part in cookie_string.split(";"):
        part = part.strip()
        if "=" in part:
            name, _, value = part.partition("=")
            cookies.append({
                "name": name.strip(),
                "value": value.strip(),
                "domain": ".linkedin.com",
                "path": "/"
            })

    findings = []

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=chrome, headless=True)
        ctx = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            viewport={"width": 1440, "height": 900}
        )
        ctx.add_cookies(cookies)
        page = ctx.new_page()

        pages_to_scan = [
            (profile_url, "profile"),
            (profile_url + "detail/recent-activity/posts/", "posts"),
            (profile_url + "detail/recent-activity/shares/", "shares"),
            (profile_url + "detail/recent-activity/comments/", "comments"),
            ("https://www.linkedin.com/my-items/saved-posts/", "saved_posts"),
            ("https://www.linkedin.com/my-items/saved-articles/", "saved_articles"),
        ]

        for url, label in pages_to_scan:
            print(f"\nScraping: {label} — {url}")
            try:
                page.goto(url, timeout=15000, wait_until="domcontentloaded")
                page.wait_for_timeout(2000)

                # Screenshot
                ss_path = f"{screenshot_dir}/{label}.png"
                page.screenshot(path=ss_path, full_page=False)
                print(f"  Screenshot: {ss_path}")

                # Extract text
                text = page.evaluate("() => document.body.innerText")
                matches = score_text(text)
                if matches:
                    print_finding(f"LinkedIn {label}", text[:1000], matches, url)
                    findings.append({"type": label, "url": url,
                                     "content": text[:2000], "criteria": list(matches.keys())})

                # Extract individual posts
                posts = page.locator(".feed-shared-update-v2, .occludable-update, .profile-creator-shared-feed-update__container")
                count = posts.count()
                print(f"  Found {count} post elements")
                for i in range(min(count, 50)):
                    try:
                        post_text = posts.nth(i).inner_text()
                        post_matches = score_text(post_text)
                        if post_matches:
                            print_finding(f"Post #{i+1}", post_text, post_matches)
                            findings.append({"type": "post", "url": url,
                                             "content": post_text[:500], "criteria": list(post_matches.keys())})
                    except Exception:
                        pass

            except Exception as e:
                print(f"  Error loading {url}: {e}")

        browser.close()

    return findings


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="LinkedIn EB-1A/NIW Evidence Scanner")
    parser.add_argument("--export", help="Path to LinkedIn data export ZIP file")
    parser.add_argument("--cookie", help='LinkedIn session cookie string: "li_at=XXXXX"')
    parser.add_argument("--profile-url", default="https://www.linkedin.com/in/ram-vadlamudi-b69097175/",
                        help="LinkedIn profile URL")
    parser.add_argument("--screenshot-dir", default="/tmp/linkedin-screenshots",
                        help="Directory to save screenshots")

    args = parser.parse_args()

    if not args.export and not args.cookie:
        parser.print_help()
        print("\nExamples:")
        print("  # Process downloaded LinkedIn export:")
        print("  python3 scanner.py --export linkedin_Basic_LinkedInDataExport.zip")
        print()
        print("  # Live scrape with session cookie (open DevTools → Application → Cookies → li_at):")
        print('  python3 scanner.py --cookie "li_at=AQEDATxxxxxx"')
        sys.exit(0)

    all_findings = []

    if args.export:
        if not os.path.exists(args.export):
            print(f"ERROR: Export file not found: {args.export}")
            sys.exit(1)
        all_findings += process_export(args.export)

    if args.cookie:
        all_findings += scrape_live(args.profile_url, args.cookie, args.screenshot_dir)

    print(f"\n{'═'*70}")
    print(f"TOTAL EB-1A/NIW EVIDENCE ITEMS FOUND: {len(all_findings)}")
    print(f"{'═'*70}")


if __name__ == "__main__":
    main()
