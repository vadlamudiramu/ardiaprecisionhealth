# Ardia One — App Details & Architecture

*One elder-first hub for your care, your records, and your bills — every answer sourced, or it stays silent.*

**Status:** Working prototype is **live** at **`https://www.ardiahealthlabs.com/ardia-one-app`** (synthetic data). Sign in as **Eleanor** (the older adult) or **Maria** (caregiver / Guardian mode). Backend architecture below is the GCP build you fund next with your Google Cloud credits.

---

## 1. What it is (the one-line)

Ardia One unites a person's **clinical record + medications + appointments + surgeries + hospital visits + bills + insurance claims** in **one governed app** — for the older adult **and** the family member who coordinates for them. No competitor unifies **clinical + financial + claims** in one elder-first, governed surface. That white space is the product.

It runs on Ardia's existing compliance kernel — **Sentinel** (de-identifies before any AI reads a word), **Crucible** (8 safety gates on every answer), **HIPAA guard/audit** — and calls the existing `/api/run` engine unchanged. Governance is **structural, not bolted on.**

**Honesty is enforced in code:** synthetic/de-identified data only until a signed BAA, every dollar labelled "modelled," non-diagnostic, safety-first "call 911," and it never fabricates an answer when the engine is offline ("engine offline" is shown honestly).

## 2. Who it's for

| Persona | What they need |
|---|---|
| **Eleanor, 80** — the older adult (owner) | COPD + heart failure + diabetes, 6+ meds, ~11 doctors/yr. One plain-language "what do I do today?", voice-first, and to know a bill or symptom is being watched — without menus. |
| **Maria, 52** — caregiver daughter | One of 59M unpaid caregivers. A shared, consent-scoped view, fall/deterioration alerts, one-tap help fighting a wrong bill. The second buyer and daily power user. |
| **James, 60** — legal proxy (POA) | Acts on his father's behalf under state-law authority — capacity-aware, fully audit-logged. |
| **Dr. Chen** — receiving clinician | A clean, de-identified hand-off of the whole-person picture instead of fragmented calls across 4+ practices. |
| **Seed investor** | A large fundable wedge with a reimbursement/outcomes story and a defensible governance moat — sourced numbers, honest "modelled" labels. |

## 3. The 9 modules

1. **Today / Home** — one plain-language snapshot: meds due, next appointment, a flagged bill, a wellbeing signal. One decision per screen. *(Aria + Cadence)*
2. **Ask Ardia (voice companion)** — the front door; de-identified before the model, safety spine (FAST stroke / C-SSRS crisis → 911), cite-or-abstain, Sentinel/Crucible/source badges shown. *(Aria on TARA)*
3. **Medications** — one reconciled list across all providers, daily pill card, taken/missed the caregiver sees, cross-drug interaction safety, "why am I on this." *(Aria + TARA)*
4. **Appointments & Procedures** — cross-provider calendar, visit prep, pre-/post-op guidance, recovery check-ins. *(Aria + TARA)*
5. **Records & Results** — aggregate the record and **explain** it: paste a lab report → in-browser de-id → reference-range pills (normal/low/high/critical) + urgent banner. *(Lumen + Sentinel)*
6. **Vitals & Devices** — wearables/home devices → trends → **early-warning signals** (weight + SpO₂ + activity), honestly framed as decision support. *(Cadence + PulmoIQ)*
7. **Billing & Claims Guardian** ⭐ — reads every bill/EOB/claim, flags errors/denials, explains in plain language, drafts appeals. **The differentiator.** *(TARA + Meridian + Sentinel)*
8. **Insurance & Coverage** — "is it covered, what will I owe?" *before* care: coverage checks that cite a real CMS policy or abstain, prior-auth, OOP-max ledger. *(TARA + Meridian)*
9. **Care Team & Family (Guardian mode)** — provider/caregiver directory + the consent graph controlling who sees what; tiered, revocable, audit-logged; auto-escalation on SOS/low-SpO₂/fall. *(Sentinel + Aria)*

**Condition packs on one timeline** (69% of Medicare beneficiaries have 2+ conditions): Elder Core (default) · Pulmonary (COPD/asthma) · Cardiometabolic (HF/diabetes/HTN) · Post-discharge/Transitions · Cognitive-support (MCI-aware).

## 4. ⭐ Claims Guardian — the wedge

**~49–80% of medical bills contain errors; about half of first-level Medicare appeals succeed — yet most people never file.** Guardian is deliberately **rules-first, AI-last** so every flag is deterministic, explainable, auditable — and stays inside the administrative safe harbor (21st Century Cures §520(o)(1)).

