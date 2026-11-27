---
title: Learning loop
---

# Learning loop

You can give feedback on any output, and the system traces it back to where it went wrong, so the next run is better. This reuses the Learn phase of [ai-sdlc-loop](https://github.com/mitulamin/ai-sdlc-loop) (`/retro`, `learn-producer`, `learn-reviewer`, the register, the scorecard) and adds what it lacks: an explicit trail from every output item to the agent step, skill version, evidence and user answers it came from.

> The JSON Schemas for trace, feedback and scorecard are stubs in [schemas/](https://github.com/mitulamin/aidev-po/tree/main/schemas) until the learning loop lands. Field names below are the design, and the schemas are the source of truth once they are filled in.

## 1. Every output item has an ID and a trace

Every item an agent writes (an FSD requirement, an actor row, a slide, a workshop agenda item) gets a **stable ID** and a **trace record**, with an anchor in the Markdown so feedback can point at it. Trace records live with the product in `.po/`.

A trace record holds:

| Field | Holds |
|-------|-------|
| item ID and type | for example a requirement, an actor, a slide |
| run, stage, agent, step | the exact agent step that wrote it |
| skill and template versions | which versions were in force |
| upstream item IDs | what it was derived from; the agent states these as it writes |
| evidence | the tag (Stated, Inferred, Assumed, Simulated, Validated) and sources |
| user answers and decisions | what the item relied on |
| review | which reviewer looked at it and what they said |

The model follows W3C PROV (entity, activity, agent) and OpenTelemetry GenAI span fields, so it can be exported to a tracing tool later. The `evidence-auditor` fails any item with no trace or no upstream IDs.

## 2. Feedback

Give feedback with `/feedback` in chat, or as a pull request review comment on the artefact Markdown. It can point at a run, an artefact, a section, an item, or a quoted sentence inside an item.

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

Feedback is recorded in the register straight away and processed in a batch at `/retro`.

## 3. The tracer

The `tracer` agent walks from the item back to **where it first went wrong**.

1. Load the feedback, the item and its trace.
2. Walk upstream through the recorded upstream IDs and the answers and decisions relied on.
3. Find the first wrong node. The earliest node where the error is already present is the **origin**; later nodes only **passed it on**.
4. Name the cause: a question never asked, an answer misheard, an unsupported inference, a skill gap, a reviewer miss, a template gap, an ignored locked decision.
5. Where it is cheap, check by replaying the suspected step with the correction.
6. Report the likely origin, the cause, a **confidence**, and one or two alternatives, including which reviewer should have caught it.

| Confidence | Basis |
|-----------|-------|
| High (0.8 or more) | One node where the error first appears, a source mismatch, replay confirms |
| Medium (0.5 to 0.8) | Clear chain, no replay or an inconclusive one |
| Low (under 0.5) | Several candidates; `po` asks you one question before proposing an edit |

Why record the trail up front: automatic failure attribution from raw logs is weak (in the Who&When benchmark the best method found the responsible agent about half the time and the exact step about a quarter). Recorded upstream IDs, honest confidence and your confirmation do the heavy lifting.

## 4. `/rerun-from`

Fix the output now. `/rerun-from` re-runs the pipeline from the traced step with the correction, so downstream items are rebuilt rather than patched by hand.

## 5. `/retro`

Fix the process for next time. At `/retro`:

1. `learn-producer` groups the attributed feedback by cause and asks blameless "why" questions that lead to conditions, not agents.
2. It proposes the **smallest edit to one surface**: a skill rule, a reviewer check or mechanical lint, a template, a question bank, an agent brief, or a client preference.
3. Each proposal is tested: replay the failing case as the baseline, then check **held-out tests** the proposer did not see. Keep the edit only if the target improves and held-out cases do not regress.
4. `learn-reviewer` checks the proposal adversarially.
5. **You approve**, in one batch. Nothing is applied without it.
6. Every accepted and rejected edit goes in the **ledger**. Approved edits apply at the start of the next run.

Each edit is scoped: global (every run), client (a preference profile kept in that client's own products repo, never pooled across clients), or product (a correction to this product's decisions, which is not a learning).

## 6. Scorecard

The scorecard reuses ai-sdlc-loop's per-skill scoring (triggered, followed, reviewer caught, outcome, cost, harm) and adds per-run measures:

| Measure | Direction |
|---------|-----------|
| Feedback items per 100 output items, by severity | Down |
| P0 and P1 feedback per run | Down |
| Items with a complete trace | 100% |
| Feedback a reviewer caught before you saw it | Up |
| Attributions you confirm | Up |
| **Repeat-cause rate**: the same cause recurring after its edit | Zero |
| Questions per gate | Down, without more feedback |
| Held-out set score | No regression |

## What is reused and what is new

Reused from ai-sdlc-loop: `/retro`, `learn-producer` and `learn-reviewer`, the register format (with `feedback` and attribution entries added), the scorecard, held-out acceptance, human approval, the ledger, applying approved edits next run. New in aidev-po: item IDs and traces, `/feedback`, the `tracer`, `/rerun-from`, client preference profiles and held-out example products.
