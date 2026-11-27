---
name: fsd
description: "Run or re-run the FSD stage (One-Page PRD + ISO/IEC/IEEE 29148 FSD, INVEST + GWT + EARS, ISO 25010 checks, and ai-sdlc-loop gate PR brief) via po."
---

Run the `fsd` stage through `po` for the product named in the argument (or catch up on the active product first):

- Upstream required: locked `01-idea.md`..`07-presentations.md` and `.po/register.jsonl`.
- Producer: `fsd-producer` (fresh context) using `templates/08-fsd.md`, `templates/08-handoff-gate.md`, and `skills/fsd-iso-29148`, `skills/invest-gwt-ears`, `skills/iso-25010-quality`, `skills/ai-sdlc-loop-handoff`, `skills/evidence-tags`, `skills/register-ops`.
- Adversarial reviewer: `fsd-reviewer` (fresh context).
- Cross-cutting before gate: `evidence-auditor` + `challenger`, followed by user consultation at the `fsd` gate and user approval before any products-repo commit or engineering Gate PR.
