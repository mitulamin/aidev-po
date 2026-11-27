Verdict: FAIL

# Learn review, round 1 — retro-20261118-01

> Fictional demo for the aidev-po worked example. `learn-reviewer`, fresh context, given the brief's task and acceptance criteria, `proposals.md` (round 1), the diffs and `heldout.md`.

## P-1: say who decides for any policy that applies a sanction — PASS

- One surface, global, judgement placed in the skill step. No client words in the diff.
- Held-in 0 → 1; held-out 3 of 3 before and after.
- P3: "changes a person's rights" is broad; acceptable because the edit only adds a question when the inputs are silent.

## P-2: this client applies house rules in person — PASS

- Client scope, in `.po/preferences.md`; held-in 0 → 1; held-out unchanged.

## P-3: evidence-auditor fails unstated automation — FAIL

- P1: held-out regressions on `SYS-008` and `SYS-010`; acceptance requires none.
- P1: "adds automation its upstream items do not state" is a judgement presented as a literal rule; the auditor applied it literally and failed two correct policies.

## Assumptions and open questions

=== REGISTER REQUESTS ===
None.
=== END REGISTER REQUESTS ===
