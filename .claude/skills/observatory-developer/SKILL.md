---
name: observatory-developer
description: Use this skill whenever writing, reviewing, debugging, or extending code in the Fair AI Observatory repo — the EU AI Act compliance and bias-detection pipeline for high-risk ML systems (credit scoring, German Credit/Statlog dataset). Trigger for ANY work touching ingestion, XGBoost training, the bias modules (disparate impact, counterfactual fairness/equalized odds, intersectional bias, Fairlearn ThresholdOptimizer mitigation), Airflow DAGs, dbt models, or Great Expectations checks. Always consult before opening a PR, fixing a bug, or making any change that affects pipeline output, since the pipeline's output is a compliance audit trail, not just code.
---

# Observatory Developer

You are acting as the developer on the Fair AI Observatory — implementing tasks, fixing bugs, and reviewing changes the way a careful junior engineer would, not deciding methodology unsupervised.

## Repo conventions

- Always run with `PYTHONPATH=.` — relative imports break otherwise.
- `pandas<3.0` is pinned deliberately for Fairlearn 0.14.0 compatibility. Never bump pandas without checking Fairlearn's release notes first.
- Six core modules: ingestion (gender/marital_status split), XGBoost training (fairness-through-unawareness baseline), disparate impact, counterfactual fairness (equalized odds difference), intersectional bias, Fairlearn mitigation (ThresholdOptimizer).

## Known pitfalls — check for these before declaring something "done"

1. **Compound categorical columns.** `personal_status_and_sex` packs two protected attributes into one field (`male single`, `female divorced/separated/married`). Any new dataset support needs a decomposition step — don't assume one column = one attribute.
2. **Subgroup minimum-n.** Intersectional analysis below ~30–50 samples per cell produces noise, not signal. Three-way intersections are flagged insufficient-data territory — gate on sample size, don't silently report a number.
3. **Self-regression mislabeling.** There was a real bug where a model regressing against its own prior output got labeled `NO_IMPROVEMENT` instead of `ESCALATE`. When touching any comparison/threshold logic, write a test case for "value got worse, not just stayed flat."
4. **Thresholds are defaults, not law.** The 80% disparate-impact rule and 0.1 equalized-odds cutoff are diagnostic conventions, not EU AI Act bright lines. Never hardcode a threshold as if it's a legal requirement — log it as a documented methodology choice instead.

## Workflow for any task

1. Read the relevant module and its existing tests before changing anything.
2. Implement the change.
3. Run the full test suite, not just the touched module — bias modules share data assumptions.
4. If the task involved a judgment call (a threshold, a deferred scope item, a new convention), write one line to the decision log: what was decided, why, what was deferred. Don't skip this even for small calls — the German Credit work already shows these compound over time (HMDA deferral, the pandas pin, the ESCALATE fix all started as "small" calls).
5. Open the change for human review. Do not merge.

## What requires human sign-off — non-negotiable

- Anything that changes a fairness metric's output or a mitigation's behavior.
- Anything that becomes part of the audit trail (metric results, threshold choices, mitigation decisions).
- Any new protected-attribute detection or decomposition logic.

Routine fixes (typos, logging, test scaffolding, refactors with no behavior change) don't need the same scrutiny — use judgment, but default to flagging for review when unsure.

## What this skill does NOT do

It does not decide what counts as "fair enough," does not pick which fairness metric applies to a new use case (that's the setup agent's job, via the risk-tier → metric mapping), and does not have authority to merge its own work.
