"""Tests that the Studio pipeline actually runs Sentinel (input de-id) and
Crucible (output gates) — the guardrails execute, they aren't just described."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "ardia-studio-app"))
import guardrails as G  # noqa: E402


def test_deid_input_strips_phi_before_model():
    clean, rep = G.deid_input("Call Jane at 214-555-0173, SSN 123-45-6789 re: results.")
    assert "214-555-0173" not in clean
    assert "123-45-6789" not in clean
    assert rep["removed"] >= 2
    assert "phone_or_fax" in rep["categories"] and "ssn" in rep["categories"]


def test_deid_input_empty_is_safe():
    clean, rep = G.deid_input("")
    assert clean == "" and rep["removed"] == 0


def test_gate_output_shape():
    gates = G.gate_output("Decision support only — not a diagnosis. Consult a clinician.")
    assert len(gates) == 6
    assert all({"gate", "passed", "reason"} <= set(g) for g in gates)


def test_clean_answer_passes_all_studio_gates():
    answer = ("Some values look outside the usual range — discuss them with your "
              "clinician. If you have chest pain, call 911 now. This is not a diagnosis.")
    gates = G.gate_output(answer)
    assert all(g["passed"] for g in gates), [g for g in gates if not g["passed"]]


def test_unsafe_answer_is_caught():
    bad = "You have cancer. Take 40mg of drugX daily. It is 100% accurate. SSN 123-45-6789."
    gates = G.gate_output(bad)
    failed = {g["gate"] for g in gates if not g["passed"]}
    assert {"non_diagnostic", "scope_of_practice", "honesty", "de_identification"} <= failed


def test_summarize_reports_pass_state():
    gates = G.gate_output("Decision support only, not a diagnosis. Consult a clinician.")
    s = G.summarize(gates)
    assert s["n_total"] == 6
    assert s["passed"] is (len(s["failed"]) == 0)
