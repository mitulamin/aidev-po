---
title: Method
---

# Method

How aidev-po works, across all stages. The stage-by-stage detail is on [Stages](stages.md).

## The coordinator pattern

You talk to one agent, `po`. It does not do the stage work itself. For each stage it starts a **producer** with a fresh, blank context and exactly the brief that stage needs, then starts an adversarial **reviewer**, also fresh, that sees only the brief and the output and exists to find problems. `po` collects the result, updates the register, and takes it to you at the gate.

Fresh contexts matter. An agent that has not seen the whole conversation cannot be swayed by your enthusiasm or carry an earlier mistake forward. This is the same shape as [ai-sdlc-loop](https://github.com/mitulamin/ai-sdlc-loop); the difference is that here you are consulted at every gate.

| Agent | Role |
|-------|------|
| `po` | Coordinator. Finds the products repo, lists products, runs stages, owns the register, consults you at every gate. |
| `<stage>-producer` | Produces that stage's artefacts. |
| `<stage>-reviewer` | Adversarial review of the stage output. |
| `evidence-auditor` | Fails any item with no evidence tag or source. |
| `challenger` | Pushes back like a real product owner. |
| `tracer`, `learn-producer`, `learn-reviewer` | The [learning loop](learning-loop.md). |

## Stage gates

At each gate `po` shows what the stage produced, the reviewer's findings and the open register items, each open question with a recommended answer. You then approve, answer, send it back, or park items. `po` never moves on without you. The gate is also the one natural moment to commit to your products repo, once per gate and only with your OK.

## Evidence tags

Every item carries one tag. This is what stops fluent invention.

| Tag | Meaning |
|-----|---------|
| **Stated** | The user said it, or a source document says it. |
| **Inferred** | The agent reasoned it from stated things. Needs confirming. |
| **Assumed** | Nobody said it; we are proceeding as if true. Goes in the register as something to test. |
| **Simulated** | Produced by simulated users or personas. A hypothesis for finding gaps, never evidence. |
| **Validated** | Confirmed by a real person or real data, with the source recorded. |

The `evidence-auditor` fails any item with no tag or source. An item with no evidence is a question, not a fact.

## The challenger

A separate agent in a fresh context, judged on the issues it finds. It works through a fixed set of moves:

1. Ask for the last real instance ("when did this last happen, what did you do?"). Opinions and futures are not evidence.
2. Ask what happens if we do nothing, and what the current workaround costs.
3. Rank assumptions by importance and evidence. Important with little evidence goes to the top as a test, not a requirement.
4. Offer at least one cheaper or different route to the same outcome, with a recommendation.
5. Run a pre-mortem: it is a year later and this failed, why? Each cause becomes a risk or a non-goal.
6. If you overrule a challenge, record a decision with your rationale. Never silently change position.

## Outliner questions

When `po` needs answers it asks in layers:

- At most **five** questions per round, ranked by impact times uncertainty.
- Each has a **recommended answer** first, with the trade-offs, so you can say "yes, that" in a word.
- Each has a **Park** option with a concrete revisit trigger, which moves it into the register as an open question instead of blocking the stage.
- Questions follow the Mom Test rules: past behaviour and specifics, no pitching, no leading.

## The register

One shared, append-only register holds open questions, assumptions and decisions, one JSON line per event, in `<product>/.po/register.jsonl`. Its shape is in [schemas/](https://github.com/mitulamin/aidev-po/tree/main/schemas) and follows the surface register in ai-sdlc-loop. Before each gate `po` curates it: duplicates marked, answered items dismissed, the rest rated by impact and urgency. Locked decisions also go on each stage file's decision sheet. A stage reviewer that fails a stage three times in a row stops the loop and the question comes to you.

## Sizing

Not every product needs everything. A small internal tool gets a one-page PRD and a thin pass through the stages; a client platform gets the full FSD. `po` triages at the start and tells you what it chose, and you can change it.
