"""HIPAA controls posture — an HONEST, machine-readable map of what is enforced in
code today vs. what a real PHI deployment still requires.

This exists so the platform's HIPAA claims are truthful and auditable. Status vocab:
  enforced       — implemented and tested in this codebase (technical safeguard)
  partial        — a meaningful piece is enforced; the full control needs more
  policy         — an organizational/process measure code cannot provide alone
  baa_required   — blocked on a signed Business Associate Agreement with vendors
  planned        — not yet built; on the roadmap
No control here is marked "enforced" unless code + a test actually backs it.
"""
from __future__ import annotations

from models.sentinel import SAFE_HARBOR_CATEGORIES

#: 45 CFR 164.308 / .310 / .312 — the HIPAA Security Rule safeguards, honestly graded.
SECURITY_RULE: list[dict] = [
    # Administrative safeguards — §164.308
    {"cite": "164.308(a)(1)", "control": "Security risk analysis & management", "status": "planned",
     "detail": "Formal risk analysis + remediation program. This guardrail library is a control input, not the program."},
    {"cite": "164.308(a)(3-4)", "control": "Access management · minimum necessary", "status": "partial",
     "detail": "Enforced: input size cap + de-identification before any third party. Role-based access to PHI is planned."},
    {"cite": "164.308(a)(5)", "control": "Workforce security awareness & training", "status": "policy",
     "detail": "Organizational training program — outside code."},
    {"cite": "164.308(a)(6)", "control": "Security incident procedures", "status": "planned",
     "detail": "Detection/response/breach-notification runbook."},
    {"cite": "164.308(a)(7)", "control": "Contingency plan (backup / DR)", "status": "planned",
     "detail": "Backup, disaster recovery, emergency-mode operation."},
    {"cite": "164.308(b)", "control": "Business Associate Agreements", "status": "baa_required",
     "detail": "A BAA is required with EVERY vendor that touches PHI (model providers, cloud). None signed yet → the enforced rule is synthetic/de-identified data only."},
    # Physical safeguards — §164.310
    {"cite": "164.310", "control": "Facility / workstation / device & media controls", "status": "planned",
     "detail": "Provided largely by a HIPAA-eligible cloud under a BAA; not applicable to the current static/serverless prototype."},
    # Technical safeguards — §164.312
    {"cite": "164.312(a)", "control": "Access control · unique user ID · auto-logoff", "status": "planned",
     "detail": "Authentication + per-user access to PHI. The Studio demo is gated by an optional shared access code only."},
    {"cite": "164.312(b)", "control": "Audit controls", "status": "partial",
     "detail": "Enforced: a PHI-free audit event per guarded AI action (audit.py). Durable, tamper-evident storage + review procedures are planned."},
    {"cite": "164.312(c)", "control": "Integrity of ePHI", "status": "partial",
     "detail": "Deterministic de-id + output PHI scan protect against leakage; full integrity/versioning is planned."},
    {"cite": "164.312(d)", "control": "Person/entity authentication", "status": "planned",
     "detail": "Real authentication for any PHI access."},
    {"cite": "164.312(e)", "control": "Transmission security (encryption in transit)", "status": "enforced",
     "detail": "TLS required by the guard (non-TLS input refused); site + API served over HTTPS (Vercel), CSP default-src 'self'."},
    {"cite": "164.312 (at rest)", "control": "Encryption of ePHI at rest", "status": "baa_required",
     "detail": "Requires a HIPAA-eligible cloud (KMS/encrypted stores) under a BAA. The prototype persists no PHI."},
    # De-identification — §164.514(b)
    {"cite": "164.514(b)(2)", "control": "Safe Harbor de-identification", "status": "enforced",
     "detail": "Sentinel removes the pattern-detectable Safe-Harbor identifiers from text before any model/third party; output is re-scanned. See identifier coverage below."},
    {"cite": "164.502(b)", "control": "Minimum necessary", "status": "partial",
     "detail": "Enforced: input cap + de-identification. Field-level minimization for structured data is planned."},
]

#: Which of the 18 Safe-Harbor identifiers this engine handles, and how.
IDENTIFIER_COVERAGE: dict[str, str] = dict(SAFE_HARBOR_CATEGORIES)

_STATUS_LABEL = {
    "enforced": "✅ enforced (code + test)",
    "partial": "🟡 partial",
    "policy": "📋 policy / org measure",
    "baa_required": "🔒 needs a BAA",
    "planned": "🗓️ planned",
}


def render_markdown() -> str:
    """Render the honest HIPAA posture as Markdown."""
    lines = [
        "# Ardia — HIPAA / PHI Guardrail Posture",
        "",
        "> **Honest scope.** These are the technical safeguards enforced in code plus an honest grade "
        "of the controls a real Protected Health Information (PHI) deployment still requires. This is "
        "**risk reduction and enforced controls, not a guarantee against all breach** — no such guarantee "
        "is possible or claimed. **Until a Business Associate Agreement (BAA) and a HIPAA-eligible "
        "environment exist, the enforced rule is: synthetic / de-identified data only.**",
        "",
        "## Security Rule safeguards (45 CFR 164.308 / .310 / .312 / .514)",
        "",
        "| § | Control | Status | Detail |",
        "|---|---|---|---|",
    ]
    for c in SECURITY_RULE:
        lines.append("| %s | %s | %s | %s |" % (
            c["cite"], c["control"], _STATUS_LABEL.get(c["status"], c["status"]), c["detail"]))
    enforced = sum(1 for c in SECURITY_RULE if c["status"] == "enforced")
    lines += [
        "",
        "_%d of %d controls are fully enforced in code today; the rest are partial, policy, BAA-blocked, "
        "or planned — stated honestly rather than marketed as done._" % (enforced, len(SECURITY_RULE)),
        "",
        "## Safe-Harbor identifier coverage (§164.514(b)(2))",
        "",
        "`regex` = detected deterministically in text · `roster` = needs a supplied name list · "
        "`out-of-scope` = not applicable to plain text (photos/biometrics).",
        "",
        "| Identifier | Handling |",
        "|---|---|",
    ]
    for ident, how in IDENTIFIER_COVERAGE.items():
        lines.append("| %s | `%s` |" % (ident.replace("_", " "), how))
    lines += [
        "",
        "> Note: free-text **name** detection without a trained NER model is best-effort and is intentionally "
        "not claimed as complete — names are removed from a supplied roster. This limitation is stated, not hidden.",
        "",
    ]
    return "\n".join(lines)
