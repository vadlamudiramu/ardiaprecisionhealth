# Cloud Credits Runbook — step by step, per program

Companion to [`cloud-credits-strategy.md`](./cloud-credits-strategy.md) (the *why*). This is the *how* — an
ordered checklist with the console paths, commands, and known friction points.

**Do them in this order.** Google first (it is your production platform and its BAA
gates everything else), NVIDIA second (it is the gateway to the AWS offer), AWS third.

> Every credit amount, tier rule and expiry below must be confirmed in your own program
> console. Third-party figures drift.

---

# PROGRAM 1 — Google for Startups Cloud

**Goal:** credits landed on the right billing account, a BAA signed, a PHI-isolated
project that Vertex and Cloud Run run inside, and budget alarms so nothing silently drains.

## Phase A — Claim and verify (days 1–3)

### A1. Find the billing account the credits landed on
Credits are deposited into **the exact billing account ID submitted on the application**,
and it is not always the one you use day to day.

```bash
gcloud auth login
gcloud billing accounts list          # 18-char ID, format ABC123-DEF456-GHI789
```
Console: **Billing → Overview → Credits**. Confirm the balance, and note the **expiry
date on each credit tranche** — AI-tier grants are typically split year 1 / year 2 with
separate expiries.

**Done when:** you have written down the billing account ID, the credited amount, and
both expiry dates.

### A2. Confirm which tier you were actually granted
The tiers are materially different (Start ~$2K · Scale up to ~$200K/2yr · AI-First up to
~$350K). The AI-First tier generally requires that you have **not already received more
than ~$5K in Google Cloud credits**.

Email your Google for Startups contact and ask, verbatim:
> *"Which tier is our grant on, what is the credited amount per year with expiry dates,
> and if we are not on the AI-First tier, what would we need to qualify for an upgrade?
> We are an AI-first healthcare startup building on Vertex AI."*

**Do not spend anything until this is answered.** Burning a small tier can foreclose the
large one. This is the single highest-value email in the runbook.

### A3. Ask about the Model Garden partner-model allowance
The AI tier typically ringfences an extra amount (~$10K) usable **only on partner models
in Model Garden** — which is how you get Claude paid for. Ask whether it is included and
whether it is already on the billing account or must be requested.

## Phase B — Make it HIPAA-capable (days 3–10)

### B1. Set up an organization, not a bare project
BAAs and org policies attach at the **organization** level. If you are currently on a
personal Gmail-owned project, create a Cloud Identity / Workspace org for
`ardiahealthlabs.com` first and migrate the billing account under it. Retrofitting this
after you hold PHI is painful.

### B2. Sign the BAA
As **Organization Administrator**, in the Google Cloud Console, go to the account's legal
/ compliance agreements section and accept the **HIPAA Business Associate Agreement**
electronically (an electronic acceptance is as binding as a signed paper one). If the
agreement is not offered self-service on your account, ask your Google startup contact or
Cloud sales to enable it — do not proceed without it.

Then: file the executed BAA in your compliance repository, and record it in
`models/hipaa/controls.py` so the posture map reflects reality.

**Critical:** the BAA covers only **HIPAA-eligible services**, and only in projects you
have designated for regulated data. Signing it does not make every API PHI-safe.

### B3. Create the project split
Three projects, one boundary that matters:

```bash
ORG=<your-org-id>; BILLING=<ABC123-DEF456-GHI789>

gcloud projects create ardia-phi-prod  --organization=$ORG   # PHI lives here. Nothing else does.
gcloud projects create ardia-dev       --organization=$ORG   # synthetic data only, never PHI
gcloud projects create ardia-research  --organization=$ORG   # eval harness, embeddings, corpus builds

for p in ardia-phi-prod ardia-dev ardia-research; do
  gcloud billing projects link $p --billing-account=$BILLING
done
```

Flag `ardia-phi-prod` for regulated data per the BAA's instructions, and keep the rule
absolute: **synthetic data never moves into the PHI project, real data never leaves it.**

