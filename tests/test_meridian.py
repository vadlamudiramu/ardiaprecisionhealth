"""TDD tests for Meridian's deterministic CLFS math.

These pin the exact figures the site shows for the seed test-mix, so the
homepage/model-page numbers can never silently drift from the model.
"""
import math

import pytest

from models.meridian.clfs import (
    CMP_PER_DAY,
    STATUTORY_MAX_CUT,
    RateLine,
    baseline_revenue,
    projected_revenue,
    reporting_penalty_ceiling,
    revenue_at_risk,
    run_rate_vs_baseline,
)

# Seed mix used by model-pama.html (2025 CLFS national rates).
SEED = [
    RateLine("80307", 62.14, 4200),
    RateLine("G0483", 246.92, 1100),
    RateLine("82306", 36.55, 5200),
    RateLine("81225", 128.00, 900),
    RateLine("82607", 18.61, 3100),
]


def test_baseline_matches_published_figure():
    assert round(baseline_revenue(SEED)) == 895_551


def test_cuts_compound_on_prior_year():
    base = baseline_revenue(SEED)
    y = projected_revenue(base, 0.15)
    assert len(y) == 3
    assert math.isclose(y[0], base * 0.85, rel_tol=1e-9)
    assert math.isclose(y[1], base * 0.85 ** 2, rel_tol=1e-9)
    assert math.isclose(y[2], base * 0.85 ** 3, rel_tol=1e-9)


def test_revenue_at_risk_matches_published_figure():
    base = baseline_revenue(SEED)
    assert round(revenue_at_risk(base, 0.15)) == 728_419


def test_run_rate_matches_published_figure():
    base = baseline_revenue(SEED)
    assert round(run_rate_vs_baseline(base, 0.15) * 100) == 61


def test_zero_cut_is_a_no_op():
    base = baseline_revenue(SEED)
    assert revenue_at_risk(base, 0.0) == 0.0
    assert run_rate_vs_baseline(base, 0.0) == 1.0


def test_cut_above_statutory_ceiling_is_rejected():
    with pytest.raises(ValueError):
        projected_revenue(1000.0, STATUTORY_MAX_CUT + 0.01)


def test_reporting_penalty_ceiling():
    assert reporting_penalty_ceiling(30) == 30 * CMP_PER_DAY == 300_000
    with pytest.raises(ValueError):
        reporting_penalty_ceiling(-1)
