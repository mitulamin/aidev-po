# 01 — Idea: Lantern Lane Tool Library — Loans & Reservations

> Fictional demo. Lantern Lane Tool Library, its people and its data are invented for the aidev-po worked example. Items tagged Simulated come from simulated personas and are not evidence; every other tag is used as it would be in a real product, inside the fiction.

- **Product slug**: `tool-library-loans`
- **Stage**: `idea`
- **Status**: `gate-approved`
- **Run ID**: `run-20261005093000-1a01`
- **Register**: `.po/register.jsonl`
<!-- TRACE_RESERVE: item_id_prefix=IDEA; trace_file=.po/traces.jsonl; fields=item_id,run,stage,agent,step,skill_versions,template_versions,upstream_ids,evidence_tag,register_refs -->

## 1. Problem Framing & Status Quo

| ID | Statement | Evidence Tag & Source | Upstream IDs |
| --- | --- | --- | --- |
| `IDEA-001` | Loans are tracked on paper cards that two volunteers copy into a shared spreadsheet; nobody sees an overdue tool until someone asks for it. Last month a tile cutter was out five weeks unnoticed. | `[Stated — r-20261005090500-2001]` | `-` |
| `IDEA-002` | If nothing is built: the coordinator keeps phoning late borrowers (about three hours a week), volunteers keep re-copying cards, and tools stay lost until someone asks. | `[Stated — r-20261005090500-2001, r-20261005090600-2002]` | `IDEA-001` |
| `IDEA-005` | House rule: three late returns in a year and a member loses borrowing for a month. | `[Stated — r-20261005090700-2003; inputs/house-rules.md rule 5]` | `-` |

## 2. Jobs to Be Done (JTBD) & Mom Test Evidence

| ID | Job Type | When `<situation>`, I want to `<motivation>`, so I can `<outcome>` | Last Real Instance / Past Workaround | Evidence Tag & Source | Upstream IDs |
| --- | --- | --- | --- | --- | --- |
| `IDEA-003` | Functional (member) | When I need a tool for a weekend job, I want to know it is in and have it held, so I do not make a wasted trip. | None collected yet; to be tested at Audience (CH-IDEA-001). | `[Assumed — r-20261005104000-200b]` | `IDEA-001` |
| `IDEA-004` | Functional (coordinator) | When a tool is late, I want to know straight away and remind the borrower, so tools come back without me phoning round. | The five-week tile cutter; three hours a week of calls. | `[Stated — r-20261005090500-2001, r-20261005090600-2002]` | `IDEA-001`, `IDEA-002` |

## 3. Lean Canvas

| ID | Box | Content | Evidence Tag & Source | Upstream IDs |
| --- | --- | --- | --- | --- |
| `IDEA-006` | Problem & Existing Alternatives | Overdue tools go unnoticed; members cannot see what is in. Today: paper cards, a shared spreadsheet, phone calls. | `[Inferred]` | `IDEA-001`, `IDEA-002` |
| `IDEA-007` | Customer Segments & Early Adopters | Members borrowing for home and garden jobs; early adopters are the Saturday regulars. Desk volunteers operate it. | `[Inferred]` | `IDEA-003`, `IDEA-004` |
| `IDEA-008` | Unique Value Proposition | "Know it's in, hold it, and get a nudge before it's due." | `[Inferred]` | `IDEA-006`, `IDEA-007` |
| `IDEA-009` | Solution (Top 3) | Online catalogue with availability and holds; desk check-out and check-in on a tablet; automatic reminder emails. | `[Inferred]` | `IDEA-006` |
| `IDEA-010` | Channels | The Saturday desk, the library's mailing list, posters in the hall. | `[Assumed — r-20261005104002-200d]` | `IDEA-007` |
| `IDEA-011` | Revenue Streams | None new. Membership stays pay-what-you-can; deposits stay refundable cash. | `[Stated — r-20261005090900-2005]` | `IDEA-007` |
| `IDEA-012` | Cost Structure | One-off build within a £6,000 community grant; small yearly hosting cost. | `[Stated — r-20261005090800-2004]` | `IDEA-009` |
| `IDEA-013` | Key Metrics | Loans more than a week overdue per month; coordinator hours spent chasing. | `[Inferred]` | `IDEA-008`, `IDEA-004` |
| `IDEA-014` | Unfair Advantage | A trusted local volunteer network already running the desk every Saturday. | `[Inferred]` | `IDEA-007` |

## 4. Initial Opportunity Solution Tree (Seed)

- **Desired Outcome (`IDEA-015`)**: loans more than a week overdue fall from about 12 a month to 4 or fewer by the end of the first season. `[Assumed — r-20261005104001-200c]`
  - **Opportunity (`IDEA-016`)**: borrowers forget return dates, and nobody notices until a tool is wanted. `[Inferred — IDEA-004]`
    - **Candidate Solution A (`IDEA-017`)**: automatic reminder emails before and after the due date. `[Inferred — IDEA-016]`
    - **Candidate Solution B (`IDEA-018`)**: an online catalogue showing what is in, with holds. `[Inferred — IDEA-003]`
    - **Assumption Test (`IDEA-019`)**: for four weeks, send reminder emails by hand from the spreadsheet and count late returns against the call log. `[Inferred — IDEA-017; added after CH-IDEA-002]`

## 5. Riskiest Assumptions (Top 3)

1. `IDEA-020`: most members read email reminders (r-20261005104002-200d).
2. `IDEA-021`: desk volunteers will record loans on a tablet instead of paper cards (r-20261005104003-200e).
3. `IDEA-022`: the shared spreadsheet is clean enough to import (r-20261005104004-200f).

## 6. Stage Exit Criteria (Given/When/Then)

- `AC-IDEA-001`: Given the coordinator's answers at intake, When the idea is framed, Then the status quo, the house rules and the riskiest assumptions are each written with an evidence tag and a source.

## 7. Decision Sheet (Locked)

| Decision ID | Choice | Who Decided | Why | Register ID |
| --- | --- | --- | --- | --- |
| `DEC-001` | Release 1 covers loans, reservations and reminders, not a full membership system. | `user` | The pain is overdue and unseen tools; membership admin works well enough on the spreadsheet. | `r-20261005141500-2012` |

## 8. Parked Items & Explicit Non-Goals

| Park ID | Item | Why It Can Wait | Revisit Trigger | Register ID |
| --- | --- | --- | --- | --- |
| `PARK-001` | Taking deposits online | Cash at the desk works and costs nothing; online payments add fees and set-up. | The treasurer reports more than 5 cash discrepancies in a quarter. | `r-20261005104005-2010` |

## Assumptions and open questions

=== REGISTER REQUESTS ===
[ASSUMPTION: Members make wasted trips because they cannot see whether a tool is in.]
[ASSUMPTION: About 12 loans a month go more than a week overdue (coordinator's estimate).]
[ASSUMPTION: Most members read email reminders.]
[ASSUMPTION: Desk volunteers will record loans on a tablet instead of paper cards.]
[ASSUMPTION: The shared spreadsheet is clean enough to import.]
[QUESTION: Should Release 1 take deposits online? Recommend: no; park it, deposits stay cash at the desk.]
=== END REGISTER REQUESTS ===
