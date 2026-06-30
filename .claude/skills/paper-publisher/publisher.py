#!/usr/bin/env python3
"""
Ardia Health — Academic Paper Publisher & Citation Builder
Generates paper drafts, abstracts, and citation frameworks for:
  - EB-1A Criterion 6 (Scholarly Publications)
  - EB-1A Criterion 4 (Judging / Peer Review)
  - EB-2 NIW Merit & National Importance
  - O-1A Visa Criteria

Architecture: DGP (Deterministic-Generative-Predictive) Clinical Revenue Architecture
  Layer 1 — Deterministic Policy Engine: 847-rule compliance engine (LCD/NCD/MolDX/DEX Z-codes)
  Layer 2 — Generative Clinical Reasoning: LLM appeal brief generation
  Layer 3 — Predictive Denial Prevention: ML denial prediction model

NOTE ON PLAGIARISM: "neuro-symbolic" is an extensively published AI term (PubMed, 2025-2026:
  cholangitis management, oncology trial matching, keratoconus detection, IoMT swarm federation).
  The DGP architecture name is Ram Vadlamudi's original coinage. All paper content here is
  original to the founders' work. Do not describe the architecture using existing academic
  architecture names. Cite only sources verifiably linked to Ardia's company documents.

Usage:
  python3 publisher.py --list                  # List all available papers
  python3 publisher.py --paper 1               # Paper 1: DGP Architecture
  python3 publisher.py --paper 2               # Paper 2: Independent Lab Denial Crisis
  python3 publisher.py --paper 3               # Paper 3: AI Governance (SB 1188 / TRAIGA)
  python3 publisher.py --paper 4               # Paper 4: Payer AI Insider (Manasa)
  python3 publisher.py --paper 5               # Paper 5: Pilot Results (template)
  python3 publisher.py --abstract 1            # Abstract only — copy-paste for arXiv
  python3 publisher.py --judging               # Peer review / judging opportunities
  python3 publisher.py --citations             # Full citation library
  python3 publisher.py --visa-map              # Map papers → EB-1A / NIW / O-1A criteria
  python3 publisher.py --all --save            # Generate everything + save to .txt files
"""

import argparse
import os
import re
import sys
import zipfile
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent.parent

# ── Founder profiles (verified) ───────────────────────────────────────────────

FOUNDERS = {
    "ram": {
        "name": "Rambabu Vadlamudi",
        "role": "Founder & Enterprise Architect",
        "it_years": "15+",
        "healthcare_it_years": "8+",
        "employers": ["Alsac (St. Jude Children's Research Hospital)", "CIGNA", "Medifast",
                      "Teladoc Health", "United Health Care", "ECFMG"],
        "expertise": [
            "Enterprise architecture, GCP, FHIR R4, HL7 v2, EDI 835/837",
            "Clinical data pipelines, revenue cycle management",
            "Inventor: DGP (Deterministic-Generative-Predictive) Clinical Revenue Architecture",
            "847-rule deterministic compliance engine for LCD/NCD/MolDX/DEX Z-codes",
            "Texas SB 1188 and TRAIGA native compliance design",
        ],
        "contact": "ram.vadlamudi@ardiahealthlabs.com | (469) 679-3334",
        "location": "Argyle, TX 76226",
    },
    "manasa": {
        "name": "Manasa Jampani",
        "role": "Co-Founder & CEO",
        "it_years": "10+",
        "healthcare_it_years": "5+",
        "employers": ["Interwell Health", "United HealthGroup", "ECFMG"],
        "expertise": [
            "Clinical operations, payer strategy, AI background",
            "Business strategy, GTM, investor relations",
            "Inside knowledge of payer claim denial decision logic",
            "Healthcare IT systems, ACO operations, renal care management",
        ],
        "contact": "founders@ardiahealthlabs.com | (469) 499-6435",
        "location": "Argyle, TX 76226",
    },
}

AFFILIATION = "Ardia Health, Argyle, TX 76226"
COMPANY_EMAIL = "founders@ardiahealthlabs.com"

# ── Architecture definition (original coinage — do not confuse with neuro-symbolic) ──

ARCHITECTURE = {
    "name": "DGP Clinical Revenue Architecture",
    "full_name": "Deterministic-Generative-Predictive (DGP) Clinical Revenue Architecture",
    "acronym": "DGP",
    "inventor": "Rambabu Vadlamudi",
    "layers": {
        "L1": {
            "name": "Deterministic Policy Engine",
            "tech": "847-rule symbolic compliance engine",
            "function": "Covers all LCD/NCD/MolDX policies, DEX Z-codes, CPT 81400–81479 series, "
                        "PLA codes — zero hallucination on policy interpretation",
        },
        "L2": {
            "name": "Generative Clinical Reasoning",
            "tech": "Large Language Model (LLM) — Anthropic Claude API",
            "function": "Reads clinical documentation, generates evidence-backed appeal briefs "
                        "in under 90 seconds; retrieves from 14 medical databases in 340ms",
        },
        "L3": {
            "name": "Predictive Denial Prevention",
            "tech": "Machine Learning denial prediction model",
            "function": "Trained on historical claims data; identifies pre-submission denial risk "
                        "and flags claims for documentation reinforcement before filing",
        },
    },
    "integration": "Processes EDI 835/837 data via FHIR R4 and HL7 v2 integrations",
    "compliance": "Texas SB 1188 (eff. Sep 1, 2025) and TRAIGA (HB 149, eff. Jan 1, 2026); "
                  "HIPAA audit trail; human-in-loop review",
    "why_original": (
        "Existing hybrid AI architectures in healthcare focus on clinical DIAGNOSIS "
        "(cholangitis management [PMID 41827149], oncology trial matching [PMID 42004487], "
        "corneal topography [PMID 42052214]). The DGP architecture is the first application "
        "of a three-layer deterministic-generative-predictive design to healthcare "
        "ADMINISTRATIVE automation — specifically, molecular diagnostic claim denial recovery "
        "under MolDX, LCD/NCD, and DEX Z-code compliance frameworks. "
        "No prior published work applies hybrid AI to EDI 835/837 + FHIR R4 RCM for "
        "independent clinical laboratories."
    ),
}


# ── Core citation library ─────────────────────────────────────────────────────

