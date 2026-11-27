---
name: presentations
description: "Run or re-run the Presentations stage (Working Backwards PR/FAQ and stakeholder presentation outline) via po."
---

Run the `presentations` stage through `po` for the product named in the argument (or catch up on the active product first):

- Upstream required: locked `01-idea.md`..`06-workshops.md`.
- Producer: `presentations-producer` (fresh context) using `templates/07-presentations.md` and `skills/pr-faq-presentations`, `skills/evidence-tags`, `skills/register-ops`.
- Adversarial reviewer: `presentations-reviewer` (fresh context).
- Cross-cutting before gate: `evidence-auditor` + `challenger`, followed by user consultation at the `presentations` gate.
