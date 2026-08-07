"""Tests for the Crucible guardrail gates — each gate proven to pass clean
output and block the specific violation it exists to catch."""
from models.crucible import (
    GATES, run_all_gates,
    non_diagnostic_gate, human_in_the_loop_gate, cite_or_abstain_gate,
    policy_override_gate, de_identification_gate, safety_escalation_gate,
    scope_of_practice_gate, honesty_gate,
)


def test_there_are_eight_gates():
    assert len(GATES) == 8


def test_non_diagnostic():
    assert non_diagnostic_gate("Decision support: findings are consistent with the ordered panel.").passed
    # Bare AI assertions of a diagnosis still fail.
    assert not non_diagnostic_gate("The patient has stage IV lung cancer.").passed
    assert not non_diagnostic_gate("You have diabetes.").passed
    assert not non_diagnostic_gate("Based on these labs, the patient has cancer.").passed
    assert not non_diagnostic_gate("You are diagnosed with hypertension.").passed


def test_non_diagnostic_exempts_attributed_claim_references():
    # An administrative appeal REFERENCING the claim's already-documented diagnosis is
    # not the model diagnosing — it must pass when the dx is attributed to the record.
    assert non_diagnostic_gate(
        "The claim's documented diagnosis of stage IV NSCLC (ICD-10 C34.90) supports coverage.").passed
    assert non_diagnostic_gate(
        "Per the medical record, the patient has a confirmed diagnosis of NSCLC.").passed
    assert non_diagnostic_gate(
        "The beneficiary was diagnosed with COPD per the chart, so the panel is indicated.").passed
    # ...but attribution must be adjacent — a distant mention doesn't launder a bare dx.
    assert not non_diagnostic_gate(
        "The record was reviewed. Separately, based on symptoms, the patient has cancer.").passed


def test_non_diagnostic_administrative_document_level():
    # An administrative appeal that grounds the dx in the record may restate it bare later;
    # the SAME text is still flagged for a patient-facing (non-administrative) model.
    appeal = ("Per the medical record, the beneficiary has a documented diagnosis of NSCLC (ICD-10 C34.90). "
              "Medical Necessity: The patient is diagnosed with Stage IV NSCLC, so the panel is warranted.")
    assert non_diagnostic_gate(appeal, administrative=True).passed
    assert not non_diagnostic_gate(appeal, administrative=False).passed
    # An 'appeal' that names a diagnosis with NO record attribution anywhere still fails, even administrative.
    bare = "Medical Necessity: The patient is diagnosed with Stage IV NSCLC, so the panel is warranted."
    assert not non_diagnostic_gate(bare, administrative=True).passed


def test_human_in_the_loop():
    assert human_in_the_loop_gate("Draft appeal prepared for a licensed reviewer to submit.").passed
    assert not human_in_the_loop_gate("The system will auto-submit the appeal.").passed
    assert not human_in_the_loop_gate("Filed automatically with no manual review.").passed


def test_cite_or_abstain():
    assert cite_or_abstain_gate("NCD 90.2 covers this NGS test.", ["NCD 90.2"]).passed
    assert cite_or_abstain_gate("", []).passed          # abstained
    assert not cite_or_abstain_gate("This test is always covered.", []).passed


def test_policy_override():
    assert policy_override_gate("DENY", "DENY").passed
    assert policy_override_gate(None, "APPEAL").passed  # no symbolic verdict to override
    assert not policy_override_gate("DENY", "APPEAL").passed


def test_de_identification():
    assert de_identification_gate("Appeal cites NCD 90.2 and the ordered CPT 81420.").passed
    assert not de_identification_gate("Contact patient at 214-555-0173, SSN 123-45-6789.").passed


def test_safety_escalation():
    assert safety_escalation_gate("Reminder to take a short walk today.").passed         # no crisis
    assert safety_escalation_gate("You mentioned chest pain — call 911 immediately.").passed  # crisis + escalation
    assert not safety_escalation_gate("You mentioned chest pain. Let's talk about dinner.").passed


def test_scope_of_practice():
    assert scope_of_practice_gate("Discuss medication options with your prescriber.").passed
    assert not scope_of_practice_gate("Take 20mg of lisinopril twice daily.").passed
    assert not scope_of_practice_gate("Administer 500 mg every 8 hours.").passed


def test_honesty():
    assert honesty_gate("Modelled target; results are illustrative and cited.").passed
    assert not honesty_gate("Our engine is 100% accurate.").passed
    assert not honesty_gate("The platform has zero hallucinations.").passed


def test_run_all_gates_clean_output_passes_all():
    results = run_all_gates(
        "Draft: NCD 90.2 supports coverage for the ordered NGS panel; a licensed "
        "reviewer should verify and submit. Decision support only, not a diagnosis.",
        claim="NCD 90.2 supports coverage for the ordered NGS panel.",
        citations=["NCD 90.2"],
        symbolic_verdict="APPEAL",
        llm_conclusion="APPEAL",
    )
    assert len(results) == 8
    assert all(r.passed for r in results), [r for r in results if not r.passed]


def test_run_all_gates_catches_multiple_violations():
    results = run_all_gates(
        "The patient has cancer; the system will auto-submit. It is 100% accurate. "
        "SSN 123-45-6789.",
        claim="This is always covered.",
        citations=[],
        symbolic_verdict="DENY",
        llm_conclusion="APPEAL",
    )
    failed = {r.gate for r in results if not r.passed}
    assert {"non_diagnostic", "human_in_the_loop", "honesty", "de_identification",
            "cite_or_abstain", "policy_override"} <= failed
