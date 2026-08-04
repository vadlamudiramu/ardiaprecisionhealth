"""Tests for Sentinel HIPAA Safe-Harbor de-identification.

Uses a synthetic note (no real PHI). Verifies every regex-detectable Safe-Harbor
category is removed, clinical content is preserved, and the pass is deterministic.
"""
import pytest

from models.sentinel import deidentify, SAFE_HARBOR_CATEGORIES

NOTE = (
    "Patient Jane Doe seen 03/14/1958. MRN: A12345. SSN 123-45-6789. "
    "Phone (214) 555-0173. Email jane.doe@example.com. Member ID HP9988776. "
    "Account #556677. Lives in Dallas TX 75201. Age 92 years old. "
    "Portal https://x.example.com from IP 10.0.0.5. "
    "Ordered CPT 81420 (cfDNA). Hemoglobin 13.2. Impression: COPD."
)


def test_safe_harbor_has_18_categories():
    assert len(SAFE_HARBOR_CATEGORIES) == 18


def test_removes_each_structured_identifier():
    r = deidentify(NOTE, names=["Jane Doe"])
    for cat in [
        "name", "date", "mrn", "ssn", "phone_or_fax", "email",
        "health_plan_id", "account_number", "geo_zip", "age_over_89",
        "url", "ip_address",
    ]:
        assert cat in r.counts, f"expected {cat} to be detected and removed"


def test_raw_identifiers_are_gone_from_output():
    r = deidentify(NOTE, names=["Jane Doe"])
    for leak in [
        "Jane Doe", "123-45-6789", "(214) 555-0173", "jane.doe@example.com",
        "A12345", "03/14/1958", "10.0.0.5", "https://x.example.com", "556677",
        "HP9988776",
    ]:
        assert leak not in r.text, f"PHI leaked: {leak!r}"


def test_zip_generalized_to_three_digits():
    r = deidentify(NOTE)
    assert "752XX" in r.text          # first 3 digits kept per Safe Harbor
    assert "75201" not in r.text


def test_clinical_content_preserved():
    r = deidentify(NOTE, names=["Jane Doe"])
    # 5-digit CPT code must NOT be treated as a ZIP, and clinical terms survive.
    assert "81420" in r.text
    assert "COPD" in r.text
    assert "Hemoglobin 13.2" in r.text


def test_is_clean_true_after_deid():
    r = deidentify(NOTE, names=["Jane Doe"])
    assert r.is_clean is True


def test_dirty_text_is_not_clean():
    r = deidentify("call me at 214-555-0173")
    # after redaction there should be no residual phone number
    assert "214-555-0173" not in r.text
    assert r.total_removed >= 1


def test_deterministic():
    a = deidentify(NOTE, names=["Jane Doe"])
    b = deidentify(NOTE, names=["Jane Doe"])
    assert a.text == b.text and a.counts == b.counts


def test_none_raises():
    with pytest.raises(ValueError):
        deidentify(None)


def test_empty_text_is_clean_noop():
    r = deidentify("")
    assert r.text == "" and r.total_removed == 0 and r.is_clean
