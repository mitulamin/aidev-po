---
name: idea
description: "Run or re-run the Idea stage (problem framing, JTBD + Mom Test, Lean Canvas, initial Opportunity Solution Tree) via po."
---

Run the `idea` stage through `po` for the product named in the argument (or select/create one first):

- Producer: `idea-producer` (fresh context) using `templates/01-idea.md` and `skills/jtbd-mom-test`, `skills/lean-canvas`, `skills/opportunity-solution-trees`, `skills/evidence-tags`, `skills/register-ops`.
- Adversarial reviewer: `idea-reviewer` (fresh context).
- Cross-cutting before gate: `evidence-auditor` + `challenger`, followed by user consultation at the `idea` gate.
