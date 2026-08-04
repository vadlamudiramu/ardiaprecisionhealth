"""Studio guardrail wiring — runs the real Sentinel + Crucible on every model call.

Sentinel de-identifies the user's text BEFORE it reaches the model (no raw PHI in
a prompt); Crucible runs the applicable guardrail gates on the model's OUTPUT after.
Both return structured metadata the UI can show, so the guardrails demonstrably run
rather than merely being described.
"""
from __future__ import annotations

import pathlib
import sys

# Make the repo-root `models/` package importable from inside ardia-studio-app/.
_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from models.sentinel import deidentify
from models.crucible import (
    non_diagnostic_gate,
    safety_escalation_gate,
    scope_of_practice_gate,
    de_identification_gate,
    honesty_gate,
    human_in_the_loop_gate,
)

# Gates that apply to a free-text health-assistant answer. (cite-or-abstain and
# policy-override need a claim/policy verdict the Studio doesn't carry, so they are
# not run here — the appeal pipeline is where those two belong.)
_STUDIO_GATES = (
    non_diagnostic_gate,
    safety_escalation_gate,
    scope_of_practice_gate,
    de_identification_gate,
    honesty_gate,
    human_in_the_loop_gate,
)


def deid_input(text: str | None) -> tuple[str, dict]:
    """De-identify the user's text. Returns (clean_text, report)."""
    if not text:
        return text or "", {"removed": 0, "categories": []}
    r = deidentify(text)
    return r.text, {"removed": r.total_removed, "categories": r.categories_hit}


def gate_output(text: str | None) -> list[dict]:
    """Run the applicable Crucible gates on model output. Returns one dict per gate."""
    text = text or ""
    out: list[dict] = []
    for gate in _STUDIO_GATES:
        r = gate(text)
        out.append({"gate": r.gate, "passed": r.passed, "reason": r.reason})
    return out


def summarize(gates: list[dict]) -> dict:
    """Compact pass/fail summary for a badge."""
    failed = [g["gate"] for g in gates if not g["passed"]]
    return {"passed": len(failed) == 0, "n_passed": len(gates) - len(failed),
            "n_total": len(gates), "failed": failed}
