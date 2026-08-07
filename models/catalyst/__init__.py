"""Catalyst — Ardia's governed discovery-to-trial pipeline.

Three stages, each answerable for its own evidence:

  1. **developability** — published filters (Lipinski, Veber, Egan, Ghose, Ro3)
     applied as arithmetic to descriptors that were supplied or fetched, never
     invented. No structure generation, no affinity prediction.
  2. **off_target** — MEASURED bioactivity retrieved from ChEMBL against the
     Bowes in vitro safety panel plus hERG. Targets with nothing measured report
     ``no_data`` and carry the absence-of-evidence caveat in the data itself.
  3. **trial_match** — de-identified profiles compared against the structured
     fields of registered studies, producing candidates for human screening with
     a per-criterion trace. Free-text eligibility is explicitly not parsed.

The deterministic core needs no dependencies and no network. :mod:`sources` adds
optional, keyless, best-effort retrieval from PubChem, ChEMBL and
ClinicalTrials.gov; when it fails, stages degrade to ``no_data`` rather than
fabricating a result.
"""
from .descriptors import Compound, DESCRIPTOR_FIELDS
from .binders import (
    DevelopabilityReport,
    RuleResult,
    assess,
    ligand_efficiency,
    lipophilic_efficiency,
    p_affinity_from_molar,
)
from .offtarget import (
    Activity,
    OffTargetReport,
    PANEL,
    PANEL_CITATION,
    PanelTarget,
    physchem_alerts,
    screen,
)
from .trials import (
    AgeBand,
    MatchResult,
    PatientProfile,
    ScreeningList,
    TrialCriteria,
    match,
)
from .pipeline import (
    DIRECTIVES,
    DiscoveryRequest,
    DiscoveryRun,
    StageResult,
    as_grounding,
    parse_request,
    run,
)

__all__ = [
    "Compound", "DESCRIPTOR_FIELDS",
    "RuleResult", "DevelopabilityReport", "assess",
    "ligand_efficiency", "lipophilic_efficiency", "p_affinity_from_molar",
    "PanelTarget", "PANEL", "PANEL_CITATION", "Activity", "OffTargetReport",
    "physchem_alerts", "screen",
    "AgeBand", "PatientProfile", "TrialCriteria", "MatchResult", "ScreeningList", "match",
    "DiscoveryRequest", "DiscoveryRun", "StageResult", "run", "as_grounding",
    "parse_request", "DIRECTIVES",
]
