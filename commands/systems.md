---
name: systems
description: "Run or re-run the Systems stage (C4 System Context, Process EventStorming, integration failure modes, hotspots) via po."
---

Run the `systems` stage through `po` for the product named in the argument (or catch up on the active product first):

- Upstream required: locked `01-idea.md`..`03-actors.md`.
- Producer: `systems-producer` (fresh context) using `templates/04-systems.md` and `skills/c4-context-eventstorming`, `skills/evidence-tags`, `skills/register-ops`.
- Adversarial reviewer: `systems-reviewer` (fresh context).
- Cross-cutting before gate: `evidence-auditor` + `challenger`, followed by user consultation at the `systems` gate.
