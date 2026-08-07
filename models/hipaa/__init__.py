"""Ardia HIPAA / PHI guardrail — the enforced technical-safeguards layer.

The single choke point every AI call passes through: TLS-only, minimum-necessary,
attachment attestation gate, Safe-Harbor de-identification before any third party,
output PHI scan, and a PHI-free audit trail. Risk reduction + testable controls —
not a guarantee against all breach (see controls.py for the honest full posture).
"""
from . import audit, controls
from .guard import (
    MAX_INPUT_CHARS,
    GuardContext,
    Postflight,
    Preflight,
    guarded_text,
    postflight,
    preflight,
    scrub,
)

__all__ = [
    "GuardContext", "Preflight", "Postflight",
    "preflight", "postflight", "guarded_text", "scrub", "MAX_INPUT_CHARS",
    "audit", "controls",
]
