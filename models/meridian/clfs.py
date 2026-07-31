"""Meridian — deterministic PAMA / CLFS rate-cliff model.

PAMA (Protecting Access to Medicare Act; CAA 2026 §6226) caps Clinical Laboratory
Fee Schedule payment reductions at up to 15%/yr for 2027, 2028 and 2029 — each
year applied to the *prior year's already-reduced* rate (i.e. compounding). This
module is the single source of truth for that math; the browser calculator in
model-pama.html mirrors it exactly. It handles NO PHI — only public CLFS rates
and a lab's own test-mix.
"""
from __future__ import annotations

from dataclasses import dataclass

#: Years the statutory cut applies (CAA 2026 §6226).
PAMA_CUT_YEARS: tuple[int, ...] = (2027, 2028, 2029)
#: Statutory ceiling on the annual CLFS reduction (15%/yr).
STATUTORY_MAX_CUT: float = 0.15
#: PAMA private-payor data-reporting civil monetary penalty ceiling ($/day).
CMP_PER_DAY: int = 10_000


@dataclass(frozen=True)
class RateLine:
    """One CPT/HCPCS line in a lab's annual test mix."""

    cpt: str
    rate: float   # 2025 CLFS national rate, USD
    volume: int   # annual volume


def baseline_revenue(mix: list[RateLine]) -> float:
    """Annual CLFS revenue at current (2025) rates."""
    return sum(line.rate * line.volume for line in mix)


def projected_revenue(base: float, cut: float, years: int = 3) -> list[float]:
    """Revenue after each compounding annual cut (applied to the prior year)."""
    if not 0.0 <= cut <= STATUTORY_MAX_CUT:
        raise ValueError(f"cut must be within [0, {STATUTORY_MAX_CUT}]")
    if years < 0:
        raise ValueError("years must be >= 0")
    out: list[float] = []
    current = base
    for _ in range(years):
        current *= 1.0 - cut
        out.append(current)
    return out


def revenue_at_risk(base: float, cut: float, years: int = 3) -> float:
    """Cumulative revenue shortfall vs baseline across the cut years."""
    return sum(base - y for y in projected_revenue(base, cut, years))


def run_rate_vs_baseline(base: float, cut: float, years: int = 3) -> float:
    """Final-year run-rate as a fraction of baseline (0..1)."""
    if base <= 0:
        return 0.0
    return projected_revenue(base, cut, years)[-1] / base


def reporting_penalty_ceiling(days_late: int) -> int:
    """Maximum PAMA data-reporting civil monetary penalty for N days late."""
    if days_late < 0:
        raise ValueError("days_late must be >= 0")
    return days_late * CMP_PER_DAY
