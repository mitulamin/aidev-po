# Retro brief <retro-id>

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
| <slug> | <AT-ID> | <FB-ID> <severity> <category> | <cause> | <agent, step> | <0.7> | <confirmed> | <path> |

## Also read

- Ledger: `<products repo>/.po/ledger.jsonl` (earlier edits, including rejected ones)
- Repeat causes: `causes` in `<products repo>/.po/scorecard.json`
- aidev-po sources you may propose to change: `agents/`, `skills/`, `commands/`, `templates/`, `scripts/`
- Client preferences: `<products repo>/.po/preferences.md`

## Write

- `<products repo>/.po/retro/<retro-id>/proposals.md` and `P-<n>.diff` per proposal
- `<products repo>/.po/retro/<retro-id>/report.md`

Held-in runs go in a scratch copy, never in the products repo or the live aidev-po checkout.
