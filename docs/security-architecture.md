# Security Architecture — minimising breach liability

**Status:** proposed · **Date:** August 2026
**Question this answers:** *"Which cloud is safer for PHI, and how do I make a breach
non-fatal for a zero-funding company?"*
**Related:** [`adr-001-cloud-portability.md`](./adr-001-cloud-portability.md) · `.claude/rules/security.md` · `models/hipaa/controls.py`

> Not legal advice. The contractual and liability sections below name the questions to
> take to a healthcare regulatory attorney — they do not answer them.

---

## 1. The honest answer on "which cloud is safer"

**Provider choice is not where your breach risk lives.** GCP, AWS and Azure all sign
BAAs, all encrypt at rest by default, all offer HIPAA-eligible service catalogues, and
none of them has been the root cause of a notable healthcare breach. The published OCR
breach reports are dominated by phishing, stolen credentials, misconfigured storage,
over-permissioned accounts, and lost devices — **customer-side failures on every
platform.**

The difference a provider makes is at the margin. On that margin, three GCP controls
matter unusually much for a PHI reasoning workload:

| Control | What it gives you |
|---|---|
| **VPC Service Controls** | A perimeter around the PHI project. Even a fully compromised service account with valid credentials cannot move data to a project outside the perimeter. This is the single strongest mitigation for the most likely breach path — a leaked credential. |
| **Cloud External Key Manager (EKM)** | Key material held outside Google, in a service you control. Google cannot decrypt your data without calling your key service, and you can revoke. This is a stronger sovereignty guarantee than running on two clouds. |
| **Access Transparency / Access Approval** | Logs of Google staff access to your data, and the option to require your approval first. Very few controls let a two-person startup say "no vendor employee reads our data without our sign-off." |

AWS's counterpart strengths are real but point at a different job: **S3 Object Lock**
(true WORM for audit logs and backups), **Nitro Enclaves** (confidential compute), and
**Comprehend Medical**. Notice that this is precisely the split ADR-001 already chose —
GCP as the production perimeter, AWS as the immutable evidence and backup store.

**Conclusion:** stay on GCP for production. The provider decision is settled and is not
the lever. Everything below is.

---

## 2. The reframe that actually caps your liability

> **The cheapest breach protection is not holding the data.**

Under 45 CFR 164.514(b), data de-identified to the Safe Harbor standard **is not PHI**.
A breach of non-PHI is not a HIPAA breach, is not reportable to OCR, triggers no 60-day
notification clock, and is not the lawsuit you are afraid of.

Every dollar and hour spent on encryption, monitoring and access control protects data
you chose to hold. Reducing what you hold is strictly better than protecting it — and it
is free.

### You are already most of the way there

`models/hipaa/guard.py` is a single choke point that de-identifies before anything
downstream sees text, blocks un-redactable binaries unless attested synthetic or
BAA-covered, scans output for residual PHI, and writes a PHI-free audit event. That is a
better starting posture than most funded healthtech companies have at Series A.

Three design moves finish the job:

### 2a. Tokenise at the edge, isolate the identity vault
At ingest, replace direct identifiers with opaque tokens. The token↔identity map lives in
**one small, separately-encrypted table** with its own KMS key, its own service account,
and no application-tier read access — resolution happens only in a narrow service at
submission time, when the appeal must carry a real patient and claim number.

Result: the reasoning corpus, the eval data, the logs, the vector index and the analytics
warehouse contain **no PHI at all**. A full compromise of the application tier exposes
de-identified text and a pile of tokens.

### 2b. Process-and-discard for Phase 1A
For the DFW pilot, ask whether you need to *retain* identified data at all. Ingest the
claim, generate the appeal, hand it back, retain only de-identified outcome data for
learning. **Retention is a liability multiplier**: 10,000 stored records is a 10,000-person
breach; the same volume processed and discarded is not.

Set retention explicitly — a TTL on every PHI store, enforced by a scheduled job, tested.
Data you no longer hold cannot be breached, subpoenaed, or leaked by a future employee.

### 2c. Make the blast radius a number you can state
Write it down and keep it current:

> *"A total compromise of our application tier exposes N de-identified records and zero
> direct identifiers. Reportable-breach exposure is limited to the identity vault: M rows,
> separate key, separate service account, no standing human access."*

That sentence is what you tell a lab's compliance officer, your insurer, and — if the day
ever comes — OCR. It is worth more than any single technical control.

---

## 3. Your actual threat model

Not nation-states. These, in descending order of likelihood — and each is cheap to close:

| Threat | Control |
|---|---|
| Credential or service-account key leaked (git, laptop, CI log) | No long-lived keys anywhere. Workload Identity Federation for CI, ADC on Cloud Run. Secret scanning on every push. **VPC-SC makes a leaked key far less useful** |
| Storage bucket or endpoint left public | `--no-allow-unauthenticated` on every service; org policy blocking public bucket ACLs; a CI check that fails the build on a public resource |
| Over-permissioned service account | One SA per workload, least privilege, zero `roles/owner` on the PHI project. Quarterly access review |
| Founder phished | Hardware security keys (FIDO2) on every account — Google, AWS, GitHub, email. Not TOTP. This is a ~$100 total control that closes the most common entry path |
| PHI written to logs | Already forbidden in `.claude/rules/security.md`; `audit.py` caps string metadata so content cannot be logged by accident. Add a log-sink scanner that alerts on identifier-shaped strings |
| Subprocessor breach (a vendor you gave data to) | Keep the subprocessor list short and BAA'd. Every vendor touching PHI needs a BAA — no exceptions, including analytics and error trackers |
| Malicious dependency | **Your `models/` layer is dependency-free — that is a genuine security asset, not just tidiness.** Keep it. Pin and hash-lock everything in the Cloud Run image; generate an SBOM |
| Insider / departing contractor | No standing human access to PHI. Break-glass only, requiring approval and emitting an audit event |