### B4. Enable only what you need
```bash
gcloud services enable --project=ardia-phi-prod \
  aiplatform.googleapis.com healthcare.googleapis.com run.googleapis.com \
  cloudkms.googleapis.com secretmanager.googleapis.com logging.googleapis.com

gcloud services enable --project=ardia-research \
  aiplatform.googleapis.com bigquery.googleapis.com storage.googleapis.com
```

### B5. Compliance substrate (do it now, while it is free)
- **CMEK** — a Cloud KMS key ring in `us-central1`; point Healthcare API, GCS and BigQuery at it.
- **VPC Service Controls** — a perimeter around `ardia-phi-prod` so data cannot be
  exfiltrated to another project by a misconfigured job.
- **Audit log sink** — org-level Data Access logs → a locked BigQuery dataset with
  retention. This is your HIPAA §164.312(b) evidence and your SOC 2 evidence.
- **Least privilege** — no `roles/owner` on the PHI project for anyone; service accounts
  per workload.

### B6. Budget alarms — before the first API call
Credits mask overspend until they run out, then the card gets charged. Set alerts now:

Console: **Billing → Budgets & alerts → Create budget** — one per project, thresholds at
50 / 90 / 100%, with email to the founders. Cap `ardia-research` deliberately (e.g.
$2,000/month) so a runaway embedding loop cannot eat a year of credit overnight.

## Phase C — Spend it (weeks 2–12)

### C1. Move the model call onto Vertex
This is the change that makes inference both credit-funded and BAA-covered.

`ardia-studio-app/server.py` already routes every call through `call_model()` — add a
Vertex backend behind that seam rather than rewriting anything.

```bash
pip install "anthropic[vertex]" google-genai
gcloud auth application-default login          # Vertex uses ADC, not an API key
```

```python
# Claude via Vertex Model Garden (enable the Anthropic models in Model Garden first).
# Model IDs on Vertex are the bare first-party IDs — no prefix.
from anthropic import AnthropicVertex

client = AnthropicVertex(project_id="ardia-phi-prod", region="us-central1")
resp = client.messages.create(
    model="claude-opus-5",
    max_tokens=16000,
    system=GUARDRAIL,
    messages=[{"role": "user", "content": deidentified_case}],
)
```

**Repo-specific constraint — this is why the split matters.** `api/run.py` is deliberately
stdlib-only ("Deps are pure stdlib + the repo's own `models/`") because Vercel's Python
builder would otherwise have to install packages. You cannot add the Anthropic SDK there.
So: **Vercel keeps the zero-dep synthetic demo unchanged; the Vertex/SDK path lives in the
Cloud Run service**, which is a container and can have whatever dependencies it needs.

### C2. Stand up the Cloud Run PHI service
```bash
gcloud run deploy ardia-engine \
  --project=ardia-phi-prod --region=us-central1 \
  --source . --no-allow-unauthenticated \
  --service-account=ardia-engine@ardia-phi-prod.iam.gserviceaccount.com \
  --set-env-vars=ARDIA_ALLOWED_ORIGIN=https://www.ardiahealthlabs.com
```
`--no-allow-unauthenticated` is not optional for a PHI endpoint. Keep the existing
`Sentinel de-identify → grounding → model → Crucible gates` pipeline exactly as-is; only
the hosting and the provider client change.

### C3. Build the corpus and the eval harness (`ardia-research`)
1. Ingest public CMS/MAC LCD/NCD + MolDX sources → GCS → BigQuery.
2. Chunk + embed via Vertex → Vector Search index. Re-embed monthly.
3. Generate the synthetic denial corpus (835/837 + notes) — synthetic only, no PHI.
4. Nightly eval sweep: model × prompt × retrieval config, scored on first-pass
   resolution against the labelled corpus. Results to BigQuery, one dashboard.

**Licensing gate before step 1:** CMS/MAC/MolDX is public. **AMA CPT descriptors, NCCN
and CPIC are licensed** — do not ingest them into a commercial product without a licence.
Raise this with counsel in the same week you start.

## Google — gotchas

