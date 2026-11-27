# skills

Skill sources, one folder per skill: `skills/<name>/SKILL.md` with `name` and `description` front matter. `scripts/build-agents.py` copies them into `.cursor/skills/`.

## Shared skills

- [outliner-qa](outliner-qa/SKILL.md): Layered Q&A (<=5 questions/round), recommended answer first, Park with revisit trigger, lock sheet, Given/When/Then
- [evidence-tags](evidence-tags/SKILL.md): Evidence tags (`Stated`, `Inferred`, `Assumed`, `Simulated`, `Validated`) and provenance rules
- [register-ops](register-ops/SKILL.md): Append-only `.po/register.jsonl` operations (`schemas/register.schema.json`, `scripts/register.py`)

## Stage skills

| Stage(s) | Skill | Purpose |
| --- | --- | --- |
| `idea`, `audience` | [jtbd-mom-test](jtbd-mom-test/SKILL.md) | Jobs to Be Done and Mom Test past-instance validation |
| `idea` | [lean-canvas](lean-canvas/SKILL.md) | One-page 9-box Lean Canvas and riskiest assumptions |
| `idea`, `audience`, `scope` | [opportunity-solution-trees](opportunity-solution-trees/SKILL.md) | Outcome -> Opportunities -> Candidate Solutions -> Assumption Tests |
| `actors` | [power-interest-stakeholder-map](power-interest-stakeholder-map/SKILL.md) | Power/Interest grid and behaviour-focused actor profiles |
| `systems` | [c4-context-eventstorming](c4-context-eventstorming/SKILL.md) | C4 Level 1/2 context and Process EventStorming flows |
| `scope` | [impact-mapping](impact-mapping/SKILL.md) | Goal (`Why`) -> Actor (`Who`) -> Behaviour (`How`) -> Deliverable (`What`) |
| `scope` | [story-mapping](story-mapping/SKILL.md) | User journey backbone and thin vertical release slices |
| `scope` | [moscow-non-goals](moscow-non-goals/SKILL.md) | MoSCoW prioritisation and Explicit Non-Goals with revisit triggers |
| `workshops` | [workshop-facilitation](workshop-facilitation/SKILL.md) | AI prepares agenda & writes up supplied notes; human runs live session |
| `presentations` | [pr-faq-presentations](pr-faq-presentations/SKILL.md) | Working Backwards PR/FAQ and stakeholder presentation outline |
| `fsd` | [fsd-iso-29148](fsd-iso-29148/SKILL.md) | ISO/IEC/IEEE 29148 FSD outline with One-Page PRD on top |
| `fsd`, `scope` | [invest-gwt-ears](invest-gwt-ears/SKILL.md) | INVEST user stories, numbered Given/When/Then, and EARS requirements |
| `fsd` | [iso-25010-quality](iso-25010-quality/SKILL.md) | ISO/IEC 25010 quality attribute checks and measurable NFRs |
| `fsd` | [ai-sdlc-loop-handoff](ai-sdlc-loop-handoff/SKILL.md) | Engineering handoff brief and Gate PR checklist for `ai-sdlc-loop` |
