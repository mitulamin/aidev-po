---
name: audience
description: "Run or re-run the Audience stage (segments, Mom Test past-instance log, expanded Opportunity Solution Tree) via po."
---

Run the `audience` stage through `po` for the product named in the argument (or catch up on the active product first):

- Upstream required: locked `01-idea.md` decisions (`DEC-NNN`).
- Producer: `audience-producer` (fresh context) using `templates/02-audience.md` and `skills/jtbd-mom-test`, `skills/opportunity-solution-trees`, `skills/evidence-tags`, `skills/register-ops`.
- Adversarial reviewer: `audience-reviewer` (fresh context).
- Cross-cutting before gate: `evidence-auditor` + `challenger`, followed by user consultation at the `audience` gate.
