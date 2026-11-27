# 07 — Presentations (PR/FAQ & Deck Outline): Lantern Lane Tool Library — Loans & Reservations

> Fictional demo. Lantern Lane Tool Library, its people and its data are invented for the aidev-po worked example. Items tagged Simulated come from simulated personas and are not evidence; every other tag is used as it would be in a real product, inside the fiction.

- **Product slug**: `tool-library-loans`
- **Stage**: `presentations`
- **Status**: `gate-approved` (reopened and approved again by rerun RR-001 on 2026-11-12: `PRS-013` rebuilt)
- **Run ID**: `run-20261029093000-7a07`; rerun `run-20261112093000-9c09`
- **Register**: `.po/register.jsonl`
<!-- TRACE_RESERVE: item_id_prefix=PRS; trace_file=.po/traces.jsonl; fields=item_id,run,stage,agent,step,skill_versions,template_versions,upstream_ids,evidence_tag,register_refs -->

## 1. Working Backwards Press Release (<= 1 Page)

- **Headline (`PRS-001`)**: Lantern Lane members can now see what's in and hold it, without a wasted trip. `[Inferred — SCP-002]`
- **Sub-headline (`PRS-002`)**: The volunteer-run tool library swaps paper cards for a simple loans app, with reminders before tools are due. `[Inferred — SCP-005, SCP-008]`
- **Dateline & Launch Summary (`PRS-003`)**: Lantern Lane, March 2027 — members browse the catalogue on their phones, hold a tool for 48 hours, and get an email the day before it is due. Volunteers check tools out and in on a tablet at the Saturday desk. `[Inferred — SCP-005 to SCP-009]`
- **Problem Paragraph (`PRS-004`)**: Until now, nobody could see what was in without walking down, and late tools went unnoticed: this autumn a tile cutter was out for five weeks before anyone asked. The coordinator spent about three hours a week phoning borrowers. `[Stated — IDEA-002; Validated — AUD-003]`
- **Solution Paragraph (`PRS-005`)**: The catalogue shows live availability and takes holds; the desk records each loan once; reminders go out on their own; the coordinator sees every overdue loan on one page. `[Inferred — SCP-005 to SCP-009, SYS-001]`
- **Leader Quote (`PRS-006`)**: "I used to spend Monday evenings on the phone. Now I spend them fixing tools." — the coordinator `[Assumed — r-20261029110000-2050; approved by her with one word changed]`
- **Customer Quote (`PRS-007`)**: "I checked on my phone, held the hedge trimmer, and it was waiting for me." `[Simulated — illustrative launch quote based on AUD-005; NOT customer validation]`
- **Call to Action (`PRS-008`)**: Ask at the Saturday desk for your login, or reply to the library's mailing-list email. `[Inferred — IDEA-010]`

## 2. Customer / External FAQ

| ID | Question | Answer (Slice 1 Reality Only) | Evidence Tag & Source | Upstream IDs |
| --- | --- | --- | --- | --- |
| `PRS-009` | Who is this for and how do I start? | Every member. Ask at the desk for a login; your loans move across from the spreadsheet. | `[Inferred]` | `AUD-001`, `SCP-011` |
| `PRS-010` | What does it NOT do yet? | No online deposits, SMS reminders, waiting list, condition photos or delivery. | `[Stated — PARK-001, PARK-002, PARK-005, PARK-006]` | `PARK-001`, `PARK-002`, `PARK-005`, `PARK-006` |

## 3. Internal / Stakeholder FAQ (Hard Questions)

| ID | Hard Question | Candid Answer | Evidence Tag & Source | Upstream IDs |
| --- | --- | --- | --- | --- |
| `PRS-011` | What happens if nothing is built? | The coordinator keeps phoning, volunteers keep copying cards, and tools stay lost until someone asks. | `[Stated — IDEA-002]` | `IDEA-002` |
| `PRS-012` | What is the top failure mode? | Volunteers drift back to paper. The workshop lowers the risk: 7 of 8 did a mock check-out in under 2 minutes. Offline use is parked (`PARK-007`). | `[Validated — WKS-004]` | `WKS-004`, `PARK-007` |
| `PRS-013` | How are the house rules on late returns applied? | The app flags a member's third late return in 12 months for the coordinator. She speaks to them and decides; the app never suspends anyone by itself. | `[Stated — r-20261112090500-2069]` | `SCP-010` |

## 4. Narrative Memo (High-Power Stakeholders)

*For the board (`ACT-002`, Keep Satisfied). Every claim cites an item or register ID.*

- **Decision Requested (`PRS-014`)**: approve spending up to the £6,000 community grant on Release 1 (`SCP-005` to `SCP-011`). `[Inferred — SCP-001, DEC-006]`
- **Problem & Cost of Status Quo (`PRS-015`)**: about 12 loans a month go more than a week overdue; the coordinator spends about three hours a week chasing. `[Stated — IDEA-002; Assumed — r-20261005104001-200c]`
- **Recommended Slice 1 & Appetite (`PRS-016`)**: catalogue and holds, desk check-out and check-in, reminders, overdue dashboard and import, live before 2027-03-01. `[Stated — SCP-001, DEC-006]`
- **Explicit Non-Goals & Top Risks (`PRS-017`)**: online deposits, SMS, delivery and offline mode are parked with revisit triggers; the top risk is volunteers drifting back to paper (`PRS-012`). `[Stated — PARK-001, PARK-002, PARK-006, PARK-007]`

## 5. Stakeholder Presentation Outline

*Decision-led: one decision, answer first, for the board.*

| Slide | Title | Target Audience | Decision & Answer-First Key Point | Upstream IDs |
| --- | --- | --- | --- | --- |
| `PRS-018` | 1. Decision & Problem Cost | `ACT-002` | **Answer first**: approve up to £6,000 for Release 1; today costs three hours a week of calls and lost tools. | `PRS-014`, `IDEA-002` |
| `PRS-019` | 2. Who It Serves | `ACT-002` | 310 members borrow; 14 operators run the Saturday desk. | `AUD-001`, `ACT-003` |
| `PRS-020` | 3. Slice 1, Appetite & Non-Goals | `ACT-002` | Seven Must items within the grant; parked items listed with triggers. | `SCP-001`, `DEC-006`, `PRS-017` |
| `PRS-021` | 4. Risks & the Ask | `ACT-002` | Volunteer adoption is the top risk, already tested; we ask for approval today. | `PRS-012`, `PRS-014` |

## 6. Decision Sheet (Locked)

| Decision ID | Choice | Who Decided | Why | Register ID |
| --- | --- | --- | --- | --- |
| `DEC-008` | Ask the board to approve spending up to the £6,000 grant on Release 1; memo first, deck second. | `user` | The board meets on 2026-11-04 and reads papers in advance. | `r-20261030100300-2057` |

## 7. Parked Items & Explicit Non-Goals

| Park ID | Item | Why It Can Wait | Revisit Trigger | Register ID |
| --- | --- | --- | --- | --- |
| `PARK-008` | Impact report for the council community fund | Nothing to report until the app has run for a season. | The grant report falls due at the end of the first season. | `r-20261029110003-2053` |

## Assumptions and open questions

=== REGISTER REQUESTS ===
[ASSUMPTION: The leader quote is a draft for the coordinator to approve.]
[QUESTION: Keep the illustrative member quote in the press release? Recommend: keep it, labelled as illustrative and simulated.]
[QUESTION: What should the board be asked to decide? Recommend: approve spending up to the £6,000 grant on Release 1.]
[QUESTION: Write the funder impact report now? Recommend: no; park until the end of the season.]
=== END REGISTER REQUESTS ===
