# Architecture and Evidence Boundaries

## Current implementation

```text
React concept demo
├── Act 1: scripted synthetic product scenario
├── Act 2: scripted governance/process scenario
├── Pipeline Schema: target architecture diagram
└── UCI Reference Run: renders repository JSON artifact

Python reference path
├── download official UCI archive
├── verify archive checksum and raw shape
├── train deterministic XGBoost baseline
├── calculate gender fairness aggregates
├── execute robustness battery
└── write artifacts/uci_german_credit_run.json
```

Implemented Python code:

- `scripts/download_uci_german_credit.py`
- `scripts/run_reference_audit.py`
- `observatory/robustness/robustness.py`

## Target architecture shown by the concept

```text
Dataset → Setup Agent → Human-approved configuration
       → Great Expectations → dbt → XGBoost
       → bias battery → Fairlearn mitigation
       → robustness battery
       → audit trail, dashboard and compliance documents
```

The following target components are not implemented end to end:

- dataset upload and general schema ingestion;
- conversational setup agent;
- Great Expectations validation suite;
- dbt transformations;
- reusable model-training pipeline;
- bias and intersectional-analysis modules;
- Fairlearn mitigation workflow;
- Airflow orchestration;
- PostgreSQL persistence;
- n8n/Jira synchronization;
- continuous monitoring, retention enforcement, override and stop controls.

## Evidence classification

| Evidence | Source | Status |
|---|---|---|
| Synthetic fairness and mitigation values | `demo/ObservatoryDemo.jsx` | Scripted concept values |
| Synthetic process and stakeholder values | `demo/ProcessCommandCenter.jsx` | Scripted concept values |
| UCI baseline and robustness values | `artifacts/uci_german_credit_run.json` | Reproducible reference result |
| Annex IV and Instructions for Use | `docs/compliance-samples/` | Sample documents |
| Target pipeline | `demo/ObservatorySchema.jsx` | Architecture concept |

## Data boundary

Raw UCI data is downloaded into ignored `data/raw/` and is not required in the repository. The versioned artifact contains only aggregate results, provenance, runtime versions, methodology settings, and limitations.

## Known technical boundary

The standalone robustness module is a technical spike rather than production validation software. Its results are useful for the concept, but its input semantics and edge cases require further hardening before production use.
