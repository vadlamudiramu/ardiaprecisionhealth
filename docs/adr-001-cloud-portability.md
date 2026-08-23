# ADR-001 — Portable-primary, not multi-cloud

**Status:** proposed · **Date:** August 2026 · **Decides:** how ARDIA avoids single-cloud
dependency without paying the multi-cloud tax
**Related:** [`cloud-credits-strategy.md`](./cloud-credits-strategy.md) · [`cloud-credits-runbook.md`](./cloud-credits-runbook.md)

## Context

The founding concern: running everything on Google Cloud creates over-dependency on one
vendor, and that feels like a security risk. The proposed remedy was a hybrid/multi-cloud
architecture.

The concern about dependency is legitimate and worth designing against. The proposed
remedy is the wrong instrument, and for a two-founder pre-revenue team four months from a
pilot it is actively harmful.

### Multi-cloud does not improve security at our size — it degrades it

Healthcare cloud breaches are overwhelmingly **misconfiguration**, not provider
compromise. Running two clouds means two IAM models, two audit-log formats and retention
setups, two network perimeters, two key hierarchies, two BAAs, two sets of default-open
footguns — maintained by the same two people. It roughly doubles the surface where the
actual failure mode lives.

It also *creates* an exposure that does not otherwise exist: PHI in transit between
clouds, over links neither provider's BAA fully owns.

And it doubles compliance scope. A SOC 2 Type II audit prices per environment; two
production clouds means two sets of evidence, two penetration-test scopes, two vendor
reviews. That is real money and real founder-weeks, spent before a single lab has signed.

### Lock-in is not about which cloud — it is about which services

This is the reframe the decision rests on. Lock-in is a spectrum measured in *migration
weeks*, and the cloud logo is almost irrelevant to it:

| Architecture | Time to move clouds |
|---|---|
| Containers + Postgres + object storage + Terraform | ~1–2 weeks |
| The above, plus a managed FHIR store and a warehouse | ~4–6 weeks |
| Firestore + Pub/Sub + Cloud Functions + Vertex Agent Builder + BigQuery-native models | ~4–6 months |

All three of those are "single-cloud." The difference in dependency between the first and
the third is a factor of ten, and it is decided entirely by which primitives we pick — not
by how many providers we run in parallel. A team can be genuinely trapped on one cloud
while running on two, and genuinely free while running on one.

### We are already not single-vendor

Site on Vercel, code on GitHub, models from Anthropic and Google, domain elsewhere. The
dependency graph is already spread across the layers where concentration would actually
hurt.

## Decision

**Adopt a portable-primary architecture: one production cloud (GCP), built exclusively on
primitives that run anywhere, plus a genuine second-provider presence at the three layers
where independence actually pays.**

### 1. Portable primitives only

| Need | Choose | Because | Avoid |
|---|---|---|---|
| Compute | OCI containers on Cloud Run | Identical image runs on ECS/Fargate/any k8s | Cloud Functions' proprietary runtime |
| System of record | **Postgres** (Cloud SQL) | Runs everywhere; pg_dump is a complete exit | Firestore, Spanner, DynamoDB |
| Vector search | **pgvector** in the same Postgres | Portable, one less system, ample for a policy corpus this size | Vertex Vector Search |
| Object storage | GCS via its **S3-compatible XML API** | Same client code works against S3 | GCS-native-only SDK paths |
| Job queue | A Postgres job table | Sufficient at our volume; zero new dependency | Pub/Sub, Cloud Tasks |
| Clinical data | FHIR R4 (Cloud Healthcare API) | Data model is an open standard — export is real, not theoretical | Any proprietary clinical schema |
| Infrastructure | Terraform / OpenTofu | Reviewable, reproducible, portable in structure | Console clickops, Deployment Manager |
| Identity | OIDC | Standard | Provider-proprietary auth flows |
| Models | `call_model()` seam, Vertex **and** Bedrock adapters | Both tested in CI | Any single-provider SDK in the critical path |

### 2. Where lock-in is acceptable

**Accept it on derived, rebuildable data. Never on the system of record.**

BigQuery for the eval harness and analytics is fine — every row in it can be regenerated
from the corpus and the eval runner. Patient-linked and claim-linked data lives in
Postgres and FHIR, where an export is a real export.

### 3. The hybrid that is actually worth building

Three layers, each cheap, each buying genuine independence:

**a. Keys outside the cloud that holds the data.** Cloud External Key Manager, with the
key material held in a service we control. Google then cannot decrypt our data without a
call to our key service, which we can revoke. This is a stronger sovereignty guarantee
than multi-cloud, at a fraction of the cost, and it answers the "one vendor sees
everything" concern directly rather than by dilution.

**b. Backups and audit logs replicated to AWS.** Encrypted nightly Postgres dumps and
append-only audit-log exports into S3 with Object Lock, in an account with separate
credentials. This survives the realistic disaster — not "Google Cloud fails," but *our GCP
org is compromised, our billing lapses, or our account is suspended.* Our data is text, so
egress is pennies. Funded by the AWS credits.

**c. Model-provider diversity.** Claude reachable through both Vertex and Bedrock behind
one interface, both exercised in CI. For an AI company this is the dependency that
genuinely bites — model availability, pricing, deprecation — and it is nearly free.

### 4. Portability must be tested or it is fiction

Quarterly drill: deploy the container to ECS/Fargate, restore the latest backup into RDS,
point it at Bedrock, run the full test suite, record the wall-clock time. Publish the
number internally.

*"We can be fully operational on AWS in N days; last verified <date>"* is a sentence that
answers a procurement officer, an investor, and this ADR's concern all at once. An
untested escape hatch answers none of them.

## Alternatives considered

**Active-active multi-cloud.** Rejected for now. Duplicate infrastructure, cross-cloud
egress on every request, two BAAs, two SOC 2 scopes, two on-call runbooks, and a latency
budget spent on inter-cloud hops. Three-to-six founder-months against a four-month pilot
window. Revisit when a customer contractually requires it.

**Active-passive with a warm standby.** Rejected for now, reconsider at Series A or first
enterprise contract. It is the natural upgrade from this decision — the drill in §4 is
what turns it on.

**Kubernetes as the portability layer.** Rejected. A container is already the portable
unit; k8s adds a large operational surface to buy portability we get from the image alone.

**Stay single-cloud without portability constraints.** Rejected. This is the actual
dependency risk, and it is the default outcome if nothing is decided.

## Consequences

**Positive.** Escape hatch measured in weeks and periodically proven. One security
posture to get right. Credits still fund production. A defensible answer to "what if
Google turns you off." Sovereignty via key control rather than architecture sprawl.

**Negative.** Some managed services are off the table even when convenient and
credit-funded — pgvector instead of Vertex Vector Search, a Postgres queue instead of
Pub/Sub. Slightly more code we own. The quarterly drill is real recurring work.

**Accepted risk.** A total, prolonged GCP outage takes production down until the standby
is stood up. For pre-revenue batch-oriented claim processing with hours of tolerance, that
is the right trade.

## Revisit when

A customer contractually requires multi-cloud · we hold PHI for more than ~10 labs ·
a drill exceeds 10 days · GCP pricing after credits materially changes the calculus.
