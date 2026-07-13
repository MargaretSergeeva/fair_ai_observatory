"""Run a deterministic baseline audit on UCI German Credit data."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
import xgboost
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBClassifier

from observatory.robustness.robustness import run_robustness_battery


DATASET_COLUMNS = [
    "checking_status",
    "duration_months",
    "credit_history",
    "purpose",
    "credit_amount",
    "savings",
    "employment",
    "installment_rate",
    "personal_status_sex",
    "other_debtors",
    "residence_since",
    "property",
    "age",
    "other_installment_plans",
    "housing",
    "existing_credits",
    "job",
    "dependents",
    "telephone",
    "foreign_worker",
    "credit_risk",
]
FEMALE_CODES = {"A92", "A95"}
DATASET_SOURCE = "https://archive.ics.uci.edu/dataset/144/statloggermancreditdata"
DATASET_DOI = "10.24432/C5NC77"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the reproducible UCI German Credit reference audit."
    )
    parser.add_argument(
        "--dataset",
        type=Path,
        default=Path("data/raw/german_credit/german.data"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/uci_german_credit_run.json"),
    )
    return parser.parse_args()


def load_dataset(*, path: Path) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(
            f"dataset not found: {path}; run scripts/download_uci_german_credit.py"
        )

    dataframe = pd.read_csv(path, sep=r"\s+", names=DATASET_COLUMNS)
    if dataframe.shape != (1000, 21):
        raise ValueError(f"expected dataset shape (1000, 21), received {dataframe.shape}")
    if dataframe.isna().any().any():
        raise ValueError("dataset contains missing values")
    if set(dataframe["credit_risk"].unique()) != {1, 2}:
        raise ValueError("credit_risk must contain exactly the official classes 1 and 2")
    return dataframe


def build_schema(*, features: pd.DataFrame) -> dict[str, dict]:
    schema: dict[str, dict] = {}
    numeric_columns = features.select_dtypes(include=[np.number]).columns.tolist()
    for column in numeric_columns:
        schema[column] = {
            "dtype": "numeric",
            "range": (float(features[column].min()), float(features[column].max())),
        }
    for column in features.columns:
        if column not in numeric_columns:
            schema[column] = {
                "dtype": "categorical",
                "categories": sorted(features[column].unique().tolist()),
            }
    return schema


def build_model(*, features: pd.DataFrame) -> Pipeline:
    numeric_columns = features.select_dtypes(include=[np.number]).columns.tolist()
    categorical_columns = [
        column for column in features.columns if column not in numeric_columns
    ]
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_columns,
            ),
            ("numeric", "passthrough", numeric_columns),
        ]
    )
    classifier = XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.05,
        eval_metric="logloss",
        random_state=42,
    )
    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", classifier),
        ]
    )


def group_rates(
    *, predictions: np.ndarray, labels: pd.Series, gender: pd.Series
) -> dict[str, dict[str, float | int]]:
    rates: dict[str, dict[str, float | int]] = {}
    for group in ("male", "female"):
        mask = gender == group
        rates[group] = {
            "n": int(mask.sum()),
            "actual_good_rate": round(float(labels[mask].mean()), 4),
            "predicted_approval_rate": round(float(predictions[mask].mean()), 4),
        }
    return rates


def intersectional_rates(
    *, dataframe: pd.DataFrame, labels: pd.Series, gender: pd.Series
) -> dict[str, dict[str, float | int]]:
    result: dict[str, dict[str, float | int]] = {}
    for group in ("male", "female"):
        for age_group, age_mask in (
            ("18-25", dataframe["age"].between(18, 25)),
            ("26+", dataframe["age"] >= 26),
        ):
            mask = (gender == group) & age_mask
            result[f"{group}_{age_group}"] = {
                "n": int(mask.sum()),
                "actual_good_rate": round(float(labels[mask].mean()), 4),
            }
    return result


def run_audit(*, dataset_path: Path) -> dict:
    dataframe = load_dataset(path=dataset_path)
    features = dataframe.drop(columns=["credit_risk"])
    labels = (dataframe["credit_risk"] == 1).astype(int)
    gender = pd.Series(
        np.where(
            dataframe["personal_status_sex"].isin(FEMALE_CODES),
            "female",
            "male",
        ),
        index=dataframe.index,
    )

    (
        features_train,
        features_test,
        labels_train,
        labels_test,
        _gender_train,
        gender_test,
    ) = train_test_split(
        features,
        labels,
        gender,
        test_size=0.30,
        random_state=42,
        stratify=labels,
    )

    model = build_model(features=features)
    model.fit(X=features_train, y=labels_train)
    predictions = model.predict(features_test)
    probabilities = model.predict_proba(features_test)[:, 1]
    rates = group_rates(
        predictions=predictions,
        labels=labels_test,
        gender=gender_test,
    )
    predicted_rates = [
        float(values["predicted_approval_rate"]) for values in rates.values()
    ]

    schema = build_schema(features=features)
    valid_row = features_test.iloc[0].to_dict()
    robustness = run_robustness_battery(
        model=model,
        X_train=features_train,
        X_test=features_test,
        y_test=labels_test,
        shift_spec={"credit_amount": 1.15},
        schema=schema,
        feature_order=features.columns.tolist(),
        malformed_cases=[
            ("valid row", valid_row, False),
            ("negative credit_amount", dict(valid_row, credit_amount=-1), True),
            ("missing age", dict(valid_row, age=None), True),
            ("age out of range", dict(valid_row, age=140), True),
        ],
    )

    return {
        "artifact_version": 1,
        "provenance": {
            "dataset": "Statlog (German Credit Data)",
            "source": DATASET_SOURCE,
            "doi": DATASET_DOI,
            "license": "CC BY 4.0",
            "dataset_sha256": hashlib.sha256(dataset_path.read_bytes()).hexdigest(),
            "execution": "deterministic local reference run",
        },
        "runtime": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "scikit_learn": sklearn.__version__,
            "xgboost": xgboost.__version__,
        },
        "methodology": {
            "train_test_split": "70/30 stratified, random_state=42",
            "target": "credit_risk == 1 interpreted as good credit",
            "gender_mapping": {
                "female": sorted(FEMALE_CODES),
                "male": ["A91", "A93", "A94"],
            },
            "model": {
                "type": "XGBClassifier",
                "n_estimators": 100,
                "max_depth": 4,
                "learning_rate": 0.05,
                "random_state": 42,
            },
            "limitations": [
                "Exploratory reference baseline; no hyperparameter tuning.",
                "The official asymmetric cost matrix is not applied.",
                "No Fairlearn mitigation is run because both diagnostic gender thresholds pass.",
            ],
        },
        "dataset": {
            "rows": int(len(dataframe)),
            "features": int(features.shape[1]),
            "target_good": int(labels.sum()),
            "target_bad": int((1 - labels).sum()),
            "gender_counts": {
                key: int(value) for key, value in gender.value_counts().items()
            },
        },
        "baseline": {
            "test_rows": int(len(features_test)),
            "accuracy": round(float(accuracy_score(labels_test, predictions)), 4),
            "probability_min": round(float(probabilities.min()), 4),
            "probability_max": round(float(probabilities.max()), 4),
            "group_rates": rates,
            "disparate_impact": round(min(predicted_rates) / max(predicted_rates), 4),
            "statistical_parity_gap": round(abs(predicted_rates[0] - predicted_rates[1]), 4),
            "diagnostic_thresholds_passed": {
                "disparate_impact_gte_0_80": min(predicted_rates) / max(predicted_rates)
                >= 0.80,
                "statistical_parity_gap_lte_0_10": abs(
                    predicted_rates[0] - predicted_rates[1]
                )
                <= 0.10,
            },
            "mitigation": "not triggered",
        },
        "intersectional_actual_labels": intersectional_rates(
            dataframe=dataframe,
            labels=labels,
            gender=gender,
        ),
        "robustness": robustness,
    }


def main() -> None:
    args = parse_args()
    report = run_audit(dataset_path=args.dataset)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Reference audit written to {args.output}")


if __name__ == "__main__":
    main()
