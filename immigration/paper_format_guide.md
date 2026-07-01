# Universal Academic Paper Format Guide
## Ardia Health Labs — Ram Vadlamudi & Manasa Jampani
## For arXiv, medRxiv, JAMIA, Health Affairs, NEJM AI, Clinical Chemistry, JALM

**Revised 2026-07-01.** The original version of this guide claimed a single 3,500–5,000-word IMRAD draft would fit every venue unmodified. A live-search audit against each venue's actual current author guidelines and a real recently published article per venue found that claim was wrong for several major targets — see the corrected Word Count table below. The Methods/Results/Discussion prose can stay largely the same across a preprint and its eventual journal submission, but **the abstract style and total length must be trimmed per venue before submission.**

**Preprints are not peer review — do not describe them as such.** Both arXiv and medRxiv explicitly disclaim peer review. medRxiv's preprint banner states papers "have not been certified by peer review and should not be relied on to guide clinical practice." In any immigration filing or petition narrative, describe an arXiv/medRxiv posting as a preprint, and describe journal review status separately and accurately — journal review is not guaranteed, can take months, and rejection is common (Health Affairs desk-rejects roughly two-thirds of submissions within days).

---

## Core Principle

Write the paper in IMRAD format with NLM numbered references. Draft the body once, then trim the abstract and total length to the specific venue's cap before submission — see the per-venue table below for actual caps (they range from ~2,000 words at JAMIA to no limit at all on arXiv/medRxiv).

Journal-specific requirements (cover letters, submission system fields, supplementary forms) go in **separate** submission documents, never inside the paper body.

---

## Paper Structure (IMRAD)

### Title
- 12–18 words maximum
- Include the key domain term and the AI/computational method
- Do NOT include "DGP" alone — spell it out: "Deterministic-Generative-Predictive"
- Format: Title Case
- Example: "ToxIQ: An Artificial Intelligence Framework for Toxicology Laboratory Claim Compliance and Denial Recovery"

### Authors
- Format: First name Last name, First name Last name
- Affiliations as footnote numbers: ¹Ardia Health Labs, Argyle, TX
- Corresponding author email at the bottom of the author block
- ORCID iD encouraged (create at orcid.org — free; adds credibility)

### Abstract (PROVIDE BOTH — use the right one per venue; caps differ significantly, see table)

**Structured, 4-part** (JAMIA — Objective / Materials and Methods / Results / Discussion / Conclusion, capped at ~150 words; NEJM AI — Background / Methods / Results / Conclusions, ~300–310 words):
```
Background: [1–2 sentences — the problem]
Methods: [2–3 sentences — what you built/studied]
Results: [2–3 sentences — quantitative findings]
Conclusions: [1–2 sentences — implications]
```

**Structured, 5-part** (Clinical Chemistry only — adds a distinct "Summary" section beyond standard IMRaD):
```
Background: [...]
Methods: [...]
Results: [...]
Conclusions: [...]
Summary: [1 sentence — plain-language takeaway]
```

**Unstructured** (arXiv, medRxiv, Health Affairs — single paragraph, no headers). Health Affairs specifically caps this at 150–180 words as part of its 3,250-word total article cap; arXiv/medRxiv have no fixed length.

Draft one long structured version first, then cut to whichever venue-specific cap applies — do not assume 250–300 words is universal; JAMIA's ~150-word cap and Health Affairs' 150–180-word cap are both tighter than that.

### Keywords
5–8 keywords separated by semicolons.  
Always include: "machine learning" OR "artificial intelligence"; "revenue cycle management"; the specific domain (e.g., "toxicology," "molecular diagnostics," "behavioral health"); "independent clinical laboratory"

---

### 1. Introduction (500–700 words)

Paragraph 1: **The problem** — quantified. Open with the key statistic.  
> "Independent clinical laboratories face a documented 35.3% molecular diagnostic claim denial rate (XiFin 2024), representing an estimated $10–12 billion in annual preventable revenue losses..."

Paragraph 2: **Why the problem persists** — the gap in current solutions.  
> "Existing healthcare administrative AI addresses general claims processing without domain specificity. No prior published framework addresses [your specific domain]..."

