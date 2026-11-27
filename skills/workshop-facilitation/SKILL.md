---
name: workshop-facilitation
description: "Use during the Workshops stage where AI prepares the structured workshop agenda, prompts, and capture templates, a human facilitates the live session, and AI synthesises the raw notes into tagged findings and register updates."
licence: CC-BY-SA-4.0
---

# Workshop Agenda and Write-Up

Strict human/AI division of labour: AI prepares the agenda and capture materials; a person runs the live workshop; AI writes up and reconciles the outcomes.

## When to use

During the `workshops` stage (or whenever stakeholder/user workshops are needed to settle high-risk assumptions from `idea`..`scope`).

## Producer: dos and don'ts

Do:
- Split the work into two clear phases in `06-workshops.md` (`WKS-NNN`):
  - **Part A — Pre-Workshop Plan (AI prepares for the human facilitator)**: goal, target participants (`ACT-NNN`), specific register assumptions/questions to resolve (`r-...`), timeboxed agenda, non-leading facilitation prompts (Mom Test / EventStorming / Story Mapping exercises), pre-read summary, and blank capture sheet
  - **Part B — Post-Workshop Write-Up (AI synthesises after the human runs it)**: attendance & date, raw observation/decision log, verbatim quotes tagged `[Stated]`/`[Validated]`, refuted/confirmed assumptions, new questions/decisions for `.po/register.jsonl`, and concrete changes required in upstream artefacts
- Explicitly mark **who runs the session**: a human facilitator runs the live workshop; AI never pretends a live workshop happened when no real notes were supplied
- If no live workshop has occurred yet, produce Part A as ready-to-run, mark Part B `PENDING HUMAN FACILITATION`, and emit a `[QUESTION: ...]` asking whether the user wants to run the workshop now, supply raw notes, or explicitly waive/park the workshop with a decision

Don't:
- Fabricate workshop transcripts, fake participant quotes, or mark assumptions `[Validated]` from a simulated workshop
- Overload a workshop agenda with items already settled or better answered asynchronously
- Leave post-workshop write-ups as unstructured prose without updating register statuses and naming impacted item IDs

## Steps

1. Pull unresolved high-impact assumptions and stakeholder conflicts from `.po/register.jsonl` and upstream artefacts.
2. Draft Part A: focused timeboxed agenda, participant list, facilitation prompts, and decision capture sheet.
3. Hand Part A to the user via `po` so a human can run the workshop (or provide notes/waiver).
4. Once real workshop notes are provided, synthesise Part B with `[Stated]`/`[Validated]` tags, lock-sheet proposals, and register updates.

## Self-check

- [ ] Does Part A tie every agenda block to specific open register items (`r-...`) or high-risk assumptions?
- [ ] Is the human facilitator role explicit, with zero fabricated or simulated workshop outcomes presented as real?
- [ ] In Part B (when notes exist), are quotes/outcomes tagged `[Stated]`/`[Validated]` and mapped to register updates and upstream artefact changes?

## Adversarial reviewer

- Fail (`P0`) if Part B presents simulated or fabricated workshop results as `[Stated]` or `[Validated]`.
- Fail (`P1`) if Part A agenda lacks timeboxes, participant roles (`ACT-NNN`), or links to the specific open assumptions it is meant to settle.
- Fail (`P1`) if Part B omits register updates for assumptions that were confirmed, refuted, or newly raised.
