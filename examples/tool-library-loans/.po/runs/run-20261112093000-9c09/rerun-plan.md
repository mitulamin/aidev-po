# Rerun plan RR-001 for tool-library-loans

> Fictional demo for the aidev-po worked example. Shown to the user on 2026-11-12 at 09:20; approved at 09:25.

Feedback: FB-001. Attribution: AT-001 (confirmed by the user; confidence 0.8 after replay).

## Start from

systems / systems-producer / step 3-event-storming (run run-20261016093000-4d04), item `SYS-012`.

## Correction

"The system never suspends anyone by itself: it flags a member's third late return in 12 months for the coordinator, who speaks to them and decides; only the coordinator sets or lifts a suspension.", recorded as register r-20261112090500-2069. Replaces: none (no earlier decision said the suspension was automatic; `SYS-012` inferred it).

## What will be rebuilt

| Stage | File | Item | Now says |
|-------|------|------|----------|
| systems | `04-systems.md` | `SYS-012` | Third late return in 12 months, then SuspendMember for 30 days (automatic). |
| systems | `04-systems.md` | `SYS-018` | Suspension: 30 days without borrowing, started by the third late return. |
| scope | `05-scope.md` | `SCP-010` | Must: automatic 30-day suspension. |
| presentations | `07-presentations.md` | `PRS-013` | House rules are applied automatically. |
| fsd | `08-fsd.md` | `US-007` | Coordinator wants members suspended automatically. |
| fsd | `08-fsd.md` | `AC-011` | Third late return blocks borrowing and emails the member. |
| fsd | `08-fsd.md` | `REQ-004` | The system shall suspend the member for 30 days. |
| fsd | `08-handoff-gate.md` | `HND-003` | Scope for /plan, including automatic suspension. |

8 item(s) in 4 stage(s). The FSD producer may add items for the coordinator's own suspension step (it added `AC-014` and `REQ-008`).

## Gates reopened

systems, scope, presentations, fsd: each comes back to you for approval.

## Also affected

- The board deck was shared on 2026-11-04 with the old `PRS-013`; send the board the corrected FAQ answer.
- The gate PR to the build team has not been opened (`PENDING USER OK`), so nothing downstream of the handoff needs undoing.

## Narrower option

Keep `FSD-004` (the Slice 1 solution summary, which lists "the late-return house rule (`SCP-010`)" without saying how it is applied) and `HND-001` (the goal for /plan, built from `FSD-001` to `FSD-004`). Both are downstream of `SYS-012` only through `SCP-010`, and neither says the rule is automatic, so rebuilding them would change no words. Recommended.

## Before starting

- Products repo working tree: clean.
- Nothing is rebuilt until you say yes. Nothing is committed without a second yes. Nothing is pushed.

Go ahead? **narrower** (the user's answer, 09:25)
