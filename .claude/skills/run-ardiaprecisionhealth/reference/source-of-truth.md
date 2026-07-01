# Source-of-truth reference for claims audits

This file is the grounding data the `claims-check` driver command (and any
agent doing a manual audit) cross-references site copy against. It was built
by extracting text directly from the company's own internal documents — not
from external fact-checking — so "verified" here means **"backed by one of
Ardia's own source documents,"** not independently fact-checked against
reality.

Source documents (paths relative to repo root):
- `Ardia_Health_White_Paper_Business_Plan.docx` — dated March 2026, cites a
  **$3.5M seed / $18M post-money SAFE**. Referred to below as **[WP]**.
- `Ardia_Health_Business_Plan_2026_v2.docx` — cites a **$500K–$750K seed**.
  Has named founders with contact info; reads as the more operationally
  current document. Referred to below as **[BP-v2]**.
- `Ardia_Investor_Outreach_Emails_2026.docx` — outreach templates. Referred
  to below as **[EMAIL]**.
- `Ardia_Health_White_Paper_Business_Plan (1).docx` — near-duplicate of
  [WP]; not separately reconciled.

**These documents disagree with each other on material facts.** Where they
agree, a site claim matching either is well-grounded. Where they conflict,
no page should silently pick one — the claims-check flags it and this file
records the conflict so the flag isn't repeated blind every run.

## ⚠️ Unresolved conflicts between source documents (founder decision needed)

| Fact | [WP] says | [BP-v2] / [EMAIL] says | Live site (as of 2026-07-01) |
|---|---|---|---|
| Cloud infrastructure | AWS US-East-1 | Google Cloud Platform (Vertex AI, Healthcare Data Engine, BigQuery, Cloud FHIR Store) [BP-v2] | GCP / Vertex AI |
| Seed raise size | $3.5M on $18M post-money SAFE | $500K–$750K seed round [BP-v2] | not consistently stated site-wide — check each page that cites a raise amount |
| Ram Vadlamudi's title | not named individually (CTO role listed as "seeking to hire") | Founder & Product Designer / Enterprise Architect; Manasa Jampani is Co-Founder & CEO [BP-v2] | "Ram Vadlamudi \| Founder & CEO" [EMAIL] |
| Appeal win rate | 89% (§2.2 core metrics), 83% (stat callout box), "50–80.7%" (§1.1 prose) — **[WP] is internally inconsistent** | 50–83% [BP-v2] | 89% |
| Cost per appeal (manual vs. AI-assisted) | $181 manual / $3.85 AI-assisted (47×) | not restated | $118 manual / $2.50 AI-assisted (47×) — ratio matches [WP], absolute dollars don't |
| LLM stack | "Claude Sonnet (Anthropic) and GPT-4o (OpenAI) in an ensemble" | "Anthropic Claude API" only, no OpenAI mention [BP-v2] | "Claude AI (Anthropic)" only |

**Do not resolve these by picking whichever number sounds better.** Surface
them in every claims-check run until a founder updates this file with the
authoritative figure — then update this table and the flag disappears.

## Facts both documents agree on (well-grounded — cite freely)

- Architecture name: **Neuro-Symbolic Sandwich Architecture** — a proprietary
  3-layer design (LLM reasoning "bread" / symbolic rules engine "filling" /
  ML outcome predictor "second bread"). Documented in both [WP] §2.2 and
  [BP-v2] §4.1. This is real, described company IP grounded in the
  published academic field of neuro-symbolic AI — **not a hallucination**,
  do not flag it as one.
- Four product modules: **ToxIQ™, MolecuIQ™, AcoIQ™, BehaviorIQ™** —
  documented identically in both docs (§6.1 [WP], §4.2 [BP-v2]).
- Symbolic rules engine: **847 LCD/NCD (/MolDX/DEX per [BP-v2]) rules**.
- Appeal brief generation: **under 90 seconds**.
- 15% success-fee business model, zero upfront cost.
- Company: Ardia Health(Labs LLC), Delaware entity, founded January 2026,
  headquartered Argyle, TX 76226 (Dallas-Fort Worth metro).
- $10–12B (BP-v2) / "~$12B" (site rounding) annual independent-lab revenue
  lost to denials — [WP] says "$10-12 billion", consistent.
- 65% of denied claims never appealed — consistent across [WP] and [BP-v2].
- 27% molecular diagnostics denial rate [WP §1.1] vs. 35.3% [BP-v2, cites
  XiFin 2024] — **these are different claims about different things**
  ([WP]'s 27% is described as the denial rate *within the independent lab
  sector specifically*; [BP-v2]'s 35.3% cites an external XiFin 2024
  benchmark). Site pages should make clear which stat and which source they
  mean, not blend them.
- 2.76× higher denial odds for independent vs. hospital labs — [BP-v2] cites
  *JAMA Network Open, April 2025, n=29,919*. Real, attributed citation.
- PAMA 2027 cuts up to 15%/year for 3 years (up to 45% cumulative by 2029).
- Texas SB 1188 (effective Sept 1, 2025) and TRAIGA/HB 149 (effective Jan 1,
  2026) — both real, named, dated Texas AI statutes described in detail in
  [WP] §1.4. Do not flag as fabricated law names.
- Founders: Ram Vadlamudi and Manasa Jampani, contact
  founders@ardiahealthlabs.com, ardiahealthlabs.com. [BP-v2] adds direct
  phone numbers (469) 679-3334 / (469) 499-6435 — treat phone numbers as
  sensitive; flag if displayed in plaintext on any *public* page.

## How to use this file in a claims-check

For each quantitative or technical claim found on a page:
1. **Matches a fact in "agree" list above, consistent phrasing** → verified,
   no flag.
2. **Matches a fact in "agree" list but numbers/phrasing drift from both
   source docs** (e.g. a third number that isn't in [WP] or [BP-v2] at all)
   → flag as **unverified — not found in either source document**.
3. **Touches a row in the "unresolved conflicts" table** → flag as
   **conflicting-source, needs founder resolution**, and reference the row.
4. **Names a technology, statistic, law, or module not present in either
   source doc and not general public knowledge** → flag as **unverified —
   possible fabrication**, highest priority for founder review.

Do not flag: the Neuro-Symbolic Sandwich Architecture name, the four IQ
module names, SB 1188/TRAIGA, or the core "$12B / 65% / 15% success fee"
narrative — these are confirmed, not hallucinated.
