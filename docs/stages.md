---
title: Stages
---

# Stages

Every product moves through the same stages, in order:

**Idea, Audience, Actors, Systems, Scope, Workshops, Presentations, FSD.**

Each stage has a producer (`<stage>-producer`) and an adversarial reviewer (`<stage>-reviewer`) in fresh contexts. Before the gate, `evidence-auditor` and `challenger` also run. At the gate you decide. Run or re-run a stage with `/po-idea`, `/po-audience`, `/po-actors`, `/po-systems`, `/po-scope`, `/po-workshops`, `/po-presentations` or `/po-fsd`, and run the gate with `/po-gate`. General rules (evidence tags, challenger, questions) are on [Method](method.md); sources for the techniques are on [Research](research.md).

## What every stage file has

Each stage writes one numbered file in your product folder (`01-idea.md` to `08-fsd.md`, plus `08-handoff-gate.md`), copied from a template in the repo's `templates/`. They share this shape:

- Items in tables with a **stable ID** (`IDEA-001`, `AUD-001`, `ACT-001`, `SYS-001`, `SCP-001`, `WKS-001`, `PRS-001`, `FSD-001`, and `US-`, `REQ-`, `NFR-`, `AC-` in the FSD), an **evidence tag** and source, and **upstream IDs** that say what each item was derived from. These feed the [learning loop](learning-loop.md).
- **Stage exit criteria** written as Given/When/Then.
- A **decision sheet** of locked decisions (`DEC-001` and so on): choice, who decided, why.
- **Parked items and non-goals** (`PARK-001`...), each with a concrete revisit trigger.
- An **Assumptions and open questions** block that goes into the register.

Where a stage reviewer finds problems, the producer revises in a fresh context, up to three attempts. After three failures `po` stops and asks you about the approach.

## 1. Idea

**File:** `01-idea.md`. **Goal:** turn a rough idea into a problem, an outcome and the riskiest assumptions. Most ideas arrive as a solution; the first job is the problem underneath.

- **Problem framing and status quo**: the core problem, and what happens if nothing is built (the current workaround and its cost).
- **Jobs to be Done and the Mom Test**: job statements ("When ..., I want to ..., so I can ...") with the last real instance or past workaround. Opinions and hypotheticals are not evidence.
- **Lean Canvas**: every box tagged, so gaps are visible.
- **Opportunity Solution Tree (seed)**: one desired outcome, opportunities under it, candidate solutions and an assumption test.
- **Riskiest assumptions**: the top three, in the register.

**Gate:** you lock the problem and outcome; the riskiest assumptions are recorded.

## 2. Audience

**File:** `02-audience.md`. **Goal:** name the first customer segment and the evidence behind it.

- **Target segments and early adopters**: frequency and trigger, current cost of the problem.
- **Mom Test evidence log**: a real past instance for each segment, the workaround and the switching friction, what they already tried or paid for.
- **Value Proposition Canvas**: per segment, the customer jobs, pains and gains, what relieves or creates them, and any feature that fixes no pain (cut or park it).
- **Expanded Opportunity Solution Tree.**
- **Discovery and validation plan**: each hypothesis, the research method (interview, observation, data) and what would pass or falsify it. Simulated-user gap checks may appear here, tagged Simulated.

**Gate:** first customer chosen; each claim tagged, with real-person evidence marked Validated.

## 3. Actors

**File:** `03-actors.md`. **Goal:** every human and system actor, and every stakeholder with power over or interest in the product.

- **Power/interest stakeholder map**: role type (buyer, decision maker, gatekeeper, user, operator), power, interest and the quadrant strategy (manage closely, keep satisfied, keep informed, monitor).
- **Actor and user profiles**: goals, context and frequency, accessibility and device constraints, trust level and permission boundary.
- **Roles, permissions and decision rights**: who can view, create or edit, approve, and what is forbidden.

**Gate:** you confirm the list is complete.

## 4. Systems

**File:** `04-systems.md`. **Goal:** the product's boundary, and everything it interacts with.

