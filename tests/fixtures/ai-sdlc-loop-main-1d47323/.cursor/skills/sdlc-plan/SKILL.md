---
name: sdlc-plan
description: "Turn the brief into a spec and a plan with verifiable goals. Runs the Plan loop with fresh-context producers and adversarial reviewers."
disable-model-invocation: true
---
<!-- Installed from ai-sdlc-loop commands/plan.md at 1d473234a504 by scripts/new-project.sh, adapted for Cursor (front matter, links and command names). Licence: MIT, see the project's LICENSE. -->

Act as the coordinator for this command: read `.cursor/agents/coordinator.md` and follow it. Start each producer and reviewer it names as a subagent from the same folder.

# /sdlc-plan

Turn the brief into a spec and a plan with verifiable goals.

For the coordinator. The human gives this command to the [coordinator](../../agents/coordinator.md) only; the coordinator runs the loop on its own and reports at the end of the cycle.

Task: the text the human typed after the command, or the brief file it names

## Register

The shared surface register is where this run's agents write their assumptions, open questions and blockers, as register-request blocks. If the arguments above contain `--register <path>`, use that path and take the flag out of the task. Otherwise use the default, `.ai-sdlc/register.jsonl`. Put the path in every brief. Treat the register as your inbox and pull it proactively, and write the register-request block of any agent that cannot write to it out verbatim, as the [coordinator](../../agents/coordinator.md) file says; its format is in [agents/README.md#the-shared-surface-register](../../../.ai-sdlc/agents.md#the-shared-surface-register).

## Loop

Phases, in order: Plan.

For each phase that runs:

1. Pick, from the phase's skills below, only the ones that apply to the task (1.8, 8.1). Write the brief to a file: the task, the acceptance criteria, the files to read, the skill IDs that apply, the register path, and where to write the output and the review.
2. Start the phase's producer in a fresh context with the brief (8.7).
3. Start the phase's reviewer in a fresh context with the brief's task and acceptance criteria and the producer's output, not its transcript or reasoning.
4. On a reviewer FAIL, start a new producer with the brief and the findings file, then a new reviewer. After three FAILs in a row, stop the phase and record it as failed with its findings (5.5).
5. On PASS, record the output and the review file for the coordinator's end-of-cycle report, and pull the register for the new entries from this phase. Do not ask the human anything here.

## Phases and the skills they load

### Plan

Producer: [plan-producer](../../agents/plan-producer.md), which loads each skill's dos and don'ts together, its related practices and its Self-check. Reviewer: [plan-reviewer](../../agents/plan-reviewer.md), which loads only each skill's adversarial reviewer checks and don'ts.

Skill IDs: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8.

- [1.1 surface-assumptions](../surface-assumptions/SKILL.md): State assumptions; when something is unclear, stop and ask rather than pick silently
- [1.2 spec-before-code](../spec-before-code/SKILL.md): Write a spec before code for non-trivial work, and gate each phase on human review
- [1.3 capability-map-and-dependency-order](../capability-map-and-dependency-order/SKILL.md): Break big asks into a capability map and build modules in dependency order
- [1.4 interview-to-shared-understanding](../interview-to-shared-understanding/SKILL.md): Interview until there is shared understanding; ask each round of open decisions with a recommended answer
- [1.5 look-up-facts-ask-for-decisions](../look-up-facts-ask-for-decisions/SKILL.md): Look facts up yourself; only ask the human for decisions
- [1.6 plans-for-a-zero-context-engineer](../plans-for-a-zero-context-engineer/SKILL.md): Write plans for an engineer who has never seen the codebase: exact files, small tasks
- [1.7 verifiable-goals](../verifiable-goals/SKILL.md): Turn every task into a verifiable goal, with a check for each step
- [1.8 size-process-to-task](../size-process-to-task/SKILL.md): Size the process to the task; skip ceremony for trivial changes
