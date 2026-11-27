# schemas

JSON Schema (draft 2020-12) for the files agents write into a product folder. Code, so GPL-3.0 like `scripts/`.

| Schema | Status | File | What |
|--------|--------|------|------|
| [register.schema.json](register.schema.json) | draft | `<product>/.po/register.jsonl` | The shared register: open questions, assumptions, decisions, and feedback and attribution entries. |
| [trace.schema.json](trace.schema.json) | draft | `<product>/.po/trace.jsonl` | Where each output item came from: write, review and remove lines. |
| [feedback.schema.json](feedback.schema.json) | draft | `<product>/.po/feedback.jsonl` | User feedback on an output: severity P0 to P3, nine categories. |
| [attribution.schema.json](attribution.schema.json) | draft | `<product>/.po/attributions.jsonl` | The tracer's finding: origin, carriers, cause, confidence, alternatives. |
| [rerun.schema.json](rerun.schema.json) | draft | `<product>/.po/reruns.jsonl` | One `/po-rerun-from`: plan, OK, rebuild, commit. |
| [ledger.schema.json](ledger.schema.json) | draft | `<products repo>/.po/ledger.jsonl` | Every accepted and rejected learned edit from `/po-retro`. |
| [scorecard.schema.json](scorecard.schema.json) | draft | `<products repo>/.po/scorecard.json` | Per-skill scores and per-run measures. |

All `.jsonl` files are JSON Lines, UTF-8 and append-only: never edit or delete a line. The register follows [ai-sdlc-loop](https://github.com/mitulamin/ai-sdlc-loop)'s surface register: declare and update lines, ids `r-<UTC timestamp>-<4 hex>`, current status is the latest update for an id. Feedback, attribution, rerun and ledger files keep the latest line for an id as its current state; a change is a full new line with the same id.

## IDs

| ID | Format | Example | Numbered |
|----|--------|---------|----------|
| Output item | `<3-letter type prefix>-<3+ digits>` | `ACT-007` | per product and prefix; prefixes in `x-item-types` in the trace schema |
| Run | `run-<yyyymmddhhmmss>-<4 hex>` | `run-20261202090000-b2b2` | `scripts/traces.py new-run` |
| Register entry | `r-<yyyymmddhhmmss>-<4 hex>` | `r-20261202091000-0002` | as in ai-sdlc-loop |
| Feedback, attribution, rerun | `FB-`, `AT-`, `RR-` + 3+ digits | `FB-001` | per product |
| Ledger entry | `LE-` + 3+ digits | `LE-001` | per products repo |
| Retro | `retro-<yyyymmdd>-<nn>` | `retro-20261211-01` | per products repo |

Item IDs never change and are never reused. A rewrite keeps the ID and adds a write line with the next `rev`.

## Checks

- `python3 scripts/check-schemas.py`: every schema is valid JSON with `$schema`, `$id`, `title` and `x-status`.
- `python3 scripts/traces.py check --product <slug>` (or `--all`): every line against its schema, plus what a schema cannot say: IDs match their type, revs in order, upstream items and register entries exist, no cycles, every item's ID is in its file, every ID in the product's Markdown has a trace, evidence tags are backed, attributions match the trace, reruns had the user's OK, and an accepted ledger edit passed review and held-out tests.
- `python3 scripts/scorecard.py check`: run totals add up, and the verdict each skill's runs point to.
- `tests/fixtures/products-repo/` is a small fictional products repo with every file in use.
