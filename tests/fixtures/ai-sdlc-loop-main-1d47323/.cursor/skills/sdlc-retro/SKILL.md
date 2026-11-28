---
name: sdlc-retro
description: "Turn the human's end-of-cycle feedback into proposed skill and check edits. Runs the Learn loop with fresh-context producers and adversarial reviewers."
disable-model-invocation: true
---
<!-- Installed from ai-sdlc-loop commands/retro.md at 1d473234a504 by scripts/new-project.sh, adapted for Cursor (front matter, links and command names). Licence: MIT, see the project's LICENSE. -->

Act as the coordinator for this command: read `.cursor/agents/coordinator.md` and follow it. Start each producer and reviewer it names as a subagent from the same folder.

# /sdlc-retro

Turn the human's end-of-cycle feedback into proposed skill and check edits.

For the coordinator. The human gives this command to the [coordinator](../../agents/coordinator.md) only; the coordinator runs the loop on its own and reports at the end of the cycle.

Task: the text the human typed after the command, or the brief file it names

## Register

The shared surface register is where this run's agents write their assumptions, open questions and blockers, as register-request blocks. If the arguments above contain `--register <path>`, use that path and take the flag out of the task. Otherwise use the default, `.ai-sdlc/register.jsonl`. Put the path in every brief. Treat the register as your inbox and pull it proactively, and write the register-request block of any agent that cannot write to it out verbatim, as the [coordinator](../../agents/coordinator.md) file says; its format is in [agents/README.md#the-shared-surface-register](../../../.ai-sdlc/agents.md#the-shared-surface-register).

## Loop

Phases, in order: Learn.

Run only after the human has given end-of-cycle feedback. The coordinator puts the proposed edits and their held-out results in its closing report for the human to approve (9.10). The Harness producer applies approved edits at the start of the next run, and every accepted or rejected edit is logged (9.12).

For each phase that runs:

1. Pick, from the phase's skills below, only the ones that apply to the task (1.8, 8.1). Write the brief to a file: the task, the acceptance criteria, the files to read, the skill IDs that apply, the register path, and where to write the output and the review.
2. Start the phase's producer in a fresh context with the brief (8.7).
3. Start the phase's reviewer in a fresh context with the brief's task and acceptance criteria and the producer's output, not its transcript or reasoning.
4. On a reviewer FAIL, start a new producer with the brief and the findings file, then a new reviewer. After three FAILs in a row, stop the phase and record it as failed with its findings (5.5).
5. On PASS, record the output and the review file for the coordinator's end-of-cycle report, and pull the register for the new entries from this phase. Do not ask the human anything here.

## Phases and the skills they load

### Learn

Producer: [learn-producer](../../agents/learn-producer.md), which loads each skill's dos and don'ts together, its related practices and its Self-check. Reviewer: [learn-reviewer](../../agents/learn-reviewer.md), which loads only each skill's adversarial reviewer checks and don'ts.

Skill IDs: 9.1, 9.2, 9.3, 9.5, 9.6, 9.7, 9.8, 9.9, 9.10, 9.11, 9.12.

- [9.1 reviewer-rule-or-mechanical-check](../reviewer-rule-or-mechanical-check/SKILL.md): When the reviewer missed a mistake, give the reviewer a new rule; if the mistake is mechanical, build a lint, hook or CI check instead
- [9.2 enforce-standards-at-review](../enforce-standards-at-review/SKILL.md): Enforce standards at review, not by loading them into the implementer's context
- [9.3 prune-rules-that-dont-change-behaviour](../prune-rules-that-dont-change-behaviour/SKILL.md): Remove or clarify rules that don't change behaviour
- [9.5 blameless-five-whys](../blameless-five-whys/SKILL.md): Ask what conditions allowed the failure, not who caused it (blameless, 5 whys)
- [9.6 group-failures-by-mechanism](../group-failures-by-mechanism/SKILL.md): Group failures by the mechanism behind them, not by error text
- [9.7 tdd-for-skills](../tdd-for-skills/SKILL.md): Before hardening a skill, reproduce the failure as a baseline scenario and record the agent's excuses; then close the loophole and re-test
- [9.8 small-one-surface-edits](../small-one-surface-edits/SKILL.md): Keep each learned edit small, to one surface, and keep behaviour that already passes
- [9.9 held-out-acceptance](../held-out-acceptance/SKILL.md): Accept a rule change coming out of a retrospective only if it measurably improves results on held-out cases it was not tuned on
- [9.10 human-approves-learned-changes](../human-approves-learned-changes/SKILL.md): A human approves each learned change before it goes live
- [9.11 capture-corrections-batch-later](../capture-corrections-batch-later/SKILL.md): Capture corrections as they happen; process them later in a batch
- [9.12 ledger-of-edits](../ledger-of-edits/SKILL.md): Keep a record of every accepted and rejected edit
