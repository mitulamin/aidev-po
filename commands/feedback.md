---
name: feedback
description: "Give feedback on any product output (an item, a quoted sentence, a section, a file or a run), or take in pull request comments from the products repo. Records severity P0-P3 and one of nine what's-wrong categories, then traces it to where it went wrong."
---

# /po-feedback

Record feedback on a product's output, then trace it back to the step where the error began.

Examples:

- `/po-feedback REQ-012 P1 the admin never deletes, only archives`
- `/po-feedback the second slide is too technical for the board`
- `/po-feedback --pr https://github.com/acme/acme-products/pull/7`

## Steps

1. **Product.** Use the product the user is working on; if unclear, ask which one (list them with `python3 scripts/products-dir.py`).
2. **Take it in** with skill `feedback-intake` (`skills/feedback-intake/SKILL.md`): find the target items and their revs, confirm severity and category with the user, keep their words, write the feedback line and its register line. With `--pr <url>`, take in the pull request's review comments as that skill says, in batches of at most five, and never post back to the pull request.
3. **Trace it.** For P0 and P1, trace straight away. For P2 and P3, ask: trace now (recommended when there are three or fewer) or leave it for `/po-retro`. To trace, start the `tracer` agent (`.cursor/agents/tracer.md`) in a fresh context, one per feedback line, with a brief that names: the product folder, the feedback ID, `scripts/traces.py`, and where to write (`<product>/.po/tracer/`). Ingest its register-request block verbatim (`python3 scripts/register.py ingest - --agent tracer --stage <stage> --via coordinator --register <register>`), then add the attribution's register line: `python3 scripts/register.py add --type attribution --record <AT-ID> --agent po --stage <origin stage> --item-id <origin item> --text "<cause, one line>" --register <register>`.
4. **Replay, if cheap.** For a P0 or P1 at medium confidence, offer to replay the origin step with the correction in a scratch copy of the product folder (a fresh producer for that stage, never in the products repo). If the item then comes out right, append a new line for the same attribution with `replay.result` `confirmed` and the confidence raised.
5. **Show the user** the tracer's finding in plain words: where it began, what only passed it on, the cause, the confidence, the alternatives, and which reviewer should have caught it. At low confidence, ask the tracer's one question first and trace again with the answer.
6. **Confirm.** Ask: confirm, reject, or not sure. Append a new line for the same attribution with `user_verdict` (and `user_note`), and a register update on its register line: status `answered`, answer `confirmed`, `rejected` or `unsure`, by `user`.
7. **Next.** Offer: fix the output now with `/po-rerun-from <AT-ID>` (recommended for P0 and P1, and whenever the cause is `input-changed`), or later. Learning from it happens at `/po-retro`.

Commit the new `.po/` lines to the products repo only with the user's OK.
