---
name: paper-publisher
description: Academic paper drafting, citation building, and judging opportunity finder for Rambabu Vadlamudi and Manasa Jampani. Generates publication-ready paper abstracts, full outlines, and citation frameworks from Ardia Health company documents to satisfy EB-1A Criterion 6 (scholarly publications), Criterion 4 (judging), and EB-2 NIW merit criteria. Use when asked about publishing papers, submitting to journals, arXiv preprints, peer reviewer roles, or building a publication record for immigration.
---

# Academic Paper Publisher & Citation Builder
## Ardia Health — Rambabu Vadlamudi & Manasa Jampani

Reads all 4 local company documents (white paper, pitch deck, business plan, outreach emails)
and generates publication-ready paper abstracts, structured outlines, citation libraries,
and judging opportunity lists for EB-1A Criterion 6, Criterion 4, EB-2 NIW, and O-1A.

Driver: `.claude/skills/paper-publisher/publisher.py`

---

## ⚠️ PLAGIARISM NOTICE — Architecture Name

**"Neuro-symbolic" is an extensively published term in healthcare AI.** PubMed (2025–2026) shows
existing papers using neuro-symbolic frameworks for: cholangitis management
([doi](https://doi.org/10.3390/jcm15051730)), oncology trial matching
([doi](https://doi.org/10.1016/j.esmorw.2026.100706)), corneal topography
([doi](https://doi.org/10.3389/frai.2026.1713747)), IoMT healthcare
([doi](https://doi.org/10.1038/s41598-025-31820-6)).

**The architecture is renamed to the DGP (Deterministic-Generative-Predictive) Clinical
Revenue Architecture** — Ram Vadlamudi's original coinage. This name is:
- Not used in any existing published paper
- Accurately describes the three layers (deterministic rules → generative LLM → predictive ML)
- Clearly differentiated by application domain: RCM/claim recovery (not clinical diagnosis)
- Protectable as intellectual property

---

## Verified Founder Profiles

| | Rambabu Vadlamudi | Manasa Jampani |
|---|---|---|
| **Role** | Founder & Enterprise Architect | Co-Founder & CEO |
| **IT Experience** | 15+ years | 10+ years |
| **Healthcare IT** | 8+ years | 5+ years |
| **Employers** | Alsac (St. Jude) / CIGNA / Medifast / Teladoc Health / United Health Care / ECFMG | Interwell Health / United HealthGroup / ECFMG |

Run `python3 publisher.py --founders` to print verified bios for paper author statements.

---

## Quick Start

```bash
cd /home/user/ardiaprecisionhealth

# Verify founder bios and architecture name FIRST
python3 .claude/skills/paper-publisher/publisher.py --founders
python3 .claude/skills/paper-publisher/publisher.py --architecture

# List all 5 papers
python3 .claude/skills/paper-publisher/publisher.py --list

# Get Paper 1 abstract — copy-paste ready for arXiv (submit TODAY)
python3 .claude/skills/paper-publisher/publisher.py --abstract 1

# Get judging opportunities (EB-1A Criterion 4) with contact details
python3 .claude/skills/paper-publisher/publisher.py --judging

# Full EB-1A / NIW / O-1A evidence status
python3 .claude/skills/paper-publisher/publisher.py --visa-map

# Generate + save all 5 papers to .txt files
python3 .claude/skills/paper-publisher/publisher.py --all --save
```

---

## The 5 Papers

| # | Title (short) | Lead | Top Journal | Visa Criteria |
|---|---------------|------|-------------|---------------|
| **1** | DGP Architecture for Clinical Claim Recovery | Ram | arXiv cs.AI → JAMIA | EB-1A C6 + C5, NIW P2 |
| **2** | Independent Lab Revenue Crisis: Systematic Analysis | Ram + Manasa | arXiv → Clinical Chemistry | EB-1A C6, NIW P1 |
| **3** | Compliance-by-Design: SB 1188 & TRAIGA | Ram + Manasa | AHIMA / Health Affairs | EB-1A C6, NIW P3 |
| **4** | Inside the Payer AI Black Box (Manasa's paper) | **Manasa** | **NEJM AI** | EB-1A C6, O-1A |
| **5** | Pilot Outcomes — DGP Architecture (post-launch) | Ram + Manasa | J Healthcare Mgmt | EB-1A C6, NIW P2 |

---

## Paper 1 — Submit NOW (arXiv, 1-2 days to public)

**Architecture name:** DGP (Deterministic-Generative-Predictive) Clinical Revenue Architecture

**What makes Paper 1 original vs. existing work:**
- All existing hybrid AI healthcare papers address clinical DIAGNOSIS
- DGP architecture addresses healthcare ADMINISTRATIVE automation (RCM/claim recovery)
- No prior published work applies this three-layer design to EDI 835/837 + FHIR R4 + MolDX compliance
- The 847-rule deterministic policy engine for LCD/NCD/MolDX/DEX Z-codes is a novel contribution

**arXiv submission steps:**
1. arxiv.org/submit → Category: **cs.AI** (primary), cs.IR (secondary), q-bio.QM (secondary)
2. Title + abstract: copy from `python3 publisher.py --abstract 1`
3. Authors: Rambabu Vadlamudi (Ardia Health, Argyle TX 76226)
4. Upload PDF — if no full paper yet, submit a technical report using the abstract + outline

---

## Paper 4 — Manasa's Unique Paper

**Why no one else can write this:**
- Manasa has 5+ years at Interwell Health, United HealthGroup, and ECFMG
- Direct healthcare IT experience inside payer and payer-adjacent organizations
- She has operational knowledge of how payer clinical operations teams configure AI denial systems
- This paper is uncopyable — the insider vantage point is unique to her career

**Target: NEJM AI** — exactly the journal seeking healthcare AI insider analysis with clinical implications.

Run: `python3 publisher.py --paper 4` for full abstract and outline.

---

## Judging / Peer Review (EB-1A Criterion 4)

| Opportunity | How | Timeline |
|-------------|-----|----------|
| **JAMIA Peer Reviewer** | Email editor@jamia.org | **This week** |
| **NIH SBIR/STTR Study Section** | csr.nih.gov — contact SRO | Rolling — highest prestige |
| **AMIA Reviewer** | amia.org | March–April annually |
| **HIMSS 2027 Reviewer** | himss.org | Q3 2026 |
| **Health Wildcatters Judge** | healthwildcatters.com/mentor | Rolling + generates press |

Run: `python3 publisher.py --judging` for exact contact details per opportunity.

---

## Citation Library (11 sources, all from Ardia documents)

| Ref | Source | Key Claim |
|-----|--------|-----------|
| [1] | JAMA Network Open April 2025 (Georgetown, n=29,919) | 2.76× higher denial odds for independent labs |
| [2] | XiFin 2024 (20M+ claims) | 35.3% molecular Dx denial rate — highest in healthcare |
| [3] | Frontiers in Pharmacology 2023 | Only 46% of PGx claims reimbursed |
| [4] | ACLA 2024 | 50%+ of labs considering selling if PAMA cuts take effect |
| [5] | HFMA/LigoLab 2024 | 65% of denied claims never appealed; 50–80.7% win rate |
| [6] | Waystar IPO 2024 | $3.5B RCM AI — hospital only, independent labs excluded |
| [7] | R1 RCM acquisition 2024 | $8.9B — validates AI RCM market |
| [8] | CMS PAMA | Up to 45% cumulative Medicare cuts by 2029 |
| [9] | Texas SB 1188 | First state healthcare AI accountability law |
| [10] | Texas TRAIGA (HB 149) | Third state with comprehensive AI legislation |
| [11] | CMS MolDX / AMA CPT | 75,000 tests, <200 CPT codes, 35%+ coding error rate |

**Note:** Verify DOIs for [1][3] before journal submission — pulled from Ardia white paper.
Run: `python3 publisher.py --citations` for full citation text with verification notes.

---

## Visa Criteria Status

| Criterion | Status | Fastest Action |
|-----------|--------|----------------|
| **EB-1A C5 — Original Contributions** | ✅ STRONG | Paper 1 documents the DGP architecture |
| **EB-1A C8 — Leading Role** | ⚠️ MODERATE | Strengthens after pilots launch |
| **EB-1A C6 — Publications** | ⚠️ GAP | **Submit Paper 1 to arXiv this week** |
| **EB-1A C4 — Judging** | ⚠️ GAP | **Email JAMIA today** |
| **EB-1A C3 — Press** | ⚠️ GAP | Pitch Becker's / MedCity |
| **EB-1A C2 — Membership** | ⚠️ GAP | Apply HIMSS + AMIA |
| **EB-1A C1 — Awards** | ⚠️ GAP | Apply Fast Company, DFW Awards |
| **NIW P1 — National Importance** | ✅ STRONG | All citations ready |
| **NIW P2 — Well Positioned** | ✅ STRONG | Both founders documented |
| **NIW P3 — Beneficial to US** | ✅ STRONG | Paper 3 covers this |

---

## Sample Output (verified working — run 2026-06-30)

```
Rambabu Vadlamudi — Founder & Enterprise Architect
  IT Experience: 15+ years total | Healthcare IT: 8+ years
  Employers: Alsac (St. Jude Children's Research Hospital) / CIGNA / Medifast /
             Teladoc Health / United Health Care / ECFMG

Manasa Jampani — Co-Founder & CEO
  IT Experience: 10+ years total | Healthcare IT: 5+ years
  Employers: Interwell Health / United HealthGroup / ECFMG

ARCHITECTURE: Deterministic-Generative-Predictive (DGP) Clinical Revenue Architecture
  L1 — Deterministic Policy Engine: 847-rule compliance engine (LCD/NCD/MolDX/DEX Z-codes)
  L2 — Generative Clinical Reasoning: LLM appeal brief generation (<90 seconds)
  L3 — Predictive Denial Prevention: ML pre-submission denial risk scoring
```

---

## Gotchas

- **Do not use "neuro-symbolic"** as the architecture name — it has extensive prior art in healthcare AI (PubMed 2025–2026). Use "DGP" or "Deterministic-Generative-Predictive" architecture.
- **arXiv preprints count for EB-1A** — USCIS accepts them as Criterion 6 evidence; no journal acceptance needed to start building the record
- **Verify DOIs** for [1] (JAMA 2025) and [3] (Frontiers Pharmacology 2023) before journal submission — they're cited in the white paper but DOIs weren't directly provided
- **Manasa's employers were Interwell Health / United HealthGroup / ECFMG** — not Cigna, Optum, or Teladoc (those were Ram's employers)
- **Paper 5** becomes the strongest evidence after pilot launch — empirical outcome data beats everything else for NIW Prong 2
- Use `--save` to generate `.txt` files that can be handed to a co-author, attorney, or ghostwriter

---

## Integration with Other Skills

- **`eb1a-niw-evidence`** — full immigration evidence profile
- **`linkedin-eb1a-scanner`** — scan LinkedIn export ZIP for additional publication/judging evidence
- **`deep-research`** — fetch latest papers citing JAMA 2025 or XiFin 2024 to build citation networks
