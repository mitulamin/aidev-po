---
name: workshops
description: "Run or re-run the Workshops stage (AI prepares agenda/capture sheet, human runs session, AI writes up supplied notes) via po."
---

Run the `workshops` stage through `po` for the product named in the argument (or catch up on the active product first):

- Upstream required: locked `01-idea.md`..`05-scope.md` and `.po/register.jsonl`.
- Producer: `workshops-producer` (fresh context) using `templates/06-workshops.md` and `skills/workshop-facilitation`, `skills/evidence-tags`, `skills/register-ops`.
- Note: pass any human-supplied workshop notes or waiver decision in the brief; never fabricate workshop outcomes.
- Adversarial reviewer: `workshops-reviewer` (fresh context).
- Cross-cutting before gate: `evidence-auditor` + `challenger`, followed by user consultation at the `workshops` gate.
