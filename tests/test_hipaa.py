"""Red-team tests for the HIPAA/PHI guardrail — try to leak PHI through every vector.

Each test asserts the guard BLOCKS or NEUTRALISES the leak. Synthetic data only.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from models.hipaa import (  # noqa: E402
    GuardContext, preflight, postflight, scrub, guarded_text, MAX_INPUT_CHARS,
)
from models.hipaa import audit, controls  # noqa: E402

PHI = ("Patient Jane Doe, DOB 03/14/1958, MRN A12345, SSN 123-45-6789, "
       "phone (214) 555-0173, jane.doe@example.com — denied 81455.")


def test_preflight_deidentifies_before_sending():
    pf = preflight(PHI, [], GuardContext(model="molec"))
    assert pf.allowed
    # raw identifiers must be gone from the text that would be sent onward
    for leak in ["123-45-6789", "jane.doe@example.com", "(214) 555-0173", "A12345", "03/14/1958"]:
        assert leak not in pf.safe_text, f"PHI leaked to model input: {leak}"
    assert pf.deid["removed"] >= 4


def test_attachment_without_attestation_is_blocked():
    pf = preflight("read this scan", [{"b64": "AAAA", "media_type": "image/png"}], GuardContext(model="lumen"))
    assert not pf.allowed and pf.error == "attest_required" and pf.safe_text == ""


def test_attachment_with_attestation_or_baa_is_allowed():
    att = [{"b64": "AAAA", "media_type": "image/png"}]
    assert preflight("scan", att, GuardContext(attested_synthetic=True)).allowed
    assert preflight("scan", att, GuardContext(has_baa=True)).allowed


def test_non_tls_transport_is_refused():
    pf = preflight(PHI, [], GuardContext(transport_tls=False))
    assert not pf.allowed and pf.error == "transport_insecure"


def test_minimum_necessary_input_cap():
    pf = preflight("x" * (MAX_INPUT_CHARS + 5000), [], GuardContext())
    assert len(pf.safe_text) <= MAX_INPUT_CHARS


def test_postflight_catches_and_redacts_residual_phi_in_output():
    out = "Appeal for the member. Contact 123-45-6789 or jane.doe@example.com."
    pfl = postflight(out, GuardContext(model="molec"))
    assert not pfl.clean and pfl.residual
    assert "123-45-6789" not in pfl.safe_output and "jane.doe@example.com" not in pfl.safe_output


def test_clean_output_passes_postflight():
    assert postflight("The claim's documented diagnosis supports coverage per LCD L38045.", GuardContext()).clean


def test_scrub_redacts_phi_before_logging():
    assert "123-45-6789" not in scrub(PHI) and "jane.doe@example.com" not in scrub(PHI)


def test_audit_events_are_phi_free():
    audit.clear()
    preflight(PHI, [], GuardContext(model="molec"))
    postflight("Contact 123-45-6789", GuardContext(model="molec"))
    events = audit.recent(50)
    assert events, "expected audit events"
    blob = repr(events)
    # no raw identifier may appear anywhere in the audit trail
    for leak in ["123-45-6789", "jane.doe@example.com", "(214) 555-0173", "A12345", "Jane Doe"]:
        assert leak not in blob, f"PHI leaked into audit trail: {leak}"
    # events carry only metadata (counts/booleans/short strings)
    for ev in events:
        for v in (ev.get("meta") or {}).values():
            assert not (isinstance(v, str) and len(v) > 64)


def test_guarded_text_convenience_matches_preflight():
    allowed, payload, pf = guarded_text(PHI, [], GuardContext(model="molec"))
    assert allowed and payload == pf.safe_text and "123-45-6789" not in payload


def test_controls_posture_is_honest_not_overclaimed():
    md = controls.render_markdown()
    assert "not a guarantee against all breach" in md
    assert "synthetic / de-identified data only" in md
    # transmission security is enforced; encryption at rest honestly needs a BAA
    assert any(c["control"].startswith("Transmission security") and c["status"] == "enforced" for c in controls.SECURITY_RULE)
    assert any(c["status"] == "baa_required" for c in controls.SECURITY_RULE)
    assert len(controls.IDENTIFIER_COVERAGE) == 18
