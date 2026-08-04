"""Crucible guardrail gates — deterministic behavioral checks on model output.

Every gate returns a :class:`GateResult`. A gate that ``passed is False`` blocks the
output from reaching a human. These encode the eight guardrails named on the TARA
page: non-diagnostic, human-in-the-loop, cite-or-abstain, policy-override block,
de-identification, safety escalation, scope-of-practice, and honesty.

No LLM, no network, no randomness — the gates are testable rules, so the guarantee
is verifiable rather than aspirational.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from models.sentinel import deidentify

#: The eight guardrail gates, in evaluation order.
GATES: tuple[str, ...] = (
    "non_diagnostic",
    "human_in_the_loop",
    "cite_or_abstain",
    "policy_override",
    "de_identification",
    "safety_escalation",
    "scope_of_practice",
    "honesty",
)


@dataclass(frozen=True)
class GateResult:
    gate: str
    passed: bool
    reason: str


_DIAGNOSTIC = re.compile(
    r"\b(you (?:have|are diagnosed)|the patient has|"
    r"diagnos(?:is is|ed with|e of)|is confirmed to have|definitely has)\b",
    re.I,
)
_AUTOFILE = re.compile(
    r"\b(auto[-\s]?(?:submit|file|filed|filing)|files? (?:it )?automatically|"
    r"without (?:human |a |any )?review|no manual review|submitted automatically)\b",
    re.I,
)
_CRISIS = re.compile(
    r"\b(suicid\w*|kill myself|end my life|want to die|chest pain|can'?t breathe|"
    r"overdose|unconscious|stroke)\b",
    re.I,
)
_ESCALATION = re.compile(
    r"\b(9-?1-?1|emergency (?:services|room)|call .{0,20}(?:immediately|now|right away)|"
    r"seek .{0,20}(?:emergency|immediate)|contact .{0,25}(?:provider|clinician|doctor)|"
    r"escalat\w*)\b",
    re.I,
)
_DRUG_DOSE = re.compile(
    r"\b(?:take|prescrib\w*|administer|start|give|increase to|titrate to)\b[^.]*?"
    r"\b\d+(?:\.\d+)?\s?(?:mg|mcg|ug|ml|units?|g|iu)\b",
    re.I,
)
_ABSOLUTE = re.compile(
    r"\b(100%\s*(?:accura\w+|correct|reliable)|zero hallucinations?|"
    r"guaranteed\s+(?:accura\w+|results?|approval|payment)|never wrong|"
    r"always correct|fully autonomous)\b",
    re.I,
)


_CONDITIONAL = re.compile(r"\b(if|when|whether|should|unless|in case)\b\s*$", re.I)


def non_diagnostic_gate(text: str) -> GateResult:
    text = text or ""
    for m in _DIAGNOSTIC.finditer(text):
        # A conditional ("if you have chest pain, call 911") is safety guidance,
        # not a diagnostic assertion — skip those.
        pre = text[max(0, m.start() - 14):m.start()]
        if _CONDITIONAL.search(pre):
            continue
        return GateResult("non_diagnostic", False, f"diagnostic language: {m.group(0)!r}")
    return GateResult("non_diagnostic", True, "no diagnostic assertion")


def human_in_the_loop_gate(text: str) -> GateResult:
    m = _AUTOFILE.search(text or "")
    return GateResult("human_in_the_loop", m is None,
                      "human review preserved" if not m else f"auto-action detected: {m.group(0)!r}")


def cite_or_abstain_gate(claim: str, citations: list[str] | None) -> GateResult:
    citations = citations or []
    empty_claim = not (claim or "").strip()
    passed = empty_claim or len(citations) > 0
    return GateResult("cite_or_abstain", passed,
                      "abstained / no claim" if empty_claim else
                      (f"{len(citations)} citation(s)" if passed else "asserted claim with no citation"))


def policy_override_gate(symbolic_verdict: str | None, llm_conclusion: str | None) -> GateResult:
    # The guarded LLM may never contradict the deterministic symbolic policy verdict.
    passed = symbolic_verdict is None or llm_conclusion is None or symbolic_verdict == llm_conclusion
    return GateResult("policy_override", passed,
                      "consistent with symbolic policy" if passed
                      else f"LLM {llm_conclusion!r} overrides policy {symbolic_verdict!r}")


def de_identification_gate(text: str) -> GateResult:
    # An output must NOT contain PHI in the first place. If Sentinel finds and
    # removes any identifier, the raw output carried PHI and the gate fails.
    report = deidentify(text or "")
    passed = report.total_removed == 0
    return GateResult("de_identification", passed,
                      "no PHI identifiers present" if passed
                      else f"PHI detected: {report.categories_hit}")


def safety_escalation_gate(text: str) -> GateResult:
    text = text or ""
    if _CRISIS.search(text):
        passed = bool(_ESCALATION.search(text))
        return GateResult("safety_escalation", passed,
                          "crisis signal escalated" if passed else "crisis signal without escalation")
    return GateResult("safety_escalation", True, "no crisis signal")


def scope_of_practice_gate(text: str) -> GateResult:
    m = _DRUG_DOSE.search(text or "")
    return GateResult("scope_of_practice", m is None,
                      "no drug-and-dose order" if not m else f"drug+dose recommendation: {m.group(0)[:40]!r}")


def honesty_gate(text: str) -> GateResult:
    m = _ABSOLUTE.search(text or "")
    return GateResult("honesty", m is None,
                      "no unqualified absolute claim" if not m else f"absolute claim: {m.group(0)!r}")


def run_all_gates(
    text: str,
    *,
    claim: str | None = None,
    citations: list[str] | None = None,
    symbolic_verdict: str | None = None,
    llm_conclusion: str | None = None,
) -> list[GateResult]:
    """Run every gate. ``claim`` defaults to ``text`` for the cite-or-abstain check."""
    return [
        non_diagnostic_gate(text),
        human_in_the_loop_gate(text),
        cite_or_abstain_gate(text if claim is None else claim, citations),
        policy_override_gate(symbolic_verdict, llm_conclusion),
        de_identification_gate(text),
        safety_escalation_gate(text),
        scope_of_practice_gate(text),
        honesty_gate(text),
    ]