| Gotcha | What to do |
|---|---|
| Credits went to the wrong billing account | Fix before spending — you cannot move a balance later |
| Spending in a project not linked to the credited billing account | Bills your card at list price while credits sit unused. Check monthly |
| BAA signed but PHI in a non-covered service | Only HIPAA-eligible services are covered. Check the covered-services list per service |
| Year-1 tranche expires with a balance | Unused credits are not extended. Track burn against expiry from month 3 |
| Free-tier `aistudio.google.com` keys | Not covered by the BAA and not credit-funded. Fine for the synthetic demo, never for PHI |

---

# PROGRAM 2 — NVIDIA Inception

**Goal:** portal profile complete, the AWS Activate offer claimed correctly (this is the
gateway — see Program 3), DLI credits allocated, and one bounded GPU workload running.

## Phase A — Portal setup (days 1–5)

### A1. Complete the profile properly
Log into the Inception portal and fill the company/product profile in **full** — benefit
eligibility and partner-manager attention are both driven by it. Describe ARDIA as
healthcare AI doing clinical reasoning and de-identification, not as "RCM software";
the former routes you to the AI benefits.

### A2. Pin down your partner manager
Approval usually comes with an assigned partner manager. Get a call. Ask directly:
> *"Which benefits are actually provisioned on our account today — AWS Activate offer,
> DGX Cloud credits, DLI credits, VC Alliance access? For each, what is the claim path
> and the expiry?"*

Written answers. **"Up to $100K DGX Cloud" is an eligibility ceiling you request against,
not a balance you hold** — this is the most common misunderstanding of the program.

### A3. Claim the benefits
Portal → **benefits request tab**:
- **AWS Activate offer** → see Program 3. Claim this first; it has the longest lead time.
- **DLI training credits** (~$10K) → allocate to whoever will own de-identification and
  retrieval. Relevant courses: clinical NLP / NER, RAG, model deployment with NIM.
- **DGX Cloud credits** → request only when you have a defined job (C1 below). Requesting
  early starts a clock against nothing.
- **VC Alliance** → you are raising a seed round. This is the benefit with the highest
  expected value in the whole program. Ask for intros to healthcare-AI investors by name.

## Phase B — Positioning (ongoing)

### B1. State membership accurately on the site
Membership in Inception is **not** endorsement, certification, or partnership, and NVIDIA
has trademark-usage rules for members. Given the claim-accuracy passes already in this
repo's history, keep any site copy to a plain factual statement of membership. Read the
program's brand guidelines before adding a logo anywhere.

## Phase C — Spend it (weeks 4–12)

### C1. The one job worth GPUs: self-hosted de-identification
`models/sentinel/deidentify.py` states plainly that free-text name detection *"is
intentionally not claimed here."* Closing that is the highest-value GPU work you have.

1. Fine-tune a clinical NER model for PHI spans on public de-id corpora (i2b2/n2c2-style
   annotated notes — check the data-use agreement for each).
2. Package it behind an **NVIDIA NIM** endpoint deployed **inside your own VPC**, so raw
   text is de-identified before it ever crosses a network boundary to any model provider.
3. Benchmark against **AWS Comprehend Medical** PHI detection (Program 3) as an
   independent second opinion — two methods disagreeing is a finding, not a failure.
4. Publish the measured precision/recall into `models/hipaa/controls.py`, and upgrade the
   Sentinel control's status honestly. Add tests in `tests/test_sentinel.py`.

Bounded: hours of GPU, not weeks. Deliverable is a compliance asset with a dollar value in
every lab procurement conversation.

### C2. Do not
Train a foundation model. Stand up a persistent GPU cluster. Take the 30% DGX Cloud
discount — it is gated behind a ~4-node / ~$75K commitment and is aimed at funded teams
with sustained training loads. That is not you in 2026.

## NVIDIA — gotchas

| Gotcha | What to do |
|---|---|
| "Up to $100K" read as a balance | It is a request ceiling. Confirm what is provisioned in writing |
| Email mismatch breaks the AWS claim | Your AWS Builder ID / account email must match the Inception registration email exactly |
| Benefits sit unclaimed | They are opt-in via the portal's benefits tab. Nothing arrives automatically |
| Silence after a request | Members report multi-month delays on the AWS Activate path. Chase your partner manager weekly and keep a written trail |

