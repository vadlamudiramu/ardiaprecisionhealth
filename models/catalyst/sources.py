"""Catalyst source layer — real public databases, best-effort, keyless.

Same split as :mod:`ardia_studio_app.research`: the PARSERS are pure functions with
offline unit tests, and the network wrappers around them are thin and catch
everything. A source that is slow, rate-limited or down degrades a Catalyst run to
"no data" for that stage; it never raises, and it never causes a fabricated result.

Three public APIs, none of which needs a key:

* **PubChem PUG-REST** — computed molecular descriptors, so Catalyst never has to
  estimate one itself.
* **ChEMBL** — MEASURED bioactivities, and the resolution of HGNC gene symbols to
  ChEMBL target accessions. Resolving these live is deliberate: hardcoding
  accessions would ship IDs that nothing verifies and that silently rot.
* **ClinicalTrials.gov v2** — registered studies with their structured eligibility.

No PHI is ever sent here. Trial queries carry condition terms only.
"""
from __future__ import annotations

import json
import urllib.parse
import urllib.request

from .descriptors import Compound
from .offtarget import Activity
from .trials import TrialCriteria

_UA = {"User-Agent": "ArdiaCatalyst/0.1 (discovery grounding; contact info@ardiahealthlabs.com)"}

_PUBCHEM = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound"
_CHEMBL = "https://www.ebi.ac.uk/chembl/api/data"
_TRIALS = "https://clinicaltrials.gov/api/v2/studies"

#: Descriptor properties requested from PubChem. The SMILES property was renamed in
#: 2025, so it is requested separately and its absence is not an error.
_PUBCHEM_PROPS = (
    "MolecularWeight,XLogP,HBondDonorCount,HBondAcceptorCount,"
    "TPSA,RotatableBondCount,HeavyAtomCount"
)
#: SMILES keys PubChem has used across API revisions, newest first.
_SMILES_KEYS = ("SMILES", "ConnectivitySMILES", "CanonicalSMILES")


