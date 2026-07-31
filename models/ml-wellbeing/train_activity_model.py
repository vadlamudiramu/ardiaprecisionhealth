"""Cadence — train + honestly evaluate the activity-recognition model.

Public benchmark: UCI HAR (Anguita et al., 2013; CC BY 4.0). 10,299 windows,
561 engineered features, 30 subjects, 6 activities. We use the dataset's own
train/test split, which is **subject-independent** (the 9 test subjects never
appear in training) — so the held-out score measures generalisation to a NEW
person, not a new window from someone already seen. Model is chosen by 5-fold
CV on the training split only; the winner is scored EXACTLY ONCE on the held-out
subjects. Whatever number that produces is what we publish — no test-set peeking.

Run:  python models/ml-wellbeing/train_activity_model.py
Writes: artifacts/cadence_model.joblib, artifacts/metrics.json
"""
from __future__ import annotations

import json
import zipfile
from pathlib import Path
from urllib.request import urlretrieve

import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import joblib

HERE = Path(__file__).resolve().parent
DATA = HERE / "data" / "UCI HAR Dataset"
ART = HERE / "artifacts"
URL = "https://archive.ics.uci.edu/static/public/240/human+activity+recognition+using+smartphones.zip"
RANDOM_STATE = 42

# 6 activities -> the 3 states the product actually tracks.
ROLLUP = {1: "Active", 2: "Active", 3: "Active", 4: "Sedentary", 5: "Sedentary", 6: "Resting"}


def ensure_data() -> None:
    if DATA.exists():
        return
    DATA.parent.mkdir(parents=True, exist_ok=True)
    outer = DATA.parent / "uci_har.zip"
    if not outer.exists():
        print("downloading UCI HAR ...")
        urlretrieve(URL, outer)
    with zipfile.ZipFile(outer) as z:
        z.extractall(DATA.parent)
    inner = DATA.parent / "UCI HAR Dataset.zip"
    if inner.exists():
        with zipfile.ZipFile(inner) as z:
            z.extractall(DATA.parent)


def _read(path: Path) -> np.ndarray:
    return pd.read_csv(path, sep=r"\s+", header=None).values


def load():
    Xtr = _read(DATA / "train" / "X_train.txt")
    ytr = _read(DATA / "train" / "y_train.txt").ravel().astype(int)
    subj_tr = _read(DATA / "train" / "subject_train.txt").ravel().astype(int)
    Xte = _read(DATA / "test" / "X_test.txt")
    yte = _read(DATA / "test" / "y_test.txt").ravel().astype(int)
    subj_te = _read(DATA / "test" / "subject_test.txt").ravel().astype(int)
    labels = {}
    for line in (DATA / "activity_labels.txt").read_text().splitlines():
        if line.strip():
            i, name = line.split()
            labels[int(i)] = name
    return Xtr, ytr, subj_tr, Xte, yte, subj_te, labels


def main() -> dict:
    ensure_data()
    ART.mkdir(parents=True, exist_ok=True)
    Xtr, ytr, subj_tr, Xte, yte, subj_te, labels = load()

    # subject-independence check (the whole point of the honest eval)
    overlap = sorted(set(subj_tr.tolist()) & set(subj_te.tolist()))
    assert not overlap, f"train/test subjects overlap: {overlap}"

    # model selection by 5-fold CV on TRAIN ONLY
    candidates = {
        # StandardScaler stabilises lbfgs and is fit within each CV fold.
        "logreg": make_pipeline(
            StandardScaler(), LogisticRegression(max_iter=1000, C=1.0)
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=200, random_state=RANDOM_STATE, n_jobs=-1
        ),
    }
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    cv_scores = {
        name: float(cross_val_score(m, Xtr, ytr, cv=cv, scoring="accuracy").mean())
        for name, m in candidates.items()
    }
    best = max(cv_scores, key=cv_scores.get)
    print("CV (train-only):", {k: round(v, 4) for k, v in cv_scores.items()}, "-> selected", best)

    # refit winner on full train, evaluate ONCE on held-out subjects
    model = candidates[best].fit(Xtr, ytr)
    pred = model.predict(Xte)

    acc = float(accuracy_score(yte, pred))
    macro_f1 = float(f1_score(yte, pred, average="macro"))
    bacc = float(balanced_accuracy_score(yte, pred))

    roll_true = np.array([ROLLUP[i] for i in yte])
    roll_pred = np.array([ROLLUP[i] for i in pred])
    rollup_acc = float((roll_true == roll_pred).mean())

    report = classification_report(
        yte, pred, target_names=[labels[i] for i in sorted(labels)], output_dict=True
    )
    per_subject = []
    for s in sorted(set(subj_te.tolist())):
        mask = subj_te == s
        per_subject.append(float(accuracy_score(yte[mask], pred[mask])))

    metrics = {
        "model": "Cadence (activity recognition)",
        "dataset": "UCI HAR (Anguita et al. 2013, CC BY 4.0)",
        "n_train_windows": int(len(ytr)),
        "n_test_windows": int(len(yte)),
        "n_features": int(Xtr.shape[1]),
        "subjects_train": len(set(subj_tr.tolist())),
        "subjects_test": len(set(subj_te.tolist())),
        "subject_independent": overlap == [],
        "cv_accuracy_train_only": {k: round(v, 4) for k, v in cv_scores.items()},
        "selected_model": best,
        "held_out_accuracy": round(acc, 4),
        "held_out_macro_f1": round(macro_f1, 4),
        "held_out_balanced_accuracy": round(bacc, 4),
        "active_sedentary_resting_accuracy": round(rollup_acc, 4),
        "worst_subject_accuracy": round(min(per_subject), 4),
        "best_subject_accuracy": round(max(per_subject), 4),
        "mean_subject_accuracy": round(float(np.mean(per_subject)), 4),
        "per_class": {
            labels[int(k)] if k.isdigit() else k: v
            for k, v in report.items()
            if isinstance(v, dict)
        },
        "confusion_matrix": confusion_matrix(yte, pred).tolist(),
        "activity_labels": {int(k): v for k, v in labels.items()},
        "sklearn_version": sklearn.__version__,
        "random_state": RANDOM_STATE,
    }

    (ART / "metrics.json").write_text(json.dumps(metrics, indent=2))
    joblib.dump(model, ART / "cadence_model.joblib")
    print(
        f"HELD-OUT (subject-independent): acc={acc:.4f} macroF1={macro_f1:.4f} "
        f"A/S/R={rollup_acc:.4f} worst-subject={min(per_subject):.4f}"
    )
    return metrics


if __name__ == "__main__":
    main()
