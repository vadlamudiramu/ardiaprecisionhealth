# Ardia — HIPAA / PHI Guardrail Posture

> **Honest scope.** These are the technical safeguards enforced in code plus an honest grade of the controls a real Protected Health Information (PHI) deployment still requires. This is **risk reduction and enforced controls, not a guarantee against all breach** — no such guarantee is possible or claimed. **Until a Business Associate Agreement (BAA) and a HIPAA-eligible environment exist, the enforced rule is: synthetic / de-identified data only.**

## Security Rule safeguards (45 CFR 164.308 / .310 / .312 / .514)

| § | Control | Status | Detail |
|---|---|---|---|
| 164.308(a)(1) | Security risk analysis & management | 🗓️ planned | Formal risk analysis + remediation program. This guardrail library is a control input, not the program. |
| 164.308(a)(3-4) | Access management · minimum necessary | 🟡 partial | Enforced: input size cap + de-identification before any third party. Role-based access to PHI is planned. |
| 164.308(a)(5) | Workforce security awareness & training | 📋 policy / org measure | Organizational training program — outside code. |
| 164.308(a)(6) | Security incident procedures | 🗓️ planned | Detection/response/breach-notification runbook. |
| 164.308(a)(7) | Contingency plan (backup / DR) | 🗓️ planned | Backup, disaster recovery, emergency-mode operation. |
| 164.308(b) | Business Associate Agreements | 🔒 needs a BAA | A BAA is required with EVERY vendor that touches PHI (model providers, cloud). None signed yet → the enforced rule is synthetic/de-identified data only. |
| 164.310 | Facility / workstation / device & media controls | 🗓️ planned | Provided largely by a HIPAA-eligible cloud under a BAA; not applicable to the current static/serverless prototype. |
| 164.312(a) | Access control · unique user ID · auto-logoff | 🗓️ planned | Authentication + per-user access to PHI. The Studio demo is gated by an optional shared access code only. |
| 164.312(b) | Audit controls | 🟡 partial | Enforced: a PHI-free audit event per guarded AI action (audit.py). Durable, tamper-evident storage + review procedures are planned. |
| 164.312(c) | Integrity of ePHI | 🟡 partial | Deterministic de-id + output PHI scan protect against leakage; full integrity/versioning is planned. |
| 164.312(d) | Person/entity authentication | 🗓️ planned | Real authentication for any PHI access. |
| 164.312(e) | Transmission security (encryption in transit) | ✅ enforced (code + test) | TLS required by the guard (non-TLS input refused); site + API served over HTTPS (Vercel), CSP default-src 'self'. |
| 164.312 (at rest) | Encryption of ePHI at rest | 🔒 needs a BAA | Requires a HIPAA-eligible cloud (KMS/encrypted stores) under a BAA. The prototype persists no PHI. |
| 164.514(b)(2) | Safe Harbor de-identification | ✅ enforced (code + test) | Sentinel removes the pattern-detectable Safe-Harbor identifiers from text before any model/third party; output is re-scanned. See identifier coverage below. |
| 164.502(b) | Minimum necessary | 🟡 partial | Enforced: input cap + de-identification. Field-level minimization for structured data is planned. |

_2 of 15 controls are fully enforced in code today; the rest are partial, policy, BAA-blocked, or planned — stated honestly rather than marketed as done._

## Safe-Harbor identifier coverage (§164.514(b)(2))

`regex` = detected deterministically in text · `roster` = needs a supplied name list · `out-of-scope` = not applicable to plain text (photos/biometrics).

| Identifier | Handling |
|---|---|
| name | `roster` |
| geo zip | `regex` |
| date | `regex` |
| age over 89 | `regex` |
| phone or fax | `regex` |
| email | `regex` |
| ssn | `regex` |
| mrn | `regex` |
| health plan id | `regex` |
| account number | `regex` |
| license number | `regex` |
| vehicle id | `regex` |
| device id | `regex` |
| url | `regex` |
| ip address | `regex` |
| biometric | `out-of-scope` |
| photo | `out-of-scope` |
| other unique id | `regex` |

> Note: free-text **name** detection without a trained NER model is best-effort and is intentionally not claimed as complete — names are removed from a supplied roster. This limitation is stated, not hidden.
