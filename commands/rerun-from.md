---
name: rerun-from
description: "Rebuild a product's output from the step where an error began (a traced attribution), instead of patching it by hand: shows what downstream is invalidated, waits for the user's OK, reruns producers and reviewers, reopens the affected gates, and commits to the products repo only with the user's OK."
---

# /po-rerun-from

Fix the product now: rebuild from the traced step with the correction, so everything downstream is rebuilt rather than patched by hand.

The argument is an attribution (`AT-004`), a feedback ID (its current attribution), or an item ID with the correction in words (`/po-rerun-from ACT-003 admins archive, never delete`).

Record each status change as a full new line in `<product>/.po/reruns.jsonl` with `python3 scripts/traces.py add rerun --product <slug>`. Format: `schemas/rerun.schema.json`.

## Steps

1. **Find the starting step.** From the attribution, take its `origin`. If the user has not confirmed it and its confidence is under 0.8, say so and ask: confirm it, pick an alternative, or stop. For a `missing` item with no origin item, the start is the origin step's stage.
2. **Check the products repo is clean.** `python3 scripts/products-dir.py`. If `uncommitted_changes` is true, show the changes and ask the user to commit, stash or keep them. Never discard anything.
3. **Write the correction down first.** Add a register `decision` line (or an answer update, if it corrects an answer) in the user's words, so the producer gets it as an input. If it replaces earlier register entries, note them as `supersedes`.
4. **Work out what is invalidated.** `python3 scripts/traces.py downstream <origin item> --register-ref <superseded register IDs> --product <slug>`. That is the origin item, every item whose upstream reaches it, and every item that relied on a superseded entry, with the stages that hold them.
5. **Show the plan** in the format of `templates/learning/rerun-plan.md`, and record it with status `planned`:
   - the step to start from and the correction;
   - every invalidated item, by stage and file, with its summary;
   - the stage gates that will be reopened (each needs the user's approval again);
   - anything committed or handed off that will change (for example a gate PR to ai-sdlc-loop);
   - a narrower option, when there is one: rebuild only the items whose content depends on the error, and keep the rest (`kept`), each with a reason.
6. **Ask for the OK.** Nothing is rebuilt until the user says yes. Record `approved` with `user_ok`, or `declined` and stop.
7. **Rebuild, stage by stage, in stage order.** Make a run ID (`python3 scripts/traces.py new-run`). For each reopened stage, start the stage's producer in a fresh context with a brief: the run ID, the rerun ID, the correction's register ID, the items to rebuild (keep their IDs; remove or add only where needed, with reasons), the items to keep unchanged, and skill `trace-records`. Every write line carries `rerun`. Then the stage's reviewer, as on any run, and its review lines. Three FAILs in a row stops the rerun: record `abandoned` with the findings and leave the files for the user.
8. **Check.** `python3 scripts/traces.py check --product <slug>` must pass, and the feedback item must now read right. Show the user the diff of the product files (`git diff` in the products repo).
9. **Gates.** Take each reopened stage through its gate with the user as usual. Then record `done` with `rebuilt`, `removed` and `added`.
10. **Commit, only with OK.** Ask whether to commit. If yes, one commit in the products repo, for example `clinic-booking: rerun RR-002 from actors (FB-007): admins archive, never delete`, and record `committed` with the commit. If no, leave the working tree as it is. Never push unless asked.

A rerun fixes this product. Whether aidev-po should change so it does not happen again is for `/po-retro`.
