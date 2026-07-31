"""TDD tests for Cadence — the trained activity-recognition model.

These read the committed metrics.json (the measured evidence) and, when the
dataset + model artifact are present, re-run inference to prove the reported
held-out accuracy reproduces. Thresholds sit safely below the measured values so
the tests act as real regression gates, not exact-value overfits.
"""
import json
from pathlib import Path

import pytest

ART = Path(__file__).resolve().parents[1] / "models" / "ml-wellbeing" / "artifacts"
METRICS = ART / "metrics.json"


@pytest.fixture(scope="module")
def metrics():
    if not METRICS.exists():
        pytest.skip("run models/ml-wellbeing/train_activity_model.py first")
    return json.loads(METRICS.read_text())


def test_evaluation_is_subject_independent(metrics):
    assert metrics["subject_independent"] is True


def test_dataset_shape_is_uci_har(metrics):
    assert metrics["n_features"] == 561
    assert metrics["n_train_windows"] == 7352
    assert metrics["n_test_windows"] == 2947


def test_held_out_accuracy_regression_gate(metrics):
    assert metrics["held_out_accuracy"] >= 0.93
    assert metrics["held_out_macro_f1"] >= 0.93


def test_active_sedentary_resting_rollup(metrics):
    assert metrics["active_sedentary_resting_accuracy"] >= 0.98


def test_worst_subject_floor_is_reported(metrics):
    # honesty: a model that averages well but fails one person in nine is not one
    # we deploy to older adults — the per-person floor must be reported and hold.
    assert metrics["worst_subject_accuracy"] >= 0.80


def test_saved_model_reproduces_reported_accuracy():
    data = ART.parent / "data" / "UCI HAR Dataset"
    model_f = ART / "cadence_model.joblib"
    if not (data.exists() and model_f.exists()):
        pytest.skip("dataset or model artifact not present locally")
    import joblib
    import pandas as pd
    from sklearn.metrics import accuracy_score

    model = joblib.load(model_f)
    Xte = pd.read_csv(data / "test" / "X_test.txt", sep=r"\s+", header=None).values
    yte = (
        pd.read_csv(data / "test" / "y_test.txt", sep=r"\s+", header=None)
        .values.ravel()
        .astype(int)
    )
    acc = accuracy_score(yte, model.predict(Xte))
    reported = json.loads(METRICS.read_text())["held_out_accuracy"]
    assert abs(acc - reported) < 1e-3
