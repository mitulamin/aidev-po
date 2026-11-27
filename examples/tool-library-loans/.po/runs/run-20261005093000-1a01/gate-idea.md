# Stage Gate Report: Lantern Lane Tool Library — Idea

> Fictional demo for the aidev-po worked example.

- **Product slug**: `tool-library-loans`
- **Stage**: `idea`
- **Run ID**: `run-20261005093000-1a01`
- **Date (UTC)**: `2026-10-05T14:30:00Z`

## 1. Stage Artefact Produced

- **Artefact**: `01-idea.md`
- **Summary**:
  - Problem: loans on paper cards and a spreadsheet; overdue tools unnoticed (IDEA-001, IDEA-002), from the intake answers.
  - House rule recorded as IDEA-005. (Later found to have dropped "I always have a word with them first" from the answer; see AT-001's alternatives.)
  - Lean Canvas IDEA-006 to IDEA-014; outcome IDEA-015 rests on an estimate (r-A2).
  - Riskiest assumptions IDEA-020 to IDEA-022, each in the register.

## 2. Fresh-Context Verdicts

| Check | Agent | Verdict | Findings File | Notes |
| --- | --- | --- | --- | --- |
| Stage Review | `idea-reviewer` | `PASS` | this report | P2 on IDEA-015: baseline is an estimate. Re-reviewed after IDEA-019 was added: PASS. |
| Evidence Audit | `evidence-auditor` | `PASS` | this report | No findings. |
| PO Challenge | `challenger` | `2 challenges` | this report | See below. |

## 3. Challenger Items & Overrules

| Challenge ID | Challenge Summary | Resolution | Decision / Register ID |
| --- | --- | --- | --- |
| `CH-IDEA-001` | Mom Test: no real instance of a member making a wasted trip (IDEA-003). | Parked to Audience: the coordinator will ask three members at the desk. | `r-20261005133000-2011` |
| `CH-IDEA-002` | Build Nothing: hand-sent reminders from the spreadsheet might be enough. | Accepted & Fixed: added as assumption test IDEA-019. | — |

## 4. Open Register Items & Outliner Q&A Rounds

Intake, before the producer ran (one round, five questions, each with a recommended answer):

| Register ID | Type | Question / Assumption | User Decision / Answer | Status |
| --- | --- | --- | --- | --- |
| `r-20261005090500-2001` | `question` | Last time a loan went badly? | Tile cutter out five weeks; paper cards and a spreadsheet. | `answered` |
| `r-20261005090600-2002` | `question` | Who feels it most, and the cost? | The coordinator, about three hours a week. | `answered` |
| `r-20261005090700-2003` | `question` | House rules on late returns? | Three in a year loses borrowing for a month; "I always have a word with them first." | `answered` |
| `r-20261005090800-2004` | `question` | Budget and deadline? | £6,000 grant; live before March 2027. | `answered` |
| `r-20261005090900-2005` | `question` | How do members pay? | Pay-what-you-can; cash deposits on power tools. | `answered` |

Gate, round 1 (four questions):

| Register ID | Type | Question / Assumption | User Decision / Answer | Status |
| --- | --- | --- | --- | --- |
| `r-20261005141500-2012` | `decision` | Release 1 scope (recommended: loans, reservations, reminders; not membership). | Agreed. DEC-001. | `decided` |
| `r-20261005104001-200c` | `assumption` | About 12 overdue loans a month (recommended: check the call log). | 10 to 14 a month. | `answered` |
| `r-20261005104005-2010` | `question` | Online deposits (recommended: no; park). | Park. PARK-001, trigger: more than 5 cash discrepancies in a quarter. | `answered` |
| `r-20261005133000-2011` | `question` | Last real wasted trip (recommended: ask three members on Saturday). | Will ask on 2026-10-10. | `surfaced` |

Still open after the gate: `r-20261005104000-200b`, `r-20261005104002-200d`, `r-20261005104003-200e`, `r-20261005104004-200f` (assumptions to test later).

## 5. Gate Decision & Products-Repo Commit

- **User Gate Decision**: `APPROVE & ADVANCE`
- **Next Stage**: `audience`
- **Products-Repo Commit**: `User OK: Yes` — `tool-library-loans: complete idea stage — problem, house rules, lean canvas, riskiest assumptions`

## Assumptions and open questions

=== REGISTER REQUESTS ===
None.
=== END REGISTER REQUESTS ===
