"""Catalyst pipeline — the agentic run, and the governance that makes it defensible.

Three stages in order, the same three the industry demo reel promises: assess the
molecule, screen it for off-target liabilities, find trials a patient could be
screened for. What differs here is that each stage is answerable for itself.

  developability -> off_target -> trial_match

Every stage returns a :class:`StageResult` whose ``status`` is one of ``ok``,
``no_data``, ``blocked`` or ``skipped``. There is no fifth option where a stage
quietly produces plausible output it has no evidence for — a stage with nothing to
stand on says ``no_data`` and the run continues honestly without it. That is the
whole reason this is a deterministic pipeline with an LLM narrating the result,
rather than an LLM producing the result.

Governance actually enforced here:

* the trial stage runs :func:`models.hipaa.guard.preflight` BEFORE any query
  leaves the process, so a profile with identifiers stuffed into it is
  de-identified (or refused) rather than matched as-is;
* profile text is NEVER used to build an outbound query — only the caller's
  explicit ``trial_condition`` is. Sentinel redacts structured identifiers, but
  its name handling is roster-based by design, so a name typed into a condition
  field would survive scrubbing; keeping profile text in-process closes that gap
  structurally rather than hoping a regex catches it;
* every stage writes a PHI-free :mod:`models.hipaa.audit` event;
* if the HIPAA guardrail cannot be imported, the trial stage fails CLOSED.

Crucible's output gates are not run here: this pipeline emits structured data, and
the narrative built from it is gated where narratives are gated — in
``ardia-studio-app/server.py``, alongside every other Ardia model.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from . import binders, offtarget, trials
from .descriptors import Compound
from .trials import AgeBand, PatientProfile

try:
    from models.hipaa import audit as phi_audit
    from models.hipaa import guard as phi_guard
    _GUARD_OK = True
except Exception:                                  # pragma: no cover - import guard
    _GUARD_OK = False

#: Stage outcomes.
OK = "ok"
NO_DATA = "no_data"
BLOCKED = "blocked"
SKIPPED = "skipped"

STAGES: tuple[str, ...] = ("developability", "off_target", "trial_match")

MODEL_NAME = "catalyst"


@dataclass
class DiscoveryRequest:
    """What to run. Anything not supplied is fetched when ``online``, else skipped."""

    compound_name: str = ""
    descriptors: Compound | None = None
    #: Measured potency at the INTENDED target, -log10(molar). Never estimated.
    primary_p_affinity: float | None = None
    affinity_source: str = ""
    activities: list | None = None                 # caller-supplied measured activities
    profile: PatientProfile | None = None
    #: The ONLY term that may be sent to ClinicalTrials.gov. Profile text is matched
    #: locally and never leaves the process — see ``_stage_trials``.
    trial_condition: str = ""
    trial_candidates: list | None = None           # caller-supplied TrialCriteria
    online: bool = True


@dataclass
class StageResult:
    stage: str
    status: str
    summary: str
    detail: object = None
    sources: list = field(default_factory=list)
    audit_id: str = ""
    reason: str = ""


@dataclass
class DiscoveryRun:
    """An ordered, auditable record of one Catalyst run."""

    compound: str
    stages: list[StageResult] = field(default_factory=list)
    scope: str = (
        "Catalyst does not design molecules, predict binding, predict off-target "
        "activity, or enrol patients. It applies published filters to descriptors, "
        "reports measured bioactivity, and shortlists trials for human screening."
    )

    def stage(self, name: str) -> StageResult | None:
        return next((s for s in self.stages if s.stage == name), None)

    @property
    def audit_ids(self) -> list:
        return [s.audit_id for s in self.stages if s.audit_id]

    def summary(self) -> str:
        return " | ".join(f"{s.stage}: {s.status}" for s in self.stages)


def _audit(action: str, **extra) -> str:
    if not _GUARD_OK:
        return ""
    return phi_audit.record(action, model=MODEL_NAME, extra=extra)


# ---- stage 1: developability ----
def _stage_developability(req: DiscoveryRequest) -> tuple[StageResult, Compound | None]:
    c = req.descriptors
    sources: list = []
    if c is None and req.online and req.compound_name:
        from . import sources as src
        c = src.fetch_compound(req.compound_name)
    if c is None:
        aid = _audit("catalyst_stage", stage="developability", status=NO_DATA)
        return StageResult("developability", NO_DATA,
                           "No descriptors available for this compound.", None, sources, aid,
                           reason=("no descriptors supplied and none retrieved from PubChem"
                                   if req.online else "no descriptors supplied and the run is offline")), None
    if c.provenance and c.provenance != "caller-supplied":
        sources.append({"source": "PubChem", "id": c.provenance, "title": c.name,
                        "url": f"https://pubchem.ncbi.nlm.nih.gov/#query={c.name}"})
    rep = binders.assess(c, req.primary_p_affinity, req.affinity_source)
    aid = _audit("catalyst_stage", stage="developability", status=OK,
                 rules=len(rep.rules), failed=len(rep.failed))
    return StageResult("developability", OK, rep.summary(), rep, sources, aid), c


# ---- stage 2: off-target ----
def _stage_offtarget(req: DiscoveryRequest, c: Compound | None) -> StageResult:
    if c is None:
        aid = _audit("catalyst_stage", stage="off_target", status=SKIPPED)
        return StageResult("off_target", SKIPPED,
                           "Skipped — no compound to screen.", None, [], aid,
                           reason="the developability stage produced no compound")
    acts = list(req.activities or [])
    sources: list = []
    if not acts and req.online and req.compound_name:
        from . import sources as src
        mol = src.resolve_molecule(req.compound_name)
        targets = src.resolve_targets([t.symbol for t in offtarget.PANEL]) if mol else {}
        acts = src.fetch_activities(mol, targets) if targets else []
        if mol:
            sources.append({"source": "ChEMBL", "id": mol, "title": f"{req.compound_name} bioactivities",
                            "url": f"https://www.ebi.ac.uk/chembl/compound_report_card/{mol}/"})
    rep = offtarget.screen(c, acts, req.primary_p_affinity)
    status = OK if acts else NO_DATA
    reason = "" if acts else (
        "no measured activities retrieved — every panel target reports no_data, which "
        "is not a safety finding")
    aid = _audit("catalyst_stage", stage="off_target", status=status,
                 flagged=len(rep.flagged), measured=len(acts))
    return StageResult("off_target", status, rep.summary(), rep, sources, aid, reason=reason)


# ---- stage 3: trial matching (PHI boundary) ----
def _deidentify_profile(p: PatientProfile) -> tuple[PatientProfile, dict, str, str]:
    """Run the HIPAA guard over a profile's free text before any query leaves.

    Returns (safe_profile, deid_counts, audit_id, block_reason). ``block_reason`` is
    non-empty only when the guard refused the input outright.
    """
    joined = " ".join([*p.conditions, *p.biomarkers, p.region])
    ctx = phi_guard.GuardContext(model=MODEL_NAME, attested_synthetic=True)
    pf = phi_guard.preflight(joined, [], ctx)
    if not pf.allowed:
        return p, {"removed": 0, "categories": []}, pf.audit_id, pf.reason
    scrub = phi_guard.scrub
    safe = PatientProfile(
        conditions=tuple(scrub(t) for t in p.conditions),
        age_band=p.age_band,
        sex=p.sex,
        biomarkers=tuple(scrub(t) for t in p.biomarkers),
        region=scrub(p.region),
    )
    return safe, pf.deid, pf.audit_id, ""


def _stage_trials(req: DiscoveryRequest) -> StageResult:
    p = req.profile
    if p is None:
        aid = _audit("catalyst_stage", stage="trial_match", status=SKIPPED)
        return StageResult("trial_match", SKIPPED, "Skipped — no patient profile supplied.",
                           None, [], aid, reason="trial matching needs a de-identified profile")
    # Fail CLOSED: without the de-identification guardrail this stage does not run.
    if not _GUARD_OK:
        return StageResult("trial_match", BLOCKED,
                           "Blocked — the de-identification guardrail is unavailable.", None, [], "",
                           reason="models.hipaa.guard could not be imported; refusing to query with a profile")
    safe, deid, aid, blocked = _deidentify_profile(p)
    if blocked:
        return StageResult("trial_match", BLOCKED, "Blocked by the HIPAA guardrail.",
                           None, [], aid, reason=blocked)

    cands = list(req.trial_candidates or [])
    sources: list = []
    if not cands and req.online:
        # The outbound query is built ONLY from the caller's explicit trial_condition,
        # never from the profile's own text. Sentinel redacts structured identifiers
        # but its name handling is roster-based by design (see sentinel/deidentify.py),
        # so a name typed into a condition field would survive scrubbing. Profile text
        # is therefore matched locally and never egresses.
        from . import sources as src
        term = (req.trial_condition or "").strip()
        if term:
            cands = src.fetch_trials(term)
            sources.append({"source": "ClinicalTrials.gov", "id": term,
                            "title": f"recruiting studies for {term}",
                            "url": "https://clinicaltrials.gov/api/v2/studies"})
    if not cands:
        _audit("catalyst_stage", stage="trial_match", status=NO_DATA, deid_removed=deid.get("removed", 0))
        return StageResult("trial_match", NO_DATA, "No registered studies retrieved to match against.",
                           None, sources, aid,
                           reason=("no candidate studies supplied, and no trial_condition was given — "
                                   "profile text is never used to build an outbound query"
                                   if req.online and not (req.trial_condition or "").strip()
                                   else "no candidate studies supplied or retrieved"))
    res = trials.match(safe, cands)
    _audit("catalyst_stage", stage="trial_match", status=OK,
           candidates=len(res.candidates_for_screening), excluded=len(res.excluded),
           deid_removed=deid.get("removed", 0))
    return StageResult("trial_match", OK, res.summary(), res, sources, aid)


# ---- request parsing: explicit directives, never inference ----
#: Directives Catalyst understands, one per line: ``key: value``.
DIRECTIVES: tuple[str, ...] = (
    "compound", "condition", "affinity", "affinity_source", "age", "sex", "region", "biomarkers",
)

_DIRECTIVE_RE = re.compile(r"^\s*(%s)\s*:\s*(.+?)\s*$" % "|".join(DIRECTIVES), re.I | re.M)
_AGE_RANGE_RE = re.compile(r"^(\d{1,3})\s*(?:-|to|–)\s*(\d{1,3})$", re.I)
_AGE_OPEN_RE = re.compile(r"^(\d{1,3})\s*\+$")


def parse_request(text: str) -> tuple[DiscoveryRequest, list]:
    """Build a :class:`DiscoveryRequest` from explicit ``key: value`` directives.

    Deliberately NOT free-text understanding. A model asked to infer "which molecule
    did they mean" will always produce an answer, including when the text names no
    molecule at all — and a confidently wrong compound poisons all three stages. So
    Catalyst reads directives and nothing else, and reports what it ignored.

    Returns the request plus human-readable notes about anything skipped.
    """
    found: dict = {}
    for key, value in _DIRECTIVE_RE.findall(text or ""):
        found.setdefault(key.lower(), value.strip())
    notes: list = []

    p_aff = None
    if "affinity" in found:
        try:
            p_aff = float(found["affinity"])
        except ValueError:
            notes.append(f"Ignored affinity {found['affinity']!r}: expected a number "
                         "(-log10 molar, e.g. 8.5).")
    source = found.get("affinity_source", "")
    if p_aff is not None and not source:
        p_aff = None
        notes.append("Ignored the affinity: no `affinity_source:` was given, and an "
                     "unattributed potency cannot be told apart from a guess.")

    band = None
    if "age" in found:
        raw = found["age"]
        m_range, m_open = _AGE_RANGE_RE.match(raw), _AGE_OPEN_RE.match(raw)
        try:
            if m_range:
                band = AgeBand(int(m_range.group(1)), int(m_range.group(2)))
            elif m_open:
                band = AgeBand(int(m_open.group(1)), None)
            else:
                notes.append(f"Ignored age {raw!r}: give a BAND, not an exact age "
                             "(e.g. `45-60` or `65+`).")
        except ValueError as e:
            notes.append(f"Ignored age {raw!r}: {e}.")

    condition = found.get("condition", "")
    biomarkers = tuple(b.strip() for b in found.get("biomarkers", "").split(",") if b.strip())
    sex = found.get("sex", "").lower()
    region = found.get("region", "")

    profile = None
    if any([condition, band, sex, biomarkers, region]):
        profile = PatientProfile(
            conditions=(condition,) if condition else (),
            age_band=band, sex=sex, biomarkers=biomarkers, region=region)

    if not found.get("compound"):
        notes.append("No `compound:` directive found — the developability and "
                     "off-target stages need a named compound.")
    if profile is not None and not condition:
        notes.append("No `condition:` directive found — trial matching needs one, and "
                     "Catalyst will not infer it from the rest of the text.")

    return DiscoveryRequest(
        compound_name=found.get("compound", ""),
        primary_p_affinity=p_aff,
        affinity_source=source,
        profile=profile,
        trial_condition=condition,
    ), notes


def run(req: DiscoveryRequest) -> DiscoveryRun:
    """Execute the three stages in order, with governance between them."""
    _audit("catalyst_run_start", online=bool(req.online))
    dev, compound = _stage_developability(req)
    out = DiscoveryRun(compound=req.compound_name or (compound.name if compound else "unnamed"))
    out.stages = [dev, _stage_offtarget(req, compound), _stage_trials(req)]
    _audit("catalyst_run_end", stages=len(out.stages),
           ok=sum(1 for s in out.stages if s.status == OK))
    return out


# ---- rendering: what an LLM is allowed to narrate ----
def as_grounding(run_: DiscoveryRun, max_targets: int = 8, max_trials: int = 5) -> str:
    """Render a completed run as the text block a narrating model may cite.

    The caveats travel WITH the numbers. A model handed this block is being given
    computed results to explain, not a topic to improvise on.
    """
    L: list[str] = ["CATALYST RUN — computed results. Narrate ONLY what appears below.",
                    f"Scope: {run_.scope}", f"Compound: {run_.compound}"]

    dev = run_.stage("developability")
    L.append("\n## Stage 1 — developability (published filters)")
    if dev and dev.status == OK and dev.detail is not None:
        rep = dev.detail
        L.append(f"Descriptor provenance: {rep.provenance}. {rep.summary()}")
        for r in rep.rules:
            if r.verdict == binders.NOT_EVALUATED:
                L.append(f"- {r.rule}: NOT EVALUATED (missing {', '.join(r.missing_descriptors)}) [{r.citation}]")
            else:
                bits = ("; ".join(r.violations)) if r.violations else "no violations"
                L.append(f"- {r.rule}: {r.verdict.upper()} — {bits} [{r.citation}]")
            if r.unevaluated_criteria:
                L.append(f"  (criteria not checked: {'; '.join(r.unevaluated_criteria)})")
        if rep.ligand_efficiency is not None:
            L.append(f"- Ligand efficiency {rep.ligand_efficiency:.3f} kcal/mol/heavy atom "
                     f"(from measured affinity — source: {rep.affinity_source})")
        if rep.lipophilic_efficiency is not None:
            L.append(f"- Lipophilic efficiency (LLE) {rep.lipophilic_efficiency:.2f}")
        L.append(f"CAVEAT: {rep.caveat}")
    else:
        L.append(f"{(dev.status if dev else NO_DATA).upper()} — {(dev.reason if dev else '')}")

    off = run_.stage("off_target")
    L.append("\n## Stage 2 — off-target liabilities (MEASURED, not predicted)")
    if off and off.detail is not None:
        rep = off.detail
        L.append(f"Panel: {rep.panel_citation}")
        L.append(rep.summary())
        shown = [f for f in rep.findings if f.status != offtarget.NO_DATA][:max_targets]
        for f in shown:
            margin = ""
            if f.selectivity_log is not None:
                margin = (f"; selectivity margin {f.selectivity_log:.1f} log units "
                          f"({'adequate' if f.selectivity_adequate else 'BELOW the 2-log rule of thumb'})")
            L.append(f"- {f.target.symbol} ({f.target.name}): {f.status.upper()} "
                     f"best pChEMBL {f.best_pchembl}{margin} — concern: {f.target.concern}")
        if not shown:
            L.append("- No panel target had a retrieved measurement.")
        L.append(f"- {len(rep.no_data)}/{len(rep.findings)} panel targets: NO DATA. {rep.absence_caveat}")
        for a in rep.alerts:
            L.append(f"- HEURISTIC ALERT {a.alert}: {a.detail} — {a.concern} [{a.citation}]")
        L.append(f"CAVEAT: {rep.caveat}")
    else:
        L.append(f"{(off.status if off else NO_DATA).upper()} — {(off.reason if off else '')}")

    tr = run_.stage("trial_match")
    L.append("\n## Stage 3 — trial candidates for HUMAN screening")
    if tr and tr.status == OK and tr.detail is not None:
        res = tr.detail
        L.append(res.summary())
        for m in res.candidates_for_screening[:max_trials]:
            L.append(f"- {m.trial.nct_id} [{m.verdict.upper()}] {m.trial.title} "
                     f"({m.trial.phase or 'phase not stated'}) {m.trial.url}")
            for c in m.criteria:
                L.append(f"    · {c.criterion}: {c.status} — {c.reason}")
        L.append(f"CAVEAT: {res.caveat}")
    else:
        L.append(f"{(tr.status if tr else SKIPPED).upper()} — {(tr.reason if tr else '')}")

    L.append("\nIf a stage above says NO DATA, BLOCKED or SKIPPED, say so plainly. "
             "Do not fill the gap with general knowledge, and do not present any "
             "number that does not appear above.")
    return "\n".join(L)
