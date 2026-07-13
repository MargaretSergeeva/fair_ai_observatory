# UCI German Credit Reference Run

## Purpose

This reference run provides a real-data technical evidence layer separate from the scripted synthetic product scenario.

## Dataset

- Name: Statlog (German Credit Data)
- Provider: UCI Machine Learning Repository
- Source: <https://archive.ics.uci.edu/dataset/144/statloggermancreditdata>
- DOI: `10.24432/C5NC77`
- License: CC BY 4.0
- Raw shape: 1,000 rows, 20 features and one target column

The downloader accepts only the expected official archive SHA-256:

```text
e12d9d5def6845c0622634a1cd2ab87fa470668c4298f1ec52a4e403376a435b
```

It also validates the raw `1000 × 21` shape before writing the dataset.

## Reproduction

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

PYTHONPATH=. python scripts/download_uci_german_credit.py
PYTHONPATH=. python scripts/run_reference_audit.py
```

Raw data is stored under ignored `data/raw/german_credit/german.data`.

The generated aggregate artifact is:

```text
artifacts/uci_german_credit_run.json
```

## Methodology

- target `credit_risk == 1` is interpreted as good credit;
- train/test split: stratified 70/30, `random_state=42`;
- categorical features: one-hot encoded;
- model: XGBoost, 100 estimators, depth 4, learning rate 0.05;
- gender mapping follows the official `personal_status_sex` definitions;
- no hyperparameter tuning;
- official asymmetric cost matrix not applied;
- no mitigation because both diagnostic gender thresholds pass.

## Captured results

| Metric | Result |
|---|---:|
| Test accuracy | 74.33% |
| Male predicted approval rate | 83.33% |
| Female predicted approval rate | 76.04% |
| Disparate impact | 0.9125 — PASS |
| Statistical parity gap | 0.0729 — PASS |
| Distribution-shift degradation | 1.33% — PASS |
| Boundary-sensitivity flip rate | 32.0% — FAIL |
| Malformed input cases | 4/4 — PASS |
| OOD flagged rate | 5.67% — INFO |

## Artifact reproducibility

With the runtime versions recorded inside the artifact, repeated local execution produced the same JSON SHA-256:

```text
8dde1d4b7a3445fdfc4332b487cde6801a57f60ee7e0f6575c6098331981898f
```

Library upgrades can change model output. Regenerate intentionally and review the full metric diff rather than accepting drift silently.

## Interpretation boundary

This is an exploratory baseline, not a production model evaluation, legal assessment, or conformity claim. Passing two diagnostic gender thresholds does not prove general fairness, and the failed boundary-sensitivity result remains an open robustness concern.
