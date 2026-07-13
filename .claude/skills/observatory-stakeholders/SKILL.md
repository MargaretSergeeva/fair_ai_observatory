---
name: observatory-stakeholders
description: Use this skill BEFORE finalizing any Fair AI Observatory methodology decision — a fairness threshold value, which metric applies to a use case, how to handle a detected proxy attribute, a scope deferral, or anything that will be logged as part of the audit trail. Also trigger on explicit phrases like "stress-test this," "pressure-test," "get pushback," or "run the stakeholder panel." Do NOT use for routine implementation, bug fixes, or status updates — only for decisions with a real tradeoff between competing interests.
---

# Observatory Stakeholder Panel

Purpose: surface the disagreement a real second perspective would have raised, before a decision gets locked in. This skill argues — it does not decide. The human decides after seeing the tension.

## The three personas

Each argues from genuine self-interest. Give each a specific objection tied to the actual decision — numbers, dataset, subgroup sizes — never a generic "consider this perspective" comment.

**1. Applicant advocate** — represents the person on the receiving end of the credit decision. Cares about: false denials, opacity, whether intersectional/proxy harms were actually checked, not just the headline attribute. Pushes back when fairness gets traded away for convenience or cost.

**2. Regulator / DPO** — cares about defensibility under audit. Pushes on: is this threshold documented as a chosen methodology or presented as if the law dictated it (it doesn't)? Is there a GDPR Art. 9(2) basis for using the special-category data this check requires? Would this decision survive someone asking "why" two years from now?

**3. Lender / business stakeholder** — cares about model performance and cost. Pushes back when a mitigation tanks approval rates or accuracy without a clear harm being prevented. Asks "what's this actually buying us" when fairness work has no measurable downside being addressed.

## How to run it

1. State the decision under review in one sentence.
2. Each persona gives: their position, their specific objection (tied to the real numbers/decision), and what would need to change for them to accept it.
3. Note where two personas agree despite opposed interests — that's a strong signal, surface it explicitly.
4. Note the irreducible tension — where they genuinely can't both be satisfied. These are the calls only a human gets to own.
5. Close with: "This is not a recommendation — here's the tradeoff, you decide."

## Grounding rules — what keeps this from being theater

- Reference the actual specifics: which metric, what threshold value, what subgroup n, what's being deferred and to where.
- Pull in the project's known pitfalls where relevant — applicant advocate should ask whether intersectional/proxy coverage was actually checked; regulator should ask whether a threshold is logged as a documented choice rather than implied as legal requirement.
- If a persona genuinely has nothing substantive to add to a specific decision, say so in one line rather than padding for balance.

## When NOT to use

- Routine code changes, refactors, bug fixes — that's the developer skill.
- Status reporting — that's the PM skill.
- Anything already shipped and logged — this runs before a decision, not as retroactive critique.

## After the panel

Log through the PM skill as usual — note in `decisions.log` that a panel was run and which tension drove the final call. That's part of what makes the audit trail credible: it shows the disagreement was surfaced, not just resolved silently.
