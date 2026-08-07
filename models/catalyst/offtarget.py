"""Catalyst off-target screening — retrieved MEASURED liabilities, not predictions.

The honest distinction this module exists to enforce: Catalyst does not predict
whether a compound hits an off-target. It reports what has already been MEASURED
against a published safety panel, with the assay record behind every flag, and it
says plainly when nothing has been measured.

That last case is the one that gets misread, so it is a first-class status
(:data:`NO_DATA`) carrying :data:`ABSENCE_CAVEAT` in the returned data structure
rather than in page copy that a later edit can drop. No measured activity at a
target means nobody has looked, or nobody has published — it is not a clean bill
of health.

The panel itself is the in vitro pharmacological profile proposed by Bowes et al.
(2012), plus hERG, which regulators require in the ICH S7B core battery. Targets
are identified by HGNC gene symbol only; ChEMBL target IDs are resolved live in
:mod:`models.catalyst.sources` and never hardcoded, so this file cannot ship a
stale or invented accession.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .descriptors import Compound

#: Per-target screening outcomes.
FLAGGED = "flagged"          # measured potency at or below 1 uM
WEAK = "weak"                # measured potency between 1 and 10 uM
NOT_FLAGGED = "not_flagged"  # measured, and weaker than 10 uM
NO_DATA = "no_data"          # nothing measured — see ABSENCE_CAVEAT

#: pChEMBL = -log10(molar IC50/EC50/Ki/Kd). 6.0 = 1 uM, 5.0 = 10 uM — the
#: concentration at which in vitro safety panels are conventionally screened.
FLAG_PCHEMBL = 6.0
WEAK_PCHEMBL = 5.0

#: Conventional med-chem selectivity expectation: two log units (100-fold) between
#: the intended potency and an off-target activity. A rule of thumb, labelled as one.
SELECTIVITY_LOG_MARGIN = 2.0

ABSENCE_CAVEAT = (
    "No measured activity was found for this target. Absence of evidence is not "
    "evidence of safety — it means no assay result was retrieved, which is the "
    "expected state for most targets and most compounds."
)


@dataclass(frozen=True)
class PanelTarget:
    """One target on the in vitro safety panel, identified by HGNC gene symbol."""

    symbol: str
    name: str
    concern: str


#: Minimum in vitro pharmacological profiling panel. Gene symbols are HGNC.
PANEL: tuple[PanelTarget, ...] = (
    # --- cardiovascular ---
    PanelTarget("KCNH2", "hERG potassium channel", "QT prolongation, torsades de pointes"),
    PanelTarget("SCN5A", "Nav1.5 sodium channel", "conduction slowing, arrhythmia"),
    PanelTarget("CACNA1C", "Cav1.2 calcium channel", "negative inotropy, hypotension"),
    PanelTarget("ADRB1", "beta-1 adrenoceptor", "heart-rate and contractility change"),
    PanelTarget("ADRB2", "beta-2 adrenoceptor", "tremor, bronchial and metabolic effects"),
    PanelTarget("ADRA1A", "alpha-1A adrenoceptor", "orthostatic hypotension"),
    PanelTarget("ADRA2A", "alpha-2A adrenoceptor", "sedation, blood-pressure change"),
    # --- CNS / neuropsychiatric ---
    PanelTarget("HTR2B", "serotonin 5-HT2B receptor", "valvular heart disease on chronic agonism"),
    PanelTarget("HTR2A", "serotonin 5-HT2A receptor", "hallucination, sedation"),
    PanelTarget("HTR1A", "serotonin 5-HT1A receptor", "serotonergic CNS effects"),
    PanelTarget("DRD2", "dopamine D2 receptor", "extrapyramidal symptoms, hyperprolactinaemia"),
    PanelTarget("CHRM1", "muscarinic M1 receptor", "cognitive impairment"),
    PanelTarget("CHRM2", "muscarinic M2 receptor", "tachycardia"),
    PanelTarget("CHRM3", "muscarinic M3 receptor", "dry mouth, urinary retention, GI stasis"),
    PanelTarget("HRH1", "histamine H1 receptor", "sedation, weight gain"),
    PanelTarget("GABRA1", "GABA-A receptor alpha-1", "sedation, dependence"),
    PanelTarget("GRIN1", "NMDA receptor GluN1", "dissociative and neurotoxic effects"),
    PanelTarget("OPRM1", "mu opioid receptor", "respiratory depression, dependence"),
    PanelTarget("OPRK1", "kappa opioid receptor", "dysphoria, sedation"),
    PanelTarget("OPRD1", "delta opioid receptor", "seizure risk"),
    PanelTarget("CNR1", "cannabinoid CB1 receptor", "psychiatric adverse effects"),
    PanelTarget("CNR2", "cannabinoid CB2 receptor", "immunomodulation"),
    PanelTarget("ADORA1", "adenosine A1 receptor", "bradycardia, AV block"),
    PanelTarget("ADORA2A", "adenosine A2A receptor", "hypotension"),
    PanelTarget("AVPR1A", "vasopressin V1a receptor", "vasoconstriction"),
    # --- transporters ---
    PanelTarget("SLC6A4", "serotonin transporter (SERT)", "serotonin syndrome, withdrawal"),
    PanelTarget("SLC6A3", "dopamine transporter (DAT)", "abuse liability"),
    PanelTarget("SLC6A2", "norepinephrine transporter (NET)", "hypertension, tachycardia"),
    # --- enzymes ---
    PanelTarget("ACHE", "acetylcholinesterase", "cholinergic crisis"),
    PanelTarget("PTGS1", "cyclooxygenase-1", "GI ulceration and bleeding"),
    PanelTarget("PTGS2", "cyclooxygenase-2", "cardiovascular thrombotic risk"),
    PanelTarget("MAOA", "monoamine oxidase A", "hypertensive crisis with tyramine"),
    PanelTarget("PDE3A", "phosphodiesterase 3A", "arrhythmia, mortality in heart failure"),
    PanelTarget("PDE4D", "phosphodiesterase 4D", "emesis"),
    PanelTarget("LCK", "lymphocyte-specific kinase", "immunosuppression"),
    # --- nuclear receptors ---
    PanelTarget("NR3C1", "glucocorticoid receptor", "metabolic and immune effects"),
    PanelTarget("AR", "androgen receptor", "endocrine disruption"),
)

PANEL_CITATION = (
    "Bowes et al. 2012, Nat Rev Drug Discov 11:909-922 (in vitro pharmacological "
    "profiling panel); hERG per ICH S7B core battery"
)

#: Symbols on the panel, for quick membership tests.
PANEL_SYMBOLS: frozenset = frozenset(t.symbol for t in PANEL)


@dataclass(frozen=True)
class Activity:
    """One MEASURED bioactivity record. Every field comes from the source database."""

    target_symbol: str
    target_chembl_id: str
    molecule_chembl_id: str
    standard_type: str          # Ki | Kd | IC50 | EC50
    pchembl: float | None       # -log10(molar); None when the source did not publish one
    assay_chembl_id: str = ""
    assay_description: str = ""

    @property
    def url(self) -> str:
        return f"https://www.ebi.ac.uk/chembl/compound_report_card/{self.molecule_chembl_id}/"

    @property
    def target_url(self) -> str:
        return f"https://www.ebi.ac.uk/chembl/target_report_card/{self.target_chembl_id}/"


@dataclass(frozen=True)
class Alert:
    """A published physicochemical heuristic that fired. A heuristic, not a finding."""

    alert: str
    concern: str
    citation: str
    detail: str


@dataclass
class TargetFinding:
    """Screening outcome at one panel target."""

    target: PanelTarget
    status: str
    activities: list[Activity] = field(default_factory=list)
    best_pchembl: float | None = None
    selectivity_log: float | None = None       # primary pAffinity - off-target pAffinity
    selectivity_adequate: bool | None = None
    note: str = ""


@dataclass
class OffTargetReport:
    """Panel-wide screening result for one compound."""

    compound: str
    findings: list[TargetFinding] = field(default_factory=list)
    alerts: list[Alert] = field(default_factory=list)
    panel_citation: str = PANEL_CITATION
    absence_caveat: str = ABSENCE_CAVEAT
    caveat: str = (
        "Catalyst does not predict off-target activity. Every flag below is a "
        "measured assay result retrieved from ChEMBL; every unflagged target is "
        "either measured-and-weak or has no retrieved data at all."
    )

    @property
    def flagged(self) -> list[TargetFinding]:
        return [f for f in self.findings if f.status == FLAGGED]

    @property
    def no_data(self) -> list[TargetFinding]:
        return [f for f in self.findings if f.status == NO_DATA]

    def summary(self) -> str:
        measured = [f for f in self.findings if f.status != NO_DATA]
        return (f"{len(self.flagged)} target(s) flagged at <= 1 uM; "
                f"{len(measured)}/{len(self.findings)} panel targets had measured data; "
                f"{len(self.alerts)} physicochemical alert(s)")


def physchem_alerts(c: Compound) -> list[Alert]:
    """Published physicochemical risk heuristics. Labelled as heuristics, always.

    These are population-level associations from retrospective analyses. They do not
    establish that a given compound is toxic, and a compound that trips none of them
    is not thereby safe.
    """
    out: list[Alert] = []
    if c.logp is not None and c.tpsa is not None and c.logp > 3 and c.tpsa < 75:
        out.append(Alert(
            "Pfizer 3/75",
            "elevated rate of in vivo toxicity findings in a retrospective compound set",
            "Hughes et al. 2008, Bioorg Med Chem Lett 18:4872-4875",
            f"logP {c.logp:.2f} > 3 and TPSA {c.tpsa:.1f} < 75",
        ))
    # The hERG lipophilic-base association needs a structural fact the caller must
    # supply — Catalyst does not infer a basic centre from SMILES (see descriptors.py).
    if c.basic_centre and c.logp is not None and c.logp > 3:
        out.append(Alert(
            "hERG lipophilic base",
            "structural class associated with hERG (KCNH2) block and QT prolongation",
            "Jamieson et al. 2006, J Med Chem 49:5029-5046",
            f"basic centre present and logP {c.logp:.2f} > 3 — confirm with a measured hERG assay",
        ))
    return out


def classify(pchembl: float | None) -> str:
    """Map a measured pChEMBL value onto a panel status."""
    if pchembl is None:
        return NO_DATA
    if pchembl >= FLAG_PCHEMBL:
        return FLAGGED
    if pchembl >= WEAK_PCHEMBL:
        return WEAK
    return NOT_FLAGGED


def screen(c: Compound, activities: list[Activity] | None = None,
           primary_p_affinity: float | None = None) -> OffTargetReport:
    """Screen measured ``activities`` against the safety panel.

    ``activities`` are records retrieved from ChEMBL (or supplied by the caller's own
    assay). Targets with no record are reported as :data:`NO_DATA`, never as clean.

    ``primary_p_affinity`` — the compound's measured potency at its INTENDED target —
    enables a selectivity margin. Without it the margin is simply not computed.
    """
    by_target: dict[str, list[Activity]] = {}
    for a in activities or []:
        if a.target_symbol in PANEL_SYMBOLS:
            by_target.setdefault(a.target_symbol, []).append(a)

    findings: list[TargetFinding] = []
    for target in PANEL:
        recs = by_target.get(target.symbol, [])
        scored = [a.pchembl for a in recs if a.pchembl is not None]
        if not scored:
            findings.append(TargetFinding(
                target, NO_DATA, recs, None, None, None,
                note=("records retrieved but none carried a pChEMBL value"
                      if recs else "no measured activity retrieved")))
            continue
        best = max(scored)
        margin = adequate = None
        if primary_p_affinity is not None:
            margin = primary_p_affinity - best
            adequate = margin >= SELECTIVITY_LOG_MARGIN
        findings.append(TargetFinding(target, classify(best), recs, best, margin, adequate))

    return OffTargetReport(compound=c.name, findings=findings, alerts=physchem_alerts(c))
