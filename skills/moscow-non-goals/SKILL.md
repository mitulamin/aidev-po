---
name: moscow-non-goals
description: "Use during the Scope stage and stage gates to classify deliverables with MoSCoW (Must/Should/Could/Won't) and define explicit Non-Goals with concrete revisit triggers."
licence: CC-BY-SA-4.0
---

# MoSCoW Prioritisation and Explicit Non-Goals

Prevent scope bloat and silent re-expansion by forcing explicit Must/Should/Could/Won't boundaries and named Non-Goals with revisit triggers.

## When to use

During the `scope` stage (and reflected in `fsd` and `presentations`), plus whenever items are parked at any stage gate.

## Producer: dos and don'ts

Do:
- Record the user-set **Appetite** (how much time, effort, or budget we are willing to spend on Release 1) and a crisp **Scope Statement (In / Out / Later)** (`SCP-001`)
- Classify every scoped item (`SCP-NNN`) using MoSCoW:
  - **Must**: non-negotiable for Slice 1 viability; if any Must fails, the release is not viable
  - **Should**: important but workaround exists for Slice 1
  - **Could**: desirable low-cost enhancement if capacity remains
  - **Won't (this release)**: explicitly excluded now
- Check the **Must budget**: Must items should normally stay <=60% of expected Slice 1 effort/complexity; if everything is Must, nothing is prioritised
- Write an **Explicit Non-Goals** table (`PARK-NNN` / `NG-NNN`) as a first-class section for every Won't or deliberately rejected capability: what is excluded, why, who might miss it, and the concrete **revisit trigger** (specific metric, user signal, or regulatory event that would reopen it)

Don't:
- Label >75% of features as "Must"
- Write vague Won't/Non-Goals without a reason and revisit trigger (never "maybe Phase 2")
- Silently re-include a Won't or Non-Goal item in `workshops`, `presentations`, or `fsd` without raising a `[QUESTION: ...]`

## Steps

1. Assign Must / Should / Could / Won't to every item in the Story Map.
2. Audit the Must list: challenge each Must with "If we launch without this and use a manual workaround, does the core JTBD still work?"
3. Move Won't and rejected ideas into the Explicit Non-Goals table with rationale and revisit triggers.
4. Surface borderline Must vs Should calls to the user at the Scope gate.

## Self-check

- [ ] Is every Must item genuinely essential for Slice 1 viability, with Should/Could/Won't meaningfully populated?
- [ ] Does every Won't / Non-Goal entry include a clear rationale and a concrete revisit trigger?
- [ ] Are contentious Must-vs-Won't trade-offs surfaced as `[QUESTION: ...]` entries with recommendations?

## Adversarial reviewer

- Fail if almost everything is marked "Must" (no real prioritisation or non-goals).
- Fail if any Won't / Non-Goal or parked item lacks a concrete revisit trigger.
- Flag any contradiction between the Story Map Slice 1 and the Must list.
