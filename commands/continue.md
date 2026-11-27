---
name: continue
description: "Catch up on an existing product (stage, register, decisions, open questions, last run summary) and resume work on its current stage."
---

Run `po`'s catch-up workflow:

1. Run `python3 scripts/products-dir.py --json` to locate the products repo (handle missing setup if needed).
2. Identify the product from the command argument, or list products and ask the user which one to continue.
3. Read `<product>/.po/state.json`, `<product>/.po/register.jsonl` (`python3 scripts/register.py list --open --register ...`), recent `decided`/`answered` register entries, and the latest gate report in `<product>/.po/runs/`.
4. Report where things stand (current stage, locked decisions, open questions/assumptions, last run summary), then continue the current stage producer/reviewer loop or stage gate.
