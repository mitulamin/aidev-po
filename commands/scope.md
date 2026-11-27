---
name: scope
description: "Run or re-run the Scope stage (Impact Mapping, Story Mapping, MoSCoW, Explicit Non-Goals with revisit triggers) via po."
---

Run the `scope` stage through `po` for the product named in the argument (or catch up on the active product first):

- Upstream required: locked `01-idea.md`..`04-systems.md`.
- Producer: `scope-producer` (fresh context) using `templates/05-scope.md` and `skills/impact-mapping`, `skills/story-mapping`, `skills/moscow-non-goals`, `skills/evidence-tags`, `skills/register-ops`.
- Adversarial reviewer: `scope-reviewer` (fresh context).
- Cross-cutting before gate: `evidence-auditor` + `challenger`, followed by user consultation at the `scope` gate.
