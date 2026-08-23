# Cloud Credits Strategy — ARDIA Precision Health

**Programs held:** Google for Startups Cloud · NVIDIA Inception · AWS Activate (via Inception)
**Written:** August 2026 · **Horizon:** now → Phase 1A DFW pilot (Q4 2026) → Phase 2A (2027)
**Companion:** [`cloud-credits-runbook.md`](./cloud-credits-runbook.md) — the step-by-step claim/setup checklist
**Status:** internal planning doc — not web content (excluded in `.vercelignore`)

---

## 0. The thesis, in one paragraph

ARDIA is an **inference-and-data** company, not a **training-and-GPU** company. The
product reasons over denial files, payer policies and clinical notes and emits a cited
appeal — that is API calls, retrieval and rules, not model pre-training. So the three
programs are not three piles of the same currency: **Google Cloud is the production
platform** (because Vertex AI + Cloud Healthcare API are HIPAA-eligible under Google's
BAA, which is what actually unblocks touching a real lab's 835s), **AWS is the
second-home and managed-service pantry** (Bedrock under the AWS BAA, Comprehend Medical,
HealthLake — plus it is what a hospital IT department will ask for), and **NVIDIA
Inception is mostly not compute at all** — its value is the badge, the VC Alliance, DLI
training, and one specific GPU-shaped job worth doing (a self-hosted de-identification
model). The failure mode to avoid is architecting *to consume credits*.

---

## 1. Where ARDIA actually is today (ground truth from this repo)

Naming this honestly is what makes the rest of the plan real.

| Layer | Reality in the repo | Implication for credits |
|---|---|---|
| Marketing site | ~40 HTML pages, static, Vercel | Costs ~nothing. Not a credit consumer. Leave it on Vercel. |
| Model layer | `models/` — Meridian (PAMA math), Sentinel (de-id), Crucible (gates), Cadence. ~970 lines, 75 tests, zero deps | Real and tested. Deterministic — **no GPU, no cloud needed**. |
| Reasoning engine | `ardia-studio-app/server.py` → `call_model()` calls **Gemini or Anthropic direct APIs** by key | This is the single seam that must move to Vertex/Bedrock. See §5. |
| Public endpoint | `api/run.py` on Vercel serverless, explicitly **"SYNTHETIC-CASE DEMO — do not send real PHI"** | Correct today. Needs a BAA-covered sibling before pilot. |
| Payer-rules KB | Marked *planned / in build* on `architecture.html` | **This is where credits should go.** It is the moat and it is unbuilt. |
| Customers | Pre-revenue. DFW design-partner outreach active | Zero production load. You will underspend, not overspend. |

---

## 2. What each program is actually for

| | Google for Startups Cloud | AWS Activate (via Inception) | NVIDIA Inception |
|---|---|---|---|
| **Typical size** | Start ~$2K; Scale up to ~$200K/2yr; **AI-First up to ~$350K** (~$250K yr1 + ~$100K yr2), plus ~$10K ringfenced for **partner models in Model Garden** | $10K–$25K typical bootstrapped; up to ~$100K with funding + demonstrated NVIDIA usage; ~2-year expiry | No cash credits by default. Up to ~$100K DGX Cloud on request; ~$10K DLI training credits; ~30% DGX Cloud discount (gated behind ~4-node / ~$75K commit); GPU reseller discounts |
| **Role for ARDIA** | **Primary production platform.** Vertex AI (Gemini + Claude), Cloud Healthcare API/FHIR, BigQuery, Cloud Run, KMS, audit logging — all under one Google BAA | **Compliance-driven second home.** Bedrock (Claude under AWS BAA), Comprehend Medical, HealthLake. Plus: "we run on AWS too" closes hospital-IT objections | **Credibility + one bounded GPU job.** Inception badge, VC Alliance intros, GTC, DLI. NIM/NeMo for a self-hosted de-id model |
| **Do NOT use it for** | Multi-region scale-out before a paying lab | A duplicate parallel stack | Training a foundation model. You do not need one |
| **Verify first** | Which tier you were actually granted, and both expiry dates | 2-yr clock; **credits do not cover** Marketplace (except Bedrock 3rd-party models), Support above basic, Professional Services, Training/Cert, upfront RI/SP fees | Whether DGX Cloud credits were granted or merely offered on request |

> **Tier gotcha (check this week):** the AI-First tier generally requires that you have
> *not* already received more than ~$5K in Google Cloud credits. If you were onboarded on
> the Start/Scale tier, confirm with your Google startup contact whether you can still be
> upgraded before you burn the smaller pool. This is a one-way door worth a phone call.

---

## 3. The reframe: your problem is underspend, not overspend

Run the arithmetic. A pre-revenue RCM startup running a DFW pilot — call it a few
thousand claims a month, each a handful of model calls over a denial file plus retrieved
policy text — spends on the order of **$500–$2,000/month** on inference, plus a few
hundred on storage, logging and Cloud Run. Over 24 months that is **~$30–60K against a
possible ~$350K + ~$25K pool**. Roughly 85% of the grant expires unused if you only pay
for production.

So the question is not *"how do I stretch these credits"*. It is:

> **What would I build if compute were free — that I would never authorise if I were
> paying list price?**

Five answers, in priority order. These are the credit-funded projects.

### 3.1 A denial-corpus evaluation harness (highest value)
Nightly sweeps of *every* candidate configuration — model (Gemini 2.5 Pro / Flash /
Claude on Vertex) × prompt variant × retrieval strategy × chunk size — scored against a
labelled corpus of denials with known outcomes. Normally cost-prohibitive; with credits
it is free and can run every night.

**Why it is the moat:** anyone can call an LLM on a denial letter. Almost nobody has a
measured answer to *"which configuration wins CO-50 medical-necessity appeals for
Palmetto GBA tox claims, and at what first-pass resolution rate."* That number is the
company. It is also the number your roadmap already names as the Phase 1A success metric.
You already have the culture for this — 75 deterministic tests across `tests/` — this is
the same discipline extended to the stochastic layer.

### 3.2 The payer-rules knowledge base
`architecture.html` lists "400+ commercial payer policies, all 7 MAC LCD/NCD databases,
MolDX dossier requirements" as *planned*. Credits pay for the whole build: crawl and
snapshot the CMS/MAC coverage databases, chunk, embed, index in Vertex AI Vector Search,
warehouse in BigQuery, re-embed monthly as policies change. The embedding sweeps and
re-sweeps are exactly the kind of bursty cost that credits absorb painlessly.

**Licensing caveat — check before ingesting:** CMS LCD/NCD and MolDX material is public.
**AMA CPT descriptors, NCCN and CPIC content are licensed** and cannot simply be scraped
into a commercial product. Build the public-source corpus first; budget for the CPT
license and approach NCCN/CPIC deliberately. Getting this wrong is a legal problem, not a
technical one.

### 3.3 A large synthetic denial corpus
You cannot hold real PHI until a BAA and a design-partner lab are signed — and that is
the gating item for Q4 2026. Meanwhile, generate a large, realistic synthetic corpus:
X12 835/837 files, matching clinical notes, LCD-relevant documentation gaps, across the
CO-50/55/151/167 families you target. Credit-funded generation at scale, no PHI, no
waiting. It makes §3.1 possible *today* and de-risks the pilot before it starts.

Keep synthetic and real strictly separated in storage and in every metric you publish.

### 3.4 Self-hosted de-identification — the one job NVIDIA credits are for
`models/sentinel/deidentify.py` is admirably honest: regex handles the structured
Safe-Harbor identifiers, names come from a supplied roster, and free-text name detection
*"is intentionally not claimed here"*. That gap is the single weakest point in a HIPAA
story you will be asked about in every lab procurement conversation.

Fix it with a fine-tuned clinical NER model, self-hosted behind an NVIDIA NIM endpoint
inside your own VPC, so **raw PHI never leaves your perimeter before de-identification**.
This is genuinely GPU-shaped, genuinely bounded (hours of GPU, not weeks), and it is
exactly what Inception compute exists for. Benchmark it against **AWS Comprehend Medical
PHI detection** (HIPAA-eligible, AWS-credit-funded) as an independent second opinion.

Then publish the measured recall — in keeping with how `models/hipaa/controls.py` already
grades every control as `enforced` / `partial` / `policy` / `planned`. Upgrading Sentinel
from "best-effort" to a measured number is a compliance asset with a dollar value.

### 3.5 The compliance substrate
VPC Service Controls, CMEK via Cloud KMS, org-level audit log sinks, BigQuery log
retention, Access Transparency. These cost real money at steady state and are precisely
what a lab's compliance officer and your SOC 2 Type II auditor ask for. Credits make it
free to stand them up correctly on day one instead of retrofitting them at Series A.

---

## 4. Milestone-gated allocation

Credits should be released against pilot milestones, not calendar quarters. Rough shape
of a 24-month plan against the AI-First pool:

| Workstream | Share | Trigger to start spending |
|---|---|---|
| Eval harness + synthetic corpus (§3.1, §3.3) | ~30% | Now — nothing blocks it |
| Payer-rules KB: ingest, embed, refresh (§3.2) | ~25% | Now, public sources only |
| Production inference: pilot + expansion (§3.5 runtime) | ~20% | On first design-partner LOI |
| Compliance substrate + SOC 2 evidence (§3.5) | ~15% | Before first BAA is signed |
| De-id model training + hosting (§3.4) | ~10% (NVIDIA/AWS pools first) | Now — small and high-leverage |

**Hard rule:** no credit-funded workstream starts without a named pilot milestone it
de-risks. "We have the credits" is not a reason.

---

## 5. Architecture changes the credits should pay for

Three concrete moves, in dependency order.

**5.1 — Put a Vertex AI backend behind `call_model()`.**
`ardia-studio-app/server.py` reads `GEMINI_API_KEY` / `ANTHROPIC_API_KEY` and calls the
consumer APIs directly. Those direct calls are (a) not credit-funded and (b) not covered
by Google's BAA. Add a Vertex backend behind the existing `call_model` seam — the seam is
already the right shape, which is why this is a contained change rather than a rewrite.
Gemini via Vertex is credit-funded and BAA-covered; **Claude via Vertex Model Garden is
also BAA-covered**, and the AI tier's ringfenced partner-model allowance is designed for
exactly that. You keep your model choice, gain BAA coverage, and stop paying cash.

**5.2 — Move the PHI-capable engine off Vercel to Cloud Run.**
`api/run.py` is correctly scoped today as a synthetic-only demo endpoint. The pilot needs
a sibling that can accept real claim data, and that path must terminate inside a
HIPAA-eligible, BAA-covered project — Cloud Run + Cloud Healthcare API in `us-central1`,
which is what `architecture.html` already describes as the target. Keep Vercel for the
marketing site and the synthetic Studio demo; it is the right tool for that and costs
nothing. Do not let PHI touch it.

**5.3 — Keep the exit portable.**
Credits expire; after that you pay list. Protect yourself now, while it is cheap:
one provider interface (you have it), data in open formats (FHIR R4, Parquet in BigQuery
— both exportable), containers on Cloud Run (portable to ECS/Fargate), and no
provider-proprietary orchestration in the critical path. A Bedrock backend behind the
same `call_model` seam — built once for the AWS credits — doubles as your insurance
policy and your answer to *"do you run on AWS?"*.

---

## 6. What not to spend credits on

- **Training a foundation model.** You have no data advantage at pre-training scale and
  every month spent there is a month not spent on the DFW pilot.
- **A large GPU cluster.** Your workload is text reasoning against retrieved policy. The
  only justified GPU spend is §3.4.
- **Multi-region / multi-continent capacity** before a single paying lab. The 2028–2031
  EU/APAC roadmap is an investor narrative, not an infrastructure requirement in 2026.
- **Anything under the "quantum-ready" heading.** Zero credit spend. Not in 2026.
- **A parallel duplicate stack on AWS.** Use AWS for *bounded services* (Bedrock,
  Comprehend Medical, HealthLake sandbox), not a second copy of production. Running two
  clouds pre-revenue is the most reliable way to convert free credits into lost months.
- **Kubernetes.** Cloud Run until something actually forces the upgrade.

---

## 7. The traps

1. **Credits are not money.** They are a discount on a bill you would not otherwise
   incur. Spending $100K of credits on infrastructure that does not move first-pass
   resolution rate has cost you engineering months at zero return.
2. **Expiry is real and non-negotiable.** GCP splits across year 1 / year 2; AWS Activate
   runs ~2 years. Unused credits are not extended or reallocated. **Sequence activation:**
   do not switch on a pool until you can consume it against a milestone.
3. **Tier ordering** (see §2 gotcha) — confirm before burning a smaller pool.
4. **Lock-in by convenience.** The cheapest managed service today is the most expensive
   migration in 2028. §5.3 is the mitigation.
5. **A BAA is not automatic.** Google's BAA is signed at the org level and PHI-bearing
   projects must be flagged for regulated data; only HIPAA-eligible services are covered.
   AWS is the same shape. Signing up for credits does not sign a BAA — do that explicitly
   before any real claim data moves.
6. **Do not over-claim the affiliations.** Given the site's recent claim-accuracy passes
   (`fix(security): qualify clinical-guideline corpus as in development`), keep program
   membership stated exactly as it is: accepted into Google for Startups and NVIDIA
   Inception. Membership is not endorsement, certification, or a partnership, and each
   program has its own trademark-usage rules. The honesty posture is an asset — do not
   spend it here.

---

## 8. The benefits worth more than the credits

**Cloud Marketplace listings are a distribution channel, not a formality.** Hospital
systems and larger labs sit on committed cloud spend (GCP CUDs, AWS EDPs). A private
offer on Google Cloud Marketplace or AWS Marketplace lets a customer buy ARDIA **out of
budget they have already committed** — which routes around procurement in a way that a
15%-contingency pitch alone cannot. For an RCM startup selling into IT-conservative
buyers, this is plausibly worth more than the entire credit pool. Start the listing
process early; it takes longer than you expect.

**People.** Ask your Google startup manager for a **healthcare/life-sciences solutions
architect**, not a generalist — someone who has taken a Cloud Healthcare API + FHIR
deployment through a HIPAA review before. Ask AWS for the equivalent and about the ISV
Accelerate path.

**NVIDIA Inception's VC Alliance** is a warm channel to healthcare-AI investors, which is
directly relevant to the seed round you are raising. Treat that, GTC visibility and
co-marketing as the real deliverable of Inception — the compute is secondary.

**DLI training credits (~$10K)** are worth spending on whoever will own the de-id and
retrieval work.

---

## 9. The next 90 days (→ Q4 2026 pilot)

**Weeks 1–2 — administrative, do not skip**
- Confirm the exact GCP tier granted, both expiry dates, and whether an AI-First upgrade
  is still possible. Same for AWS Activate: amount and expiry.
- Sign the **Google Cloud BAA at org level**; create a separate PHI project flagged for
  regulated data. Nothing else here matters until this exists.
- Confirm whether DGX Cloud credits were granted or merely offered on request.

**Weeks 3–6 — make the engine credit-funded and BAA-covered**
- Vertex backend behind `call_model()` (§5.1); Claude via Model Garden on the partner
  allowance.
- Stand up the Cloud Run PHI-capable engine path (§5.2). Vercel keeps the site and the
  synthetic demo.
- Compliance substrate: CMEK, VPC-SC, audit sinks (§3.5).

**Weeks 5–10 — build the thing only credits make possible**
- Synthetic denial corpus (§3.3), then the eval harness (§3.1) running nightly.
- Public-source payer-rules KB ingest + embed (§3.2). CPT/NCCN/CPIC licensing raised with
  counsel in parallel.

**Weeks 8–12 — the compliance asset**
- Fine-tune + NIM-host the de-id NER model (§3.4); benchmark against Comprehend Medical;
  publish the measured recall into `models/hipaa/controls.py`'s honest grading.
- Begin both Marketplace listings (§8).

---

## 10. And the part the credits cannot buy

The credits are not what makes the product effective. **One DFW design-partner lab
handing you twelve months of historical 835s under a signed BAA** is. Everything above is
in service of being ready the week that happens — and nothing above substitutes for it.

Two disciplines matter more than any infrastructure decision here:

- **Narrow ruthlessly.** The site presents nine models, six phases, forty countries and a
  2032 quantum era. That is a legitimate investor narrative. The *product* for the next
  two quarters is one denial family — CO-50 medical necessity on toxicology claims in one
  MAC jurisdiction — won measurably. Your own Phase 1A definition already says this.
  Credits make it tempting to widen. Do not.
- **Measure the one number.** First-pass resolution rate on CO-50, baselined against what
  the lab achieves manually today. Publish it internally every week. A pre-revenue RCM
  company with a defensible, measured win rate on one denial family raises a seed round;
  one with a broad platform and no number does not.

---

## Sources

- [Google for Startups Cloud Program — AI tier](https://cloud.google.com/startup/ai)
- [Google for Startups Cloud Program: credits, AI tier, eligibility](https://guptadeepak.com/startup-offers/programs/google-for-startups-cloud)
- [NVIDIA Inception program guide (2026)](https://www.thundercompute.com/blog/nvidia-inception-program-guide)
- [NVIDIA Inception: credits & eligibility (2026)](https://radgrants.com/programs/nvidia-inception)
- [AWS Activate Terms & Conditions](https://aws.amazon.com/activate/terms)
- [Everything you need to know about AWS Activate Credits](https://aws.amazon.com/aws-startups/learn/everything-you-need-to-know-about-aws-activate-credits/)
- [HIPAA-eligible model providers in 2026](https://callsphere.ai/blog/vw1f-hipaa-eligible-model-providers-2026)
- [HIPAA-compliant AI in 2026: BAA vendors + safe architecture](https://verticomply.com/blog/hipaa-compliant-ai)

*Third-party summaries above are directional. Confirm every credit amount, tier rule and
expiry date in your own program console before planning against it.*

**Next:** the strategy behind these steps — why Google is the platform, why NVIDIA is
mostly not compute, and what to build with the headroom — is in
[`cloud-credits-strategy.md`](./cloud-credits-strategy.md).
