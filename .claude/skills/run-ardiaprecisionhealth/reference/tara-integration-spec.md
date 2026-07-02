# TARA Integration Spec — canonical grounding for the 2026-07 redesign

This is the **only** approved source of facts for the TARA redesign. Every
edit and every new page must trace to this file. If a number, citation, or
product claim is **not** in this file, it may **not** appear on the site.
This exists because the site is a pre-revenue, investor- and
customer-facing healthcare product where a fabricated claim is a legal and
reputational risk (see `audit-2026-07-01.md` for what was already wrong).

Extracted verbatim from the founder's own June-2026 redesign package
(`ClaudeCode/` folder: `ardia-v2.html`, `market-validation.html`,
`docs/INVESTOR_FAQ.md`, `docs/COMPLIANCE.md`, `src/data/products.js`).
That package supersedes the older business-plan docs where they conflict —
it is the newest, most disciplined framing and the one the founder chose.

## 0. Hard rules (non-negotiable)

1. **No Ardia performance numbers.** Ardia is pre-revenue. There is no win
   rate, no recovery rate, no "$X recovered," no per-appeal cost *for
   Ardia*, no live customer, no testimonial. Any such claim is a
   fabrication and must be removed or reframed.
2. **Every statistic is an industry benchmark with a named source** from
   §2 below, and must be visibly labelled as such ("Industry benchmark —
   not Ardia data"). Never present a benchmark as Ardia's own outcome.
3. **No invented citations.** No PubMed IDs, ALJ case numbers, LCD/NCD
   section numbers, NCCN page numbers, or study names unless they appear
   in this spec. The demo may cite **LCD L38016** and its §3.2/§4.1 (used
   in the founder's own demo) — nothing else specific.
4. **Demos are synthetic.** Any claim/patient/dashboard data is labelled
   "Demo · synthetic data · no PHI · representative amounts · Ardia is
   pre-revenue."
5. **Don't delete pages or sections wholesale.** Correct claims in place;
   preserve layout, branding, nav, footer, colour tags. Additive where
   possible.

## 1. Architecture rename (canonical)

The architecture is now **TARA — the Triadic Adjudicative Reasoning
Architecture**. It is the same three-layer neuro-symbolic system the site
previously called the "Neuro-Symbolic Sandwich Architecture," renamed and
clarified. Rename rules:

- "Neuro-Symbolic Sandwich Architecture" → **"Triadic Adjudicative
  Reasoning Architecture (TARA)"** on first mention per page, then
  **"TARA"** thereafter.
- "Neuro-Symbolic Sandwich" → **"TARA"**.
- Drop the "sandwich / bread / filling" metaphor. Where a sentence leans on
  it, rewrite to TARA's three named layers (below) without inventing new
  claims.
- Generic lowercase "neuro-symbolic" as a *technique* descriptor
  (e.g. "a neuro-symbolic approach") may stay — TARA genuinely is
  neuro-symbolic. Only the branded *name* changes.

**TARA's three layers** (use these exact framings):
- **Layer 1 — Symbolic Policy Engine.** Deterministic, zero hallucinations,
  no LLM. Encodes LCD/NCD/MolDX DEX policy as rules; cross-references a
  denial code against the exact policy section for that CPT under that MAC.
  Rule execution, not inference. Scope: **400+ LCD/NCD policies, all 7
  MACs, MolDX DEX, weekly CMS updates, PAMA-aware.**
- **Layer 2 — Clinical Reasoning Engine.** AI-powered, grounded in the
  patient record only. Reads clinical documentation (FHIR R4, HL7 v2; on
  GCP Vertex AI) against payer medical-necessity criteria; every inference
  traces to a specific line in the record; if documentation doesn't support
  an appeal, it says so.
- **Layer 3 — Denial Pattern Library.** A compounding data asset on
  BigQuery/GCP built from the EDI 835/837 corpus; after 60–90 days enables
  pre-submission screening (flag claims matching learned denial patterns
  before they go out). This corpus is the moat / flywheel.

**Why TARA produces zero hallucinations** (approved talking points): Layer 1
is deterministic logic (can't invent a policy section); Layer 2 is grounded
inference only (cites the record, not a plausible invention); every AI
output requires practitioner attestation before submission (TX SB 1188);
full timestamped audit trail (CLIA/CAP-grade).

## 2. Approved industry-benchmark whitelist (the ONLY stats allowed)

Each must appear with its source and an "industry benchmark, not Ardia
data" label.

| Value | Label | Source |
|---|---|---|
| $3.8B | Lab revenue cut by PAMA since 2018 | CMS PAMA Final Rule · MedPAC 2024 |
| 23–31% | Avg denial rate, independent molecular labs | XiFin Revenue Cycle Intelligence Report 2024 |
| 65% | Of denied claims never appealed by independent labs | MGMA Denial Management Survey 2023 |
| $118 | Average cost of a manual appeal | Change Healthcare Revenue Cycle Report 2023 |
| 45% | Manual appeal success rate (industry average) | HFMA Denials Management Survey 2024 |
| $70B+ | AI in RCM market by 2030 (24% CAGR) | Grand View Research, AI in RCM Market 2024 |
| 2.76× | Higher denial rate, independent vs. hospital labs | JAMA Network Open 2024, n=29,919 |
| $803M | Texas MSSP shared savings generated in 2024 | CMS MSSP Public Use File 2024 |
| ~$12B | Independent-lab annual revenue lost to denials (TAM) | derived: XiFin/MGMA above |
| $1.8B–$2.4B | Annual recoverable opportunity, independent-lab vertical | derived from TAM × denial × never-appealed |

Also allowed (regulatory facts, from COMPLIANCE.md): TX SB 1188 (eff.
Sept 1 2025; up to $250K penalty), TRAIGA/HB 149 (eff. Jan 1 2026;
$10K–$200K civil penalty; 36-month sandbox; NIST AI RMF safe harbor),
HIPAA, FCA, CLIA/CAP.

## 3. Ardia honest facts (approved)

- **Entity:** Founded January 2026 as Ardia Health Labs LLC (Delaware LLC);
  converting to **Ardia Precision Health, Inc. (Delaware C-Corp)**.
- **Stage:** Pre-revenue, seed. **Seed target $750K–$1.5M.** 18-month
  runway at $1M; first-revenue target Q4 2026.
- **Traction reality:** No customers, no production software in customer
  hands. Demo engine in development (60–90 day target). Q3 2026 DFW pilot
  target (ToxIQ™ Phase 1). Primary pilot prospect: HealthTrackRx (Denton,
  TX), ~15 min from HQ.
- **HQ:** Argyle, TX 76226 (DFW metro).
- **Pricing:** 15% contingency on recovered revenue; no upfront cost.
- **Unit economics (illustrative, labelled as such):** a lab with 5,000–
  10,000 claims/mo at ~25% denial has ~$1.25M–$2.5M denied/yr; ~65% never
  appealed ≈ $812K–$1.6M recoverable; at 15% contingency on ~60% recovery ≈
  $73K–$146K per lab/yr; 10 labs ≈ $730K–$1.46M ARR. Mark as *illustrative
  model, not a forecast of results.*
- **Tech stack:** GCP (us-central1, US data residency): Vertex AI,
  Healthcare Data Engine, Cloud Healthcare API (FHIR R4 store), BigQuery
  (CMEK), Cloud Run. Backend Python/FastAPI. Frontend Next.js/React.
  Interop: FHIR R4, HL7 v2, EDI 835/837. AES-256 at rest, TLS 1.3 in
  transit. **GCP is the AI infrastructure — NOT Salesforce/AWS.** Salesforce
  Health Cloud, if mentioned at all, is only a CRM/distribution tool — never
  the AI platform.
- **IP:** Four provisional patent areas identified (tox denial recovery
  pipeline; MolDX/DEX Z-code adjudication reasoning; PAMA-aware test-mix
  optimization; contingency-aware claim selection). Provisionals in
  preparation.
- **Team:** Ram Vadlamudi (founder/architect; payer-side denial-systems
  background: Cigna/Evernorth, UnitedHealth Group/Optum, Teladoc; also
  ALSAC). Combined team 20+ yrs healthcare IT. (Do not invent titles or
  employers beyond these.)
- **Modules (unchanged, keep):** ToxIQ™ (toxicology), MolecuIQ™ (molecular/
  MolDX/PGx), AcoIQ™ (ACO analytics), BehaviorIQ™ (behavioral health). No
  other named modules. **"RareSense" is not a product** — remove or clearly
  mark as an aspirational future research direction with no metrics.
- **Compliance posture:** HIPAA (GCP BAA signed), NIST AI RMF 1.0
  (GOVERN/MAP/MEASURE/MANAGE), SB 1188 + TRAIGA native, FCA safe harbor via
  human-in-the-loop attestation, CLIA/CAP (labs must hold; Ardia does not
  test). **SOC 2 Type II: not yet certified — targeted Q1 2027.**

## 4. Claim-correction table (fix these where they appear)

From `audit-2026-07-01.md`. Replace with grounded framing from §1–§3.

| Fabricated / risky claim (any page) | Correction |
|---|---|
| "89% appeal win rate" / "89% win rate" as Ardia's result | Remove as an Ardia stat. If a win-rate figure is needed, use "**45%** manual appeal success rate (industry average, HFMA 2024)" labelled as a benchmark. Never an Ardia outcome. |
| "$2.50 per appeal" / "47× cost reduction" (Ardia) | Remove the Ardia per-appeal cost and the 47× multiplier. Keep "**$118** average manual appeal cost (Change Healthcare 2023)" as a benchmark; frame Ardia's value qualitatively (automation of a costly manual process), not with a fabricated number. |
| Salesforce Health Cloud Native / AppExchange 150K+ orgs / 12 Salesforce certifications / Einstein AI (index, architecture) | Replace with the real GCP stack (§3). Salesforce may be named only as a CRM/distribution tool, not AI infra. Remove AppExchange/certification/Einstein claims entirely. |
| mobile-app demo: LCD L35391 + F11.10; PMID 38412847 "Milligan et al 2025"; "ASCO 2025 Guidelines"; ALJ-2025-TOX-089 | Remove all four. Reframe demo evidence to the approved synthetic pattern (LCD L38016 §3.2/§4.1; CO-197/CO-50; synthetic, no PHI). No PMIDs/ALJ numbers. |
| plg-sandbox: "847 payer-specific patterns," "1,247 LCD rules," "892 NCD policies," "89% L1 win rate vs 34% industry avg" | Replace counts with "**400+ LCD/NCD policies**" (§1). Remove the 89%/34% win-rate line. |
| dashboard: "Armstrong Toxicology Lab" as a LIVE customer with $47,280 MTD, 312 appeals, specific claim IDs | Keep the dashboard as a **product demo**, but label it unmistakably: "Demo environment · synthetic data · representative amounts · Ardia is pre-revenue." Remove "Live · All Systems Operational" as if a real customer. No real recovered-$ implied. |
| precision-medicine: "$537B by 2035 · 16.3% CAGR," "38.7% CAGR," "$8.8B→$180B by 2034," "$87B 2023," "CO-55 denials surged 2,600% 2018–2021" | Remove all unsourced market/percentage figures. Replace with approved benchmarks (2.76× JAMA; 23–31% XiFin; $70B AI-RCM Grand View). Drop the 2,600% surge. |
| case-studies: "Top 5 DFW Prospects" with named orgs + funding + "Est. Denial Volume $"; NCCN NSCLC v2.2025 "pages MS-5–MS-12"; unattributed "Lab Director"/"Medical Director" testimonials claiming results | Remove named third-party prospect funding/denial-$ figures from this public page. Remove fabricated NCCN page numbers. Remove result-claiming testimonials (Ardia is pre-revenue, no customers). Reframe as **illustrative synthetic scenarios** or point to `market-validation.html`. |
| vision: "$1T+ Silent Revenue Crisis" | Remove the $1T figure. Use the grounded ~$12B independent-lab TAM / $1.8B–$2.4B recoverable framing. |
| investors: "$118 manual vs $2.50" pairing; any 89%; 5-yr projections stated as fact | Keep $118 benchmark; remove $2.50. Keep projections only if clearly labelled "illustrative model, not a forecast." Remove any Ardia win rate. |
| research: "RareSense™ … 300M+ rare disease patients" | Remove the 300M stat. Either drop RareSense or mark it "aspirational future research direction — not a current product," no metrics. |

## 5. New pages to build (in the current site's design system)

Build these using the **existing** CSS classes (`.page-hero`, `.ph-tag`,
`.ph-title`, `.ph-sub`, `.sol-section`, `.sh`, `.st`, `.arch-layer`,
`.comp-table`, `.card`, etc.) cloned from a current page — **not** the
folder's Tailwind markup. Each must carry the standard nav, footer,
favicon, and a `.page-category-tag` per `coding-style.md`.

- **`tara-framework.html`** (category: Product & Platform, `#0ea5e9`) —
  the three TARA layers (§1), the zero-hallucination guarantees, and the
  "generic AI vs TARA" comparison. Content from `ardia-v2.html` TARA
  section, restyled.
- **`market-validation.html`** (category: Investors & Business, `#d946ef`)
  — the three-tier honest-validation page (Tier 1 sourced benchmarks; Tier
  2 discovery conversations 0/15 in progress; Tier 3 LOIs 0/3 pipeline).
  Content from folder `market-validation.html`, restyled. This is the
  flagship investor-credibility page.
- **`compliance.html`** (category: Clinical & Compliance, `#22c55e`) —
  SB 1188, TRAIGA, HIPAA, NIST AI RMF, CLIA/CAP, AKS/FCA, SOC 2 roadmap.
  Content from `docs/COMPLIANCE.md`, restyled. Complements existing
  `security.html`.

Wire all three into the footer nav (and the main nav where it fits), on
every page, consistently.

## 6. Investors page enhancement (additive)

Fold in grounded content from `INVESTOR_FAQ.md`: honest stage, unit
economics (labelled illustrative), use-of-funds allocation, honest risk
list, competition framing, "why invest pre-revenue." No fabricated metrics.
