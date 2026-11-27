---
title: Stages
---

# Stages

Every product moves through the same stages, in order:

**Idea, Audience, Actors, Systems, Scope, Workshops, Presentations, FSD.**

Each stage has a producer and an adversarial reviewer in fresh contexts, ends at a gate where you decide, and writes into your product folder. The techniques below are the established methods each stage draws on; sources are on [Research](research.md). General rules (evidence tags, challenger, questions) are on [Method](method.md).

## 1. Idea

**Goal:** turn a rough idea into a problem, an outcome and a list of the riskiest assumptions. Most ideas arrive as a solution; the first job is the problem underneath.

- **Double Diamond** discipline: diverge then converge on the problem before any solution talk. No feature is recorded until the problem statement is locked.
- **Lean Canvas**: one page that makes you state problem, customer, alternatives, value proposition and key metric. Each box is tagged Stated, Inferred or Missing, and only Missing boxes get questions.
- **Opportunity Solution Tree**: one measurable outcome at the root, opportunities (needs) under it, solutions under those. Every later feature must hang off a branch.
- **Assumption mapping** (desirability, viability, feasibility): the top assumptions go in the register as things to test.

**Produces:** idea brief with a one-sentence problem, outcome and metric, Lean Canvas, tree root, top assumptions.
**Gate:** you lock the problem and outcome; riskiest assumptions are recorded.

## 2. Audience

**Goal:** name the first customer segment and the job they are trying to get done, with evidence rather than opinion.

- **Jobs to be Done**: job statements and job stories ("When ..., I want to ..., so I can ...") plus the current workaround.
- **The Mom Test**: interview guides use past behaviour and specifics; no "would you", no pitching. Every question bank is checked against these rules.
- **Value Proposition Canvas**: jobs, pains and gains matched to relievers and creators, which exposes features that fix no pain.
- Personas are built on validated jobs, never invented first.

**Produces:** audience pack with segments, first-customer choice, job statements, value proposition canvas, and interview guides for real people.
**Gate:** first customer chosen; each job tagged as hypothesis or validated.

## 3. Actors

**Goal:** list every human and system actor, and every stakeholder with power over or interest in the product.

- **Actor modelling** (primary, supporting, offstage): a fixed checklist of actor types finds the ones people forget: admins, support, auditors, payers, people affected but not using.
- **Power/interest map**: each stakeholder placed on the grid with an engagement plan (manage closely, keep satisfied, keep informed, monitor). This drives who is invited to workshops and who gets which presentation.
- Goals, frequency and permissions per actor.
- Optionally, simulated users to find gaps. Everything they produce is tagged Simulated and a person must confirm it.

**Produces:** actor catalogue, stakeholder map and engagement plan, personas grounded in jobs.
**Gate:** you confirm the list is complete; no actor without a goal.

## 4. Systems

**Goal:** draw the product's boundary and list every external system, data flow and owner.

- **C4 system context diagram**, written as diagram code (Mermaid) so it can be diffed and reviewed. The aidev-platform contract appears as a known external system for Shravi client work.
- **Integration register**: direction, data, protocol, owner, volume and failure behaviour for each interface. Unknown cells become questions, never guesses.
- **EventStorming** (big picture): a strawman event timeline from what is known; hotspots (disagreements, unknowns) become workshop agenda items.
- Glossary and bounded contexts, so the FSD and the code share one language.

**Produces:** context diagram, integration register, event timeline with hotspots, glossary.
**Gate:** every arrow on the diagram has an owner and a row in the integration register.

## 5. Scope

**Goal:** decide the first release and write down what is out, so scope stays tied to the outcome.

- **Impact mapping** (goal, actors, impacts, deliverables): every deliverable must trace to an actor behaviour change that moves the goal. Orphans are cut.
- **Story mapping**: a backbone of activities with stories beneath, sliced into a thin end-to-end first release.
- **MoSCoW** with an explicit Won't-this-time list. Musts are capped and any Must without a reason is challenged.
- **Non-goals** as a first-class section, each with a revisit trigger, plus an appetite (how much we are willing to spend) that you set.

**Produces:** scope statement (in, out, later), impact map, story map with the release 1 slice, MoSCoW list, non-goals, appetite.
**Gate:** release 1 and non-goals locked; every Must traces to a goal and an actor.

## 6. Workshops

**Goal:** plan the sessions that confirm, correct and enrich what the agents drafted, then turn the results back into the register.

**AI plans, a person runs.** The agents prepare the session and write up the result; a human facilitates. Decisions lock only after you confirm the write-up.

- Plans per session: objective, invitees (from the power/interest map), agenda and timings, pre-read, question bank, capture template.
- Formats picked to fit the goal: Design Sprint for a big risky question, EventStorming with a pre-filled strawman so the room corrects instead of starting blank, Liberating Structures for getting every voice heard, Example Mapping to turn stories into rules and examples, and a pre-mortem in the first stakeholder session.
- After the session: synthesis from your notes or transcript, covering decisions, conflicts, new questions and register updates.

**Produces:** workshop plans and post-session syntheses.
**Gate:** you confirm the synthesis before decisions lock.

## 7. Presentations

**Goal:** tell the story so a stakeholder can decide, tailored to where they sit on the stakeholder map.

- **PR/FAQ** (working backwards): a one-page future press release plus external and internal FAQs, drafted early and revised at each gate.
- A **narrative memo** for high-power stakeholders, then **decision-led decks**: one decision per deck, answer first, one deck per audience from the same source material.
- A **one-page PRD** as the cover of the FSD and the summary slide.
- Every claim cites a register or artefact ID.

**Produces:** PR/FAQ, memo, audience decks, one-page PRD.
**Gate:** the evidence auditor finds no claim without a source.

## 8. FSD

**Goal:** the full functional design specification, ready for ai-sdlc-loop.

The skeleton follows **ISO/IEC/IEEE 29148**, with a one-page PRD on top and testable requirement formats inside:

1. Summary: the one-page PRD (problem, outcome, metrics, non-goals)
2. Background and problem, with the PR/FAQ attached
3. Users, actors and stakeholders
4. System context and external interfaces
5. Scope, non-goals, assumptions, constraints, dependencies
6. Functional requirements by capability
7. Domain model and glossary
8. Quality requirements
9. Governance, compliance and data protection
10. Release slicing
11. Decisions log and open questions
12. Traceability matrix and verification approach

Inside it:

- **User stories checked against INVEST** (independent, negotiable, valuable, estimable, small, testable).
- **Given/When/Then** acceptance criteria that ai-sdlc-loop can turn into tests, seeded from the workshops' example mapping.
- **EARS** sentence patterns for system behaviour, to remove ambiguity.
- **ISO/IEC 25010** quality sweep: performance, reliability, security, usability, compatibility, maintainability, portability, safety, and the rest of the model.
- A requirements smell check (vague words, compound requirements, missing actor, untestable criteria) and a consistency check across the spec, glossary and diagrams.
- Every requirement traces to a goal, an actor and a source.

**Handoff:** by a gate PR. You review and approve the FSD there, and it becomes the brief for ai-sdlc-loop's planning.
**Gate:** you approve the gate PR.

## Sizing the FSD

The depth is sized by triage at the start: a one-page PRD plus the essentials for a small internal tool, the full outline for a client platform.
