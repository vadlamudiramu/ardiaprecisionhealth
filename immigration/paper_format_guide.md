# Universal Academic Paper Format Guide
## Ardia Health Labs — Ram Vadlamudi & Manasa Jampani
## For arXiv, medRxiv, JAMIA, Health Affairs, NEJM AI, Clinical Chemistry, JALM

This guide defines the format for all papers. The format described here is accepted by arXiv, medRxiv, JAMIA, Health Affairs, NEJM AI, Clinical Chemistry, JALM, and all other target venues without modification to the paper body.

---

## Core Principle

Write the paper in IMRAD format with NLM numbered references and a word count of 3,500–5,000. This fits within the acceptable range of every target venue. Submit the same manuscript to arXiv/medRxiv (preprint) and then to the journal — no reformatting required.

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

### Abstract (PROVIDE BOTH — use the right one per venue)

**Structured abstract** (for JAMIA, Clinical Chemistry, most medical journals):
```
Background: [1–2 sentences — the problem]
Methods: [2–3 sentences — what you built/studied]
Results: [2–3 sentences — quantitative findings]
Conclusions: [1–2 sentences — implications]
```
Word limit: 250–300 words

**Unstructured abstract** (for arXiv, NEJM AI Perspective, Health Affairs):
Single paragraph, 200–250 words. Same content, no section headers.

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
- Comparison to industry benchmark (65% of denials never appealed; 50–80.7% win rate when appealed)

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

**Citations for every paper (must include):**
- XiFin 2024 Payor Denial Impact Report (non-peer-reviewed; cite as industry report)
- JAMA Network Open 2025 Georgetown study (cite as peer-reviewed journal article)
- Deep Claim, Kim 2020, arXiv 2007.06229 (cite for differentiation)
- Health Affairs 2025 payer AI paper, DOI: 10.1377/hlthaff.2025.00897 (for Manasa's papers)

---

## Word Count Guidelines

| Section | Target |
|---------|--------|
| Abstract | 250–300 (structured) or 200–250 (unstructured) |
| Introduction | 500–700 |
| Background | 400–600 |
| Methods/Architecture | 900–1,200 |
| Results/Evaluation | 600–900 |
| Discussion | 500–700 |
| Conclusion | 150–250 |
| **Total body** | **3,300–4,650** |
| References (not counted) | varies |
| **Total with abstract** | **~3,500–5,000** |

This range fits:
- arXiv: no word limit
- medRxiv: no word limit
- JAMIA: 3,500–5,000 (research articles)
- Health Affairs: 3,500–6,000 (full articles)
- NEJM AI: 2,500–4,000 (Original Investigation) or 1,500–2,500 (Perspective)
- Clinical Chemistry: 2,500–4,000 (Technical Briefs/Articles)
- JALM: 3,000–5,000 (research articles)

For NEJM AI Perspective (Manasa's Paper 4): trim to 2,500 words; cut methods section to 400 words, focus on analysis and implications.

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
