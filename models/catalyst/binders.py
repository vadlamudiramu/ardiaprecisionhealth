"""Catalyst developability rules — published filters, evaluated deterministically.

WHAT THIS IS NOT. There is no trained binding-affinity predictor here, and nothing
in this module "designs" or "invents" a molecule. Every number below comes from a
peer-reviewed filter published between 1997 and 2008, applied as plain arithmetic to
descriptors the caller supplied or PubChem published. That is the whole claim.

Passing these filters means a compound resembles the oral drugs the filters were
derived from. It does not mean the compound binds anything, is safe, or will
survive development — many marketed drugs (and most antibiotics and biologics)
fail them outright. They are triage, not a verdict.

Ligand efficiency is the one place a potency number appears, and it is only ever
computed from an affinity the CALLER measured. Catalyst never estimates affinity.

A rule whose descriptors are missing returns :data:`NOT_EVALUATED` — never a pass.
Silent treatment of "unknown" as "fine" is the failure mode these filters are most
often misused for.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from .descriptors import Compound

#: Rule verdicts. ``NOT_EVALUATED`` is a first-class outcome, not an error.
PASS = "pass"
FAIL = "fail"
NOT_EVALUATED = "not_evaluated"

#: Gas constant x 300 K x ln(10), kcal/mol — the Hopkins ligand-efficiency constant.
LE_CONSTANT = 1.37


@dataclass(frozen=True)
class RuleResult:
    """One published filter applied to one compound."""

    rule: str
    verdict: str                                   # PASS | FAIL | NOT_EVALUATED
    citation: str
    violations: list[str] = field(default_factory=list)
    #: Criteria in the original publication this implementation could not check,
    #: and why. Disclosed so a partial evaluation is never read as a full one.
    unevaluated_criteria: list[str] = field(default_factory=list)
    missing_descriptors: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        """True only on an affirmative pass — NOT_EVALUATED is not a pass."""
        return self.verdict == PASS


def _need(c: Compound, fields: tuple[str, ...], rule: str, citation: str):
    """Return a NOT_EVALUATED result if any required descriptor is missing."""
    missing = c.missing(fields)
    if missing:
        return RuleResult(rule, NOT_EVALUATED, citation, missing_descriptors=missing)
    return None


def lipinski(c: Compound) -> RuleResult:
    """Lipinski Rule of Five — poor absorption is more likely above these limits.

    The original formulation allows ONE violation; two or more predicts poor
    permeability/absorption. Note the rule was derived from orally administered
    drugs and explicitly excludes substrates of biological transporters.
    """
    cite = "Lipinski et al. 1997, Adv Drug Deliv Rev 23:3-25"
    rule = "Lipinski Rule of Five"
    if (nv := _need(c, ("mw", "logp", "hbd", "hba"), rule, cite)) is not None:
        return nv
    v = []
    if c.mw > 500:
        v.append(f"MW {c.mw:.1f} > 500")
    if c.logp > 5:
        v.append(f"logP {c.logp:.2f} > 5")
    if c.hbd > 5:
        v.append(f"HBD {c.hbd} > 5")
    if c.hba > 10:
        v.append(f"HBA {c.hba} > 10")
    # One violation is tolerated by the rule as published; two or more is a fail.
    return RuleResult(rule, PASS if len(v) <= 1 else FAIL, cite, violations=v,
                      unevaluated_criteria=["transporter-substrate exemption (not structural)"])


def veber(c: Compound) -> RuleResult:
    """Veber — oral bioavailability in rat correlates with flexibility and polarity."""
    cite = "Veber et al. 2002, J Med Chem 45:2615-2623"
    rule = "Veber"
    if (nv := _need(c, ("rot_bonds", "tpsa"), rule, cite)) is not None:
        return nv
    v = []
    if c.rot_bonds > 10:
        v.append(f"rotatable bonds {c.rot_bonds} > 10")
    if c.tpsa > 140:
        v.append(f"TPSA {c.tpsa:.1f} > 140")
    return RuleResult(rule, PASS if not v else FAIL, cite, violations=v,
                      unevaluated_criteria=["alternative H-bond-count criterion (sum <= 12)"])


def egan(c: Compound) -> RuleResult:
    """Egan "egg" — absorption confidence ellipse in logP / TPSA space."""
    cite = "Egan et al. 2000, J Med Chem 43:3867-3877"
    rule = "Egan"
    if (nv := _need(c, ("logp", "tpsa"), rule, cite)) is not None:
        return nv
    v = []
    if not -1.0 <= c.logp <= 5.88:
        v.append(f"logP {c.logp:.2f} outside [-1.0, 5.88]")
    if c.tpsa > 131.6:
        v.append(f"TPSA {c.tpsa:.1f} > 131.6")
    return RuleResult(rule, PASS if not v else FAIL, cite, violations=v)


def ghose(c: Compound) -> RuleResult:
    """Ghose qualifying range for drug-likeness (MW / logP window).

    The published filter has four criteria; two of them — molar refractivity and
    TOTAL atom count (hydrogens included) — are not derivable from this descriptor
    set, so they are reported as unevaluated rather than assumed satisfied.
    """
    cite = "Ghose et al. 1999, J Comb Chem 1:55-68"
    rule = "Ghose"
    if (nv := _need(c, ("mw", "logp"), rule, cite)) is not None:
        return nv
    v = []
    if not 160 <= c.mw <= 480:
        v.append(f"MW {c.mw:.1f} outside [160, 480]")
    if not -0.4 <= c.logp <= 5.6:
        v.append(f"logP {c.logp:.2f} outside [-0.4, 5.6]")
    return RuleResult(rule, PASS if not v else FAIL, cite, violations=v,
                      unevaluated_criteria=["molar refractivity 40-130", "total atom count 20-70"])


def rule_of_three(c: Compound) -> RuleResult:
    """Congreve Rule of Three — a FRAGMENT-screening filter, not a lead filter.

    Reported for context on small compounds. A drug-sized molecule failing Ro3 is
    entirely expected and is not a liability.
    """
    cite = "Congreve et al. 2003, Drug Discov Today 8:876-877"
    rule = "Rule of Three (fragments)"
    if (nv := _need(c, ("mw", "logp", "hbd", "hba", "rot_bonds", "tpsa"), rule, cite)) is not None:
        return nv
    v = []
    if c.mw >= 300:
        v.append(f"MW {c.mw:.1f} >= 300")
    if c.logp > 3:
        v.append(f"logP {c.logp:.2f} > 3")
    if c.hbd > 3:
        v.append(f"HBD {c.hbd} > 3")
    if c.hba > 3:
        v.append(f"HBA {c.hba} > 3")
    if c.rot_bonds > 3:
        v.append(f"rotatable bonds {c.rot_bonds} > 3")
    if c.tpsa > 60:
        v.append(f"TPSA {c.tpsa:.1f} > 60")
    return RuleResult(rule, PASS if not v else FAIL, cite, violations=v)


#: Evaluation order for :func:`assess`.
RULES = (lipinski, veber, egan, ghose, rule_of_three)


def ligand_efficiency(p_affinity: float, heavy_atoms: int) -> float:
    """Hopkins ligand efficiency, kcal/mol per heavy atom: 1.37 x pAffinity / HAC.

    ``p_affinity`` is a MEASURED -log10(molar Ki/Kd/IC50). Catalyst never supplies
    this value itself.
    """
    if heavy_atoms <= 0:
        raise ValueError("heavy_atoms must be > 0")
    return LE_CONSTANT * p_affinity / heavy_atoms


def lipophilic_efficiency(p_affinity: float, logp: float) -> float:
    """Leeson lipophilic ligand efficiency (LLE / LipE): pAffinity - logP."""
    return p_affinity - logp


def p_affinity_from_molar(value_molar: float) -> float:
    """Convert a measured molar Ki/Kd/IC50 into its p-scale value."""
    if value_molar <= 0:
        raise ValueError("affinity must be > 0 M")
    return -math.log10(value_molar)


@dataclass
class DevelopabilityReport:
    """Aggregate of every published filter applied to one compound."""

    compound: str
    provenance: str
    rules: list[RuleResult] = field(default_factory=list)
    ligand_efficiency: float | None = None
    lipophilic_efficiency: float | None = None
    affinity_source: str = ""
    #: Fixed caveat carried in the data, so it cannot be dropped by presentation code.
    caveat: str = (
        "These are published triage filters for oral small molecules, not a prediction "
        "of binding, efficacy or safety. Catalyst does not estimate affinity: ligand "
        "efficiency appears only when a measured affinity was supplied."
    )

    @property
    def evaluated(self) -> list[RuleResult]:
        return [r for r in self.rules if r.verdict != NOT_EVALUATED]

    @property
    def failed(self) -> list[RuleResult]:
        return [r for r in self.rules if r.verdict == FAIL]

    def summary(self) -> str:
        """One honest line: passed/evaluated, and how many could not be evaluated."""
        ev = self.evaluated
        skipped = len(self.rules) - len(ev)
        head = f"{sum(1 for r in ev if r.passed)}/{len(ev)} published filters passed"
        return head + (f"; {skipped} not evaluated (missing descriptors)" if skipped else "")


def assess(c: Compound, p_affinity: float | None = None,
           affinity_source: str = "") -> DevelopabilityReport:
    """Apply every published filter to ``c``; add efficiency metrics only if measured.

    ``p_affinity`` must be a measured -log10(molar) potency together with the
    ``affinity_source`` that documents where it came from. Passing one without the
    other is refused — an unattributed potency is indistinguishable from a guess.
    """
    if p_affinity is not None and not affinity_source:
        raise ValueError("affinity_source is required when p_affinity is supplied")
    rep = DevelopabilityReport(compound=c.name, provenance=c.provenance,
                               rules=[rule(c) for rule in RULES])
    if p_affinity is not None:
        rep.affinity_source = affinity_source
        if c.heavy_atoms:
            rep.ligand_efficiency = ligand_efficiency(p_affinity, c.heavy_atoms)
        if c.logp is not None:
            rep.lipophilic_efficiency = lipophilic_efficiency(p_affinity, c.logp)
    return rep
