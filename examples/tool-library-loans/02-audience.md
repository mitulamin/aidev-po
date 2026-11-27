# 02 — Audience: Lantern Lane Tool Library — Loans & Reservations

> Fictional demo. Lantern Lane Tool Library, its people and its data are invented for the aidev-po worked example. Items tagged Simulated come from simulated personas and are not evidence; every other tag is used as it would be in a real product, inside the fiction.

- **Product slug**: `tool-library-loans`
- **Stage**: `audience`
- **Status**: `gate-approved`
- **Run ID**: `run-20261012093000-2b02`
- **Register**: `.po/register.jsonl`
<!-- TRACE_RESERVE: item_id_prefix=AUD; trace_file=.po/traces.jsonl; fields=item_id,run,stage,agent,step,skill_versions,template_versions,upstream_ids,evidence_tag,register_refs -->

## 1. Target Segments & Early Adopters

| ID | Segment | Early-Adopter Characteristics | Frequency & Trigger | Current Spend / Cost of Problem | Evidence Tag & Source | Upstream IDs |
| --- | --- | --- | --- | --- | --- | --- |
| `AUD-001` | Members borrowing for home and garden jobs (about 310 active) | Saturday regulars who borrow monthly or more | A weekend job; most borrow a few times a year | Wasted trips; sometimes paying to hire instead (£35 a day in one case) | `[Stated — r-20261012090200-2018]` | `IDEA-007` |
| `AUD-002` | Desk volunteers (14 on the rota) | The Saturday desk team | Every Saturday, 10:00 to 13:00 | 20 to 30 minutes per shift re-copying cards into the spreadsheet | `[Stated — r-20261012090200-2018, r-20261005090600-2002]` | `IDEA-007` |

## 2. Mom Test Evidence & Last Real Instance Log

| ID | Segment | Real Past Instance (When / Context / Action Taken) | Current Workaround & Switching Friction | What They Already Tried / Paid For | Evidence Tag & Source | Upstream IDs |
| --- | --- | --- | --- | --- | --- | --- |
| `AUD-003` | `AUD-001` | Two of three members asked at the desk on 2026-10-10 had made a wasted trip or call in the past month; one hired a pressure washer instead. | Walk down or phone a number nobody answers on weekdays. | £35 hire (member M1). | `[Validated — inputs/desk-conversations-2026-10-10.md]` | `AUD-001`, `IDEA-003` |
| `AUD-004` | `AUD-002` | Every Saturday shift ends with two volunteers copying the day's cards into the spreadsheet. | Paper cards are quick at the desk; the copying is the cost. | A shared calendar for holds in spring 2025: volunteers double-booked and gave up after six weeks. | `[Stated — r-20261012090200-2018, r-20261005090600-2002]` | `AUD-002`, `IDEA-001` |

*Note: simulated user exploration is in Section 5 and tagged `[Simulated]`, never here.*

## 3. Value Proposition Canvas

| ID | Segment | Customer Jobs | Pains | Gains | Pain Relievers & Gain Creators | Unmatched Features (Cut/Park) | Evidence Tag & Source | Upstream IDs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `AUD-005` | `AUD-001` | When I need a tool for a weekend job, I want to know it is in and have it held, so I do not make a wasted trip. | Wasted trips; forgetting return dates. | Getting the tool first time. | Live availability; a 48-hour hold; a reminder before the due date. | Tool reviews and ratings: fix no pain, cut. | `[Inferred]` | `AUD-003` |
| `AUD-006` | `AUD-002` | When I run the desk, I want to record a loan once, so I can go home when the shift ends. | Re-copying cards; reading handwriting. | Shift ends on time. | Check-out and check-in on a tablet; no copying. | Volunteer rota planning: not this pain, cut. | `[Inferred]` | `AUD-004` |

## 4. Expanded Opportunity Solution Tree

- **Desired Outcome (`AUD-007`)**: loans more than a week overdue fall to 4 or fewer a month by the end of the first season, and no member reports a wasted trip in the end-of-season survey. (upstream: `IDEA-015`) `[Assumed — r-20261005104001-200c]`
  - **Opportunity (`AUD-008`)**: members cannot see whether a tool is in before they come. (upstream: `IDEA-016`, `AUD-003`) `[Validated — AUD-003]`
    - **Sub-opportunity (`AUD-009`)**: borrowers forget the return date. `[Stated — inputs/desk-conversations-2026-10-10.md, member M3]`
      - **Candidate Solution 1 (`AUD-010`)**: a reminder email the day before the due date and an overdue notice the day after. `[Inferred — AUD-009]`
      - **Candidate Solution 2 (`AUD-011`)**: online availability with a 48-hour hold. `[Inferred — AUD-008]`
      - **Fastest Assumption Test (`AUD-012`)**: the four-week hand-sent reminder test from `IDEA-019`. `[Inferred — IDEA-019]`

## 5. Discovery & Validation Plan (Incl. `[Simulated]` Gap Checks)

| ID | Hypothesis / Gap | Research Method | Pass / Falsify Criterion | Tag | Upstream IDs |
| --- | --- | --- | --- | --- | --- |
| `AUD-013` | Gap found by a simulated walk-through as an older member without email: reminders by email alone may miss some members. **Simulated persona, not evidence.** | Count members with no email address after the import; ask ten members at the desk how they want reminders. | Pass if 80% or more of active members have a working email address. | `[Simulated]` | `AUD-010` |
| `AUD-014` | At least one in four loans will start with an online reservation. | Count reservations against loans in the first two months. | Falsified if fewer than 1 in 10 loans start online. | `[Assumed — r-20261012110000-201a]` | `AUD-011` |

## 6. Stage Exit Criteria (Given/When/Then)

- `AC-AUD-001`: Given the members and volunteers segments, When the gate is held, Then each has at least one real past instance with a source, and any simulated input is labelled and not counted as evidence.

## 7. Decision Sheet (Locked)

| Decision ID | Choice | Who Decided | Why | Register ID |
| --- | --- | --- | --- | --- |
| `DEC-002` | Members are the primary segment; desk volunteers are the operators. | `user` | Members feel the wasted trips; volunteers run the system for them. | `r-20261012145000-201d` |

## 8. Parked Items & Explicit Non-Goals

| Park ID | Item | Why It Can Wait | Revisit Trigger | Register ID |
| --- | --- | --- | --- | --- |
| `PARK-002` | SMS reminders | Cost per message, and nobody yet knows how many members lack email. | More than 20% of active members have no working email address after the import. | `r-20261012110002-201c` |

## Assumptions and open questions

=== REGISTER REQUESTS ===
[ASSUMPTION: At least one in four loans will start with an online reservation.]
[ASSUMPTION: About one in ten members have no email address on file.]
[QUESTION: Should Release 1 send SMS reminders? Recommend: no; park until we know how many members lack email.]
=== END REGISTER REQUESTS ===
