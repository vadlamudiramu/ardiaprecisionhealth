"""Catalyst descriptors — the molecular facts every downstream rule reads from.

A :class:`Compound` is a *container for measured or computed descriptors*, not a
structure parser. Catalyst deliberately does NOT parse SMILES: deriving logP, TPSA
or H-bond counts from a structure requires a fitted cheminformatics model (RDKit /
Crippen / Ertl), and a hand-rolled approximation would be confidently wrong in
exactly the cases that matter. Descriptors therefore come from one of two honest
places:

  1. the caller supplies them (a lab's own measured/computed values), or
  2. :mod:`models.catalyst.sources` fetches them from PubChem, which publishes
     the computed values it stands behind.

``smiles`` is carried through for provenance and display only — nothing in this
package derives a number from it.
"""
from __future__ import annotations

from dataclasses import dataclass

#: Descriptor fields a rule may require. Used to report which rules could not be
#: evaluated for a given compound rather than silently treating missing as passing.
DESCRIPTOR_FIELDS: tuple[str, ...] = (
    "mw", "logp", "hbd", "hba", "tpsa", "rot_bonds", "heavy_atoms", "aromatic_rings",
)


@dataclass(frozen=True)
class Compound:
    """One compound's descriptor set. ``None`` means "not known", never "zero"."""

    name: str
    smiles: str = ""
    mw: float | None = None              # molecular weight, Da
    logp: float | None = None            # octanol/water partition coefficient (computed)
    hbd: int | None = None               # hydrogen-bond donors
    hba: int | None = None               # hydrogen-bond acceptors
    tpsa: float | None = None            # topological polar surface area, A^2
    rot_bonds: int | None = None         # rotatable bonds
    heavy_atoms: int | None = None       # non-hydrogen atom count
    aromatic_rings: int | None = None
    #: Caller-supplied structural flag. Not derived from SMILES — the hERG
    #: lipophilic-base heuristic needs it, and guessing it would be unsound.
    basic_centre: bool | None = None
    #: Where these descriptors came from, e.g. "PubChem CID 2244" or "caller-supplied".
    provenance: str = "caller-supplied"

    def missing(self, fields: tuple[str, ...]) -> list[str]:
        """Which of ``fields`` this compound has no value for."""
        return [f for f in fields if getattr(self, f, None) is None]

    def known(self) -> list[str]:
        """Descriptor fields that actually carry a value."""
        return [f for f in DESCRIPTOR_FIELDS if getattr(self, f, None) is not None]
