# Retro brief retro-20261118-01

> Fictional demo for the aidev-po worked example.

## Task

Turn the attributions below into proposed learned edits: one surface per edit, smallest change that would have stopped the failure, each with a held-in baseline. Propose only.

## Acceptance criteria

- Every attribution below is covered by a proposal, or by a reason it needs none.
- Each proposal changes one surface and has a scope (global, client or product).
- Each conclusion names a condition to change, not an agent's mistake.
- Each held-in case was run red without the edit and green with it, with the excuses recorded.
- No proposal adds a rule to a producer's always-on context or to `AGENTS.md`.
- No global proposal carries a client's words, names or product details.

## Attributions

| Product | Attribution | Feedback | Cause | Origin agent, step | Confidence | User | Tracer report |
|---------|-------------|----------|-------|--------------------|------------|------|---------------|
| tool-library-loans | AT-001 | FB-001 P1 misunderstood-intent | `unsupported-inference` | systems-producer, 3-event-storming | 0.8 (replay confirmed) | confirmed | `tool-library-loans/.po/tracer/FB-001-AT-001.md` |

Not gathered: FB-002 (P3, open, not yet traced; the user chose to leave it for a later retro).

## Also read

- Ledger: `.po/ledger.jsonl` (empty before this retro)
- Repeat causes: `causes` in `.po/scorecard.json`: `unsupported-inference / systems-producer`, 1 time in 1 run, 0 after an edit
- aidev-po sources you may propose to change: `agents/`, `skills/`, `commands/`, `templates/`, `scripts/`
- Client preferences: `.po/preferences.md`

## Write

- `.po/retro/retro-20261118-01/proposals.md` and `P-<n>.diff` per proposal
- `.po/retro/retro-20261118-01/report.md`

Held-in runs go in a scratch copy, never in the products repo or the live aidev-po checkout.