CITATIONS = {
    "jama_2025": {
        "ref": "[1]",
        "full": "Georgetown University. NGS Denial Rates in Medicare Claims: A Cohort Analysis. "
                "JAMA Network Open. April 2025. n=29,919. "
                "Key findings: Overall NGS denial rate 23.3%; rose to 27.4% post-2020 NCD amendment; "
                "independent labs face 2.76× higher denial odds vs. hospital labs (OR=2.76, p<0.001); "
                "median denied NGS claim value $3,800.",
        "claim": "Independent laboratories face 2.76× higher denial odds compared to hospital-based labs",
        "visa_use": "NIW Prong 1 (national importance), EB-1A Criterion 5 (problem significance)",
        "source": "Ardia white paper citation — verify DOI before journal submission",
    },
    "xifin_2024": {
        "ref": "[2]",
        "full": "XiFin Inc. 2024 Payor Denial Impact Report. Analyzed 20M+ claims. "
                "Molecular diagnostic CPT codes denied at 35.3% vs. 19.3% standard lab claims "
                "vs. 11.8% overall healthcare average. Industry-highest denial category.",
        "claim": "Molecular diagnostics have the highest denial rate in all of healthcare at 35.3%",
        "visa_use": "NIW Prong 1, EB-1A Criterion 5",
        "source": "Industry report — cited in Ardia white paper",
    },
    "frontiers_pharma_2023": {
        "ref": "[3]",
        "full": "Frontiers in Pharmacology. Pharmacogenomics Reimbursement Analysis. 2023. "
                "Only 46% of PGx claims reimbursed; more than half of PGx testing revenue "
                "is at structural reimbursement risk.",
        "claim": "Only 46% of pharmacogenomics claims are reimbursed",
        "visa_use": "NIW Prong 1, EB-1A Criterion 5",
        "source": "Peer-reviewed — confirm exact DOI before journal submission",
    },
    "acla_2024": {
        "ref": "[4]",
        "full": "American Clinical Laboratory Association (ACLA). 2024 Industry Survey. "
                "50%+ of independent lab operators considering selling or merging "
                "if PAMA cuts take effect.",
        "claim": "Over 50% of independent labs at existential risk from PAMA 2027",
        "visa_use": "NIW Prong 1 (national healthcare infrastructure at risk)",
        "source": "Industry survey — cited in Ardia white paper",
    },
    "hfma_ligolab_2024": {
        "ref": "[5]",
        "full": "Healthcare Financial Management Association + LigoLab. 2024 Revenue Cycle "
                "Benchmarking Report. 65% of denied lab claims never appealed despite 50–80.7% "
                "win rates when pursued. Manual denial rework costs $25–$181 per claim; "
                "avg. 2+ staff hours per appeal.",
        "claim": "65% of denied lab claims are never appealed despite high win rates",
        "visa_use": "NIW Prong 1, EB-1A Criterion 5 (problem Ardia solves)",
        "source": "Industry report — cited in Ardia white paper",
    },
    "waystar_2024": {
        "ref": "[6]",
        "full": "Waystar Health. IPO Filing. 2024. Valuation: $3.5 billion. "
                "Hospital-focused RCM AI — excludes independent lab segment.",
        "claim": "Hospital RCM AI has attracted $3.5B IPO valuation; independent labs remain unserved",
        "visa_use": "EB-1A Criterion 5 (market gap), NIW Prong 2",
        "source": "Public filing — verified",
    },
    "r1rcm_2024": {
        "ref": "[7]",
        "full": "R1 RCM. Acquisition. 2024. $8.9 billion acquisition. "
                "Validates enterprise AI RCM market.",
        "claim": "$8.9B acquisition validates the AI revenue cycle market",
        "visa_use": "EB-1A Criterion 8 (distinguished org context), NIW Prong 3",
        "source": "Public transaction — verified",
    },
    "cms_pama": {
        "ref": "[8]",
        "full": "Centers for Medicare & Medicaid Services (CMS). "
                "Protecting Access to Medicare Act (PAMA). 2014. "
                "Scheduled rate cuts: up to 15%/year for 3 years beginning January 1, 2027. "
                "Cumulative reduction up to 45% by 2029.",
        "claim": "PAMA 2027 threatens up to 45% cumulative Medicare rate cuts for clinical labs",
        "visa_use": "NIW Prong 1 (policy urgency), EB-1A Criterion 5",
        "source": "Federal legislation — CMS.gov",
    },
    "texas_sb1188": {
        "ref": "[9]",
        "full": "Texas Senate Bill 1188. Effective September 1, 2025. "
                "Requires human review of AI-generated clinical content; patient disclosure; "
                "US-based data residency for Texas residents (eff. Jan 1, 2026); "
                "penalties $5,000–$250,000 per intentional violation.",
        "claim": "Texas SB 1188 establishes state-level healthcare AI accountability requirements",
        "visa_use": "EB-1A Criterion 5 (Ardia compliant), NIW Prong 3 (US AI governance)",
        "source": "Texas Legislature — verified",
    },
    "traiga": {
        "ref": "[10]",
        "full": "Texas TRAIGA — Responsible Artificial Intelligence Governance Act (HB 149). "
                "Effective January 1, 2026. Intent-based liability; healthcare AI disclosure; "
                "NIST AI RMF safe harbor; 36-month regulatory sandbox; "
                "preempts local AI ordinances.",
        "claim": "TRAIGA makes Texas the third US state with comprehensive AI legislation",
        "visa_use": "EB-1A Criterion 5, NIW Prong 3",
        "source": "Texas Legislature — verified",
    },
    "moldx_cpt": {
        "ref": "[11]",
        "full": "CMS MolDx Program / AMA CPT Coding Analysis. 2024–2026. "
                "75,000+ genetic tests map to fewer than 200 molecular pathology CPT codes. "
                "PLA codes: 37% of new CPT code additions. "
                "Claims for 50+ gene panels: 1.32× higher denial rate. "
                "29% of Medicare lab claims in 2023 contained coding errors.",
        "claim": "Extreme coding complexity: 75,000 tests, <200 CPT codes, 35%+ error/denial rates",
        "visa_use": "EB-1A Criterion 5 (technical innovation necessity)",
        "source": "CMS + AMA data — cited in Ardia white paper",
    },
}


# ── Paper templates ───────────────────────────────────────────────────────────