- **C4 level 1, system context** as a Mermaid `C4Context` diagram. For Shravi client work the aidev-platform contract is a known external system.
- **Integration register**: every arrow on the diagram has an owner and a row (direction, data, protocol, volume or SLA, failure behaviour). Unknown cells become open questions, never guesses.
- **C4 level 2, containers**, only where needed for scope or risk.
- **EventStorming flow**: commands, domain events, policies and external systems, step by step.
- **EventStorming hotspots**: unknowns, risks and conflicts, which become [workshop](#6-workshops) agenda items.
- **Glossary and bounded contexts**: one canonical definition per domain term, shared by the FSD and the code, with the synonyms to avoid.

**Gate:** every arrow has an owner and a row in the integration register, and the hotspots are listed.

## 5. Scope

**File:** `05-scope.md`. **Goal:** decide the first release and write down what is out, so scope stays tied to the outcome.

- **Appetite**: the ceiling you set for release 1 (budget, effort band or timebox), with a one-line scope summary of in, out and later.
- **Impact map**: goal, who, how their behaviour changes, what candidate deliverable. A deliverable with no path to the goal is cut.
- **User story map**: a backbone of activities and tasks with release slices, the first being a walking skeleton.
- **MoSCoW** for the first slice, with why each Must is essential and what the workaround is if dropped.
- **Explicit non-goals and parked scope**, each with who might want it and a revisit trigger.
- **Candidate acceptance criteria** in Given/When/Then.

**Gate:** release 1 and non-goals locked.

## 6. Workshops

**File:** `06-workshops.md`. **Goal:** settle the riskiest open assumptions and conflicts with real people.

**AI plans, a person runs.** The agents never pretend a workshop happened. If it has not been run, Part B stays pending and `po` asks whether you want to run it now, bring notes, or waive or park it.

- **Part A, before the workshop (AI prepares):** the objective and the register items to settle, participants and roles drawn from the actor map, a timeboxed agenda with non-leading prompts, and a capture sheet.
- **Part B, after the workshop (AI synthesises from your notes):** session details, findings tagged Stated or Validated, which register items were confirmed or refuted, new questions and decisions, and what must change in earlier artefacts.

**Gate:** you confirm the write-up before decisions lock.

## 7. Presentations

**File:** `07-presentations.md`. **Goal:** tell the story so a stakeholder can decide, tailored to where they sit on the stakeholder map.

**What you get:** text in one Markdown file, a structured deck outline (slide by slide: audience, key point, sources) plus the PR/FAQ and a narrative memo. It is not a designed deck: no slides, layouts or visuals are made. A person builds the deck from the outline in their own tool.

- **PR/FAQ** (working backwards): a one-page press release, a customer FAQ and a hard-questions internal FAQ, answering for the first slice only.
- **Narrative memo**: a short memo for high-power stakeholders (Manage Closely or Keep Satisfied on the actor map): the decision requested, the problem and cost of the status quo, the recommended slice 1 and appetite, and the non-goals and top risks. Every claim cites an ID.
- **Stakeholder presentation outline**: decision-led, with one decision per deck and the answer first, tailored per audience from the same material. Each slide names its target audience from the actor map and its key point.

**Gate:** the evidence auditor finds no claim without a source.

## 8. FSD

**Files:** `08-fsd.md` and `08-handoff-gate.md`. **Goal:** the full functional specification, ready for [ai-sdlc-loop](https://github.com/mitulamin/ai-sdlc-loop).

`08-fsd.md` follows **ISO/IEC/IEEE 29148**, with a one-page PRD on top:

0. One-page PRD (executive summary)
1. Purpose and scope
2. Product perspective
3. User characteristics and roles
4. Constraints, assumptions and dependencies
5. Specific functional requirements: user stories checked against **INVEST**, each with **Given/When/Then** acceptance criteria, **EARS** statements for system and edge-case behaviour, and data and information requirements (what each entity holds, its source and owner, who may read or change it, how long it is kept)
6. Non-functional requirements as an **ISO/IEC 25010** quality matrix (a target and verification method per characteristic, or `N/A` with a reason)
7. Verification and traceability matrix
8. Decision sheet
9. Parked items and non-goals
10. Definitions and glossary, taken from the Systems stage glossary

Every item carries its evidence tag and upstream IDs, so each requirement traces back to a goal, an actor and a source.

**Handoff:** `08-handoff-gate.md` is the brief for ai-sdlc-loop's `/plan`. It has a readiness checklist (reviewer, evidence auditor and challenger all clear, no high-urgency open questions), the goal and slice 1 scope, the locked decisions, the non-goals, an index of acceptance criteria, the `/plan` command with `--register` pointing at a copy of the product's register in the gate bundle (so locked decisions carry over), and the plan for the **gate PR**. No PR is opened and nothing is pushed in an engineering repo without your explicit OK.

**Gate:** you approve the FSD and the gate PR plan.

## Sizing

Depth is sized by triage at the start of a product: a thin pass plus the one-page PRD for a small internal tool, the full FSD for a client platform. `po` tells you what it chose and you can override it. The choice is kept as `depth` (`thin` or `full`) in the product's `.po/state.json`, and every producer and reviewer brief states it.
