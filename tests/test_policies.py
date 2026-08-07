"""Tests for CMS coverage-policy grounding (match_policies). Pure functions, no network.

Every LCD id/URL in policies.py was hand-verified against the live CMS Medicare
Coverage Database; these tests lock the matching behaviour and the shape of the
citation dicts so a reimbursement answer can only ever surface real, linkable LCDs.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "ardia-studio-app"))
import policies as P  # noqa: E402


def test_every_policy_is_wellformed():
    for p in P.POLICIES:
        assert re.fullmatch(r"L\d{4,6}", p["lcd_id"]), p["lcd_id"]
        assert p["title"] and isinstance(p["keywords"], list) and p["keywords"]
        assert isinstance(p["cpt_codes"], list)


def test_ngs_query_matches_ngs_lcd_by_keyword():
    # The classic 81455 large-panel denial: 81455 isn't in a verified code list, so the
    # match comes from topic keywords — and it must return a real NGS solid-tumor LCD.
    out = P.match_policies("Payer denied 81455, a large NGS panel, on a stage IV NSCLC patient. Build the appeal.")
    assert out, "expected at least one policy"
    ids = [s["id"] for s in out]
    assert any(i in ("L38045", "L38158") for i in ids)         # NGS solid tumors
    assert "L35025" in ids                                     # MolDX MDT umbrella (molecular CPT present)
    for s in out:
        assert s["source"] == "CMS Medicare Coverage Database (LCD)"
        assert s["url"].startswith("https://www.cms.gov/medicare-coverage-database/view/lcd.aspx?lcdid=")
        assert s["id"][1:] in s["url"]                         # url carries the real id
        assert s["id"] in s["title"] and "verify" in s["status"].lower()


def test_toxicology_code_query_matches_drug_testing_lcd():
    out = P.match_policies("Definitive urine drug test 80305 denied as not medically necessary.")
    ids = [s["id"] for s in out]
    assert any(i in ("L34645", "L36029", "L36393") for i in ids)


def test_pgx_query_matches_pgx_lcd():
    out = P.match_policies("CYP2C19 pharmacogenomic testing, CPT 81225, for clopidogrel.")
    assert any(s["id"] in ("L38294", "L38335") for s in out)


def test_no_match_and_empty_query_return_empty():
    assert P.match_policies("what time is my appointment tomorrow") == []
    assert P.match_policies("") == []
    assert P.match_policies(None) == []


def test_dedupes_by_title_and_caps():
    out = P.match_policies("urine drug testing toxicology 80305 80306 80307 g0480 g0659 presumptive definitive", n=2)
    titles = [s["title"].rsplit(" (", 1)[0] for s in out]
    assert len(titles) == len(set(titles))     # no duplicate policy titles
    assert len(out) <= 2                        # respects the cap