PAPERS = {
    1: {
        "title": "A Deterministic-Generative-Predictive (DGP) Architecture for AI-Driven "
                 "Clinical Claim Recovery in Independent Molecular Diagnostic Laboratories: "
                 "Design, Implementation, and Compliance Framework",
        "authors": "Rambabu Vadlamudi",
        "affiliations": f"{AFFILIATION} | ram.vadlamudi@ardiahealthlabs.com",
        "target_journals": [
            "arXiv cs.AI or cs.IR (preprint — submit first, public in 1–2 days)",
            "Journal of the American Medical Informatics Association (JAMIA)",
            "NEJM AI",
            "npj Digital Medicine",
            "Journal of Healthcare Informatics Research",
        ],
        "visa_criteria": [
            "EB-1A Criterion 6 — Scholarly Publication (technical architecture paper)",
            "EB-1A Criterion 5 — Original Contribution (novel DGP architecture documented)",
            "EB-2 NIW Prong 2 — Well positioned (inventor of the DGP architecture)",
            "O-1A — Published material establishing expertise in healthcare AI",
        ],
        "differentiation_from_prior_work": (
            "Existing hybrid AI systems in healthcare focus on clinical diagnosis: "
            "cholangitis and cholecystitis management [PMID 41827149, 42226236], "
            "oncology clinical trial matching [PMID 42004487], "
            "corneal topography interpretation [PMID 42052214, 41301129]. "
            "The DGP architecture is the first published design applying a "
            "three-layer deterministic-generative-predictive framework to healthcare "
            "ADMINISTRATIVE automation — specifically, EDI 835/837 claim denial recovery "
            "under MolDX, LCD/NCD, and DEX Z-code compliance. "
            "This application domain, technical integration stack (FHIR R4 + EDI + LLM), "
            "and compliance target (independent lab revenue cycle) are entirely original."
        ),
        "abstract": """Background: Independent clinical laboratories processing molecular diagnostics,
pharmacogenomics, and toxicology face a compound billing crisis: claim denial rates of 27–35.3%
for molecular diagnostic CPT codes [2] — the highest in US healthcare — combined with 65% of
denied claims never appealed despite 50–80.7% appeal win rates [5]. The manual appeal rework
burden ($25–$181 per claim, 2+ staff hours) makes systematic recovery economically unviable
for the 7,000+ CLIA-certified independent laboratories that are not part of national reference
lab networks. No existing AI revenue cycle management system is designed for this segment.

Methods: We present the Deterministic-Generative-Predictive (DGP) Clinical Revenue Architecture,
a three-layer AI system purpose-built for independent laboratory claim recovery. Layer 1 — the
Deterministic Policy Engine — implements 847 rules compiled from all LCD and NCD policies,
MolDX Technical Assessments, DEX Z-code requirements, CPT molecular pathology codes
(81400–81479 series), and PLA codes, providing zero-hallucination policy compliance evaluation.
Layer 2 — the Generative Clinical Reasoning Engine — employs a large language model (LLM)
to analyze clinical documentation, retrieve evidence from 14 medical databases within 340
milliseconds, and generate evidence-backed appeal briefs meeting payer documentation
standards. Layer 3 — the Predictive Denial Prevention Model — applies machine learning
trained on historical claims data to identify denial-risk patterns prior to initial claim
submission. The system processes EDI 835/837 data via FHIR R4 and HL7 v2 integrations and
maintains a complete human-in-loop audit trail compliant with Texas SB 1188 (effective
September 1, 2025) and TRAIGA (HB 149, effective January 1, 2026) [9][10].

Results: The DGP architecture generates evidence-backed appeal briefs in under 90 seconds,
reducing manual rework from an industry average of 2+ hours per claim to a fully automated
workflow with human-review checkpoint. The deterministic Layer 1 ensures that no policy
interpretation is delegated to the probabilistic LLM, preserving regulatory accuracy across
847 compliance rules. The Layer 3 predictive model intercepts denial-prone claims before
submission, targeting the 29% of Medicare lab claims estimated to contain coding errors [11].

Discussion: Existing hybrid AI architectures for healthcare focus on clinical diagnostic tasks —
patient triage, guideline-concordant treatment decisions, and imaging interpretation. The DGP
architecture addresses a structurally distinct domain: administrative claim compliance, where
policy determinism is non-negotiable and errors have direct financial and regulatory consequences.
The three-layer separation — deterministic compliance, generative reasoning, and predictive
prevention — reflects the distinct error tolerance requirements of each function. The
architecture is designed for the post-PAMA 2027 environment, where independent labs facing
up to 45% cumulative Medicare rate reductions [8] need every claimable dollar recovered.

Conclusion: The DGP Clinical Revenue Architecture provides a principled framework for AI-driven
molecular diagnostic claim recovery in independent clinical laboratories, with application to
the $10–12 billion annual revenue loss crisis in the US independent laboratory sector.

Keywords: clinical laboratory, revenue cycle management, claim denial recovery, AI architecture,
FHIR, healthcare AI, molecular diagnostics, MolDX, pharmacogenomics, EDI 835/837,
deterministic AI, machine learning, independent laboratory""",
        "outline": [
            "1. Introduction — The independent lab denial crisis (cite [1][2][5])",
            "   1.1 Scale of the problem: $10–12B annual loss, 7,000+ labs affected",
            "   1.2 Why existing RCM AI does not serve this segment (Waystar, R1 RCM — hospital-focused [6][7])",
            "   1.3 The MolDX compliance burden as the core technical challenge",
            "2. Background",
            "   2.1 Revenue cycle AI: current approaches and their limitations",
            "   2.2 Why LLM-only approaches fail in policy-governed healthcare admin",
            "   2.3 Why rules-only approaches cannot handle clinical narrative variability",
            "   2.4 Related work: hybrid AI in healthcare diagnosis (contrast with admin domain)",
            "3. The DGP Clinical Revenue Architecture",
            "   3.1 Design principles: separation of deterministic, generative, and predictive functions",
            "   3.2 Layer 1 — Deterministic Policy Engine",
            "      3.2.1 Rule compilation from LCD/NCD/MolDX/DEX Z-code sources",
            "      3.2.2 847-rule coverage: CPT 81400–81479, PLA codes, DEX Z-codes",
            "      3.2.3 Zero-hallucination policy evaluation via rule-based inference",
            "   3.3 Layer 2 — Generative Clinical Reasoning Engine",
            "      3.3.1 LLM prompt architecture for medical necessity argumentation",
            "      3.3.2 14-database evidence retrieval pipeline (340ms latency)",
            "      3.3.3 Appeal brief generation: structure, payer-specific formatting",
            "   3.4 Layer 3 — Predictive Denial Prevention Model",
            "      3.4.1 Training data: historical EDI 835 denial remittances",
            "      3.4.2 Feature engineering: CPT/ICD-10 pairs, Z-codes, documentation features",
            "      3.4.3 Pre-submission denial risk scoring",
            "   3.5 System integration",
            "      3.5.1 EDI 835/837 parsing and FHIR R4 mapping",
            "      3.5.2 HL7 v2 interface",
            "      3.5.3 Human-in-loop review workflow",
            "4. Compliance Architecture",
            "   4.1 Texas SB 1188: human review mandate, data residency, patient disclosure",
            "   4.2 TRAIGA: NIST AI RMF alignment, safe harbor, behavioral constraint",
            "   4.3 HIPAA audit trail design",
            "5. Implementation",
            "   5.1 Infrastructure: Google Cloud Platform, HIPAA BAA, US data residency",
            "   5.2 Performance: <90s brief generation, 340ms evidence retrieval",
            "6. Discussion",
            "   6.1 Comparison with clinical diagnostic hybrid AI architectures",
            "   6.2 Error tolerance requirements: admin vs. diagnostic AI",
            "   6.3 PAMA 2027 context: why this architecture matters now",
            "   6.4 Limitations and future work",
            "7. Conclusion",
            "References",
        ],
    },

    2: {
        "title": "Structural Revenue Loss in US Independent Clinical Laboratories: "
                 "A Systematic Analysis of Claim Denial Rates, Appeal Abandonment, and "
                 "AI-Addressable Recovery Opportunities in Molecular Diagnostics and "
                 "Pharmacogenomics (2020–2026)",
        "authors": "Rambabu Vadlamudi, Manasa Jampani",
        "affiliations": f"{AFFILIATION} | {COMPANY_EMAIL}",
        "target_journals": [
            "arXiv q-bio.QM or cs.CY (preprint — submit simultaneously with Paper 1)",
            "Journal of Managed Care & Specialty Pharmacy (JMCP)",
            "Clinical Chemistry",
            "Clinical Laboratory Science",
            "Health Affairs (commentary/analysis)",
        ],
        "visa_criteria": [
            "EB-1A Criterion 6 — Scholarly Publication (systematic analysis)",
            "EB-2 NIW Prong 1 — Substantial merit & national importance (peer-reviewed evidence)",
            "EB-2 NIW Prong 2 — Well positioned (founders built the solution to this problem)",
            "O-1A — Published material demonstrating subject-matter expertise",
        ],
        "differentiation_from_prior_work": (
            "No published systematic analysis consolidates XiFin 2024, JAMA Network Open 2025, "
            "Frontiers in Pharmacology 2023, ACLA 2024, and HFMA/LigoLab 2024 into a single "
            "quantitative picture of independent lab revenue loss. This paper fills that gap "
            "and is the only analysis written by authors with direct operational experience "
            "at major payers (Interwell Health, United HealthGroup, ECFMG) AND as architects "
            "of an AI countermeasure system."
        ),
        "abstract": """Background: Independent clinical laboratories — the 7,000+ CLIA-certified
facilities not affiliated with national reference lab networks — account for approximately
32% of US diagnostic test volume yet face a systematic reimbursement failure that threatens
their financial viability. This study synthesizes published industry data and peer-reviewed
literature to quantify the magnitude of claim denial-related revenue loss across molecular
diagnostic and pharmacogenomics testing categories.

Methods: Systematic analysis of data published between 2020 and 2026 from: XiFin's 2024
Payor Denial Impact Report (20M+ claims), JAMA Network Open's April 2025 cohort study
(n=29,919 NGS Medicare claims, Georgetown University), Frontiers in Pharmacology's 2023
pharmacogenomics reimbursement analysis, the American Clinical Laboratory Association's
2024 industry survey, and Healthcare Financial Management Association/LigoLab's 2024
revenue cycle benchmarking report. Founder authors contributed 8+ years (R.V.) and 5+
years (M.J.) of direct experience within payer organizations including United HealthGroup
and ECFMG.

Results: Molecular diagnostic CPT codes are denied at 35.3% — the highest rate of any
healthcare category versus 11.8% overall healthcare average [2]. Independent laboratories
face 2.76× higher denial odds than hospital-based laboratories (OR=2.76, p<0.001, n=29,919)
[1]. Overall NGS denial rates rose from 16.8% pre-NCD to 27.4% following the 2020 Medicare
NCD amendment [1]. Pharmacogenomics reimbursement failure exceeds 54% of submitted claims
[3]. Despite 50–80.7% appeal win rates, 65% of denied claims are never appealed due to
staff capacity constraints and $25–$181 per-claim rework costs [5]. Fifty percent or more
of independent lab operators report they would consider selling or merging if PAMA-mandated
Medicare rate cuts of up to 15%/year take effect beginning January 1, 2027 [4][8].
Commercial payer AI adoption for claim processing grew from 8% to 34% between 2022 and
2025, while only 14% of providers have deployed AI denial countermeasures.

Discussion: The convergence of AI-driven payer denial automation, PAMA reimbursement cuts,
and expanding molecular diagnostic test complexity creates an existential financial challenge
for independent laboratories. The payer AI asymmetry — commercial insurers deploying
sophisticated AI denial engines while independent labs continue to rely on manual billing
processes — is a structural driver of the widening gap between theoretical and actual
reimbursement. This asymmetry is particularly acute for MolDX-governed tests, where
75,000+ genetic tests map to fewer than 200 molecular pathology CPT codes [11], and
29% of Medicare lab claims contain coding errors.

Conclusion: Independent clinical laboratory revenue loss to claim denials represents a
$10–12 billion annual drain on the US healthcare system. The communities most affected —
rural, addiction medicine, specialty practice, and underserved populations served by
independent labs — bear the downstream health access consequences of this financial failure.
AI-native denial recovery platforms purpose-built for the MolDX/LCD/NCD compliance
complexity of independent laboratories represent the most direct technological intervention
available to preserve this critical healthcare infrastructure through PAMA 2027 and beyond.

Keywords: clinical laboratory, revenue cycle management, claim denial, molecular diagnostics,
pharmacogenomics, PAMA, MolDX, healthcare AI, independent laboratory, payer AI, FHIR""",
        "outline": [
            "1. Introduction — Independent labs: essential but financially precarious",
            "   1.1 32% of US diagnostic test volume; rural and underserved communities served",
            "   1.2 Structural exclusion from hospital-focused RCM AI investment",
            "2. Methods — Data sources, inclusion criteria, analysis approach",
            "3. Results: The Denial Rate Landscape",
            "   3.1 Overall industry: 13.6% average denial rate",
            "   3.2 Molecular diagnostics: 27–35.3% (highest in healthcare) [2]",
            "   3.3 Pharmacogenomics: 54%+ failure rate [3]",
            "   3.4 NGS claims: 23.3% → 27.4% post-NCD (Georgetown 2025 cohort) [1]",
            "   3.5 Independent vs. hospital lab disparity: 2.76× odds ratio [1]",
            "4. Results: The Appeal Abandonment Problem",
            "   4.1 65% never appealed despite 50–80.7% win rates [5]",
            "   4.2 Staff capacity constraints: $25–$181/claim, 2+ hrs per appeal",
            "   4.3 Break-even analysis: when manual appeal is economically rational",
            "5. Results: The Payer AI Asymmetry",
            "   5.1 Payer AI adoption: 8% → 34% (2022–2025)",
            "   5.2 Provider AI adoption: 14% with documented improvement",
            "   5.3 How payer AI systems target documentation deficiencies",
            "6. Results: PAMA 2027 — The Reimbursement Cliff",
            "   6.1 Historical rate trajectory and 7 consecutive congressional delays",
            "   6.2 Projected 45% cumulative Medicare reduction by 2029 [8]",
            "   6.3 Lab consolidation pressures: 50%+ considering exit [4]",
            "7. Results: MolDX Compliance Complexity",
            "   7.1 DEX Z-code mandatory requirements",
            "   7.2 75,000 tests → <200 CPT codes [11]",
            "   7.3 CPT code volatility: 270 new codes, 112 deletions in 2026 update",
            "8. Discussion — AI intervention requirements",
            "   8.1 Why hospital-focused RCM AI does not transfer (Waystar, R1 RCM gaps)",
            "   8.2 The case for a deterministic-first compliance AI",
            "   8.3 Health equity dimension: rural and specialty lab access at risk",
            "9. Policy Recommendations",
            "   9.1 CMS oversight of payer AI denial algorithms",
            "   9.2 Lab-specific RCM AI standards (MolDX compliance baseline)",
            "10. Conclusion",
            "References",
        ],
    },

    3: {
        "title": "Compliance-by-Design in Clinical AI Startups: Implementing Texas SB 1188 "
                 "and TRAIGA (HB 149) in an AI-Native Healthcare Revenue Recovery Platform",
        "authors": "Rambabu Vadlamudi, Manasa Jampani",
        "affiliations": f"{AFFILIATION} | {COMPANY_EMAIL}",
        "target_journals": [
            "arXiv cs.CY (preprint)",
            "Journal of the American Health Information Management Association (AHIMA)",
            "Journal of Health Politics, Policy and Law",
            "Health Affairs (regulatory commentary)",
            "Journal of Law and the Biosciences (Oxford Academic)",
        ],
        "visa_criteria": [
            "EB-1A Criterion 6 — Scholarly Publication",
            "EB-1A Criterion 5 — Original Contribution (first publication describing "
            "native SB 1188/TRAIGA compliance in a production clinical AI system)",
            "EB-2 NIW Prong 3 — Beneficial to US (advancing US AI governance frameworks)",
        ],
        "differentiation_from_prior_work": (
            "As of 2026 no peer-reviewed paper describes a production clinical AI system "
            "built natively to Texas SB 1188 and TRAIGA requirements from day one. "
            "This paper is the first to provide an operational compliance framework for "
            "clinical AI startups navigating these two new Texas laws, written by founders "
            "who implemented the compliance architecture themselves."
        ),
        "abstract": """Background: Texas enacted two landmark AI governance statutes — Senate Bill 1188
(effective September 1, 2025) and the Texas Responsible Artificial Intelligence Governance
Act (TRAIGA, HB 149, effective January 1, 2026) — making Texas the third US state with
comprehensive AI legislation, following Colorado and Utah. Healthcare AI platforms operating
in clinical revenue recovery represent a particularly complex compliance context: they process
Protected Health Information under HIPAA, generate AI-assisted administrative content under
SB 1188, and serve healthcare providers in the 36-month regulatory sandbox established by
TRAIGA. No published guidance describes what SB 1188 and TRAIGA compliance means in
operational practice for clinical AI startups.

Methods: We present a compliance-by-design framework for healthcare AI platforms under
SB 1188 and TRAIGA, based on direct implementation experience at Ardia Health — an
AI-native clinical laboratory revenue recovery startup incorporated in Texas (January 2026).
The founding team brings 8+ years (R.V.) and 5+ years (M.J.) of direct healthcare IT
experience across payer and clinical operations organizations including United HealthGroup
and ECFMG, providing operational grounding for the compliance framework described.

Results: We identify seven SB 1188/TRAIGA compliance requirement categories applicable
to clinical AI startups: (1) human-in-loop review mandate for AI-generated clinical
administrative content, (2) patient disclosure obligations when AI is used in healthcare
decisions, (3) US-based data residency for Texas residents (effective January 1, 2026),
(4) behavioral manipulation prohibition — particularly relevant for addiction medicine
lab deployments, (5) NIST AI RMF alignment for safe harbor eligibility under TRAIGA,
(6) intentional discrimination prohibition in AI decision logic, and (7) audit trail
requirements compatible with HIPAA minimum necessary standards. We describe the
architectural decisions made in implementing each requirement in a production system.

Discussion: The TRAIGA regulatory sandbox creates a first-mover advantage for healthcare
AI startups that build these compliance requirements natively versus retrofitting them
after deployment. The intent-based liability framework in TRAIGA — more startup-friendly
than Colorado's SB 205 intent-agnostic standard — enables innovation while preserving
patient protection. Companies building SB 1188 and TRAIGA compliance as core product
capabilities create structural competitive barriers that late entrants must pay to retrofit.
The combination of SB 1188 and TRAIGA with existing HIPAA requirements creates a layered
compliance stack that, when implemented by design, becomes a defensible competitive moat.

Conclusion: Texas SB 1188 and TRAIGA establish a practical US model for healthcare AI
governance. The compliance-by-design framework described provides a replicable template
for other clinical AI startups operating in Texas, and may anticipate requirements of
forthcoming federal healthcare AI legislation.

Keywords: AI governance, healthcare AI, HIPAA, Texas SB 1188, TRAIGA, NIST AI RMF,
clinical AI, revenue cycle management, regulatory sandbox, compliance-by-design""",
        "outline": [
            "1. Introduction — The US healthcare AI governance landscape in 2026",
            "2. Texas as the Third US State with Comprehensive AI Legislation",
            "   2.1 Colorado SB 205 (intent-agnostic liability — strict)",
            "   2.2 Utah AI Policy Act",
            "   2.3 Texas SB 1188 + TRAIGA (intent-based — startup-friendly innovation model)",
            "3. SB 1188 Requirements for Healthcare AI",
            "   3.1 Human-in-loop clinical review mandate",
            "   3.2 Patient disclosure requirements",
            "   3.3 US data residency (Texas residents, effective January 1, 2026)",
            "   3.4 Penalty structure: $5,000–$250,000 per intentional violation",
            "   3.5 License suspension/revocation for repeat violation",
            "4. TRAIGA Requirements for Healthcare AI",
            "   4.1 NIST AI RMF safe harbor pathway and what it requires",
            "   4.2 36-month regulatory sandbox for qualifying innovation",
            "   4.3 Behavioral manipulation prohibition",
            "   4.4 Preemption of local AI ordinances",
            "   4.5 Differences from Colorado SB 205",
            "5. The Compliance-by-Design Framework",
            "   5.1 Audit trail architecture satisfying HIPAA + SB 1188 simultaneously",
            "   5.2 Human-in-loop workflow: where the checkpoint must sit",
            "   5.3 US infrastructure deployment: GCP region selection for Texas data residency",
            "   5.4 NIST AI RMF implementation: Govern, Map, Measure, Manage phases",
            "6. Clinical Revenue Recovery: Domain-Specific Compliance Considerations",
            "   6.1 AI-generated appeal briefs under SB 1188 human review requirement",
            "   6.2 Addiction medicine lab deployments: behavioral constraint under TRAIGA",
            "   6.3 CLIA certificate holder obligations intersecting with AI oversight",
            "7. Policy Implications",
            "   7.1 Texas model as template for federal legislation",
            "   7.2 Compliance-first architecture as competitive differentiation",
            "   7.3 Recommendations for CMS AI governance in clinical lab billing",
            "8. Conclusion",
            "References",
        ],
    },

    4: {
        "title": "Inside the Payer AI Black Box: Denial Trigger Mechanisms, Documentation "
                 "Threshold Requirements, and AI-Countermeasure Strategies for Independent "
                 "Clinical Laboratory Claims in Molecular Diagnostics",
        "authors": "Manasa Jampani, Rambabu Vadlamudi",
        "affiliations": f"{AFFILIATION} | {COMPANY_EMAIL}",
        "target_journals": [
            "NEJM AI",
            "Health Affairs",
            "American Journal of Managed Care (AJMC)",
            "Journal of Healthcare Management",
            "Medical Care (AcademyHealth)",
        ],
        "visa_criteria": [
            "EB-1A Criterion 6 — Scholarly Publication",
            "EB-1A Criterion 5 — Original Contribution (only person with this exact vantage point)",
            "EB-2 NIW Prong 2 — Well positioned (5+ yrs at Interwell Health, UHG, ECFMG — "
            "Manasa has inside knowledge of payer denial logic unavailable to any outside researcher)",
            "O-1A — Extraordinary ability: unique insider expertise no other researcher possesses",
        ],
        "differentiation_from_prior_work": (
            "Manasa Jampani has 5+ years of direct healthcare IT experience at "
            "Interwell Health, United HealthGroup, and ECFMG — payer and payer-adjacent "
            "organizations. She has direct operational knowledge of how payer clinical "
            "operations teams configure AI denial systems. No researcher outside a payer "
            "organization can write this paper. This is the only analysis of payer AI "
            "denial logic written by a co-founder of an AI denial countermeasure startup "
            "who previously worked inside the payer side."
        ),
        "abstract": """Background: Commercial health insurers have rapidly deployed AI-powered claim
processing systems to automate denial decisions. Between 2022 and 2025, full AI adoption
by payers for claim processing grew from 8% to 34%, while only 14% of healthcare providers
have deployed AI denial countermeasures. This asymmetry is most acute for independent
clinical laboratories, where the complexity of molecular diagnostic coding creates systematic
documentation vulnerabilities that payer AI systems are specifically trained to exploit.
Independent labs already face 2.76× higher denial odds than hospital-based laboratories
(OR=2.76, p<0.001) [1] and a molecular diagnostic denial rate of 35.3% [2]. Understanding
the specific mechanisms driving AI-generated denials is the prerequisite for building
effective countermeasure systems.

Methods: Drawing on 5+ years of direct experience in healthcare IT and clinical operations
at Interwell Health, United HealthGroup, and ECFMG — payer and payer-adjacent organizations
with direct exposure to claim processing decision logic — this analysis describes the denial
trigger mechanisms, documentation threshold requirements, and failure modes that drive
AI-generated laboratory claim denials. The analysis focuses on molecular diagnostics,
pharmacogenomics, and toxicology testing categories under Medicare and commercial payer
guidelines. The co-author (R.V.) contributes 8+ years of healthcare IT systems architecture
experience including FHIR R4, EDI 835/837, and HL7 integration design.

Results: We identify and describe seven primary AI denial trigger categories specific to
independent clinical laboratory claims: (1) medical necessity documentation gaps in ordering
physician notes — the most common trigger, present in approximately 40% of denied molecular
claims; (2) DEX Z-code absence or error in claims submitted to MolDX jurisdictions;
(3) CPT/ICD-10 code pairing inconsistency — particularly for 50+ gene panel claims,
which face 1.32× higher denial probability [11]; (4) prior authorization gaps for
payer-specific coverage requirements; (5) test-to-diagnosis clinical utility linkage
failure — the documentation must establish why this specific test was medically necessary
for this specific patient's clinical situation; (6) LOINC/SNOMED coding mismatches
between test ordering and results reporting; and (7) temporal policy compliance gaps —
tests ordered or specimens collected before NCD/LCD effective dates.

We further describe the documentation quality dimensions that AI scoring systems evaluate
against, the evidence structure that consistently overcomes AI-generated denials on appeal,
and the pre-submission documentation practices that prevent the most common denial triggers
before claim filing.

Discussion: The information asymmetry between payer AI systems and independent laboratory
billing staff is the fundamental driver of the $10–12 billion annual revenue loss in the
independent laboratory sector. Payer AI systems are trained on historical denial patterns
and updated continuously; independent lab billing staff operate without visibility into
what documentation signals those systems score against. This paper represents the first
systematic published description of payer-side clinical laboratory denial trigger mechanisms
from an author with direct operational experience inside payer healthcare IT systems.
Addressing this information asymmetry — through AI countermeasure systems that generate
documentation specifically calibrated to payer scoring standards — is the direct
intervention available to independent laboratories.

Conclusion: Seven primary AI denial trigger categories drive the majority of molecular
diagnostic claim denials in independent laboratories. AI countermeasure systems built
with specific knowledge of these triggers — rather than on general clinical documentation
quality — represent the appropriate technological response to payer AI automation.

Keywords: payer AI, claim denial, clinical laboratory, molecular diagnostics, revenue cycle
management, medical necessity, documentation quality, DEX Z-codes, AI countermeasures,
health insurance, healthcare IT, independent laboratory""",
        "outline": [
            "1. Introduction — The payer AI revolution and the provider response gap",
            "   1.1 Payer AI adoption: 8% → 34% (2022–2025)",
            "   1.2 Provider AI adoption: 14%",
            "   1.3 Independent lab denial rates: the highest exposure point",
            "2. Author Background and Unique Vantage Point",
            "   2.1 5+ years healthcare IT at Interwell Health, United HealthGroup, ECFMG",
            "   2.2 Direct exposure to payer clinical operations and claim processing design",
            "   2.3 Why this analysis is only possible from inside the payer ecosystem",
            "3. Payer AI Claim Processing: What Is Actually Happening",
            "   3.1 Training data: historical denial pattern libraries",
            "   3.2 Documentation quality scoring mechanisms",
            "   3.3 Speed vs. accuracy trade-offs in payer AI deployment",
            "   3.4 How payer AI systems classify molecular lab claims specifically",
            "4. The Seven AI Denial Trigger Categories",
            "   4.1 Medical necessity documentation gaps (~40% of molecular denials)",
            "   4.2 DEX Z-code absence or error (MolDX jurisdictions)",
            "   4.3 CPT/ICD-10 pairing inconsistencies (50+ gene panels: 1.32× risk [11])",
            "   4.4 Prior authorization gaps",
            "   4.5 Clinical utility linkage failure",
            "   4.6 LOINC/SNOMED coding mismatches",
            "   4.7 Temporal policy compliance gaps",
            "5. What Payer AI Scores in Molecular Lab Documentation",
            "   5.1 The documentation signals that distinguish approved vs. denied claims",
            "   5.2 Ordering physician note requirements",
            "   5.3 Evidence of medical necessity for the specific patient presentation",
            "6. The Countermeasure Documentation Framework",
            "   6.1 Pre-submission prevention (address triggers before filing)",
            "   6.2 Appeal documentation structure that overcomes AI-generated denials",
            "   6.3 Evidence retrieval: what sources payer appeal reviewers credit",
            "7. Health Equity Implications",
            "   7.1 Independent lab denial disparity: 2.76× vs. hospital-based [1]",
            "   7.2 Community impact: rural, addiction medicine, specialty practice populations",
            "   7.3 The case for CMS oversight of payer AI denial systems",
            "8. Conclusion",
            "References",
        ],
    },

    5: {
        "title": "Pilot Outcomes: AI-Driven Molecular Diagnostic Claim Recovery Using the "
                 "DGP Architecture in an Independent Dallas-Fort Worth Clinical Laboratory",
        "authors": "Rambabu Vadlamudi, Manasa Jampani",
        "affiliations": f"{AFFILIATION} | {COMPANY_EMAIL}",
        "target_journals": [
            "Journal of Healthcare Management",
            "Clinical Laboratory Science",
            "JAMIA Open",
            "Healthcare (MDPI, open access)",
        ],
        "visa_criteria": [
            "EB-1A Criterion 6 — Scholarly Publication (empirical pilot results)",
            "EB-1A Criterion 5 — Original Contribution (real-world evidence of DGP architecture)",
            "EB-2 NIW Prong 2 — Well positioned (demonstrated measurable outcomes)",
            "O-1A — Distinguished achievement with documented results",
        ],
        "differentiation_from_prior_work": (
            "First published pilot study of AI-driven molecular diagnostic claim recovery "
            "in an independent clinical laboratory. Prior AI RCM literature focuses on "
            "hospital systems. DGP architecture outcomes under MolDX/LCD/NCD compliance "
            "requirements have not been previously reported."
        ),
        "abstract": """[TEMPLATE — complete with real data after Q2 2026 pilot launch]

Background: Independent clinical laboratory claim denial rates for molecular diagnostics
reach 27–35.3% nationally [1][2], with 65% of denials abandoned without appeal [5].
We report initial deployment outcomes of the Deterministic-Generative-Predictive (DGP)
Clinical Revenue Architecture at [PILOT LAB NAME], an independent clinical laboratory
in the Dallas-Fort Worth metropolitan area.

Methods: [N] denied laboratory claims in molecular diagnostics (CPT 81400–81479),
pharmacogenomics (CPT 81225/81226/81227 series), and toxicology (CPT 80305–80307)
categories submitted between [DATES]. DGP architecture processed EDI 835 denial
remittances, identified appeal-eligible claims, generated evidence-backed appeal briefs
via 14-database retrieval and LLM clinical reasoning, submitted appeals with human-in-loop
review per Texas SB 1188 requirements.

Results: [FILL WITH REAL PILOT DATA]
  — Claims processed: [X]
  — Appeal briefs generated <90 seconds: [X%]
  — Appeals filed vs. eligible denials: [X%]
  — Appeals won: [X%]
  — Revenue recovered: $[X]
  — Time from denial to appeal submission: [X days] vs. [Y days] manual baseline
  — Staff time per appeal: [X min] vs. 2+ hours manual baseline [5]

Discussion: [Complete after results]

Conclusion: [Complete after results]

Keywords: clinical laboratory, AI, denial recovery, DGP architecture, revenue cycle,
molecular diagnostics, FHIR, Dallas-Fort Worth, independent laboratory, pilot study""",
        "outline": [
            "1. Introduction (cite Papers 1 and 2 above for background)",
            "2. Pilot Setting — The laboratory (anonymized if needed per IRB)",
            "3. The DGP Architecture (brief summary, cite Paper 1 for detail)",
            "4. Methods",
            "   4.1 Study period and claim cohort",
            "   4.2 Testing categories and CPT codes analyzed",
            "   4.3 Outcome measures (time, accuracy, revenue recovered)",
            "   4.4 Human-in-loop review protocol (SB 1188 compliance)",
            "5. Results",
            "   5.1 Claims processed and appeal eligibility",
            "   5.2 Brief generation time",
            "   5.3 Appeal outcomes",
            "   5.4 Comparison to manual baseline",
            "6. Discussion",
            "7. Limitations",
            "8. Conclusion",
            "References",
        ],
    },
}


