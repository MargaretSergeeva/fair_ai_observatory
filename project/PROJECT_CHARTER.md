# Fair AI Observatory — Project Charter & Management Approach

## 1. Concept Summary

The Fair AI Observatory is an open-source EU AI Act compliance and bias-detection pipeline for high-risk ML systems, built against the UCI Statlog German Credit dataset as the reference case. It combines a deterministic data/ML pipeline (Airflow, PostgreSQL, Great Expectations, dbt, XGBoost, Fairlearn) with an AI-agent layer that assists development, project management, and decision pressure-testing — and, as a product feature, helps new users configure the pipeline for their own datasets.

Originally scoped as a two-person project, the ML/LLM and governance design work has been fully absorbed into a single-owner build. This charter formalizes how the project is run going forward — it documents the current state honestly rather than pretending the project starts from zero.

**Current state:** six core modules complete (ingestion, XGBoost baseline, disparate impact, counterfactual fairness, intersectional bias, Fairlearn mitigation). HMDA dataset support deferred to v1.1.

## 2. Project Governance Model

**Human owner:** Margarita — sole decision-maker on anything that becomes part of the audit trail. Agents propose; she approves. This is non-negotiable for any output that functions as compliance evidence.

**Agent team:**
| Agent | Role | Decision authority |
|---|---|---|
| Developer | Implements, tests, flags PRs for review | None — never merges |
| PM Assistant | Tracks status, logs decisions, guides phase gates, syncs Jira | None — surfaces, doesn't decide |
| Stakeholder Panel | Pressure-tests methodology decisions pre-commit | None — argues, doesn't decide |
| Setup Agent *(product feature, not project team)* | Helps end users configure their own pipeline | Proposes config only; user approves |

## 3. PM Assistant — Expanded Mandate

The PM assistant's job is broader than status reporting. Across the project lifecycle, it:

- **Gatekeeps phase transitions** — before work moves from one phase to the next (e.g. starting a new module's "Execution"), checks that the required artifacts from the prior gate exist: a decision log entry for the metric/threshold choice, a stakeholder panel run if the decision had real tradeoffs, a Jira issue created and scoped.
- **Nudges toward best practice, grounded in the actual course material** — not generic PM advice. It consults a knowledge base built from the THRIVE AI-Augmented Project Management coursework (frameworks, templates, terminology) rather than relying on whatever a general model happens to know about project management.
- **Flags missing artifacts** — e.g. a module marked "in progress" with no risk note, a decision made in conversation but never logged, a stakeholder register entry with no defined engagement approach.
- **Still does the original job** — status reporting, decision logging, Jira sync (see prior design).

The distinction that matters: a reporting tool tells you what happened. A PM assistant with this mandate also tells you what's *missing* before it becomes a problem — closer to a process coach than a dashboard.

## 4. Knowledge Base

A `pm-knowledge/` directory in the repo holds the actual course material — frameworks, templates, rubrics from THRIVE — as the PM assistant's reference, plus a short `index.md` describing what's in each file so the skill knows what to consult and when (e.g. "stakeholder register template," "phase-gate checklist," "risk register format"). The PM assistant skill should be instructed to check this directory before giving any best-practice recommendation, and to say so when it's drawing on a specific framework versus general judgment — that traceability is itself good practice, and useful for the portfolio case study.

## 5. Stakeholder Register (project-level — real people, not the simulated panel)

| Stakeholder | Interest | Influence | Engagement |
|---|---|---|---|
| Margarita (Owner/PM) | Full ownership, portfolio credibility, learning outcome | Full | Daily |
| Future open-source contributors | Potential collaborators, code quality | TBD — none yet | Via repo, once public |
| End users (compliance teams, hypothetical) | Eventual adopters of the setup agent | Shapes setup agent design | Via setup agent feedback loop, once built |

## 6. Project Phases

| Phase | Status | PM Assistant gate check |
|---|---|---|
| Initiation | Retroactively formalized by this document | Charter + stakeholder register exist |
| Planning | Partially done (six-module scope, dataset choice) | Decision log covers scope calls (HMDA deferral, etc.) |
| Execution | In progress — six modules done, agent layer being built | Each module has a logged decision trail; Jira issue exists |
| Monitoring & Control | Starting now, via PM assistant + Jira sync | Weekly status digest running; blockers tracked |
| Closure (v1 / v1.1) | Not started | HMDA support, setup agent shipped, documentation complete |

## 7. Tooling Map

```
Jira (human-facing record)
   ⇅  n8n sync workflows
decisions.log / module_status.yaml (agent-facing state)
   ⇅
.claude/skills/  →  observatory-developer | observatory-pm | observatory-stakeholders
   ⇅
GitHub repo  →  Airflow → Great Expectations → dbt → XGBoost/Fairlearn pipeline
```

## 8. Next Steps

2. Set up the Jira project: one epic per phase, one issue per module, custom fields for risk tier and metric set
3. Create `pm-knowledge/` and add the first batch of THRIVE course material with an index
4. Install all three skill files (`developer`, `pm`, `stakeholders`) into `.claude/skills/`
5. Run the PM assistant once against current state — let it tell you what's missing per the gate checks above, treat the output as the real starting backlog
