"""Tests for Studio research grounding — the JSON parsers and the grounding block.
Pure functions only; no network calls, so these are deterministic and offline-safe."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "ardia-studio-app"))
import research as R  # noqa: E402

PUBMED_SAMPLE = {
    "result": {
        "uids": ["31536761", "0000000"],
        "31536761": {"title": "GOLD 2019 report: COPD management.", "source": "Chest", "pubdate": "2019 Nov"},
        "0000000": {"title": "", "source": "X", "pubdate": "2020"},  # no title -> dropped
    }
}

TRIALS_SAMPLE = {
    "studies": [
        {"protocolSection": {
            "identificationModule": {"nctId": "NCT01234567", "briefTitle": "A Study of Inhaled X in COPD"},
            "statusModule": {"overallStatus": "RECRUITING"}}},
        {"protocolSection": {"identificationModule": {"nctId": "", "briefTitle": "no id"}}},  # dropped
    ]
}


def test_parse_pubmed_summary():
    out = R.parse_pubmed_summary(PUBMED_SAMPLE)
    assert len(out) == 1                      # empty-title entry dropped
    s = out[0]
    assert s["source"] == "PubMed"
    assert s["id"] == "31536761"
    assert s["title"] == "GOLD 2019 report: COPD management"   # trailing period stripped
    assert s["journal"] == "Chest" and s["year"] == "2019"
    assert s["url"] == "https://pubmed.ncbi.nlm.nih.gov/31536761/"


def test_parse_trials():
    out = R.parse_trials(TRIALS_SAMPLE)
    assert len(out) == 1                      # no-id entry dropped
    s = out[0]
    assert s["source"] == "ClinicalTrials.gov"
    assert s["id"] == "NCT01234567"
    assert s["status"] == "RECRUITING"
    assert s["url"] == "https://clinicaltrials.gov/study/NCT01234567"


def test_parsers_tolerate_empty_or_garbage():
    assert R.parse_pubmed_summary({}) == []
    assert R.parse_trials({}) == []
    assert R.parse_pubmed_summary({"result": {"uids": []}}) == []


def test_grounding_block_numbers_sources():
    sources = R.parse_pubmed_summary(PUBMED_SAMPLE) + R.parse_trials(TRIALS_SAMPLE)
    block = R.grounding_block(sources)
    assert "[1]" in block and "[2]" in block
    assert "pubmed.ncbi.nlm.nih.gov" in block
    assert "clinicaltrials.gov/study/NCT01234567" in block
    assert "if none fits a claim, say so" in block


def test_grounding_block_empty_when_no_sources():
    assert R.grounding_block([]) == ""


def test_gather_sources_skips_short_queries_without_network():
    # too-short queries return [] immediately (no network call attempted)
    assert R.gather_sources("", 3) == []
    assert R.gather_sources("ab", 3) == []
    assert R.gather_sources(None, 3) == []


def test_keywords_strips_filler_keeps_medical_terms():
    # A raw sentence sent to PubMed's AND-search matches nothing; _keywords must
    # drop instruction/filler words and keep content terms (incl. gene tokens).
    q = "Summarize the evidence for CYP2C19 pharmacogenomic testing to guide clopidogrel therapy. Cite sources."
    toks = R._keywords(q).split()
    low = [t.lower() for t in toks]
    for filler in ("summarize", "the", "evidence", "for", "to", "guide", "cite", "sources"):
        assert filler not in low
    assert "CYP2C19" in toks           # alphanumeric medical token preserved
    assert "clopidogrel" in low
    assert len(toks) == len(set(low))  # deduped
    assert len(toks) <= 8              # capped


def test_keywords_dedupes_and_caps():
    toks = R._keywords("aspirin ASPIRIN aspirin warfarin " + " ".join(f"drug{i}" for i in range(20))).split()
    assert len(toks) <= 8
    assert sum(1 for t in toks if t.lower() == "aspirin") == 1


def test_keywords_empty_on_all_filler():
    assert R._keywords("what is the of and to for") == ""
