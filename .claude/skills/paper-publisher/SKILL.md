---
name: paper-publisher
description: Academic paper drafting, citation building, and judging opportunity finder for Rambabu Vadlamudi and Manasa Jampani. Generates publication-ready paper abstracts, full outlines, and citation frameworks from Ardia Health company documents to satisfy EB-1A Criterion 6 (scholarly publications), Criterion 4 (judging), and EB-2 NIW merit criteria. Use when asked about publishing papers, submitting to journals, arXiv preprints, peer reviewer roles, or building a publication record for immigration.
---

# Academic Paper Publisher & Citation Builder
## Ardia Health — Rambabu Vadlamudi & Manasa Jampani

Reads all 4 local company documents (white paper, pitch deck, business plan, outreach emails) and generates publication-ready paper abstracts, structured outlines, complete citation libraries, and judging opportunity lists — everything needed to submit to arXiv, JAMIA, NEJM AI, and other journals to build EB-1A Criterion 6 and O-1A evidence.

Driver: `.claude/skills/paper-publisher/publisher.py`
Source docs (auto-loaded): white paper, pitch deck, business plan (all in repo root)

---

## Quick Start

```bash
cd /home/user/ardiaprecisionhealth

# See all 5 papers in the pipeline
python3 .claude/skills/paper-publisher/publisher.py --list

# Generate Paper 1 with abstract (submit to arXiv TODAY — live in 1-2 days)
python3 .claude/skills/paper-publisher/publisher.py --paper 1

# Get abstract only (copy-paste ready for arXiv submission form)
python3 .claude/skills/paper-publisher/publisher.py --abstract 1

# Check full EB-1A/NIW/O-1A status and gaps
python3 .claude/skills/paper-publisher/publisher.py --visa-map

# Find peer review / judging opportunities (EB-1A Criterion 4)
python3 .claude/skills/paper-publisher/publisher.py --judging

# Generate everything + save each paper to a .txt file
python3 .claude/skills/paper-publisher/publisher.py --all --save
```

---

## The 5 Papers

| # | Title (short) | Lead Author | Top Journal | Visa Criteria |
|---|---------------|-------------|-------------|---------------|
| **1** | Neuro-Symbolic Sandwich Architecture for Healthcare RCM | Ram | arXiv cs.AI → JAMIA | EB-1A C6, C5, NIW P2 |
| **2** | Independent Lab Revenue Crisis: Systematic Review | Ram + Manasa | arXiv → Clinical Chemistry | EB-1A C6, NIW P1 |
| **3** | AI Governance Under Texas SB 1188 & TRAIGA | Ram + Manasa | AHIMA / Health Affairs | EB-1A C6, NIW P3 |
| **4** | Payer AI Denial Algorithms: Insider Analysis | **Manasa** | NEJM AI | EB-1A C6, O-1A |
| **5** | Pilot Outcomes (after Q2 2026 launch) | Ram + Manasa | J Healthcare Mgmt | EB-1A C6, NIW P2 |

---

## Paper 1 — Submit NOW (arXiv, 1-2 days to public)

**Title:** Neuro-Symbolic Sandwich Architecture for Healthcare Revenue Cycle Management: Combining Large Language Model Clinical Reasoning, Deterministic Policy Engines, and Machine Learning Denial Prediction

**Why arXiv first:**
- arXiv preprint is publicly citable the day it goes live (1–2 business days)
- Counts as a peer-reviewed publication for EB-1A/O-1A under USCIS practice
- Creates a timestamp proving Ram invented the NSSA before any competitor
- Can simultaneously submit to JAMIA; arXiv does not preclude journal submission

**arXiv submission steps:**
1. Go to arxiv.org/submit
2. Category: cs.AI (primary), cs.IR (secondary), q-bio.QM (secondary)
3. Title: copy from `--paper 1` output
4. Abstract: copy from `--abstract 1` output
5. Authors: Rambabu Vadlamudi (Ardia Health, Argyle TX)
6. Upload PDF of the paper (or use the abstract alone as a technical report)

---

## Paper 4 — Manasa's Unique Paper (Only She Can Write This)

**Title:** Payer AI Denial Algorithms in Clinical Laboratory Claims: An Insider Analysis of Decision Logic, Documentation Requirements, and AI-Countermeasure Strategies

**Why this is extraordinary:**
- Manasa spent 12+ years at Cigna, UnitedHealth Group, Optum, and Teladoc Health
- She literally built the payer-side denial systems that Ardia now defeats
- No other researcher has this insider vantage point — makes this paper uncopyable
- NEJM AI, Health Affairs, and AJMC actively want this type of industry insider perspective

Run: `python3 publisher.py --paper 4` for the full abstract and outline.

---

## Judging / Peer Review Opportunities (EB-1A Criterion 4)

| Opportunity | Org | Act By | Notes |
|-------------|-----|--------|-------|
| **JAMIA Peer Reviewer** | JAMIA | **Now** | Email editor@jamia.org — fastest route |
| **AMIA Reviewer** | AMIA | Q1 each yr | Annual Symposium reviews March–April |
| **NIH SBIR/STTR Study Section** | NIH | Rolling | Highest prestige EB-1A judging evidence |
| **Health Wildcatters Judge** | HW Dallas | Rolling | Also generates press (Criterion 3) |
| **HIMSS Reviewer** | HIMSS | Q3 2026 | For HIMSS 2027 |
| **SXSW Health Pitch Judge** | SXSW | Sep–Oct | Also generates press |

Run: `python3 publisher.py --judging` for exact contact details and how-to for each.

---

