"""Crucible — Ardia's guardrail gate harness.

Each gate is a pure, deterministic function returning a GateResult. An output must
pass every applicable gate before a human ever sees it. These are the eight
guardrails described on the TARA framework page, implemented and unit-tested.
"""
from .gates import (
    GateResult,
    GATES,
    non_diagnostic_gate,
    human_in_the_loop_gate,
    cite_or_abstain_gate,
    policy_override_gate,
    de_identification_gate,
    safety_escalation_gate,
    scope_of_practice_gate,
    honesty_gate,
    run_all_gates,
)

__all__ = [
    "GateResult", "GATES",
    "non_diagnostic_gate", "human_in_the_loop_gate", "cite_or_abstain_gate",
    "policy_override_gate", "de_identification_gate", "safety_escalation_gate",
    "scope_of_practice_gate", "honesty_gate", "run_all_gates",
]
