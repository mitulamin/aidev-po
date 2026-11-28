---
name: blameless-five-whys
description: "Use when end-of-run retro on any failure. Amalgamated skill for principle 9.5 (Learn)."
license: MIT
metadata:
  source: "skills/9.5-blameless-five-whys/SKILL.md"
  principles: "9.5"
  principle: "9.5 Ask what conditions allowed the failure, not who caused it (blameless, 5 whys)"
  category: learn
  status: "draft, untested"
---
<!-- Installed from ai-sdlc-loop skills/9.5-blameless-five-whys/SKILL.md at 1d473234a504 by scripts/new-project.sh, adapted for Cursor (front matter, links and command names). Licence: MIT, see the project's LICENSE. -->

# 9.5 Blameless five whys

Principle 9.5 (Learn): Ask what conditions allowed the failure, not who caused it (blameless, 5 whys)

## When to use

End-of-run retro on any failure.

## Producer: dos and don'ts

Do:
- Ask why five times toward conditions, not agents
- End with a system change

Don't:
- Conclude 'the agent made a mistake'

## Steps

1. State failure
2. 5 whys
3. Pick condition to change
4. Assign fix

## Self-check

Before you hand off, answer each item yes, no or N/A, with evidence. Fix every no, or record it as a `[BLOCKER: ...]`.

- [ ] Did the five whys lead to conditions, not to an agent's mistake?
- [ ] Does the conclusion name a change to the system?

## Adversarial reviewer (fresh context, tries to prove the work fails)

- Check the conclusion names a changeable condition
- Default verdict is FAIL until evidence shows otherwise; report findings to a file with P0-P3 severity.

## How the source skills compare

wshobson postmortem-writing and steipete five: ask what conditions allowed the failure (blameless, 5 whys).

## Sources

The licence-clean source files are listed with their licences and pinned links in SOURCES.md. Text here is written in our own words and released under MIT (see SOURCES.md for the sources it was adapted from).

## Test plan

- Test app: All runs (harness and Learn)
- Phase: Learn
- Test order: slot 36
- Record results in https://github.com/mitulamin/ai-sdlc-loop/blob/1d473234a504e587cfc1c4f53dafe03775fd3cb7/data/scorecard.json (criteria in https://github.com/mitulamin/ai-sdlc-loop/blob/1d473234a504e587cfc1c4f53dafe03775fd3cb7/README.md)