def _get_json(url: str, timeout: float = 10.0) -> dict:
    req = urllib.request.Request(url, headers=_UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def _num(v, cast=float):
    """PubChem and ChEMBL both return numbers as strings in places. Be tolerant."""
    if v is None or v == "":
        return None
    try:
        return cast(float(v))
    except (TypeError, ValueError):
        return None


# ---- pure parsers (unit-tested, no network) ----
def parse_pubchem_properties(js: dict, name: str = "") -> Compound | None:
    """Turn a PUG-REST PropertyTable into a :class:`Compound`, or None if empty."""
    props = ((js or {}).get("PropertyTable", {}) or {}).get("Properties", []) or []
    if not props:
        return None
    p = props[0]
    cid = p.get("CID")
    smiles = next((p[k] for k in _SMILES_KEYS if p.get(k)), "")
    return Compound(
        name=name or (str(cid) if cid else "unknown"),
        smiles=smiles,
        mw=_num(p.get("MolecularWeight")),
        logp=_num(p.get("XLogP")),
        hbd=_num(p.get("HBondDonorCount"), int),
        hba=_num(p.get("HBondAcceptorCount"), int),
        tpsa=_num(p.get("TPSA")),
        rot_bonds=_num(p.get("RotatableBondCount"), int),
        heavy_atoms=_num(p.get("HeavyAtomCount"), int),
        provenance=f"PubChem CID {cid}" if cid else "PubChem",
    )


def parse_chembl_targets(js: dict, symbols) -> dict:
    """Map HGNC gene symbol -> ChEMBL target id from a ChEMBL /target response.

    Only human single proteins are accepted, and only when the requested symbol is
    an exact (case-insensitive) synonym of a target component — a substring match
    would happily bind CHRM1 to CHRM10-style names.
    """
    want = {s.upper() for s in symbols or ()}
    out: dict = {}
    # ChEMBL nests synonyms under "target_component_synonyms"; accept the shorter
    # spelling too so a service-side rename degrades to fewer hits, not zero.
    syn_keys = ("target_component_synonyms", "component_synonyms")
    for t in (js or {}).get("targets", []) or []:
        if t.get("target_type") != "SINGLE PROTEIN":
            continue
        if (t.get("organism") or "") != "Homo sapiens":
            continue
        tid = t.get("target_chembl_id")
        if not tid:
            continue
        for comp in t.get("target_components", []) or []:
            for key in syn_keys:
                for syn in comp.get(key, []) or []:
                    s = (syn.get("component_synonym") or "").upper()
                    if s in want and s not in out:
                        out[s] = tid
    return out


def parse_chembl_activities(js: dict, target_symbols: dict | None = None) -> list[Activity]:
    """Turn a ChEMBL /activity response into measured :class:`Activity` records.

    ``target_symbols`` maps ChEMBL target id -> gene symbol (the inverse of
    :func:`parse_chembl_targets`), so each activity can be attributed to a panel
    target. Records whose target is unknown to the panel are dropped.
    """
    by_id = {v: k for k, v in (target_symbols or {}).items()}
    out: list[Activity] = []
    for a in (js or {}).get("activities", []) or []:
        tid = a.get("target_chembl_id") or ""
        mid = a.get("molecule_chembl_id") or ""
        symbol = by_id.get(tid, "")
        if not tid or not mid or not symbol:
            continue
        out.append(Activity(
            target_symbol=symbol,
            target_chembl_id=tid,
            molecule_chembl_id=mid,
            standard_type=a.get("standard_type") or "",
            pchembl=_num(a.get("pchembl_value")),
            assay_chembl_id=a.get("assay_chembl_id") or "",
            assay_description=(a.get("assay_description") or "")[:200],
        ))
    return out


def parse_chembl_molecule(js: dict) -> str:
    """First molecule_chembl_id from a ChEMBL molecule search, or ''."""
    for m in (js or {}).get("molecules", []) or []:
        if m.get("molecule_chembl_id"):
            return m["molecule_chembl_id"]
    return ""


def parse_age(value: str) -> int | None:
    """ClinicalTrials.gov publishes ages as '18 Years' / '6 Months'. Convert to years.

    Sub-year durations floor to 0 rather than rounding up, so an infant study is
    never made to look like it accepts adults.
    """
    if not value:
        return None
    parts = str(value).strip().split()
    if len(parts) < 2:
        return None
    n = _num(parts[0])
    if n is None:
        return None
    unit = parts[1].lower().rstrip("s")
    if unit == "year":
        return int(n)
    if unit == "month":
        return int(n // 12)
    if unit == "week":
        return int(n // 52)
    if unit == "day":
        return int(n // 365)
    return None


def parse_trial_eligibility(js: dict) -> list[TrialCriteria]:
    """Turn a ClinicalTrials.gov v2 studies response into :class:`TrialCriteria`."""
    out: list[TrialCriteria] = []
    for s in (js or {}).get("studies", []) or []:
        ps = s.get("protocolSection", {}) or {}
        idm = ps.get("identificationModule", {}) or {}
        stm = ps.get("statusModule", {}) or {}
        cond = ps.get("conditionsModule", {}) or {}
        des = ps.get("designModule", {}) or {}
        elig = ps.get("eligibilityModule", {}) or {}
        loc = ps.get("contactsLocationsModule", {}) or {}
        nct = idm.get("nctId", "")
        title = (idm.get("briefTitle") or "").strip()
        if not nct or not title:
            continue
        places = []
        for site in loc.get("locations", []) or []:
            bits = [site.get(k, "") for k in ("facility", "city", "state", "country")]
            joined = ", ".join(b for b in bits if b)
            if joined:
                places.append(joined)
        out.append(TrialCriteria(
            nct_id=nct,
            title=title,
            status=stm.get("overallStatus", "") or "",
            conditions=tuple(cond.get("conditions", []) or []),
            min_age_years=parse_age(elig.get("minimumAge", "")),
            max_age_years=parse_age(elig.get("maximumAge", "")),
            sex=(elig.get("sex") or "").upper(),
            phase=", ".join(des.get("phases", []) or []),
            locations=tuple(places[:25]),
            eligibility_text=(elig.get("eligibilityCriteria") or "")[:8000],
        ))
    return out


# ---- network wrappers (best-effort; never raise) ----
def fetch_compound(name: str, timeout: float = 8.0) -> Compound | None:
    """Look up a compound's computed descriptors on PubChem by name. None on failure."""
    if not name or len(name.strip()) < 2:
        return None
    q = urllib.parse.quote(name.strip())
    # SMILES first; if this API revision rejects the property name, retry numerics only.
    for props in (f"{_PUBCHEM_PROPS},SMILES", _PUBCHEM_PROPS):
        try:
            js = _get_json(f"{_PUBCHEM}/name/{q}/property/{props}/JSON", timeout)
            c = parse_pubchem_properties(js, name.strip())
            if c is not None:
                return c
        except Exception:
            continue
    return None


def resolve_targets(symbols, timeout: float = 8.0, max_lookups: int = 5,
                    budget: float = 15.0) -> dict:
    """Resolve HGNC gene symbols to ChEMBL target ids. Partial results are fine.

    One bulk filtered request first; whatever it leaves unresolved is retried
    individually, capped by ``max_lookups`` AND a wall-clock ``budget`` so a broken
    bulk filter degrades to a bounded delay instead of one request per panel target.
    The caps matter: this runs inside a 60-second serverless function. Symbols that
    stay unresolved simply report ``no_data`` downstream.
    """
    import time
    started = time.monotonic()
    syms = [s for s in (symbols or ()) if s]
    if not syms:
        return {}
    q = urllib.parse.quote(",".join(syms))
    url = (f"{_CHEMBL}/target?format=json&limit=1000"
           f"&target_components__target_component_synonyms__component_synonym__in={q}"
           f"&organism=Homo+sapiens&target_type=SINGLE+PROTEIN")
    out: dict = {}
    try:
        out = parse_chembl_targets(_get_json(url, timeout), syms)
    except Exception:
        out = {}
    for s in [s for s in syms if s.upper() not in out][:max_lookups]:
        if time.monotonic() - started > budget:
            break
        try:
            js = _get_json(f"{_CHEMBL}/target/search?q={urllib.parse.quote(s)}&format=json", timeout)
            out.update(parse_chembl_targets(js, [s]))
        except Exception:
            continue
    return out


def resolve_molecule(name: str, timeout: float = 8.0) -> str:
    """Resolve a compound name to a ChEMBL molecule id. '' on failure."""
    if not name or len(name.strip()) < 2:
        return ""
    q = urllib.parse.quote(name.strip())
    try:
        return parse_chembl_molecule(_get_json(f"{_CHEMBL}/molecule/search?q={q}&format=json", timeout))
    except Exception:
        return ""


def fetch_activities(molecule_chembl_id: str, targets: dict,
                     limit: int = 300, timeout: float = 12.0) -> list[Activity]:
    """Fetch measured activities for one molecule across resolved panel targets."""
    if not molecule_chembl_id or not targets:
        return []
    ids = ",".join(sorted(set(targets.values())))
    url = (f"{_CHEMBL}/activity?format=json&limit={limit}"
           f"&molecule_chembl_id={urllib.parse.quote(molecule_chembl_id)}"
           f"&target_chembl_id__in={urllib.parse.quote(ids)}")
    try:
        return parse_chembl_activities(_get_json(url, timeout), targets)
    except Exception:
        return []


def fetch_trials(condition: str, n: int = 10, recruiting_only: bool = True,
                 timeout: float = 10.0) -> list[TrialCriteria]:
    """Fetch registered studies for a condition term. Never sends PHI — terms only."""
    if not condition or len(condition.strip()) < 3:
        return []
    url = (f"{_TRIALS}?query.cond={urllib.parse.quote(condition.strip())}"
           f"&pageSize={max(1, min(n, 50))}")
    if recruiting_only:
        url += "&filter.overallStatus=RECRUITING"
    try:
        return parse_trial_eligibility(_get_json(url, timeout))
    except Exception:
        return []
