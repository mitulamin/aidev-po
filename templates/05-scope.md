# 05 — Scope & Prioritisation: <Product Name>

- **Product slug**: `<slug>`
- **Stage**: `scope`
- **Status**: `draft` | `gate-approved`
- **Run ID**: `<run-id>`
- **Register**: `.po/register.jsonl`
<!-- TRACE_RESERVE: item_id_prefix=SCP; trace_file=.po/traces.jsonl; fields=item_id,run,stage,agent,step,skill_versions,template_versions,upstream_ids,evidence_tag,register_refs -->

## 1. Appetite

- **Appetite (`SCP-001`)**: `<user-set ceiling: budget, effort band, or timebox for Release 1>` `[Stated / Assumed — r-...]`
- **Scope Summary**: **In**: `<Slice 1>`; **Out**: `<Non-Goals PARK-NNN>`; **Later**: `<Slice 2+>`.

## 2. Impact Map (Why -> Who -> How -> What)

| ID | Why (Goal / Metric) | Who (`ACT-NNN`) | How (Actor Behaviour Change) | What (Candidate Deliverable) | Evidence Tag & Source | Upstream IDs |
| --- | --- | --- | --- | --- | --- | --- |
| `SCP-002` | ... | `ACT-002` | ... | ... | `[Inferred / Assumed — ...]` | `AUD-004`, `ACT-002` |

## 3. User Story Map (Backbone & Release Slices)

| Activity | Task (`SYS-NNN`) | Slice 1: Walking Skeleton / MVP | Slice 2: Release 2 | Later / Parked | Upstream IDs |
| --- | --- | --- | --- | --- | --- |
| `<Activity 1>` | `<Task 1.1>` | `SCP-003`: ... `[Tag]` | `SCP-004`: ... `[Tag]` | `PARK-005`: ... | `SCP-002`, `SYS-005` |

## 4. MoSCoW Prioritisation (Slice 1 Focus)

| ID | Capability / Story | MoSCoW (`Must` / `Should` / `Could` / `Won't`) | Slice | Why Essential / Workaround If Dropped | Evidence Tag & Source | Upstream IDs |
| --- | --- | --- | --- | --- | --- | --- |
| `SCP-003` | ... | `Must` | Slice 1 | ... | `[Stated / Inferred — ...]` | `SCP-002` |

## 5. Explicit Non-Goals & Parked Scope

| Park / NG ID | Excluded Item | Why Excluded Now | Who Might Want It | Revisit Trigger | Register ID | Upstream IDs |
| --- | --- | --- | --- | --- | --- | --- |
| `PARK-005` | ... | ... | `ACT-...` | `<concrete metric/signal/event>` | `r-...` | `SCP-002` |

## 6. Candidate Acceptance Criteria (Given/When/Then)

- `AC-SCP-001`: Given `<precondition>`, When `<Slice 1 user action>`, Then `<end-to-end outcome>`.

## 7. Decision Sheet (Locked)

| Decision ID | Choice | Who Decided | Why | Register ID |
| --- | --- | --- | --- | --- |
| `DEC-005` | ... | `user` / `po` | ... | `r-...` |

## Assumptions and open questions

=== REGISTER REQUESTS ===
None.
=== END REGISTER REQUESTS ===
