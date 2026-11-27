---
name: outliner-qa
description: "Use when conducting user stage-gate interviews, resolving open questions, locking decisions, or parking deferred items with revisit triggers."
licence: CC-BY-SA-4.0
---

# Outliner Q&A

Structured decision-tree questioning for stage gates: small layered batches, recommended answers first, explicit Park options with revisit triggers, and a locked decision sheet.

## When to use

Whenever `po` consults the user at a stage gate, at product intake, or when resolving open register questions and assumptions.

## Producer: dos and don'ts

Do:
- Ground every round first: read the current stage artefact, upstream locked decisions, and `.po/register.jsonl` so you never ask a question that existing evidence already answers
- Build a decision tree for the current stage gate ordered by coupling: settle upstream/structural choices before downstream details they unlock
- Ask at most 5 questions per round, grouped by layer
- Use one consistent format per question:
  1. Question and what depends on it
  2. Options with the **recommended option first** and the concrete reason
  3. What changes if a non-recommended option is picked
  4. Explicit **Park** option (when deferrable), stating what can wait and a proposed **revisit trigger**
- Record every user answer in `.po/register.jsonl` (`answered` / `decided`) and in the stage's Lock Sheet (`DEC-NNN`: choice, who decided, why, register ID)
- Record every parked item (`PARK-NNN`: item, why it can wait, concrete revisit trigger event)
- Write testable criteria and stage behaviours as numbered `Given/When/Then` statements where applicable
- Treat locked decisions as binding in all later stages; if new evidence contradicts a locked decision, raise a `[QUESTION: ...]` with that evidence rather than overriding silently

Don't:
- Dump more than 5 questions in one turn or mix coupled layers randomly
- Ask open-ended questions without a recommended answer and trade-offs
- Park an item without a concrete revisit trigger (never write "revisit later")
- Silently override or narrow a locked decision in a later stage
- Leave a choice open at a gate when it blocks correctness, authorisation, scope boundaries, or source of truth

## Steps

1. Pull open `question` and high-impact/high-urgency `assumption` entries from `.po/register.jsonl`.
2. Dismiss any item already answered by evidence; group remaining items into coupled layers.
3. Present Layer 1 (at most 5 questions) with options, recommended answer first, trade-offs, and a Park option.
4. Log each answer or Park into `.po/register.jsonl` and the stage Lock Sheet; ask Layer 2 only if unlocked branches remain.
5. Confirm all gate-blocking choices are either locked (`DEC-NNN`) or parked with a revisit trigger (`PARK-NNN`).

## Self-check

- [ ] Was each round capped at 5 questions, ordered by coupling (upstream before downstream)?
- [ ] Did every question lead with a recommended option + reason, show what changes for alternatives, and include a Park option where deferrable?
- [ ] Does every Lock Sheet entry record choice, who decided, why, and register ID (`r-...`)?
- [ ] Does every parked item state why it can wait and a concrete revisit trigger?

## Adversarial reviewer

- Flag any question round exceeding 5 questions or missing a recommended answer and trade-offs.
- Flag any Lock Sheet entry missing who decided, why, or a valid register ID in `.po/register.jsonl`.
- Flag any parked item missing a concrete revisit trigger event.
- Flag any downstream artefact that silently changes or drops a locked decision without raising a `[QUESTION: ...]`.