## Citation Library (All from Ardia's Source Docs)

| Ref | Source | Key Claim | Visa Use |
|-----|--------|-----------|----------|
| [1] | JAMA Network Open, April 2025 (Georgetown, n=29,919) | 2.76× higher denial odds for independent labs | NIW P1, EB-1A C5 |
| [2] | XiFin 2024 (20M+ claims) | 35.3% molecular Dx denial rate — highest in healthcare | NIW P1 |
| [3] | Frontiers in Pharmacology 2023 | Only 46% of PGx claims reimbursed | NIW P1 |
| [4] | ACLA 2024 | 50%+ of labs considering selling if PAMA cuts take effect | NIW P1 |
| [5] | HFMA/LigoLab 2024 | 65% of denied claims never appealed; 50–80.7% win rate | NIW P1 |
| [6] | Waystar IPO 2024 | $3.5B RCM AI valuation — hospital only, independent labs excluded | EB-1A C5 |
| [7] | R1 RCM acquisition 2024 | $8.9B — validates AI RCM market | NIW P3 |
| [8] | CMS PAMA | Up to 45% cumulative Medicare cuts by 2029 | NIW P1 |
| [9] | Texas SB 1188 | First state healthcare AI accountability law | EB-1A C5, NIW P3 |
| [10] | Texas TRAIGA (HB 149) | Third state with comprehensive AI legislation | EB-1A C5, NIW P3 |
| [11] | CMS MolDX / AMA CPT | 75,000 tests → <200 CPT codes; 35%+ error/denial rates | EB-1A C5 |

Run: `python3 publisher.py --citations` for full citations with paragraph-length details.

---

## Visa Criteria Map (Summary)

| Criterion | Status | Fastest Action |
|-----------|--------|----------------|
| **EB-1A C5 — Original Contributions** | ✅ STRONG | Paper 1 documents the NSSA architecture |
| **EB-1A C8 — Leading Role** | ⚠️ MODERATE | Strengthens after pilots launch |
| **EB-1A C6 — Publications** | ⚠️ GAP | Submit Paper 1 to arXiv this week |
| **EB-1A C4 — Judging** | ⚠️ GAP | Email JAMIA today; apply to NIH study section |
| **EB-1A C3 — Press** | ⚠️ GAP | Pitch Becker's / MedCity on PAMA 2027 story |
| **EB-1A C2 — Membership** | ⚠️ GAP | Apply to HIMSS, AMIA, Forbes Tech Council |
| **EB-1A C1 — Awards** | ⚠️ GAP | Apply to Fast Company, DFW Innovation Awards |
| **NIW P1 — National Importance** | ✅ STRONG | All citations ready (refs [1]–[5][8]) |
| **NIW P2 — Well Positioned** | ✅ STRONG | White paper + Paper 4 (Manasa) |
| **NIW P3 — Beneficial to US** | ✅ STRONG | Paper 3 (AI governance) documents this |

Run: `python3 publisher.py --visa-map` for detailed evidence + documents needed per criterion.

---

## Sample Output (verified working — run 2026-06-30)

```
════════════════════════════════════════════════════════════════════════
AVAILABLE PAPERS — Ardia Health Academic Publication Pipeline
════════════════════════════════════════════════════════════════════════

Paper 1: Neuro-Symbolic Sandwich Architecture for Healthcare Revenue Cycle Mana...
  Authors: Rambabu Vadlamudi
  Top journal: arXiv cs.AI (preprint — submit first, public in 1–2 days)
  Key criterion: EB-1A Criterion 6 — Scholarly Publication (peer-reviewed technical paper)

Paper 2: The Independent Laboratory Revenue Crisis: A Systematic Analysis of Cl...
  Authors: Rambabu Vadlamudi, Manasa Jampani
  Top journal: arXiv q-bio.QM or cs.CY (preprint)
  Key criterion: EB-1A Criterion 6 — Scholarly Publication (systematic review)
...

NEXT STEPS (priority order):
  1. Submit Paper 1 abstract to arXiv cs.AI — goes live in 1-2 days
     → Immediately satisfies EB-1A Criterion 6 (scholarly publication)
  2. Email JAMIA / AMIA to register as peer reviewer
     → Immediately satisfies EB-1A Criterion 4 (judging)
  3. Submit Paper 2 to arXiv q-bio.QM
  4. Apply for HIMSS + AMIA membership (Criterion 2)
  5. Pitch Becker's / MedCity on PAMA 2027 story (Criterion 3)
```

---

## Gotchas

- **arXiv preprints count for EB-1A** — USCIS has repeatedly accepted arXiv preprints as evidence for Criterion 6; you do not need to wait for peer review
- **Paper 4 is Manasa's strongest individual credential** — no other researcher can write an insider payer AI analysis with her exact background; prioritize this for O-1A
- **LinkedIn data export** (when it arrives) may contain post content, comments, and reactions that can be cited as additional evidence of field contribution — run the linkedin-eb1a-scanner skill on the ZIP
- **Pilot results (Paper 5)** becomes the strongest individual paper after launch — it's the one with empirical outcome data
- **Save flag** — use `--save` to generate `.txt` files in the repo root that can be handed to a ghostwriter, attorney, or co-author

---

## Integration with Other Skills

- **`eb1a-niw-evidence`** — full immigration evidence profile (complement to this skill)
- **`linkedin-eb1a-scanner`** — scans LinkedIn posts/activity for additional evidence once export ZIP arrives
- **`deep-research`** — use to fetch latest publications citing the JAMA 2025 Georgetown study or XiFin 2024 data to strengthen citation networks
