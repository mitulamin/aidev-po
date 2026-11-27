---
name: learning-loop
description: "For po. Use on every run to keep the learning loop working: give each stage pass a run ID, have producers declare traces, record reviews in the trace, block a gate on trace errors, show open feedback at catch-up, and run /po-feedback, /po-rerun-from and /po-retro."
---

# Learning loop (for `po`)

What `po` does so that any feedback can be traced back to where it went wrong and turned into a small, tested, approved edit. The stage work itself is in `po`'s own file; this is only the learning-loop part.

## Files

| File | Holds | Schema |
|------|-------|--------|
| `<product>/.po/traces.jsonl` | Item writes, reviews and removals | trace (`schemas/trace.schema.json`) |
| `<product>/.po/feedback.jsonl` | Feedback | feedback (`schemas/feedback.schema.json`) |
| `<product>/.po/attributions.jsonl` | Tracer findings | attribution (`schemas/attribution.schema.json`) |
| `<product>/.po/reruns.jsonl` | Reruns | rerun (`schemas/rerun.schema.json`) |
| `<product>/.po/register.jsonl` | The register, with feedback and attribution lines | register (`schemas/register.schema.json`) |
| `<product>/.po/tracer/` | Tracer reports | |
| `<products repo>/.po/ledger.jsonl` | Every accepted and rejected learned edit | ledger (`schemas/ledger.schema.json`) |
| `<products repo>/.po/scorecard.json` | Per-skill scores and per-run measures | scorecard (`schemas/scorecard.schema.json`) |
| `<products repo>/.po/preferences.md` | This client's preference profile | |
| `<products repo>/.po/retro/<retro-id>/` | Retro brief, proposals, held-out results, review | |

The products repo is wherever `python3 scripts/products-dir.py` says, outside the aidev-po checkout. All the scripts below find it the same way, or take `--repo`.

## On every stage pass

1. **Run ID.** At the start of each stage pass, and of each rerun, make one: `python3 scripts/traces.py new-run`. Put it, the product slug, and "load skill trace-records" in every producer brief.
2. **Reviews.** After each reviewer (stage reviewer, challenger, evidence-auditor) finishes, append one review line per file it reviewed: the item IDs in the file, the verdict, the findings file, and each finding that names an item with its severity. Reviewers do not write the trace themselves.
3. **Before the gate.** Run `python3 scripts/traces.py check --product <slug>`. Any error blocks the gate: send it back to the producer. Show warnings at the gate.
4. **Corrections in chat.** When the user says an output is wrong, offer to record it as feedback (skill feedback-intake). Capture now; never edit a skill, agent or template mid-run (9.11).

## On catch-up

Besides the register, tell the user:

- feedback that is open (not traced yet) or traced but not fixed, by severity;
- attributions waiting for the user's confirm or reject;
- reruns that are planned or approved but not done;
- how many confirmed attributions are not yet in the ledger, and how much feedback is still untraced (`python3 scripts/traces.py open-feedback --all`). At five or more of either, or at the end of the FSD stage, offer `/po-retro`, which traces open feedback first, with the user's OK.

## Commands

- `/po-feedback` (`commands/feedback.md`): record feedback and trace it.
- `/po-rerun-from` (`commands/rerun-from.md`): rebuild from the step where the error began.
- `/po-retro` (`commands/retro.md`): turn traced feedback into small, tested, approved edits.

## Rules

- Commit to the products repo only with the user's OK each time; never push unless asked.
- Change aidev-po itself only for an accepted global edit, on a new branch, with the user's OK to commit. Never put client words or product names in an aidev-po commit.
- Client preferences stay in that client's products repo, never pooled across clients.
- Never contact anyone but the user. Never reply on a pull request unless the user asks.

## Self-check

- [ ] Did every producer brief carry a run ID and the trace-records skill?
- [ ] Is there a review line for every reviewed file?
- [ ] Did `traces.py check` pass before each gate?
- [ ] Was every correction the user made in chat offered as feedback, and no skill edited mid-run?