Paragraph 3: **What exists (adjacent work)** — what you are NOT.  
Cite the adjacent papers from research_gaps.md (Deep Claim, Johnson 2023, Health Affairs 2025) and explain why they don't solve the problem.

Paragraph 4: **Your contribution** — one clear sentence.  
> "This paper presents [name], the first published framework for [specific domain] using [approach]."

Paragraph 5: **Paper organization** — one sentence.  
> "The remainder of this paper describes [structure]."

---

### 2. Background / Related Work (400–600 words)

Subsections as appropriate:
- 2.1 Clinical/policy context (PAMA, MolDX, etc. — whatever is relevant to the paper's domain)
- 2.2 Prior AI approaches (general healthcare AI — Deep Claim, Johnson 2023, etc.)
- 2.3 The gap (why existing approaches are insufficient for this domain)

This section must cite all adjacent work. Do not omit papers that could be seen as prior art — address them directly and explain differentiation.

---

### 3. Architecture / Methods (900–1,200 words)

For DGP-based papers:

**3.1 Overview**  
Brief description of the three-layer architecture. One sentence each on Layer 1 (Deterministic), Layer 2 (Generative), Layer 3 (Predictive).

**3.2 Layer 1: Deterministic Policy Engine**  
- Rule encoding methodology
- Sources: LCD, NCD, MolDX DEX Z-codes, CPT codes, etc.
- Validation approach
- Key metric: number of rules; zero-hallucination guarantee on policy interpretation

**3.3 Layer 2: Generative Clinical Reasoning**  
- LLM integration (can reference "Claude API" generically or as "a large language model API")
- Appeal brief generation approach
- Database integration (14 medical databases, 340ms)
- Human review workflow

**3.4 Layer 3: Predictive Denial Prevention**  
- ML model type and training data source (EDI 835 historical claims)
- Feature set
- Pre-submission denial risk scoring mechanism

**3.5 Integration and Compliance**  
- FHIR R4, HL7 v2, EDI 835/837 interoperability
- Texas SB 1188 / TRAIGA compliance by design

*Note: For domain-specific papers (ToxIQ, BehaviorIQ, etc.), adapt these subsections to focus on domain-specific regulatory requirements (e.g., DEA Schedule IV/V for toxicology, 42 CFR Part 2 for behavioral health) while referencing DGP as the underlying architecture.*

---

### 4. Evaluation / Results (600–900 words)

For architecture papers (pre-pilot):
- Describe the evaluation methodology
- Present case study or simulation results
- If real data is available: denial rate before/after; appeal success rate; revenue recovered
- Include a table or figure (journals expect at least one visual)

For pilot outcome papers (Paper 5/M5):
- Patient/claim volume
- Baseline denial rate vs. post-intervention denial rate
- Revenue recovery rate
- Comparison to an industry benchmark — **do not use the "65% of denials never appealed / 50–80.7% win rate" figures.** The citation audit (2026-07-01) traced these to a non-existent "HFMA/LigoLab 2024 Laboratory Revenue Recovery Report" — no real source was found for either number across any of the 11 papers that used them. Use only verified figures (the 35.3% XiFin molecular diagnostics denial rate, or the 2.76× Georgetown/JAMA Network Open disparity, PMID 40249617) until a real appeal-rate source is located.

**Figures and Tables:**
- Tables: numbered Table 1, Table 2, etc.; caption below the table
- Figures: numbered Figure 1, Figure 2, etc.; caption below the figure
- Keep to 2–4 visuals per paper; more can be supplementary

---

### 5. Discussion (500–700 words)

Paragraph 1: Summary of main findings.  
Paragraph 2: How findings address the problem stated in the Introduction.  
Paragraph 3: Comparison with existing approaches (show superiority or complementarity).  
Paragraph 4: Limitations — be honest; one paragraph of genuine limitations strengthens credibility.  
Paragraph 5: Future work — pilot data, expanded deployment, additional domains.

---

### 6. Conclusion (150–250 words)

3–4 sentences. Restate the problem, your contribution, and the implication. Do NOT introduce new information. End with a forward-looking sentence about national healthcare impact.

---

### Acknowledgments

```
The authors thank [names if applicable]. This research received no external funding.
[Any conflicts of interest: "R.V. is the founder and M.J. is the co-founder of Ardia Health Labs, which is developing commercial implementations of the DGP architecture described in this paper."]
```

Conflict of interest disclosure is required by all journals. Disclosing it fully does NOT hurt the paper — concealing it does.

---

### References

**Format: NLM numbered (Vancouver style)**  
This is the required format for arXiv (default), medRxiv, JAMIA, Clinical Chemistry, JALM, and is accepted by Health Affairs and NEJM AI.

```
1. Author AB, Author CD. Title of article. Journal Name. Year;Volume(Issue):pages. doi:10.xxxx/xxxxx.

2. Author AB. Title of book. City: Publisher; Year.

3. Organization Name. Title of report [Internet]. City: Publisher; Year [cited 2026 Jun 30]. Available from: URL
```

**Key rules:**
- Number references in order of appearance in text
- Cite in text as superscript numbers: denial rates exceed 35%¹ or (1) — use consistent style
- Maximum 35–40 references for a full research article; 15–20 for a short communication
- Do NOT use author-date (APA) format in the paper body — journals format their published version; you submit in NLM and let them convert

**Citations for every paper (must include) — verified exact forms, 2026-07-01 audit:**
- XiFin, Inc. *2024 Payor Denial Impact Report* (industry report, no DOI — cite as gray literature; 20M+ claims, 35.3% molecular diagnostics denial rate — confirmed accurate)
- Kang SY, Odouard I, Gresenz CR. "Claim Denials for Cancer-Related Next-Generation Sequencing in Medicare." *JAMA Netw Open.* 2025;8(4):e255785. doi:10.1001/jamanetworkopen.2025.5785. PMID 40249617. (n=29,919 claims, 24,443 beneficiaries; OR 2.76 independent vs. hospital labs — this is a **cohort study**, not "cross-sectional," and the authors are Georgetown University School of Health/McCourt School of Public Policy + Johns Hopkins Bloomberg School of Public Health, not "Georgetown University Medical Center")
- Kim BH, Sridharan S, Atwal A, Ganapathi V. "Deep Claim: Payer Response Prediction from Claims Data with Deep Learning." arXiv preprint arXiv:2007.06229. 2020.
- Mello MM, Trotsyuk AA, Djiberou Mahamadou AJ, Char D. "The AI Arms Race In Health Insurance Utilization Review: Promises Of Efficiency And Risks Of Supercharged Flaws." *Health Affairs.* 2026;45(1):6-13. doi:10.1377/hlthaff.2025.00897. PMID 41494115. **This is the only real article behind this DOI** — the audit found it fabricated with different author names in 7 of the 11 generated papers. Never attach a different author list to this DOI.

**Do not reuse a DOI/PMID/arXiv ID across papers with different author names or titles.** If a citation needs re-derivation for a new paper, look it up fresh — do not recall it from memory or from how a prior paper cited it.

---

## Word Count Guidelines

**Draft the full-length version first** (Introduction 500–700 / Background 400–600 / Methods 900–1,200 / Results 600–900 / Discussion 500–700 / Conclusion 150–250 ≈ 3,300–4,650-word body). This full-length draft is what goes to arXiv/medRxiv as a preprint (no limit). **Before submitting to any journal below, cut to that journal's real cap** — several are far tighter than the original body:

| Venue | Verified actual cap (2026-07-01 audit) | Abstract style | Peer-reviewed? |
|-------|------------------------------------------|----------------|-----------------|
| arXiv (cs.AI) | No limit — but as of Oct 2025, review/survey/"position" papers are declined unless already peer-reviewed elsewhere; original research is fine | Unstructured, author's own format | **No** — moderation/screening only |
| medRxiv | No limit — but requires ethics/IRB statement, trial registry ID if applicable, data availability statement, 36-month conflict-of-interest lookback | Structured IMRaD, incl. explicit Limitations subsection | **No** — administrative + scope screening only |
| JAMIA (Research and Applications) | **~2,000 words** (excl. abstract/acknowledgments/references) | Structured, ~150-word cap: Objective / Materials and Methods / Results / Discussion / Conclusion | Yes |
| Health Affairs (flagship) | **3,250 words total** (incl. abstract), up to 4 exhibits | **Unstructured**, 150–180 words | Yes — ~2/3 of submissions desk-rejected within days; external review adds 6–8 weeks |
| NEJM AI (Original Investigation) | ~3,000–3,800-word body, ~310-word abstract | Structured: Background / Methods / Results / Conclusions | Yes |
| Clinical Chemistry | Est. 4,000–7,000 words (based on page count of a verified example; not independently confirmed) | Structured **5-part**: Background / Methods / Results / Conclusions / **Summary** | Yes |
| JALM | **≤3,500 words**, ≤40 references, ≤6 tables/figures combined | Unstructured confirmed for review-type articles; original-research abstract policy unconfirmed — verify before submitting | Yes, ~4-week decision typical |
| Journal of Healthcare Management | Est. 4,000–6,000 words (indirect estimate; guidelines page could not be independently verified — reverify before submitting) | Unconfirmed — appears to support IMRaD headers for empirical work | Yes (per secondary sources; not independently confirmed) |
| J Behavioral Health Services & Research | Not independently confirmed — direct fetch of Springer/USF-hosted guideline pages was blocked (403) on every attempt; word count and abstract style should be verified directly before submission (accepted types: Regular Articles, Brief Reports, Policy Perspectives, Literature Reviews, Commentaries, Notes from the Field) | Not independently confirmed | Yes — Springer journal, official publication of the National Council for Behavioral Health. Submission portal (confirmed via search): `http://www.editorialmanager.com/jbhs/default.aspx`. Open-access APC confirmed at $3,990 USD. |

Note the direction of the correction: this guide previously stated JAMIA accepts 3,500–5,000 words and Health Affairs 3,500–6,000 — both were wrong. JAMIA's real cap (~2,000 words) is less than half what was stated; Health Affairs' real cap (3,250 words *including* abstract) is also lower, and its abstract is unstructured, not structured as many other medical journals use.

For NEJM AI Perspective (shorter format): trim to ~1,500–2,500 words; cut methods section to ~400 words, focus on analysis and implications.

---

## What Does NOT Go in the Paper Body

Never embed these in the paper manuscript:
- Journal submission instructions
- Cover letter text
- Author biographies (go in submission system form, not paper)
- Immigration-related framing ("this work supports our national interest waiver...")
- Future tense promises ("in a future paper we will...")
- Company promotional language ("Ardia Health Labs' revolutionary platform...")

These belong in separate documents (submission guide, cover letter, etc.).

---

## Checklist Before Submitting Any Paper

- [ ] Title is 12–18 words; no jargon undefined in abstract
- [ ] Abstract has both structured and unstructured versions ready
- [ ] Introduction opens with a quantified statistic from a citable source
- [ ] Adjacent work is cited and differentiated (not ignored)
- [ ] Conflict of interest is disclosed
- [ ] References are in NLM numbered format
- [ ] Word count is 3,500–5,000
- [ ] At least 1 figure or table is included
- [ ] No journal-specific submission instructions are in the paper body
- [ ] ORCID iDs included for all authors
- [ ] File is a clean PDF (for arXiv/medRxiv) or .docx (for journal submission systems)

---

## arXiv vs. medRxiv — Which to Use

| Use arXiv | Use medRxiv |
|-----------|------------|
| cs.AI, cs.IR papers (DGP architecture, ML methods) | Health sciences papers (clinical analysis, outcomes, policy) |
| Paper 1 (DGP architecture) | Paper 4 (Payer AI Black Box) |
| Paper 6 (PAMA + AI) | Paper M3 (Renal Care + Mol Dx) |
| Paper 9 (MolDX Compliance AI) | Paper M5 (Pilot Outcomes) |
| Papers 8, 10 (ToxIQ, BehaviorIQ — technical AI) | Papers M1, M2, M4 (ACO, Payer accountability, Value-based care) |

When in doubt: use arXiv cs.AI for papers where the AI architecture is the primary contribution; use medRxiv for papers where the clinical or policy analysis is the primary contribution.
