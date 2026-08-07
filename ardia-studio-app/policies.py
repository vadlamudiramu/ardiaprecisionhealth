"""Ardia Studio — CMS coverage-policy grounding (Local Coverage Determinations).

A small, HAND-VERIFIED set of real, currently-active Medicare LCDs relevant to the
molecular / NGS / toxicology / pharmacogenomics reimbursement work Ardia's
denial-recovery models reason about. Every id + title + URL below was confirmed
against the LIVE CMS Medicare Coverage Database on 2026-08-07 — the page <title>
and the Document Information block ("Retirement Date: N/A" = still active). There
is NO public JSON API for the MCD, so this is a curated snapshot rather than a live
feed; coverage policy changes, so the grounding always tells the model (and the
reader) to verify the current revision on CMS. Nothing here is model-generated.

match_policies() is a pure function (unit-tested, no network): it maps a
de-identified query's CPT/HCPCS codes + topic keywords to the applicable LCDs so a
reimbursement answer can cite the REAL policy instead of a vague reference — and
only codes CMS actually lists are recorded here (e.g. we do not assert 81455 is in
a code list we could not verify; keyword matching covers such cases instead).
"""
from __future__ import annotations

import re

_MCD = "https://www.cms.gov/medicare-coverage-database/view/lcd.aspx?lcdid="

# Verified 2026-08-07 against www.cms.gov/medicare-coverage-database (active; Retirement Date N/A).
POLICIES = [
    {"lcd_id": "L35025", "title": "MolDX: Molecular Diagnostic Tests (MDT)", "umbrella": True,
     "cpt_codes": [],
     "keywords": ["moldx", "molecular", "molecular diagnostic", "genetic test", "genetic testing",
                  "biomarker", "genomic", "z-code", "unique identifier", "molecular pathology"]},
    {"lcd_id": "L38045", "title": "MolDX: Next-Generation Sequencing for Solid Tumors",
     "cpt_codes": ["81445", "81449", "81457", "81458", "81459", "81479",
                   "0244u", "0250u", "0329u", "0334u", "0379u", "0391u", "0543u"],
     "keywords": ["ngs", "next-generation sequencing", "next generation sequencing", "solid tumor",
                  "tumor profiling", "genomic profiling", "comprehensive genomic", "panel", "sequencing"]},
    {"lcd_id": "L38158", "title": "MolDX: Next-Generation Sequencing for Solid Tumors",
     "cpt_codes": [],
     "keywords": ["ngs", "next-generation sequencing", "next generation sequencing", "solid tumor",
                  "tumor profiling", "genomic profiling", "comprehensive genomic", "panel", "sequencing"]},
    {"lcd_id": "L36393", "title": "Controlled Substance Monitoring and Drugs of Abuse Testing",
     "cpt_codes": ["80305", "80306", "80307", "g0480", "g0483", "g0659"],
     "keywords": ["toxicology", "drug testing", "drug test", "controlled substance", "drugs of abuse",
                  "presumptive", "definitive", "udt", "urine drug", "medication monitoring"]},
    {"lcd_id": "L34645", "title": "Urine Drug Testing",
     "cpt_codes": ["80305", "80306", "80307", "g0480", "g0481", "g0482", "g0483", "g0659"],
     "keywords": ["urine drug", "drug testing", "drug test", "toxicology", "udt", "presumptive", "definitive"]},
    {"lcd_id": "L36029", "title": "Urine Drug Testing",
     "cpt_codes": ["80305", "80306", "80307", "g0659"],
     "keywords": ["urine drug", "drug testing", "drug test", "toxicology", "udt", "presumptive", "definitive"]},
    {"lcd_id": "L38294", "title": "MolDX: Pharmacogenomics Testing",
     "cpt_codes": ["81225", "81226", "81418"],
     "keywords": ["pharmacogenomic", "pharmacogenomics", "pgx", "cyp2c19", "cyp2d6", "drug metabolism",
                  "drug-gene", "gene-drug"]},
    {"lcd_id": "L38335", "title": "MolDX: Pharmacogenomics Testing",
     "cpt_codes": ["81225", "81226", "81418"],
     "keywords": ["pharmacogenomic", "pharmacogenomics", "pgx", "cyp2c19", "cyp2d6", "drug metabolism",
                  "drug-gene", "gene-drug"]},
]

_CODE_RE = re.compile(r"\b(8\d{4}|g0\d{3}|0\d{3}u)\b", re.I)
_MOLECULAR_CODE_RE = re.compile(r"\b81\d{3}\b|\b0\d{3}u\b", re.I)  # any molecular CPT / PLA code


def match_policies(query, n=3):
    """Return applicable real CMS LCDs (as source dicts) for a query. Pure; never raises."""
    if not query:
        return []
    q = query.lower()
    codes = {c.lower() for c in _CODE_RE.findall(q)}
    has_molecular_code = bool(_MOLECULAR_CODE_RE.search(q))
    scored = []
    for p in POLICIES:
        s = 0
        for c in p["cpt_codes"]:
            if c in codes or c in q:
                s += 4
        for kw in p["keywords"]:
            if kw in q:
                s += 1
        if p.get("umbrella") and has_molecular_code:   # MolDX MDT governs all molecular tests
            s += 2
        if s:
            scored.append((s, p))
    scored.sort(key=lambda x: -x[0])
    out, seen = [], set()
    for _, p in scored:
        if p["title"] in seen:            # one citation per distinct policy title
            continue
        seen.add(p["title"])
        out.append({
            "source": "CMS Medicare Coverage Database (LCD)",
            "id": p["lcd_id"],
            "title": "%s (%s)" % (p["title"], p["lcd_id"]),
            "url": _MCD + p["lcd_id"][1:],
            "status": "active — verify current revision on CMS MCD",
            "year": "",
        })
        if len(out) >= n:
            break
    return out