- **Layer 0 — Intake & de-id:** parse 837/835 EDI or OCR a photographed bill/EOB → normalized line items; Sentinel de-identifies; RBAC-gated, every access audit-logged.
- **Layer 1 — Deterministic rules (no AI, 100% explainable):** duplicate detection, EOB↔bill reconciliation, cost-share recompute + running OOP-max ledger (Meridian), timely-filing math, No Surprises Act guard, Good-Faith-Estimate $400 overage.
- **Layer 2 — Symbolic code-intelligence:** CARC/RARC interpreter (each code → plain meaning + appealability), NCCI unbundling/modifier edits, CPT↔ICD compatibility, price benchmark vs published fee schedules.
- **Layer 3 — Governed AI (after de-id) does only 3 narrow things:** plain-language explanation, appeal/dispute letter drafting citing the specific line + code + rule, and ambiguous-case question routing — under cite-or-abstain, non-diagnostic, administrative gates. **AI never decides a charge is wrong; the rules flag, AI explains and drafts.**

The elder sees only **three states**: 🔴 *Likely a billing error* · 🟡 *Worth checking* · 🟢 *Looks correct.* One-tap actions: Dispute · Appeal (with deadline tracker) · Price-check · Ask care team · "This bill may be illegal" (NSA) · Report fraud. Every dollar "modelled from published fee schedules"; every draft "review before sending." Ardia never sends anything for you.

## 5. GCP architecture (what you build with your credits)

| Layer | Services | Role |
|---|---|---|
| **Client** | Web (Next.js/React) · Mobile (Flutter/React Native) · Firebase Auth SDK + App Check | Elder-first UX; **no PHI in identity attributes**; TLS 1.3. |
| **Identity** | Identity Platform (GCIP/Firebase Auth) · MFA · multi-tenant | AuthN + short session TTL. Guardian/caregiver access is a **consent + relationship graph** (Firestore/Postgres), enforced server-side — never in IdP tokens. |
| **Edge** | Cloud Load Balancing + Cloud Armor (WAF) · Cloud Run · Apigee | App backend on Cloud Run (scales to zero). Apigee for PHI-bearing partner/payer/EHR FHIR APIs. |
| **Services** | Cloud Run (FastAPI microservices) · Pub/Sub · Eventarc · Cloud Tasks · **existing `/api/run` → call_model** | Business logic + the governed AI choke point (Sentinel→ground→model→Crucible), unchanged. PHI-free audit event per action. |
| **Data** | **Cloud Healthcare API — FHIR R4 store** (+HL7v2, DICOM) · Cloud Storage + CMEK · Firestore/Cloud SQL/AlloyDB (consent graph, dues/claims ledger) · Healthcare de-id + Cloud DLP · BigQuery + BQ ML · Dataflow | Clinical data as FHIR R4; files in CMEK buckets; ops/consent in Postgres; analytics + overcharge scoring in BigQuery. No PHI in IDs/object/table names. |
| **AI** | Vertex AI — **Gemini** · **MedGemma/MedSigLIP** on your own endpoint · Vector Search/RAG (payer policies, CARC/RARC, fee schedules) · Agent Engine (Claims Guardian) · Document AI (EOB/bill extraction) · Speech-to-Text (logging **off**) · BQ ML | All PHI-adjacent inference in-project under your IAM/region on **Vertex** (BAA-covered). Sentinel de-id runs before the prompt. Human-in-the-loop: AI drafts, guardian approves. |
| **Governance** | **Assured Workloads** — US Data Boundary for Healthcare & Life Sciences (HIPAA+HITRUST, US residency, CMEK+TLS enforced, free tier) · VPC Service Controls · Cloud KMS (CMEK) · Cloud Audit Logs (Data Access on) · Access Transparency · Secret Manager · least-privilege IAM · Org Policy | Wraps every layer: US-only residency, CMEK on every PHI store, an exfiltration perimeter, an immutable who/what/when/which-patient trail (6-yr retention), gated Google-staff access. |