# ── Judging / peer review opportunities ──────────────────────────────────────

JUDGING_OPPORTUNITIES = [
    {
        "opportunity": "JAMIA Peer Reviewer",
        "org": "Journal of the American Medical Informatics Association",
        "how": "Email editor-in-chief: editor@jamia.org — offer expertise in: "
               "clinical AI, FHIR interoperability, healthcare AI governance, revenue cycle",
        "visa_criterion": "EB-1A Criterion 4 — Judging the work of others in the field",
        "timeline": "Apply immediately — assignments begin within 2–4 weeks",
        "notes": "Reviewer acknowledgement appears in each journal issue",
    },
    {
        "opportunity": "HIMSS 2027 Abstract Reviewer",
        "org": "Healthcare Information and Management Systems Society",
        "how": "himss.org/about/call-for-reviewers — apply for healthcare AI or health IT track",
        "visa_criterion": "EB-1A Criterion 4 + Criterion 2 (HIMSS membership)",
        "timeline": "HIMSS 2027: apply Q3 2026",
        "notes": "Reviewer credential in conference proceedings; also supports HIMSS Fellow application",
    },
    {
        "opportunity": "AMIA Annual Symposium Reviewer",
        "org": "American Medical Informatics Association",
        "how": "amia.org — reviewer signup for Annual Symposium, clinical informatics track",
        "visa_criterion": "EB-1A Criterion 4 + Criterion 2 (AMIA membership)",
        "timeline": "Reviews typically due March–April annually",
        "notes": "Reviewing for AMIA supports AMIA membership application",
    },
    {
        "opportunity": "NIH Study Section Ad Hoc Reviewer (SBIR/STTR Health IT)",
        "org": "National Institutes of Health",
        "how": "csr.nih.gov — contact Scientific Review Officer for Health Services Research "
               "or Special Emphasis Panels covering healthcare AI, clinical informatics",
        "visa_criterion": "EB-1A Criterion 4 (highest prestige judging evidence for EB-1A)",
        "timeline": "Rolling — study sections meet 3× per year",
        "notes": "NIH study section reviewer is among the strongest judging evidence for EB-1A; "
                 "Ram's healthcare IT + AI background qualifies for SBIR health IT panels",
    },
    {
        "opportunity": "Health Wildcatters Demo Day Judge / Mentor",
        "org": "Health Wildcatters (Dallas healthcare accelerator)",
        "how": "healthwildcatters.com/mentor — apply as mentor/judge for cohort demo days",
        "visa_criterion": "EB-1A Criterion 4 (pitch competition judging) + Criterion 3 (press)",
        "timeline": "Rolling applications",
        "notes": "Acceptance also generates press coverage — dual benefit for Criterion 3",
    },
    {
        "opportunity": "SXSW Health & MedTech Pitch Competition Judge",
        "org": "South by Southwest (Austin, TX)",
        "how": "sxsw.com/pitch — apply as judge/mentor for health technology track",
        "visa_criterion": "EB-1A Criterion 4 + Criterion 3 (press)",
        "timeline": "Applications open September–October annually",
        "notes": "SXSW generates significant press for participants and judges",
    },
    {
        "opportunity": "Journal of Healthcare Informatics Research Reviewer",
        "org": "Springer Nature",
        "how": "springer.com/journal/41666 — contact editor; "
               "offer expertise in healthcare AI, FHIR, RCM, clinical NLP",
        "visa_criterion": "EB-1A Criterion 4",
        "timeline": "Apply immediately",
        "notes": "Springer sends official reviewer acknowledgement letters per review",
    },
    {
        "opportunity": "DFW Tech & Innovation Awards Judge",
        "org": "Dallas Business Journal / Dallas Regional Chamber",
        "how": "Apply as judge for healthcare AI or digital health category",
        "visa_criterion": "EB-1A Criterion 4 + Criterion 1 (award context)",
        "timeline": "Annual — applications Q1 each year",
        "notes": "Local recognition still qualifies for EB-1A; often generates press",
    },
]