---

# PROGRAM 3 — AWS Activate (via NVIDIA Inception)

**Goal:** credits applied to an AWS account, the BAA accepted org-wide, and AWS used for
three bounded jobs — not a second copy of production.

## Phase A — Claim (days 5–20, longest lead time)

### A1. Get the offer from the Inception portal
The Activate offer for Inception members is claimed through your Inception portal, not by
applying to Activate directly. You will need an **Organization ID** issued for the
Inception→AWS path — this is the step that most often stalls.

### A2. Match the email exactly
The email on your AWS Builder ID / AWS account **must be the same official business email
used for the Inception registration**. A mismatch is the single most common cause of
rejection and of the multi-month delays members report in the NVIDIA forums.

### A3. If it stalls
Members have reported four-month waits on the Org-ID / tier-mapping question. Escalate
through your **Inception partner manager**, not AWS support — AWS cannot resolve an
Inception-side mapping. Keep a dated written trail and re-send weekly. Meanwhile, nothing
on the Google track is blocked by this — carry on.

### A4. Verify the credits landed
Console: **Billing and Cost Management → Credits**. Record amount and expiry (Activate is
typically ~2 years). Note what credits **do not** cover: Marketplace (except third-party
foundation models on Bedrock), Support above basic, Professional Services, Training &
Certification, Route 53 domain registration, and upfront Reserved Instance / Savings Plan
fees.

## Phase B — HIPAA setup (days 20–25)

### B1. Accept the BAA — it is self-service
1. Set up **AWS Organizations** with a management account (do this first — it lets one
   acceptance cover every account).
2. From the management account, open **AWS Artifact → Agreements → AWS Business Associate
   Addendum**.
3. Review, confirm your legal entity details, accept **on behalf of the organization** —
   this designates all existing and future member accounts as HIPAA Accounts.
4. Download the executed agreement and file it with the Google BAA.

```bash
aws organizations describe-organization        # confirm the org exists
aws organizations list-accounts
```

### B2. Restrict PHI to HIPAA-eligible services
Only process PHI in services named in the BAA. Bedrock, Bedrock AgentCore, Comprehend
Medical, Transcribe Medical, HealthLake, S3, KMS are in scope; verify anything else
against the HIPAA Eligible Services Reference before it touches PHI.

### B3. Budget alarms
**Billing → Budgets → Create budget**, alerts at 50/90/100%. Same reasoning as Google:
credits hide overspend right up until they don't.

## Phase C — Spend it (weeks 6–16) — three bounded jobs only

### C1. Comprehend Medical as the de-id benchmark
The independent second opinion for §C1 of Program 2. HIPAA-eligible, credit-funded,
purpose-built for PHI detection in clinical text. Run it over the same held-out set as
your NIM model and compare. Cheap, fast, and it produces a number you can show a
compliance officer.

### C2. Bedrock as the portability proof
Add a Bedrock backend behind the same `call_model()` seam. Two payoffs: an honest
"yes, we run on AWS" in procurement, and a real exit path if GCP pricing turns after the
credits expire.

```bash
pip install "anthropic[bedrock]"
```
```python
# Bedrock model IDs take an "anthropic." prefix; Vertex IDs do not. Same seam, one adapter.
from anthropic import AnthropicBedrockMantle

client = AnthropicBedrockMantle(aws_region="us-east-1")
resp = client.messages.create(
    model="anthropic.claude-opus-5",
    max_tokens=16000,
    system=GUARDRAIL,
    messages=[{"role": "user", "content": deidentified_case}],
)
```

### C3. HealthLake as the FHIR sandbox
A managed FHIR R4 store to develop the SMART-on-FHIR ingestion path against without
building a FHIR server. Synthetic data only until a design partner signs.

### C4. Do not
Duplicate the production stack. Run EKS. Move the primary data store. AWS is a pantry of
three services and a portability hedge — nothing more until a customer demands otherwise.

## AWS — gotchas

