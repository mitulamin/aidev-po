# Held-out results for <retro-id>

Cases the proposer never saw, chosen from `heldout-pool.md`. Each run in a scratch copy: a scratch git worktree of aidev-po with the proposal's diff applied, and a copy of the case's product folder.

| Proposal | Case | Without the edit | With the edit | Regression? |
|----------|------|------------------|---------------|-------------|
| P-<n> | <examples/<slug> actors stage> | pass | pass | no |
| P-<n> | <product/FB-ID from an earlier retro> | pass | fail | **yes** |

## Per proposal

| Proposal | Held-out before | Held-out after | Regressions |
|----------|-----------------|----------------|-------------|
| P-<n> | <3 of 3> | <3 of 3> | none |

A proposal is accepted only if the held-in cases improve and no held-out case regresses (ai-sdlc-loop 9.9).