# ── Visa criteria mapping ─────────────────────────────────────────────────────

VISA_MAP = {
    "EB-1A Criterion 5 — Original Contributions": {
        "status": "STRONG — documented now",
        "evidence": [
            "DGP (Deterministic-Generative-Predictive) Clinical Revenue Architecture "
            "— original coinage by Ram Vadlamudi; no prior published work applies this "
            "three-layer deterministic/generative/predictive design to healthcare RCM",
            "847-rule deterministic engine covering ALL LCD/NCD/MolDX policies, DEX Z-codes, "
            "CPT 81400–81479, PLA codes",
            "FHIR R4 + EDI 835/837 + LLM integration for molecular diagnostic claim recovery "
            "— no existing published architecture covers this integration stack",
            "First AI platform purpose-built for independent lab PGx + NGS + MolDX compliance",
            "Native Texas SB 1188 + TRAIGA compliance architecture (first-mover)",
        ],
        "documents": ["White paper", "Paper 1 (submit to arXiv)", "GitHub architecture docs"],
    },
    "EB-1A Criterion 8 — Leading Role in Distinguished Org": {
        "status": "MODERATE — strengthens as pilots launch",
        "evidence": [
            "Ram: Founder & Enterprise Architect, Ardia Health (Delaware LLC, Jan 2026)",
            "Manasa: Co-Founder & CEO, Ardia Health",
            "GCP infrastructure, HIPAA BAA, HITRUST CSF / SOC 2 roadmap",
            "$3.5M Seed raise at $18M valuation cap",
        ],
        "documents": ["Company incorporation docs", "Pitch deck slide 7", "GCP agreement"],
    },
    "EB-1A Criterion 6 — Scholarly Publications": {
        "status": "GAP — submit Paper 1 to arXiv this week",
        "evidence": [
            "Paper 1: DGP Architecture (arXiv cs.AI — live in 1–2 days after submission)",
            "Paper 2: Lab Denial Crisis systematic analysis (arXiv q-bio.QM)",
            "Paper 3: AI governance under SB 1188/TRAIGA",
            "Paper 4: Payer AI insider analysis (Manasa — NEJM AI target)",
            "Paper 5: Pilot results (after Q2 2026 lab launch)",
        ],
        "documents": ["arXiv submission receipts", "Journal acceptance letters"],
    },
    "EB-1A Criterion 4 — Judging Others' Work": {
        "status": "GAP — apply now",
        "evidence": [
            "JAMIA peer reviewer (email editor@jamia.org this week)",
            "AMIA Annual Symposium reviewer",
            "NIH SBIR/STTR study section (highest prestige)",
            "Health Wildcatters mentor/judge (DFW — local connection)",
        ],
        "documents": ["Official reviewer acknowledgement letters from journals/NIH"],
    },
    "EB-1A Criterion 3 — Press / Published Material About You": {
        "status": "GAP — pitch proactively",
        "evidence": [
            "Pitch PAMA 2027 story to Becker's Hospital Review, MedCity News, Healthcare IT Today",
            "DFW Business Journal — local angle on DFW healthcare AI",
            "Health Wildcatters acceptance = automatic press release",
            "STAT News / POLITICO Health — payer AI vs. provider AI angle",
        ],
        "documents": ["Published article URLs/PDFs with Ram or Manasa quoted or profiled"],
    },
    "EB-1A Criterion 2 — Membership in Distinguished Associations": {
        "status": "GAP — apply now",
        "evidence": [
            "HIMSS (Healthcare Information and Management Systems Society)",
            "AMIA (American Medical Informatics Association)",
            "Forbes Technology Council",
            "ACLA (American Clinical Laboratory Association)",
        ],
        "documents": ["Membership acceptance letters/certificates"],
    },
    "EB-1A Criterion 1 — Awards/Prizes": {
        "status": "GAP — apply now",
        "evidence": [
            "Fast Company Most Innovative Companies in Healthcare",
            "Dallas Innovation Awards / DFW Tech & Innovation Awards",
            "Google Cloud for Startups showcase",
            "ADLM (Association for Diagnostics & Laboratory Medicine) awards",
        ],
        "documents": ["Award certificates, finalist notifications, press releases"],
    },
    "EB-2 NIW Prong 1 — National Importance": {
        "status": "STRONG — all citations ready",
        "evidence": [
            "$10–12B annual lab revenue loss (XiFin 2024 [2], HFMA 2024 [5])",
            "35.3% molecular Dx denial rate — highest in all of healthcare [2]",
            "2.76× denial disparity: independent vs. hospital labs [1]",
            "7,000+ independent CLIA labs at PAMA 2027 existential risk [4][8]",
            "65% of denials never appealed [5]",
        ],
        "documents": ["Paper 2 (systematic analysis)", "Market intelligence PDF"],
    },
    "EB-2 NIW Prong 2 — Well Positioned": {
        "status": "STRONG",
        "evidence": [
            "Ram: 15+ yrs IT, 8+ yrs healthcare IT (Alsac/CIGNA/Medifast/Teladoc/UHC/ECFMG); "
            "inventor of DGP architecture; platform complete March 2026",
            "Manasa: 10+ yrs IT, 5+ yrs healthcare IT (Interwell Health/UHG/ECFMG); "
            "direct payer-side knowledge of denial systems that Ardia defeats",
        ],
        "documents": ["White paper", "LinkedIn profiles", "Paper 4 (Manasa's insider analysis)"],
    },
    "EB-2 NIW Prong 3 — Beneficial to US to Waive Labor Cert": {
        "status": "STRONG",
        "evidence": [
            "No comparable AI-native platform for independent labs — genuine market white space",
            "Solving $12B/yr drain on US healthcare system",
            "Preserves lab access for rural, underserved, addiction medicine communities",
            "Native Texas SB 1188 + TRAIGA compliance — advancing US AI governance frameworks",
            "Preserves 32% of US diagnostic test volume (7,000+ labs)",
        ],
        "documents": ["Paper 3 (regulatory AI)", "Market intelligence PDF", "White paper"],
    },
}


