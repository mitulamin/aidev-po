# 06 — Workshops: Lantern Lane Tool Library — Loans & Reservations

> Fictional demo. Lantern Lane Tool Library, its people and its data are invented for the aidev-po worked example. Items tagged Simulated come from simulated personas and are not evidence; every other tag is used as it would be in a real product, inside the fiction.

- **Product slug**: `tool-library-loans`
- **Stage**: `workshops`
- **Status**: `gate-approved`
- **Human Facilitator**: the coordinator (AI prepared the agenda and wrote up her notes; she ran the session)
- **Run ID**: `run-20261022093000-6f06`
- **Register**: `.po/register.jsonl`
<!-- TRACE_RESERVE: item_id_prefix=WKS; trace_file=.po/traces.jsonl; fields=item_id,run,stage,agent,step,skill_versions,template_versions,upstream_ids,evidence_tag,register_refs -->

## Part A — Pre-Workshop Agenda & Facilitation Guide (AI Prepared)

### A1. Workshop Objective & Target Assumptions to Settle

| ID | Target Register ID / Assumption | Question / Risk to Settle | Desired Output | Upstream IDs |
| --- | --- | --- | --- | --- |
| `WKS-001` | `r-20261005104003-200e`, `r-20261020113000-203a` | Will volunteers record loans on a tablet, and keep doing so? | Confirm / Falsify | `IDEA-021`, `SCP-007` |
| `WKS-002` | `SYS-009` | Does the check-out flow, with deposits, fit a busy Saturday desk? | Confirm / Decide | `SYS-009`, `SCP-007` |
| `WKS-003` | `r-20261016113002-2031` | Who merges duplicate members before the import, and how many are there? | Decide | `SYS-013` |

### A2. Participants & Roles

| Stakeholder / Role | Actor ID | Why Needed | Pre-Read Sent |
| --- | --- | --- | --- |
| Desk volunteers (8 of 14) | `ACT-003` | They run the desk and will use the tablet. | Yes |
| Coordinator (facilitator) | `ACT-001` | Owns the product; runs the session. | Yes |
| Treasurer (notes) | `ACT-012` | Reconciles deposits; takes notes and times the mock check-outs. | Yes |

### A3. Timeboxed Agenda (Human Facilitator Runs)

| Block | Duration | Exercise / Non-Leading Prompts | Capture Target |
| --- | --- | --- | --- |
| 1. Context & Ground Rules | 10 min | Share the problem and what is out of scope; ask for real recent examples, no pitching. | `WKS-001` |
| 2. Mock check-out | 30 min | Each volunteer checks out three tools on the clickable mock-up while the treasurer times it. "Tell me about the last busy Saturday: what slowed you down?" | `WKS-001`, `WKS-002` |
| 3. Deposits and import | 15 min | "When did a deposit last cause a problem? What happened?" "Who would merge duplicate members?" | `WKS-002`, `WKS-003` |

### A4. Live Capture Sheet (For Facilitator)

- **Participant quotes / past examples**: in the notes file below.
- **Workflow corrections / missing constraints**: deposits, waivers.
- **Decisions agreed / disputed**: listed in the notes file.

---

## Part B — Post-Workshop Write-Up (AI Synthesised from Human Notes)

*Status: notes supplied 2026-10-27; synthesised 2026-10-28.*

### B1. Session Metadata

- **Date**: 2026-10-27
- **Facilitator**: the coordinator
- **Attendees**: 8 desk volunteers, the coordinator, the treasurer
- **Raw Notes Source**: `workshops/2026-10-27-notes.md`

### B2. Synthesised Findings & Evidence Updates

| ID | Finding / Quote | Evidence Tag & Source | Impact on Register | Upstream Artefact Update Needed |
| --- | --- | --- | --- | --- |
| `WKS-004` | 7 of 8 volunteers finished a mock check-out in under 2 minutes; the eighth did it in 1:55 on a second try. | `[Validated — workshops/2026-10-27-notes.md, "Mock check-out"]` | Confirmed `r-20261005104003-200e` | None |
| `WKS-005` | Only the coordinator may waive a deposit, and she records why. Agreed by the room. | `[Stated — workshops/2026-10-27-notes.md, "Deposits"]` | New question `r-20261028103000-2049`, decided at the gate as `DEC-007` | `08-fsd.md` (new requirement) |
| `WKS-006` | About 25 duplicate member rows; the coordinator merges them before the import. | `[Stated — workshops/2026-10-27-notes.md, "Import"]` | Answered `r-20261016113002-2031` | None (`SCP-011` already depends on it) |
| `WKS-007` | The hall Wi-Fi dropped once for about a minute; a volunteer says it happens most Saturdays. Not measured. | `[Stated — workshops/2026-10-27-notes.md, "Wi-Fi"]` | New question `r-20261028103001-204a` | None |

## 3. Decision Sheet (Locked)

| Decision ID | Choice | Who Decided | Why | Register ID |
| --- | --- | --- | --- | --- |
| `DEC-007` | Only the coordinator can waive a deposit, with a reason recorded. | `user` | Agreed with the volunteers at the workshop; keeps the treasurer's reconciliation simple. | `r-20261028150100-204d` |

## 4. Parked Items & Explicit Non-Goals

| Park ID | Item | Why It Can Wait | Revisit Trigger | Register ID |
| --- | --- | --- | --- | --- |
| `PARK-007` | Offline mode for the desk tablet | One short drop seen; paper cards remain the fallback for a few minutes. | The hall Wi-Fi fails for more than 5 minutes on two or more Saturdays in a month. | `r-20261028103001-204a` |

## Assumptions and open questions

=== REGISTER REQUESTS ===
[QUESTION: Who facilitates the volunteer session? Recommend: the coordinator, with the treasurer taking notes.]
[QUESTION: Can volunteers waive a deposit for regular members? Recommend: only the coordinator can, with a reason.]
[QUESTION: Should the desk tablet work offline? Recommend: no; park.]
=== END REGISTER REQUESTS ===
