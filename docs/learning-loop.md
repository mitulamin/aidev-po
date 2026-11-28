---
title: Learning loop
---

# Learning loop

You can give feedback on any output, and the system traces it back to where it went wrong, so the next run is better. This reuses the Learn phase of [ai-sdlc-loop](https://github.com/mitulamin/ai-sdlc-loop) (its `/retro` flow, `learn-producer`, `learn-reviewer`, the register, the scorecard) and adds what it lacks: an explicit trail from every output item to the agent step, skill version, evidence and user answers it came from.

> The JSON Schemas for trace, feedback, attribution, rerun, ledger and scorecard are drafts in [schemas/](https://github.com/mitulamin/aidev-po/tree/main/schemas), next to the register schema. They are the source of truth for field names; this page is the overview.

## Where the files live

Per product, in `<products repo>/<slug>/.po/`:

| File | Holds |
|------|-------|
| `traces.jsonl` | Item writes, reviews and removals |
| `feedback.jsonl` | Feedback |
| `attributions.jsonl` | The tracer's findings |
| `reruns.jsonl` | Reruns |
| `register.jsonl` | The register, which also carries feedback and attribution lines |
| `tracer/` | Tracer reports |

At the root of the products repo, in `<products repo>/.po/`:

| File | Holds |
|------|-------|
| `ledger.jsonl` | Every accepted and rejected learned edit |
| `scorecard.json` | Per-skill scores and per-run measures |
| `preferences.md` | This client's preference profile |
| `retro/` | One folder per `/po-retro`: brief, proposals, held-out results, review |

The ledger and scorecard live in the products repo, not in aidev-po, so client evidence stays private. All `.jsonl` files are append-only: a change is a new line.

## 1. Every output item has an ID and a trace

Every item an agent writes (an FSD requirement, an actor row, a slide, a workshop agenda item) gets a **stable ID** and a **trace record**. The ID is written at the start of the item (a list item, the first table column, or a heading) so a reader or a pull request comment can find it; it is not an HTML anchor. IDs never change and are never reused. The producer declares the trace line as it writes the item, because it knows what it used.

A trace record holds:

| Field | Holds |
|-------|-------|
| item ID and type | for example a requirement, an actor, a slide |
| run, stage, agent, step | the exact agent step that wrote it |
| skill and template versions | which versions were in force |
| upstream item IDs | what it was derived from; the agent states these as it writes |
| evidence | the tag (Stated, Inferred, Assumed, Simulated, Validated) and sources |
| register references | the user answers, decisions and assumptions it relied on |

An item needs **upstream IDs or register references**. An Idea item can rest on a user's answer alone; anything else with neither is a question for the register, not an item.

**Reviews** are separate lines in the same `traces.jsonl`, not a field on the item. After each reviewer finishes (stage reviewer, `challenger`, `evidence-auditor`), `po` writes one review line per file it reviewed, with the verdict and the findings that name items.

**The trace check.** `po` runs `scripts/traces.py check` before each gate, and any error blocks the gate: the work goes back to the producer. The check validates every line against its schema and also what a schema cannot say: IDs match their type, upstream items and register entries exist, there are no cycles, every ID in the product's Markdown has a trace, and evidence tags are backed. The `evidence-auditor` reads for unsupported claims; it is not what catches a missing trace.

The model follows W3C PROV (entity, activity, agent) and OpenTelemetry GenAI span fields, so it can be exported to a tracing tool later.

## 2. Feedback

Give feedback with `/po-feedback` in chat, or as a pull request review comment on the artefact Markdown. It can point at a run, an artefact, a section, an item, or a quoted sentence inside an item.

**Severity:**

| | Meaning |
|-|---------|
| P0 | Blocks use |
| P1 | Wrong |
| P2 | Weak |
| P3 | Polish |

**What's wrong** (nine ways):

1. Wrong or invented
2. Missing
3. Misunderstood intent
4. Wrong scope or priority
5. Unclear or untestable
6. Inconsistent
7. Wrong for the audience
8. Process (too many questions, a leading question, a skipped gate)
9. Not sure (the tracer asks one follow-up)

Feedback is recorded in `feedback.jsonl` and the register straight away. The `tracer` runs at once for P0 and P1, and for P2 and P3 after `po` asks whether you want it traced. Learning edits are batched and processed at `/po-retro`, never mid-run.

## 3. The tracer

The `tracer` agent walks from the item back to **where it first went wrong**.

1. Load the feedback, the item and its trace.
2. Walk upstream through the recorded upstream IDs and the answers and decisions relied on.
3. Find the first wrong node. The earliest node where the error is already present is the **origin**; later nodes only **passed it on**.
4. Name the cause, one of ten (below).
5. Report the likely origin, the cause, a **confidence**, and one or two alternatives, including which reviewer should have caught it. The result is an attribution line plus a report in `tracer/`.

The tracer does not replay anything. For P0 and P1, `po` offers to replay the suspected step with the correction in a scratch copy, which can raise the confidence.

**The ten causes:**

| Cause | Meaning |
|-------|---------|
| `question-not-asked` | Nothing in the register covers it and the stage never asked |
| `answer-misheard` | An answer it relied on says something different from what was written |
| `unsupported-inference` | It inferred or assumed beyond its inputs, or tagged an inference Stated |
| `skill-gap` | The skill told it to do this, or lacked a rule a careful agent needed |
| `reviewer-miss` | A reviewer had an applicable check and passed it |
| `template-gap` | The template had no place for it, or pushed the agent wrong |
| `ignored-decision` | A locked decision or answer in force at the time says otherwise |
| `input-changed` | It matched what you said then; you have since changed it. Not a learning |
| `client-preference` | Fine in general; this client wants it another way |
| `unknown` | The trace does not show it |

| Confidence | Basis |
|-----------|-------|
| High (0.8 or more) | One node where the error first appears, a source mismatch, replay confirms |
| Medium (0.5 to 0.8) | Clear chain, no replay or an inconclusive one |
| Low (under 0.5) | Several candidates; `po` asks you one question before proposing an edit |

Why record the trail up front: automatic failure attribution from raw logs is weak (in the Who&When benchmark the best method found the responsible agent about half the time and the exact step about a quarter). Recorded upstream IDs, honest confidence and your confirmation do the heavy lifting.

## 4. `/po-rerun-from`

Fix the output now. `/po-rerun-from` re-runs the pipeline from the traced step with the correction, so downstream items are rebuilt rather than patched by hand. `po` shows the plan first and needs your OK; each rerun is recorded in `reruns.jsonl`.

## 5. `/po-retro`

Fix the process for next time. At `/po-retro`:

1. `learn-producer` groups the attributed feedback by cause and asks blameless "why" questions that lead to conditions, not agents.
2. It proposes the **smallest edit to one surface**: a skill rule, a reviewer check or mechanical lint, a template, a question bank, an agent brief, or a client preference.
3. Each proposal is tested: replay the failing case as the baseline, then check **held-out tests** the proposer did not see. Keep the edit only if the target improves and held-out cases do not regress.
4. `learn-reviewer` checks the proposal adversarially.
5. **You approve**, in one batch. Nothing is applied without it.
6. Every accepted and rejected edit goes in the **ledger** (`ledger.jsonl` in the products repo). Approved edits apply at the start of the next run.

Each edit is scoped: global (every run), client (a preference profile in `preferences.md` in that client's own products repo, never pooled across clients), or product (a correction to this product's decisions, which is not a learning).

Accepted **global** edits change aidev-po itself. They go on a local `learn/<retro-id>` branch in the aidev-po checkout and are committed only with your OK, with no client words or product names in the commit. Retro files (brief, proposals, held-out results, review) are kept under `retro/<retro-id>/` in the products repo.

## 6. Scorecard

The scorecard reuses ai-sdlc-loop's per-skill scoring (triggered, followed, reviewer caught, outcome, cost, harm) and adds per-run measures:

| Measure | Direction |
|---------|-----------|
| Feedback items per 100 output items, by severity | Down |
| P0 and P1 feedback per run | Down |
| Items with a complete trace | 100% |
| Feedback a reviewer caught before you saw it | Up |
| Attributions you confirm | Up |
| **Repeat-cause rate** (`repeat_cause_rate`): attributions whose cause and origin agent were already seen in an earlier run | Down |
| **Recurrence after edit** (`recurrence_after_edit`): the same cause and origin agent coming back after an accepted, applied ledger edit | Zero |
| Questions per gate | Down, without more feedback |
| Held-out regressions (`held_out_regressions`, from the ledger): accepted edits with any held-out regression | Zero |

## What is reused and what is new

Reused from ai-sdlc-loop: the `/retro` flow (here `/po-retro`), `learn-producer` and `learn-reviewer`, the register format (one shared taxonomy, with decision, `feedback` and attribution entries as the optional aidev-po extension, DEC-002), the scorecard, held-out acceptance, human approval, the ledger, applying approved edits next run. New in aidev-po: item IDs and traces, `/po-feedback`, the `tracer`, `/po-rerun-from`, client preference profiles and held-out example products.