---

## 4. Control layers, ordered by return

1. **Don't hold it** — de-identify, tokenise, discard, TTL. Free. Biggest effect.
2. **Isolate what you must hold** — identity vault, own key, own SA, no app-tier reads.
3. **Own the keys** — CMEK now, EKM before scale. Revocable.
4. **Perimeter** — VPC Service Controls; no public endpoints; private egress only.
5. **No standing access** — break-glass with approval + audit; hardware keys everywhere.
6. **Immutable audit** — point `audit.add_sink()` at a real append-only store; replicate to S3 with Object Lock so logs survive a compromise of the primary cloud.
7. **Supply chain** — keep `models/` dependency-free; pin, hash-lock and SBOM the rest.
8. **Detect and rehearse** — alerts on anomalous access; a written IR plan; one tabletop exercise before the first PHI arrives.
9. **Transfer the residual risk** — insurance and contract terms (§5).

Layers 1–3 do most of the work. Do not let layers 6–8 delay them.

---

## 5. The non-technical controls that actually cap liability

Technical controls reduce the *probability* of a breach. These cap the *consequence* —
which is the thing that ends a zero-funding company.

**Cyber liability insurance with breach-response coverage.** The single highest-ROI item
on this page and the one founders skip. For a pre-revenue company holding few records,
premiums are typically low four figures a year for meaningful limits — but the number
depends entirely on record count and controls, so get real quotes. Look for breach
*response* cover (forensics, notification, credit monitoring, legal), not just liability.
Most lab contracts will require you to carry it anyway, so you are buying something you
will be asked to show.

**Your BAA with the lab is a negotiation, not a form.** Take these to a healthcare
regulatory attorney before signing anything: liability cap, indemnity scope, who pays for
breach notification, breach-notice timelines to the covered entity, subcontractor terms,
data return/destruction on termination, and audit rights. A few hours of specialist time
here is cheap against the risk you are describing.

**Sequence the pilot to earn the risk.** Phase the design-partner agreement:
*synthetic → de-identified historical → identified live*, with the controls in §4 signed
off before each step. This is both a genuine liability control and an easier ask of the
lab — "we start on de-identified data" is a smaller decision for their compliance officer
than handing you live PHI on day one.

**Incident response plan.** HIPAA §164.308(a)(6) requires one, and `models/hipaa/
controls.py` currently grades it `planned`. Write it before PHI arrives: who declares an
incident, the 60-day OCR clock, the 500-record media threshold, who calls the insurer and
the attorney. An IR plan written during an incident is not a plan.

**Corporate hygiene.** Keep the C-Corp veil intact — separate accounts and records, no
personal guarantees on anything touching the platform.

---

## 6. Performance — briefly, since it was asked

Between GCP and AWS, the performance difference for this workload is noise next to model
latency. Two things do matter:

- **Co-locate** the model call, the data and the service in one region (`us-central1`).
  Cross-region hops cost more latency than any instance-type choice.
- **Prompt-cache the payer-policy context.** Appeals inject large, repeated LCD/NCD text
  per request. Caching that prefix is the single biggest latency and cost win available
  in this architecture — far larger than any infrastructure tuning. Keep the stable
  policy text first in the prompt and the per-claim text last, or the cache never hits.

---

## 7. Where you actually stand

`models/hipaa/controls.py` grades 15 Security Rule controls honestly: 2 `enforced`,
4 `partial`, 1 `baa_required` for encryption at rest, 1 `policy`, and the rest `planned`.
That honesty is itself an asset — it is what an auditor and a compliance officer want to
see, and it is rarer than it should be.

**The gate before any real PHI touches the system** — the `planned` items that are not
optional:

- [ ] `164.308(a)(1)` — written security risk analysis (also your SOC 2 starting point)
- [ ] `164.308(a)(6)` — incident response procedures
- [ ] `164.308(a)(7)` — backup and contingency plan (and a tested restore)
- [ ] `164.312(a)` — unique user IDs, access control, auto-logoff
- [ ] `164.312(d)` — person/entity authentication (hardware keys)
- [ ] `164.312 (at rest)` — CMEK, which unblocks on the signed BAA
- [ ] `164.308(b)` — BAAs signed: Google, AWS, and every subprocessor
- [ ] Cyber liability policy bound
- [ ] Tokenisation + identity-vault split implemented and tested
- [ ] Retention TTLs enforced by a scheduled job, with a test

Update the statuses in `controls.py` as each lands. The rule already in
`.claude/rules/security.md` holds until every box is ticked: **synthetic and de-identified
data only.**
