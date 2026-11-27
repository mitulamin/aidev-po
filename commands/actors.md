---
name: actors
description: "Run or re-run the Actors stage (Power/Interest stakeholder map, actor profiles, roles and permissions) via po."
---

Run the `actors` stage through `po` for the product named in the argument (or catch up on the active product first):

- Upstream required: locked `01-idea.md` and `02-audience.md`.
- Producer: `actors-producer` (fresh context) using `templates/03-actors.md` and `skills/power-interest-stakeholder-map`, `skills/evidence-tags`, `skills/register-ops`.
- Adversarial reviewer: `actors-reviewer` (fresh context).
- Cross-cutting before gate: `evidence-auditor` + `challenger`, followed by user consultation at the `actors` gate.
