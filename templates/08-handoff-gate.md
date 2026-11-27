# 08b — Engineering Handoff & Gate PR Brief: <Product Name>

- **Product slug**: `<slug>`
- **Target Engineering Repo**: `<owner/repo or TBD>`
- **Source FSD**: `08-fsd.md`
- **Register**: `.po/register.jsonl`
- **Handoff Target**: `ai-sdlc-loop` coordinator (`/plan`)
<!-- TRACE_RESERVE: item_id_prefix=HND; trace_file=.po/traces.jsonl; fields=item_id,run,stage,agent,step,skill_versions,template_versions,upstream_ids,evidence_tag,register_refs -->

## 1. Handoff Readiness Gate

- [ ] `fsd-reviewer`: `Verdict: PASS` (zero P0/P1 findings)
- [ ] `evidence-auditor`: `Verdict: PASS` (zero untagged/unsourced claims)
- [ ] `challenger`: all challenges resolved or recorded as decisions
- [ ] `.po/register.jsonl`: zero `open` or `surfaced` high-urgency questions (`scripts/register.py list --open`)

## 2. Brief for `ai-sdlc-loop` `/plan`

- **Goal (`HND-001`)**: `<from One-Page PRD FSD-001..004>`
- **Users & Actors (`HND-002`)**: `<from ACT-NNN>`
- **Scope — Slice 1 Only (`HND-003`)**: `<list US-NNN, REQ-NNN, NFR-NNN>`
- **Authoritative Spec Path**: `<path to 08-fsd.md>`

## 3. Locked Decisions (Do Not Override Downstream)

| Decision ID | Choice | Who Decided | Why | Register ID |
| --- | --- | --- | --- | --- |
| `DEC-001` | ... | `user` | ... | `r-...` |

## 4. Explicit Non-Goals (Do Not Build)

| Park ID | Excluded Capability | Reason | Revisit Trigger |
| --- | --- | --- | --- |
| `PARK-001` | ... | ... | ... |

## 5. Numbered Acceptance Criteria Index (Given/When/Then)

- `AC-001` (`US-001`): Given ..., When ..., Then ...

## 6. Gate PR Plan (Requires Explicit User OK)

- **Proposed branch in target repo**: `<e.g. docs/fsd-<slug>>`
- **Files to include in Gate PR**: `08-fsd.md`, `08-handoff-gate.md`
- **User approval to open Gate PR**: `PENDING USER OK` (never push or open PR without explicit user approval)

## Assumptions and open questions

=== REGISTER REQUESTS ===
None.
=== END REGISTER REQUESTS ===