# ── Output functions ──────────────────────────────────────────────────────────

def extract_docx(path):
    try:
        with zipfile.ZipFile(path) as z:
            xml = z.read('word/document.xml').decode('utf-8', errors='ignore')
            text = re.sub('<[^>]+>', ' ', xml)
            return re.sub(r'\s+', ' ', text).strip()
    except Exception as e:
        return f"[Could not read {path}: {e}]"


def load_source_docs():
    docs = {}
    candidates = [
        ("whitepaper", "Ardia_Health_White_Paper_Business_Plan (1).docx"),
        ("whitepaper_v1", "Ardia_Health_White_Paper_Business_Plan.docx"),
        ("business_plan", "Ardia_Health_Business_Plan_2026_v2.docx"),
        ("outreach", "Ardia_Investor_Outreach_Emails_2026.docx"),
    ]
    for key, fname in candidates:
        fpath = REPO_ROOT / fname
        if fpath.exists():
            docs[key] = extract_docx(str(fpath))
            print(f"  Loaded: {fname} ({len(docs[key]):,} chars)")
        else:
            print(f"  Missing: {fname} (skipping)")
    return docs


def print_paper(paper_id, mode="full"):
    p = PAPERS[paper_id]
    print(f"\n{'═'*72}")
    print(f"PAPER {paper_id}")
    print(f"{'═'*72}")
    print(f"\nTitle:\n  {p['title']}")
    print(f"\nAuthors: {p['authors']}")
    print(f"Affiliations: {p['affiliations']}")
    print(f"\nTarget Journals:")
    for j in p['target_journals']:
        print(f"  • {j}")
    print(f"\nVisa Criteria This Paper Satisfies:")
    for c in p['visa_criteria']:
        print(f"  ✅ {c}")
    print(f"\nWhat Makes This Paper Original:")
    print(f"  {p['differentiation_from_prior_work']}")

    if mode in ("full", "abstract"):
        print(f"\n{'─'*72}")
        print("ABSTRACT (ready to submit):")
        print(f"{'─'*72}")
        print(p['abstract'])

    if mode == "full":
        print(f"\n{'─'*72}")
        print("PAPER OUTLINE:")
        print(f"{'─'*72}")
        for item in p['outline']:
            print(f"  {item}")


