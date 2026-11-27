# 05 — Scope & Prioritisation: Lantern Lane Tool Library — Loans & Reservations

> Fictional demo. Lantern Lane Tool Library, its people and its data are invented for the aidev-po worked example. Items tagged Simulated come from simulated personas and are not evidence; every other tag is used as it would be in a real product, inside the fiction.

- **Product slug**: `tool-library-loans`
- **Stage**: `scope`
- **Status**: `gate-approved` (reopened and approved again by rerun RR-001 on 2026-11-12: `SCP-010` rebuilt)
- **Run ID**: `run-20261020093000-5e05`; rerun `run-20261112093000-9c09`
- **Register**: `.po/register.jsonl`
<!-- TRACE_RESERVE: item_id_prefix=SCP; trace_file=.po/traces.jsonl; fields=item_id,run,stage,agent,step,skill_versions,template_versions,upstream_ids,evidence_tag,register_refs -->

## 1. Appetite

- **Appetite (`SCP-001`)**: Release 1 within the £6,000 community grant, live before the spring season on 2027-03-01. `[Stated — r-20261005090800-2004]`
- **Scope Summary**: **In**: Slice 1 (`SCP-005` to `SCP-011`); **Out**: `PARK-005`, `PARK-006` and earlier parked items; **Later**: Slice 2 (`SCP-012`, `SCP-013`).

## 2. Impact Map (Why -> Who -> How -> What)

| ID | Why (Goal / Metric) | Who | How (Behaviour Change) | What (Candidate Deliverable) | Evidence Tag & Source | Upstream IDs |
| --- | --- | --- | --- | --- | --- | --- |
| `SCP-002` | Overdue loans down to 4 or fewer a month | `ACT-004` | Members return tools on time and see availability before coming | Reminder emails; online catalogue with holds | `[Inferred]` | `AUD-007`, `ACT-004` |
| `SCP-003` | Shifts end on time | `ACT-003` | Volunteers record each loan once, at the desk | Check-out and check-in on the tablet | `[Inferred]` | `AUD-006`, `ACT-003` |
| `SCP-004` | Coordinator stops chasing by phone | `ACT-001` | The coordinator works from a list instead of the spreadsheet | Overdue dashboard | `[Inferred]` | `IDEA-004`, `ACT-001` |

## 3. User Story Map (Backbone & Release Slices)

| Activity | Task | Slice 1: Walking Skeleton / MVP | Slice 2: Release 2 | Later / Parked | Upstream IDs |
| --- | --- | --- | --- | --- | --- |
| Find a tool | Browse and reserve (`SYS-007`) | `SCP-005` browse with availability; `SCP-006` reserve with a 48-hour hold | `SCP-012` waiting list | `PARK-006` delivery | `SCP-002`, `SYS-007` |
| Borrow and return | Desk check-out and check-in (`SYS-009`, `SYS-011`) | `SCP-007` check-out and check-in with deposit record | — | `PARK-005` condition photos | `SCP-003`, `SYS-009` |
| Stay on time | Reminders and follow-up (`SYS-010`, `SYS-012`) | `SCP-008` reminder and overdue emails; `SCP-009` overdue dashboard; `SCP-010` flag third late return for review | `SCP-013` member loan history | — | `SCP-002`, `SCP-004`, `SYS-010` |
| Get started | Move off the spreadsheet (`SYS-004`) | `SCP-011` one-off import | — | — | `SYS-004` |

## 4. MoSCoW Prioritisation (Slice 1 Focus)

| ID | Capability / Story | MoSCoW | Slice | Why Essential / Workaround If Dropped | Evidence Tag & Source | Upstream IDs |
| --- | --- | --- | --- | --- | --- | --- |
| `SCP-005` | Browse the catalogue with live availability | `Must` | Slice 1 | Without it wasted trips continue. | `[Inferred]` | `SCP-002`, `AUD-008` |
| `SCP-006` | Reserve a tool; hold 48 hours, then release | `Must` | Slice 1 | Availability alone does not stop someone else taking it first. | `[Stated — r-20261016113000-202f]` | `SCP-002`, `SYS-008` |
| `SCP-007` | Desk check-out and check-in on the tablet, with deposit record | `Must` | Slice 1 | Without it the cards and the copying stay. | `[Inferred]` | `SCP-003`, `SYS-009`, `SYS-011` |
| `SCP-008` | Reminder email the day before due; overdue notice the day after | `Must` | Slice 1 | The main lever on late returns. | `[Inferred]` | `SCP-002`, `SYS-010` |
| `SCP-009` | Overdue dashboard for the coordinator | `Must` | Slice 1 | Without it the coordinator still searches the spreadsheet. | `[Inferred]` | `SCP-004` |
| `SCP-010` | Flag a member's third late return in 12 months on the dashboard for the coordinator's review; only the coordinator records a suspension | `Must` | Slice 1 | The house rule must be visible, but applied by a person. | `[Stated — r-20261112090500-2069]` | `SYS-012`, `SCP-004` |
| `SCP-011` | One-off import from the spreadsheet, after the coordinator merges duplicates (`SYS-013`) | `Must` | Slice 1 | Re-keying 310 members and 400 tools by hand is not realistic. | `[Inferred]` | `SYS-004`, `SYS-013` |
| `SCP-012` | Waiting list when a tool is reserved | `Should` | Slice 2 | Workaround: check again later. | `[Stated — r-20261020113001-203b]` | `SCP-006` |
| `SCP-013` | Members see their own loan history | `Could` | Slice 2 | Workaround: ask at the desk. | `[Inferred]` | `ACT-011` |

## 5. Explicit Non-Goals & Parked Scope

| Park / NG ID | Excluded Item | Why Excluded Now | Who Might Want It | Revisit Trigger | Register ID | Upstream IDs |
| --- | --- | --- | --- | --- | --- | --- |
| `PARK-005` | Photos of tool condition at check-in | Damage disputes are rare; adds a step at a busy desk. | `ACT-001` | More than 3 damage disputes in a quarter. | `r-20261020113002-203c` | `SCP-007` |
| `PARK-006` | Delivery or collection service | Needs drivers, insurance and a new process. | `ACT-004` | The funder asks for it, or 10 members ask for it in a season. | `r-20261020113003-203d` | `SCP-002` |

## 6. Candidate Acceptance Criteria (Given/When/Then)

- `AC-SCP-001`: Given a member sees a drill is in, When they reserve it on their phone and arrive within 48 hours, Then a volunteer checks it out to them on the tablet and the reminder email arrives the day before it is due.

## 7. Decision Sheet (Locked)

| Decision ID | Choice | Who Decided | Why | Register ID |
| --- | --- | --- | --- | --- |
| `DEC-005` | Overrule CH-SCOPE-001: build the online catalogue with holds rather than a shared calendar and mail-merge reminders. | `user` | The library tried a shared calendar in spring 2025; volunteers double-booked and gave up after six weeks. | `r-20261020150100-2040` |
| `DEC-006` | Release 1 is Slice 1, `SCP-005` to `SCP-011`. Slice 2 waits for a season of use. | `user` | Fits the appetite; each item answers a pain with evidence. | `r-20261020150300-2042` |

## Assumptions and open questions

=== REGISTER REQUESTS ===
[ASSUMPTION: Volunteers will keep using the tablet after the first month.]
[QUESTION: Should a waiting list be in Release 1? Recommend: Slice 2.]
[QUESTION: Should check-in take photos of tool condition? Recommend: no; park.]
[QUESTION: Should Release 1 offer delivery or collection? Recommend: no; park.]
=== END REGISTER REQUESTS ===
