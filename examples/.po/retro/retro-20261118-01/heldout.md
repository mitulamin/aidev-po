# Held-out results for retro-20261118-01

> Fictional demo for the aidev-po worked example. The runs below are described, not recorded: no model was actually run for this example.

Cases the proposer never saw, chosen from `heldout-pool.md`. Each run in a scratch copy: a scratch git worktree of aidev-po with the proposal's diff applied, and a copy of the case's product folder.

| Proposal | Case | Without the edit | With the edit | Regression? |
|----------|------|------------------|---------------|-------------|
| P-1 | tool-library-loans/SYS-008 automatic hold release | pass | pass | no |
| P-1 | tool-library-loans/SYS-010 automatic reminders | pass | pass | no |
| P-1 | tool-library-loans/SYS-009 deposit rule at check-out | pass | pass | no |
| P-2 | tool-library-loans/SYS-008 automatic hold release | pass | pass | no |
| P-2 | tool-library-loans/SYS-010 automatic reminders | pass | pass | no |
| P-2 | tool-library-loans/SYS-009 deposit rule at check-out | pass | pass | no |
| P-3 | tool-library-loans/SYS-008 automatic hold release | pass | fail | **yes** |
| P-3 | tool-library-loans/SYS-010 automatic reminders | pass | fail | **yes** |
| P-3 | tool-library-loans/SYS-009 deposit rule at check-out | pass | pass | no |

With P-3, the evidence audit failed `SYS-008` and `SYS-010` as "automation not stated upstream". `SYS-008`'s release is in DEC-004 and `SYS-010`'s reminders are in scope (`SCP-008`), but neither upstream item uses the word "automatic", so a literal check cannot tell them from `SYS-012`.

## Per proposal

| Proposal | Held-out before | Held-out after | Regressions |
|----------|-----------------|----------------|-------------|
| P-1 | 3 of 3 | 3 of 3 | none |
| P-2 | 3 of 3 | 3 of 3 | none |
| P-3 | 3 of 3 | 1 of 3 | `SYS-008`, `SYS-010` |

A proposal is accepted only if the held-in cases improve and no held-out case regresses (ai-sdlc-loop 9.9).
