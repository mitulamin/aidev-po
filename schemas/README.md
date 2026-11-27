# schemas

JSON Schema (draft 2020-12) for the files agents write into a product folder. Code, so GPL-3.0 like `scripts/`.

| Schema | Status | What |
|--------|--------|------|
| [register.schema.json](register.schema.json) | draft | The shared register: open questions, assumptions and decisions. One JSON object per line, append-only. |
| [trace.schema.json](trace.schema.json) | stub | Where an output item came from. |
| [feedback.schema.json](feedback.schema.json) | stub | User feedback on an output item. |
| [scorecard.schema.json](scorecard.schema.json) | stub | Per-skill scores across runs. |

The register follows [ai-sdlc-loop](https://github.com/mitulamin/ai-sdlc-loop)'s surface register: declare and update lines, ids `r-<UTC timestamp>-<4 hex>`, current status is the latest update for an id. Differences: the types are assumption, question and decision, and there is no separate blocker type.

Stubs are marked `"x-status": "stub"`. Their full shape, and the tracer that uses them, arrive with the learning loop in a later PR.

`python3 scripts/check-schemas.py` checks that every schema is valid JSON with `$schema`, `$id`, `title` and `x-status`.