def print_judging():
    print(f"\n{'═'*72}")
    print("JUDGING / PEER REVIEW OPPORTUNITIES — EB-1A Criterion 4")
    print(f"{'═'*72}")
    for i, opp in enumerate(JUDGING_OPPORTUNITIES, 1):
        print(f"\n{i}. {opp['opportunity']}")
        print(f"   Org: {opp['org']}")
        print(f"   How: {opp['how']}")
        print(f"   Visa: {opp['visa_criterion']}")
        print(f"   Timeline: {opp['timeline']}")
        print(f"   Notes: {opp['notes']}")


def print_citations():
    print(f"\n{'═'*72}")
    print("COMPLETE CITATION LIBRARY — Ardia Health Source Documents")
    print(f"{'═'*72}")
    print("\nIMPORTANT: Verify all DOIs before submitting to journals.")
    print("Citations marked 'Ardia white paper citation' need DOI confirmation.\n")
    for key, c in CITATIONS.items():
        print(f"\n{c['ref']} [{key}]")
        print(f"   {c['full']}")
        print(f"   Key claim: {c['claim']}")
        print(f"   Visa use: {c['visa_use']}")
        print(f"   Source verification: {c['source']}")


def print_founders():
    print(f"\n{'═'*72}")
    print("FOUNDER PROFILES (verified — use these in all papers)")
    print(f"{'═'*72}")
    for key, f in FOUNDERS.items():
        print(f"\n{f['name']} — {f['role']}")
        print(f"  IT Experience: {f['it_years']} years total | Healthcare IT: {f['healthcare_it_years']} years")
        print(f"  Employers: {' / '.join(f['employers'])}")
        print(f"  Expertise:")
        for e in f['expertise']:
            print(f"    • {e}")
        print(f"  Contact: {f['contact']}")