| Gotcha | What to do |
|---|---|
| Applying to Activate directly | Breaks the Inception attribution. Claim through the Inception portal |
| Email mismatch | Same email on Inception and AWS Builder ID. Verify before submitting |
| BAA accepted on a member account only | Accept from the **management** account to cover the whole org |
| Credits applied to the wrong account | Check **Billing → Credits** in the account you actually build in |
| Expiry passes quietly | ~2 years, no extension, no reallocation. Diary the date |

---

# Cross-program: the first 30 days, in order

| Day | Action | Blocks |
|---|---|---|
| 1 | `gcloud billing accounts list`; record credited amount + both expiry dates | everything |
| 1 | Email Google contact: which tier, can we upgrade to AI-First, is the Model Garden allowance included | all GCP spend |
| 2 | Complete the NVIDIA Inception portal profile in full | AWS claim |
| 2 | Request the AWS Activate offer via the Inception portal (longest lead time — start now) | Program 3 |
| 3 | Book the Inception partner-manager call; get benefits confirmed in writing | — |
| 4 | Create the Cloud org (if not already); accept the **Google BAA** | all PHI work |
| 5 | Create `ardia-phi-prod` / `ardia-dev` / `ardia-research`; link billing; enable APIs | — |
| 6 | Budget alerts on every project, both clouds | — |
| 7 | KMS + VPC-SC + audit log sink on `ardia-phi-prod` | first PHI |
| 8–12 | Vertex backend behind `call_model()`; enable Claude in Model Garden | — |
| 10–14 | Cloud Run `ardia-engine` deployed, authenticated-only | pilot |
| 12 | Raise CPT / NCCN / CPIC licensing with counsel | corpus |
| 14–20 | Synthetic denial corpus, then the nightly eval harness | the metric |
| 20–25 | AWS Organizations + **AWS BAA** via Artifact | AWS PHI work |
| 25–30 | Start both Marketplace listings (GCP + AWS) — long lead time | distribution |

**The gate on everything:** two signed BAAs and one DFW design-partner lab. Steps that
depend on neither should run in parallel starting today; steps that depend on either
should not start until it is signed.

---

## Sources

- [Google for Startups Cloud Program — apply](https://cloud.google.com/startup/apply) · [account setup for startups](https://cloud.google.com/startup/onboarding) · [AI tier](https://cloud.google.com/startup/ai)
- [Google Cloud HIPAA compliance](https://cloud.google.com/security/compliance/hipaa-compliance) · [establishing a BAA with Google](https://www.totalhipaa.com/how-to-get-a-baa-with-google/) · [GCP BAA, covered services & configuration](https://www.accountablehq.com/post/is-google-cloud-hipaa-compliant-a-practical-guide-to-the-baa-covered-services-and-configuration)
- [NVIDIA Inception program guide (2026)](https://www.thundercompute.com/blog/nvidia-inception-program-guide) · [application walkthrough](https://klymentiev.com/blog/nvidia-inception-program) · [NVIDIA × AWS Activate for startups](https://aws.amazon.com/blogs/startups/accelerating-startup-growth-how-nvidia-and-aws-are-collaborating-to-grow-ai-startups)
- Known friction on the Inception→AWS path: [Org ID / tier mapping thread](https://forums.developer.nvidia.com/t/nvidia-inception-x-aws-activate-four-months-in-still-no-answer-on-the-org-id-tier-mapping-question/371135) · [approval delay thread](https://forums.developer.nvidia.com/t/aws-activate-credits-approval-delay-through-nvidia-inception-program/330953)
- [AWS Activate terms](https://aws.amazon.com/activate/terms) · [Activate credits explained](https://aws.amazon.com/aws-startups/learn/everything-you-need-to-know-about-aws-activate-credits/) · [AWS HIPAA compliance](https://aws.amazon.com/compliance/hipaa-compliance/) · [accept a BAA for all accounts in your organization](https://aws.amazon.com/blogs/security/accept-a-baa-with-aws-for-all-accounts-in-your-organization) · [activate a BAA via AWS Artifact](https://repost.aws/knowledge-center/activate-artifact-baa-agreement)
