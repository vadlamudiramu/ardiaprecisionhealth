"""Catalyst trial matching — candidates for human screening, never an enrolment.

The post that prompted this module talks about "recruiting patients for the trial".
Catalyst does not recruit anyone. It compares a DE-IDENTIFIED profile against the
structured fields of registered studies and returns a shortlist for a human to
screen, with the reasoning for every criterion shown.

Two design choices carry the honesty:

1. :class:`PatientProfile` has no field that can hold a HIPAA identifier. Age is an
   AGE BAND, not a date of birth — and bands top out at 90+, matching Safe Harbor
   (45 CFR 164.514(b)(2)(i)(C)), which is also why a band that only partially
   overlaps a trial's age window resolves to :data:`UNDETERMINED` rather than a
   guess. Precision was given up deliberately; pretending to have it back would
   defeat the point.

2. Real eligibility lives in free-text inclusion/exclusion criteria — ECOG status,
   washout periods, lab windows, comorbidities. This module does NOT parse that
   text, and says so on every result via a standing ``free_text_eligibility``
   criterion that is permanently :data:`UNDETERMINED`. A match here means "worth a
   clinician's time", not "qualifies".
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

#: Per-criterion and overall outcomes.
MATCHED = "matched"
EXCLUDED = "excluded"
UNDETERMINED = "undetermined"

#: Only actively recruiting studies can accept a candidate.
RECRUITING_STATUS = "RECRUITING"

#: Top age band, per HIPAA Safe Harbor aggregation of ages over 89.
MAX_BAND_AGE = 90


@dataclass(frozen=True)
class AgeBand:
    """An age RANGE, never an exact age. ``high=None`` means "90 and over"."""

    low: int
    high: int | None = None

    def __post_init__(self):
        if self.low < 0:
            raise ValueError("age band low must be >= 0")
        if self.high is not None and self.high < self.low:
            raise ValueError("age band high must be >= low")
        if self.low >= MAX_BAND_AGE and self.high is not None:
            raise ValueError("ages 90+ must be an open band (high=None) per Safe Harbor")

    @property
    def label(self) -> str:
        return f"{self.low}+" if self.high is None else f"{self.low}-{self.high}"


@dataclass(frozen=True)
class PatientProfile:
    """A de-identified candidate profile. No names, dates, MRNs or contact details."""

    conditions: tuple[str, ...] = ()
    age_band: AgeBand | None = None
    sex: str = ""                          # "male" | "female" | "" (unspecified)
    biomarkers: tuple[str, ...] = ()
    region: str = ""                       # e.g. "Texas" or "United States"


@dataclass(frozen=True)
class TrialCriteria:
    """The structured, machine-comparable part of a registered study."""

    nct_id: str
    title: str
    status: str
    conditions: tuple[str, ...] = ()
    min_age_years: int | None = None
    max_age_years: int | None = None
    sex: str = ""                          # "ALL" | "MALE" | "FEMALE"
    phase: str = ""
    locations: tuple[str, ...] = ()
    eligibility_text: str = ""             # free text — deliberately NOT parsed

    @property
    def url(self) -> str:
        return f"https://clinicaltrials.gov/study/{self.nct_id}"


@dataclass(frozen=True)
class CriterionResult:
    criterion: str
    status: str
    reason: str


@dataclass
class MatchResult:
    """One study assessed against one profile, with the full per-criterion trace."""

    trial: TrialCriteria
    verdict: str
    criteria: list[CriterionResult] = field(default_factory=list)

    @property
    def matched_count(self) -> int:
        return sum(1 for c in self.criteria if c.status == MATCHED)

    @property
    def undetermined(self) -> list[CriterionResult]:
        return [c for c in self.criteria if c.status == UNDETERMINED]


def _norm(term: str) -> str:
    """Lowercase and collapse punctuation so condition terms compare sanely."""
    return re.sub(r"[^a-z0-9 ]+", " ", (term or "").lower()).strip()


def _terms(values) -> set:
    """Split a set of phrases into comparable word-level tokens plus whole phrases."""
    out: set = set()
    for v in values or ():
        n = _norm(v)
        if not n:
            continue
        out.add(n)
        out.update(w for w in n.split() if len(w) > 3)
    return out


def _check_status(t: TrialCriteria) -> CriterionResult:
    if not t.status:
        return CriterionResult("recruiting_status", UNDETERMINED, "study status not published")
    if t.status.upper().replace(" ", "_") != RECRUITING_STATUS:
        return CriterionResult("recruiting_status", EXCLUDED, f"status is {t.status}, not recruiting")
    return CriterionResult("recruiting_status", MATCHED, "actively recruiting")


def _check_condition(p: PatientProfile, t: TrialCriteria) -> CriterionResult:
    if not p.conditions:
        return CriterionResult("condition", UNDETERMINED, "no condition given in the profile")
    if not t.conditions:
        return CriterionResult("condition", UNDETERMINED, "study lists no structured condition")
    overlap = _terms(p.conditions) & _terms(t.conditions)
    if overlap:
        return CriterionResult("condition", MATCHED, "shared term(s): " + ", ".join(sorted(overlap)[:3]))
    return CriterionResult("condition", EXCLUDED,
                           f"no overlap with study conditions: {', '.join(t.conditions[:3])}")


def _check_age(p: PatientProfile, t: TrialCriteria) -> CriterionResult:
    if p.age_band is None:
        return CriterionResult("age", UNDETERMINED, "no age band given in the profile")
    if t.min_age_years is None and t.max_age_years is None:
        return CriterionResult("age", UNDETERMINED, "study publishes no age limits")
    lo, hi = p.age_band.low, p.age_band.high
    t_lo = t.min_age_years if t.min_age_years is not None else 0
    t_hi = t.max_age_years if t.max_age_years is not None else 200
    band_hi = hi if hi is not None else 200
    if band_hi < t_lo or lo > t_hi:
        return CriterionResult("age", EXCLUDED,
                               f"band {p.age_band.label} lies outside the study window {t_lo}-{t_hi}")
    if lo >= t_lo and band_hi <= t_hi:
        return CriterionResult("age", MATCHED, f"band {p.age_band.label} within {t_lo}-{t_hi}")
    # Partial overlap: the exact age was deliberately not collected, so this cannot
    # be resolved here — a screener with the chart can resolve it in one look.
    return CriterionResult("age", UNDETERMINED,
                           f"band {p.age_band.label} only partly overlaps {t_lo}-{t_hi}; "
                           "exact age not collected by design")


def _check_sex(p: PatientProfile, t: TrialCriteria) -> CriterionResult:
    if not t.sex:
        return CriterionResult("sex", UNDETERMINED, "study publishes no sex eligibility")
    ts = t.sex.upper()
    if ts == "ALL":
        return CriterionResult("sex", MATCHED, "study accepts all sexes")
    if not p.sex:
        return CriterionResult("sex", UNDETERMINED, f"study restricted to {ts}; profile unspecified")
    if p.sex.upper() == ts:
        return CriterionResult("sex", MATCHED, f"profile matches study restriction ({ts})")
    return CriterionResult("sex", EXCLUDED, f"study restricted to {ts}")


def _check_biomarkers(p: PatientProfile, t: TrialCriteria) -> CriterionResult:
    if not p.biomarkers:
        return CriterionResult("biomarkers", UNDETERMINED, "no biomarkers given in the profile")
    hay = _norm(t.eligibility_text + " " + t.title)
    hits = [b for b in p.biomarkers if _norm(b) and _norm(b) in hay]
    if hits:
        return CriterionResult("biomarkers", MATCHED,
                               "study text mentions: " + ", ".join(hits[:3]))
    return CriterionResult("biomarkers", UNDETERMINED,
                           "no profile biomarker appears in the study text; "
                           "biomarker eligibility is often unpublished")


def _check_region(p: PatientProfile, t: TrialCriteria) -> CriterionResult:
    if not p.region:
        return CriterionResult("region", UNDETERMINED, "no region given in the profile")
    if not t.locations:
        return CriterionResult("region", UNDETERMINED, "study publishes no site locations")
    r = _norm(p.region)
    if any(r and r in _norm(loc) for loc in t.locations):
        return CriterionResult("region", MATCHED, f"a site is listed in {p.region}")
    return CriterionResult("region", UNDETERMINED,
                           f"no listed site in {p.region}; travel or new sites may still apply")


def _free_text_criterion() -> CriterionResult:
    """Always undetermined — this module does not read inclusion/exclusion prose."""
    return CriterionResult(
        "free_text_eligibility", UNDETERMINED,
        "inclusion/exclusion prose (labs, performance status, washout, comorbidity) "
        "is not parsed by Catalyst and must be screened by a human")


def match_one(p: PatientProfile, t: TrialCriteria) -> MatchResult:
    """Assess one study against one profile. Any EXCLUDED criterion excludes."""
    checks = [
        _check_status(t),
        _check_condition(p, t),
        _check_age(p, t),
        _check_sex(p, t),
        _check_biomarkers(p, t),
        _check_region(p, t),
        _free_text_criterion(),
    ]
    if any(c.status == EXCLUDED for c in checks):
        verdict = EXCLUDED
    elif any(c.status == UNDETERMINED for c in checks):
        verdict = UNDETERMINED
    else:
        verdict = MATCHED
    return MatchResult(t, verdict, checks)


@dataclass
class ScreeningList:
    """The output of trial matching: a shortlist for a human, plus what was ruled out."""

    profile_terms: tuple[str, ...]
    results: list[MatchResult] = field(default_factory=list)
    caveat: str = (
        "These are candidates for human screening, not eligibility determinations. "
        "Catalyst does not read free-text inclusion/exclusion criteria and does not "
        "contact, enrol or rank patients. A qualified screener confirms eligibility."
    )

    @property
    def candidates_for_screening(self) -> list[MatchResult]:
        """Not-excluded studies, best-evidenced first."""
        keep = [r for r in self.results if r.verdict != EXCLUDED]
        return sorted(keep, key=lambda r: (-r.matched_count, r.trial.nct_id))

    @property
    def excluded(self) -> list[MatchResult]:
        return [r for r in self.results if r.verdict == EXCLUDED]

    def summary(self) -> str:
        return (f"{len(self.candidates_for_screening)} candidate study(ies) for human "
                f"screening; {len(self.excluded)} excluded on structured criteria")


def match(p: PatientProfile, trials: list[TrialCriteria] | None) -> ScreeningList:
    """Match a de-identified profile against registered studies."""
    results = [match_one(p, t) for t in (trials or [])]
    return ScreeningList(profile_terms=tuple(p.conditions), results=results)
