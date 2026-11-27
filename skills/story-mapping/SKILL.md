---
name: story-mapping
description: "Use during the Scope stage to organise deliverables along a horizontal user journey backbone and slice thin vertical releases (walking skeleton / MVP and follow-on releases)."
licence: CC-BY-SA-4.0
---

# User Story Mapping

Organise scope around the end-to-end user journey rather than flat feature backlogs, and cut thin vertical release slices.

## When to use

During the `scope` stage after Impact Mapping, and before MoSCoW / FSD handoff.

## Producer: dos and don'ts

Do:
- Build the horizontal **Backbone** in narrative time order: **Activities** (high-level user goals) -> **Tasks** (concrete steps across `ACT-NNN` and `SYS-NNN` events)
- Slice vertically into horizontal **Release Bands**:
  - **Slice 1 (Walking Skeleton / MVP)**: minimum end-to-end flow that proves the core JTBD and Desired Outcome
  - **Slice 2 (Release 2)**: high-value depth, automation, edge cases
  - **Later / Future**: parked with triggers
- Ensure Slice 1 traverses the whole end-to-end journey (even with manual/simple steps) rather than polishing one early step
- Give every card a stable ID (`SCP-NNN`), upstream link (`ACT-NNN` / `SYS-NNN`), and evidence tag

Don't:
- Produce a flat ungrouped list of features or technical layers ("backend stories", "frontend stories")
- Leave Slice 1 incomplete end-to-end (a dead-end journey that cannot deliver the core outcome)
- Pack nice-to-have edge cases or admin polish into Slice 1 without justification

## Steps

1. Lay out User Activities left-to-right across the primary journey.
2. Break each Activity into concrete User Tasks aligned with EventStorming commands/events.
3. Place deliverable slices underneath each Task and draw the MVP / Slice 1 cut line.
4. Walk the Slice 1 walking skeleton end-to-end to verify there are no missing links or dead ends.

## Self-check

- [ ] Does the backbone follow chronological user/actor flow from trigger to outcome?
- [ ] Can a user complete the core JTBD end-to-end using only Slice 1?
- [ ] Is every story card linked to an upstream Impact/Actor and tagged with evidence?

## Adversarial reviewer

- Fail if Slice 1 has a broken end-to-end journey (e.g. creates records with no way to act on or complete the outcome).
- Flag horizontal technical tasks ("build database", "setup auth UI") masquerading as user journey steps.
- Flag scope creep where secondary optimisation cards sit above the MVP cut line without Goal justification.
