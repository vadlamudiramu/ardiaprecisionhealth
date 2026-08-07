"""Studio research grounding — live retrieval from PubMed and ClinicalTrials.gov.

Both are public APIs (no key). Retrieval is best-effort: any network/parse failure
returns an empty list rather than raising, so a model run never breaks because a
source lookup timed out. The JSON parsers are pure functions (unit-tested against
sample payloads); the network wrappers are thin and exercised at runtime.

The query passed here is already de-identified by Sentinel, so no PHI is sent to
NCBI / ClinicalTrials.gov.
"""
from __future__ import annotations

import json
import urllib.parse
import urllib.request

_UA = {"User-Agent": "ArdiaStudio/0.1 (research grounding; contact info@ardiahealthlabs.com)"}
_PUBMED = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
_TRIALS = "https://clinicaltrials.gov/api/v2/studies"

# Instruction/filler words that must never enter a PubMed query. PubMed ANDs every
# term, so a raw sentence ("summarize the evidence ... cite sources") matches nothing.
# Keep only content words (medical / drug / gene terms like "CYP2C19", "clopidogrel").
_STOP = frozenset("""
a about above across after against all also an and any are as at based be been before being below
between by can cannot cite could describe detail details did do does done during each evidence
explain for from generate give guidance guide had has have help how i in into is it its list may me
might more most my need no not note of on only or other our out over own patient patients please
provide question report review same shall should show so some source sources studies study such
summarise summarize summary support tell than that the their them then there these this those to
under use used using was we what when where which who why will with would you your
""".split())


def _keywords(text: str, cap: int = 8) -> str:
    """Reduce a natural-language prompt to a compact keyword query for PubMed.

    PubMed ANDs every term, so filler words zero out results. Keep content words
    (incl. alphanumeric tokens like 'CYP2C19'), drop stopwords, dedupe, cap length.
    """
    import re
    out: list[str] = []
    seen: set[str] = set()
    for tok in re.findall(r"[A-Za-z0-9][A-Za-z0-9-]*", text or ""):
        low = tok.lower()
        if len(low) < 3 or low in _STOP or low in seen:
            continue
        seen.add(low)
        out.append(tok)
        if len(out) >= cap:
            break
    return " ".join(out)


def _get_json(url: str, timeout: float = 8.0) -> dict:
    req = urllib.request.Request(url, headers=_UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


# ---- pure parsers (unit-tested, no network) ----
def parse_pubmed_summary(js: dict) -> list[dict]:
    """Turn an NCBI esummary JSON into a list of source dicts."""
    out: list[dict] = []
    res = js.get("result", {}) or {}
    for uid in res.get("uids", []) or []:
        d = res.get(uid, {}) or {}
        title = (d.get("title") or "").strip().rstrip(".")
        if not title:
            continue
        out.append({
            "source": "PubMed",
            "id": uid,
            "title": title,
            "journal": d.get("source", "") or d.get("fulljournalname", ""),
            "year": (d.get("pubdate", "") or "")[:4],
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{uid}/",
        })
    return out


def parse_trials(js: dict) -> list[dict]:
    """Turn a ClinicalTrials.gov v2 studies JSON into a list of source dicts."""
    out: list[dict] = []
    for s in js.get("studies", []) or []:
        ps = s.get("protocolSection", {}) or {}
        idm = ps.get("identificationModule", {}) or {}
        stm = ps.get("statusModule", {}) or {}
        nct = idm.get("nctId", "")
        title = (idm.get("briefTitle") or "").strip()
        if not nct or not title:
            continue
        out.append({
            "source": "ClinicalTrials.gov",
            "id": nct,
            "title": title,
            "status": stm.get("overallStatus", ""),
            "url": f"https://clinicaltrials.gov/study/{nct}",
        })
    return out


# ---- network wrappers (best-effort) ----
def search_pubmed(query: str, n: int = 3, timeout: float = 8.0) -> list[dict]:
    try:
        terms = query.split()
        # PubMed ANDs terms, so a long keyword query can over-narrow to zero hits.
        # Try the full query, then progressively relax to the most salient terms.
        variants = [query]
        if len(terms) > 4:
            variants.append(" ".join(terms[:4]))
        if len(terms) > 3:
            variants.append(" ".join(terms[:3]))
        for v in variants:
            q = urllib.parse.quote(v)
            es = _get_json(f"{_PUBMED}/esearch.fcgi?db=pubmed&retmode=json&retmax={n}&term={q}", timeout)
            ids = (es.get("esearchresult", {}) or {}).get("idlist", []) or []
            if ids:
                su = _get_json(f"{_PUBMED}/esummary.fcgi?db=pubmed&retmode=json&id={','.join(ids)}", timeout)
                return parse_pubmed_summary(su)
        return []
    except Exception:
        return []


def search_trials(query: str, n: int = 2, timeout: float = 8.0) -> list[dict]:
    try:
        q = urllib.parse.quote(query)
        js = _get_json(f"{_TRIALS}?query.term={q}&pageSize={n}", timeout)
        return parse_trials(js)
    except Exception:
        return []


def gather_sources(query: str | None, n: int = 3) -> list[dict]:
    """Best-effort mix of PubMed + trial sources for a query. Never raises."""
    if not query or len(query.strip()) < 3:
        return []
    # Build a keyword query — the raw prompt is a sentence, which PubMed's AND
    # semantics would reduce to zero hits. Fall back to the trimmed text only if
    # the prompt yields no extractable keywords.
    q = _keywords(query) or query.strip()[:120]
    return (search_pubmed(q, n) + search_trials(q, max(1, n - 1)))[: n + 2]


def grounding_block(sources: list[dict]) -> str:
    """Render sources as a numbered block the model may cite; '' if none."""
    if not sources:
        return ""
    lines = []
    for i, s in enumerate(sources, 1):
        meta = " ".join(x for x in [s.get("journal", ""), s.get("year", ""), s.get("status", "")] if x)
        lines.append(f"[{i}] {s['title']} — {s.get('source','')}{(' · ' + meta) if meta else ''} ({s['url']})")
    return (
        "\n\n---\nGrounding sources you MAY cite by number. Cite a source only where it "
        "genuinely supports a statement; if none fits a claim, say so plainly rather than "
        "inventing support:\n" + "\n".join(lines)
    )
