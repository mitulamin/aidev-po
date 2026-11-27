# 03 — Actors & Stakeholders: Lantern Lane Tool Library — Loans & Reservations

> Fictional demo. Lantern Lane Tool Library, its people and its data are invented for the aidev-po worked example. Items tagged Simulated come from simulated personas and are not evidence; every other tag is used as it would be in a real product, inside the fiction.

- **Product slug**: `tool-library-loans`
- **Stage**: `actors`
- **Status**: `gate-approved`
- **Run ID**: `run-20261014093000-3c03`
- **Register**: `.po/register.jsonl`
<!-- TRACE_RESERVE: item_id_prefix=ACT; trace_file=.po/traces.jsonl; fields=item_id,run,stage,agent,step,skill_versions,template_versions,upstream_ids,evidence_tag,register_refs -->

## 1. Power / Interest Stakeholder Map

| ID | Stakeholder / Group | Role Type | Power | Interest | Quadrant Strategy | Evidence Tag & Source | Upstream IDs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ACT-001` | Coordinator (part-time, paid) | Decision Maker / Operator | High | High | Manage Closely | `[Stated — r-20261005090600-2002, r-20261014090000-2021]` | `IDEA-004` |
| `ACT-002` | Board of trustees, including the treasurer | Buyer (signs off grant spend) | High | Low | Keep Satisfied | `[Stated — r-20261014090100-2022]` | `IDEA-012` |
| `ACT-003` | Desk volunteers | Operator | Low | High | Keep Informed | `[Stated — r-20261012090200-2018]` | `AUD-002` |
| `ACT-004` | Members | User | Low | High | Keep Informed | `[Stated — r-20261012090200-2018]` | `AUD-001` |
| `ACT-005` | Council community fund (grant funder) | Gatekeeper | High | Low | Keep Satisfied | `[Stated — r-20261014090100-2022]` | `IDEA-012` |

## 2. Actor & User Profiles

| ID | Actor Name | Primary Goal(s) | Usage Context & Frequency | Tech Literacy / Accessibility / Device | Trust Level & Permission Boundary | Evidence Tag & Source | Upstream IDs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ACT-006` | Coordinator | Stop chasing late tools by phone; see what is overdue at a glance. | Weekdays at home on a laptop; Saturdays at the desk. | Confident; uses the shared spreadsheet daily. | Full administration. | `[Stated — r-20261005090600-2002, r-20261014090000-2021]` | `ACT-001`, `IDEA-004` |
| `ACT-007` | Desk volunteer | Record a loan once and finish the shift on time. | Saturdays 10:00 to 13:00 on a shared desk tablet. | Mixed; some have never used a tablet. Large text needed. | Runs the desk; no refunds or membership changes. | `[Stated — r-20261014090000-2021; Inferred — AUD-004]` | `ACT-003`, `AUD-004` |
| `ACT-008` | Member | Know a tool is in, hold it, and be reminded before it is due. | Own phone, mostly evenings and Saturday mornings. | Wide range; about one in ten may have no email on file. | Own loans and reservations only. | `[Assumed — r-20261012110001-201b]` | `ACT-004`, `AUD-005` |
| `ACT-012` | Treasurer (board member) | Reconcile cash deposits each month. | Monthly, at home. | Confident with spreadsheets. | Read-only deposit reports. | `[Stated — r-20261014090100-2022]` | `ACT-002` |

## 3. Roles, Permissions & Decision Rights

| ID | Actor ID | Can View | Can Create / Edit | Can Approve / Administer | Forbidden Actions | Evidence Tag & Source | Upstream IDs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ACT-009` | `ACT-006` | Everything | Tools, members, loans, reservations | Deposit refunds and write-offs; member accounts; volunteer logins | None | `[Stated — r-20261014090000-2021]` | `ACT-006` |
| `ACT-010` | `ACT-007` | Tools, members' names and contact details, loans | Check-out, check-in, taking a deposit | Nothing | Refunding a deposit; changing membership; deleting anything | `[Stated — r-20261014090000-2021]` | `ACT-007` |
| `ACT-011` | `ACT-008` | The catalogue and availability; own loans and reservations | Own reservations | Nothing | Seeing any other member's details or loans | `[Stated — r-20261014090000-2021]` | `ACT-008` |
| `ACT-013` | `ACT-012` | Deposit report (taken, refunded, written off) | Nothing | Nothing | Changing loans or deposits | `[Stated — r-20261014090100-2022]` | `ACT-012` |

## 4. Stage Exit Criteria (Given/When/Then)

- `AC-ACT-001`: Given a desk volunteer is logged in, When they try to refund a deposit, Then the action is not offered, and the coordinator is the only actor who can approve refunds and write-offs.

## 5. Decision Sheet (Locked)

| Decision ID | Choice | Who Decided | Why | Register ID |
| --- | --- | --- | --- | --- |
| `DEC-003` | Each volunteer has their own login; there is no shared desk account. | `user` | Every loan then shows who recorded it (raised by CH-ACT-001). | `r-20261014145000-2027` |

## 6. Parked Items & Explicit Non-Goals

| Park ID | Item | Why It Can Wait | Revisit Trigger | Register ID |
| --- | --- | --- | --- | --- |
| `PARK-003` | Members editing their own details online | Changes are rare and the desk handles them in seconds. | The desk gets more than 10 change requests in a month. | `r-20261014110001-2026` |

## Assumptions and open questions

=== REGISTER REQUESTS ===
[QUESTION: Should volunteers share one desk login or have their own? Recommend: their own, so every loan shows who recorded it.]
[QUESTION: Can members edit their own details online? Recommend: no in Release 1; park.]
=== END REGISTER REQUESTS ===