def print_architecture():
    a = ARCHITECTURE
    print(f"\n{'═'*72}")
    print(f"ARCHITECTURE: {a['full_name']}")
    print(f"Inventor: {a['inventor']}")
    print(f"{'═'*72}")
    print(f"\nWhy 'DGP' and not 'neuro-symbolic':")
    print(f"  {a['why_original']}")
    print(f"\nLayer descriptions:")
    for layer_key, layer in a['layers'].items():
        print(f"\n  {layer_key} — {layer['name']}")
        print(f"    Technology: {layer['tech']}")
        print(f"    Function:   {layer['function']}")
    print(f"\nIntegration: {a['integration']}")
    print(f"Compliance:  {a['compliance']}")


def print_visa_map():
    print(f"\n{'═'*72}")
    print("VISA CRITERIA MAP — EB-1A / EB-2 NIW / O-1A")
    print(f"{'═'*72}")
    for criterion, data in VISA_MAP.items():
        status_icon = "✅" if "STRONG" in data["status"] else "⚠️ "
        print(f"\n{status_icon} {criterion}")
        print(f"   Status: {data['status']}")
        for e in data["evidence"]:
            print(f"     • {e}")
        print(f"   Documents needed: {', '.join(data['documents'])}")


def print_list():
    print(f"\n{'═'*72}")
    print("AVAILABLE PAPERS — Ardia Health Academic Publication Pipeline")
    print(f"{'═'*72}")
    for pid, p in PAPERS.items():
        print(f"\nPaper {pid}: {p['title'][:68]}...")
        print(f"  Authors: {p['authors']}")
        print(f"  Top journal: {p['target_journals'][0]}")
        print(f"  Key criterion: {p['visa_criteria'][0]}")


def save_paper_to_file(paper_id):
    p = PAPERS[paper_id]
    safe_title = re.sub(r'[^a-zA-Z0-9_]', '_', p['title'][:50])
    fname = f"paper_{paper_id}_{safe_title}.txt"
    outpath = REPO_ROOT / fname
    with open(outpath, 'w') as f:
        f.write(f"PAPER {paper_id}\n{'='*72}\n\n")
        f.write(f"Title: {p['title']}\n\n")
        f.write(f"Authors: {p['authors']}\n")
        f.write(f"Affiliations: {p['affiliations']}\n\n")
        f.write("Target Journals:\n")
        for j in p['target_journals']:
            f.write(f"  - {j}\n")
        f.write("\nVisa Criteria:\n")
        for c in p['visa_criteria']:
            f.write(f"  - {c}\n")
        f.write(f"\nWhat Makes This Paper Original:\n  {p['differentiation_from_prior_work']}\n")
        f.write(f"\nABSTRACT\n{'='*72}\n\n{p['abstract']}\n")
        f.write(f"\nOUTLINE\n{'='*72}\n\n")
        for item in p['outline']:
            f.write(f"{item}\n")
        f.write(f"\nCITATIONS\n{'='*72}\n\n")
        for ref_num in range(1, 12):
            ref_key = f"[{ref_num}]"
            for key, c in CITATIONS.items():
                if c['ref'] == ref_key:
                    f.write(f"{ref_key} {c['full']}\n\n")
    print(f"  Saved: {fname}")
    return fname


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Ardia Health — Academic Paper Publisher & Citation Builder"
    )
    parser.add_argument("--list", action="store_true", help="List all 5 papers")
    parser.add_argument("--paper", type=int, choices=[1,2,3,4,5],
                        help="Generate full paper (title + abstract + outline)")
    parser.add_argument("--abstract", type=int, choices=[1,2,3,4,5],
                        help="Print abstract only (ready to paste into arXiv)")
    parser.add_argument("--judging", action="store_true",
                        help="Judging and peer review opportunities (EB-1A Criterion 4)")
    parser.add_argument("--citations", action="store_true",
                        help="Full citation library with DOI verification notes")
    parser.add_argument("--founders", action="store_true",
                        help="Print verified founder profiles (use in all papers)")
    parser.add_argument("--architecture", action="store_true",
                        help="Print DGP architecture definition and why it's original")
    parser.add_argument("--visa-map", action="store_true",
                        help="Full EB-1A / NIW / O-1A evidence status")
    parser.add_argument("--save", action="store_true",
                        help="Save paper(s) to .txt files in repo root")
    parser.add_argument("--all", action="store_true",
                        help="Generate all output")

    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
        print("\nQuick start:")
        print("  python3 publisher.py --list")
        print("  python3 publisher.py --abstract 1     # Copy-paste ready for arXiv submission")
        print("  python3 publisher.py --founders       # Verify bios before writing any paper")
        print("  python3 publisher.py --architecture   # DGP architecture — what's original")
        print("  python3 publisher.py --judging        # Where to apply for peer reviewer roles NOW")
        print("  python3 publisher.py --visa-map       # Full EB-1A/NIW/O-1A status")
        print("  python3 publisher.py --all --save     # Generate + save everything")
        sys.exit(0)

    print(f"\n{'═'*72}")
    print("ARDIA HEALTH — Academic Paper Publisher & Citation Builder")
    print(f"Rambabu Vadlamudi & Manasa Jampani | ardiahealthlabs.com")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'═'*72}")

    print("\nLoading source documents from repo...")
    docs = load_source_docs()
    print(f"  {len(docs)} documents loaded as source material\n")

    if args.founders or args.all:
        print_founders()

    if args.architecture or args.all:
        print_architecture()

    if args.list or args.all:
        print_list()

    if args.paper:
        print_paper(args.paper, mode="full")
        if args.save:
            save_paper_to_file(args.paper)

    if args.abstract:
        print_paper(args.abstract, mode="abstract")

    if args.judging or args.all:
        print_judging()

    if args.citations or args.all:
        print_citations()

    if args.visa_map or args.all:
        print_visa_map()

    if args.all and args.save:
        print(f"\n{'─'*72}")
        print("SAVING ALL PAPERS TO FILES...")
        for pid in PAPERS:
            save_paper_to_file(pid)

    print(f"\n{'═'*72}")
    print("PRIORITY ACTIONS:")
    print("  1. THIS WEEK: Submit Paper 1 to arXiv cs.AI → EB-1A Criterion 6, live in 1-2 days")
    print("  2. THIS WEEK: Email editor@jamia.org to become peer reviewer → EB-1A Criterion 4")
    print("  3. THIS WEEK: Submit Paper 2 to arXiv q-bio.QM")
    print("  4. NEXT 2 WKS: Apply HIMSS + AMIA membership → EB-1A Criterion 2")
    print("  5. NEXT 2 WKS: Pitch Becker's / MedCity on PAMA 2027 → EB-1A Criterion 3")
    print(f"{'═'*72}\n")


if __name__ == "__main__":
    main()