**Data flow — "upload an EOB → Guardian flags a wrongful charge":** MFA sign-in + App Check → server re-verifies the guardian↔patient link against the consent graph → signed-URL upload to a **CMEK** bucket inside the **VPC-SC** perimeter → Eventarc → Cloud Run ingestion → **Document AI/Gemini** extracts payer, CPT/HCPCS, billed vs allowed vs patient-responsibility, CARC/RARC → normalized to **FHIR EOB/Claim/Coverage** → Guardian runs **rules-first → BQ-ML overcharge score → Vertex RAG agent** (grounded on the member's plan doc + CARC/RARC + CMS LCDs) → drafts an appeal → guardian approves → **every step emits a Cloud Audit Log entry, in-perimeter, CMEK.**

### ⚠️ Do-not-use (not HIPAA-eligible — build-time guardrails)
- **Consumer Gemini / AI Studio / `generativelanguage` API** — not BAA-covered; use **Vertex AI** for anything PHI-adjacent.
- **MedLM** retired (Sept 2025) → use **MedGemma** on your own Vertex endpoint. **Healthcare NL API** deprecated → use Gemini on Vertex. **Healthcare Data Engine** deprecated (gone Jul 2026) → Cloud Healthcare API + Dataflow + BigQuery.
- **Speech-to-Text data-logging opt-in voids BAA coverage** — keep it **off**.
- Firebase Analytics/Crashlytics — keep PHI out; use Firestore (covered) for PHI.
- Anything **Preview/Experimental** — not covered until GA. **API Gateway** — confirm on the live covered list (Apigee is confirmed).
- **Sign the Google Cloud BAA before any PHI touches the project**, and a BAA with every vendor touching PHI. Re-verify each service against the live covered-services list.

## 6. HIPAA controls (highlights)

- **BAA / default-deny until covered** — `has_baa` false ⇒ synthetic/de-identified path only, enforced in code.
- **Audit every PHI access** (§164.312(b)) — Data-Access logs + PHI-free app-layer events (action, model, de-id counts, hash of already-de-identified text; 64-char cap) → append-only/WORM, 6-yr retention.
- **TLS 1.3** in transit; **CMEK** at rest on every PHI store; **VPC-SC** exfiltration perimeter.
- **Safe-Harbor de-id** (§164.514(b)(2)) — Sentinel removes the 18 identifiers in-process before any prompt; Cloud DLP/Healthcare de-id as the managed second pass on stored FHIR/DICOM.
- **RBAC · minimum-necessary · MFA · auto-logoff**; input hard-capped; break-glass logged.
- **Fail-closed:** a failed Crucible gate blocks output; a failing audit sink never opens the gate.

**Voice:** a transcript is PHI the instant it exists, and audio can't be redacted — so raw audio never reaches a non-BAA model. Consent **before** capture (elder/guardian consent where capacity is lacking) → STT with **logging off** inside VPC-SC → transcript encrypted (CMEK) → **de-id before any model** (same choke point as text) → deterministic FAST/C-SSRS safety screens → audit every step. Voice is offered as co-equal input, **never required.**

## 7. Roadmap

| Phase | Scope |
|---|---|
| **0 — Shell + honest skeleton** (wk 0–4) | The elder app shell + 9 module frames; lift Lumen (Records) and the Aria FAST/C-SSRS→911 spine. Synthetic data, honesty labels live. **← the live prototype is here.** |
| **1 — Live governed engine, still synthetic** (wk 4–10) | Point Ask Ardia / Records / Coverage at the existing `/api/run`; ship Meds reconciliation + Vitals. Funded by the $300 trial / $2k Start credits (managed Gemini, no GPU). |
| **2 — Claims Guardian MVP** (wk 8–16) | Document AI → FHIR EOB/Claim → Layer-1 rules + Meridian ledger → CARC/RARC + NCCI packs → governed drafting. Traffic-light findings + one-tap actions + deadline tracker. Synthetic bills only. |
| **3 — HIPAA-eligible cloud + BAA** (mo 4–8) | Sign the BAA; Assured Workloads + VPC-SC + CMEK + Data-Access logs + Identity Platform MFA (retire the demo access-code). Flip `has_baa`; limited real-PHI pilot. |
| **4 — Condition packs + caregiver scale** (mo 8–14) | Pulmonary/Cardiometabolic/Post-discharge/Cognitive packs; full Guardian-mode dashboards; device ingestion at scale; BQ-ML overcharge scoring; de-identified clinician hand-off. |
| **5 — Interop + regulatory** (mo 12+) | 1up/Apple-Health FHIR pipes; Apigee payer/EHR proxy; 510(k) exploration for any respiratory/deterioration signal moving from decision-support to a cleared claim; formal SRA + HITRUST review. |

## 8. Why it's fundable

An 80-year-old with COPD, HF and diabetes sees ~11 physicians across 4+ practices a year, forgets half her meds, and is one fall from an ~$18,600 hospital stay — while her daughter (one of **59M** unpaid caregivers doing **$1T/yr** of labor) coordinates it all by phone and sticky note. No one owns the whole picture, and no one fights the wrong bills. Adherence, fall detection, and denial recovery each map to real payer cost pools ($80B/yr falls · ~$2B polypharmacy waste · 22.6% COPD 30-day readmissions) — a **reimbursement-and-outcomes** story, not a gadget. We sit inside a **$503B→$938B** long-term-care market and a ~**$169B** home-care market growing ~10%/yr, inside a ~**$9T** longevity economy that still draws **under 2%** of venture dollars. The moat is structural governance (Sentinel de-id + TARA cite-or-abstain + Crucible gate) — the *trustworthy* one.

*Honesty notes: market figures cited as ranges where analysts differ; RPM/fall-detection framed as decision support (cohort evidence strong, largest RCTs mixed) — we do not claim guaranteed readmission reduction.*

## 9. What we will NOT do

- **No diagnosis, no dosing.** Ardia informs, explains, drafts, and escalates — clinicians and payers decide.
- **No fabricated answers.** Cite a source or abstain; "engine offline" is shown honestly.
- **No real PHI before a signed BAA.** Synthetic/de-identified only, enforced in code.
- **No claim that a charge is "wrong."** Rules flag *possible* errors; the person and their care team decide. Not legal, tax, or medical advice.
- **No PHI to a non-BAA model, no PHI in logs/URLs/prompts, no data-logging on voice.**

---
*Ardia Precision Health, Inc. · Delaware C-Corp · Dallas–Fort Worth · Pre-revenue. This document describes a prototype and a build plan, not a shipped regulated product.*
