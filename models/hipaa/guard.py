"""Ardia HIPAA/PHI guardrail — the single choke point EVERY AI call must pass through.

Honest scope. This is the technical-safeguards layer (45 CFR 164.312) enforced in
code. It:
  1. refuses input over a non-TLS channel (transmission security),
  2. enforces a minimum-necessary input cap,
  3. blocks binary attachments (images/PDFs — Sentinel cannot redact pixels) unless
     the caller attests they are synthetic/de-identified OR a BAA covers the path,
  4. DE-IDENTIFIES text (HIPAA Safe Harbor) before anything downstream/third-party
     sees it — raw PHI never leaves this boundary,
  5. SCANS model output for residual PHI before it is returned,
  6. writes a PHI-free audit event for every decision.

It REDUCES risk and makes the controls testable. It is NOT — and cannot be — a
guarantee against all breach. Processing REAL PHI additionally requires a signed BAA
with every vendor in the path, encryption at rest, access control, workforce
training and the rest of the HIPAA Security Rule program (see controls.py). Until
those exist the enforced rule is: SYNTHETIC / DE-IDENTIFIED DATA ONLY.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field

from models.sentinel import deidentify

from . import audit

#: Minimum-necessary cap on free-text input reaching a model (public-endpoint safe).
MAX_INPUT_CHARS = 6000


@dataclass(frozen=True)
class GuardContext:
    """Who/where a guarded call happens — used for enforcement + the audit trail."""
    model: str = ""
    attested_synthetic: bool = False   # caller attests any uploaded file carries no real PHI
    has_baa: bool = False              # a signed BAA covers this destination vendor
    transport_tls: bool = True         # the request/response travels over TLS


@dataclass
class Preflight:
    allowed: bool
    reason: str
    safe_text: str                     # de-identified text safe to send onward ("" if blocked)
    deid: dict = field(default_factory=lambda: {"removed": 0, "categories": []})
    error: str | None = None           # machine code when blocked
    audit_id: str = ""


@dataclass
class Postflight:
    clean: bool
    reason: str
    residual: list = field(default_factory=list)   # PHI categories found in output (must be empty)
    safe_output: str = ""              # output with any residual identifiers redacted (belt & suspenders)
    audit_id: str = ""


def _hash(text: str) -> str:
    """Correlation hash of the DE-IDENTIFIED text only (not PHI, not reversible to content)."""
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()[:16]


def preflight(text: str | None, attachments, ctx: GuardContext) -> Preflight:
    """Enforce the input-side controls and return the text that is safe to send onward."""
    text = text or ""
    atts = attachments or []

    # 1) transmission security — never accept/forward input over a non-TLS channel
    if not ctx.transport_tls:
        aid = audit.record("blocked", model=ctx.model, extra={"code": "transport_insecure"})
        return Preflight(False, "Refusing to process input over a non-TLS channel.", "",
                         error="transport_insecure", audit_id=aid)

    # 2) minimum necessary — cap input size
    text = text[:MAX_INPUT_CHARS]

    # 3) attachments are binary; Sentinel cannot redact pixels/embedded text. They may
    #    only leave for a third party if attested synthetic OR a BAA covers the path.
    if atts and not (ctx.attested_synthetic or ctx.has_baa):
        aid = audit.record("blocked", model=ctx.model, extra={"code": "attest_required", "attachments": len(atts)})
        return Preflight(False,
                         "Uploaded files are sent to the AI provider and are not automatically de-identified. "
                         "Confirm the file is synthetic/de-identified (no real patient identifiers) — real PHI "
                         "requires a signed BAA before it can be processed.", "",
                         error="attest_required", audit_id=aid)

    # 4) de-identify text BEFORE anything downstream/third-party sees it
    r = deidentify(text)
    deid = {"removed": r.total_removed, "categories": r.categories_hit}
    aid = audit.record("preflight", model=ctx.model, deid=deid,
                       extra={"attachments": len(atts), "attested": ctx.attested_synthetic,
                              "has_baa": ctx.has_baa, "content": _hash(r.text)})
    return Preflight(True, "de-identified; safe to send onward", r.text, deid, None, aid)


def postflight(output: str | None, ctx: GuardContext) -> Postflight:
    """Scan model OUTPUT for residual PHI before it is returned; redact any that slipped through."""
    r = deidentify(output or "")
    clean = r.total_removed == 0
    aid = audit.record("postflight", model=ctx.model,
                       extra={"output_clean": clean, "residual": r.categories_hit})
    reason = "no residual PHI in output" if clean else ("residual PHI redacted: %s" % r.categories_hit)
    return Postflight(clean, reason, r.categories_hit, r.text, aid)


def guarded_text(text: str | None, attachments, ctx: GuardContext):
    """Convenience: run preflight and return (allowed, safe_text_or_reason, preflight).

    Callers send ``safe_text`` to the model, then MUST call ``postflight`` on the
    model output before returning it. Kept as two calls so the model invocation
    stays in the caller (which owns provider/keys), with enforcement on both sides.
    """
    pf = preflight(text, attachments, ctx)
    return pf.allowed, (pf.safe_text if pf.allowed else pf.reason), pf


def scrub(text: str | None) -> str:
    """Redact PHI from any string before it is logged/emitted anywhere (never log raw)."""
    return deidentify(text or "").text
