---
name: learn-edits
description: "Use at /po-retro to turn traced feedback into learned edits. learn-producer loads the dos and don'ts; learn-reviewer loads only the reviewer checks and the don'ts. Small one-surface edits, blameless causes, held-in and held-out tests, human approval and a ledger, as in ai-sdlc-loop's Learn phase."
---

# Learned edits

This is ai-sdlc-loop's Learn phase (skills 9.1 to 9.12, `/retro`, `learn-producer`, `learn-reviewer`) adapted to aidev-po. The difference: here the input is not a summary but attributions from the `tracer`, each naming the step where an error began, its cause and a confidence. The numbers in brackets are the ai-sdlc-loop skills each rule comes from.

## When to use

`/po-retro`, after feedback has been traced and the user has confirmed the attributions.

## Producer: dos and don'ts

Do:
- Work only from confirmed attributions, or ones at 0.8 confidence or more that the user has not rejected.
- Group the attributions by the mechanism behind them (cause and origin agent, then what actually happened), not by the feedback's wording (9.6).
- Ask why toward conditions, not agents, until you reach something in aidev-po or the client's preferences that could change (9.5).
- Propose the smallest edit to **one** surface per proposal: one skill rule, one reviewer check, one lint or script check, one template, one question bank entry, one agent brief line, or one client preference (9.8).
- Send a judgement miss to the reviewer as one new check; send a mechanical miss to a script check (for example in `scripts/traces.py check`), not to a rule (9.1).
- Put enforcement in reviewer files, and give producers only a short do or don't (9.2).
- Scope each edit: global (aidev-po, every client), client (`.po/preferences.md` in the products repo) or product (a register decision, not a learning).
- Reproduce each failure first: write the held-in case as a scenario, run the step without the edit, record that it fails and the excuses the agent gives; then with the edit, until it passes (9.7).
- For each rule you touch, say what behaviour would change without it; propose removing rules that change nothing (9.3).
- Write proposals only. Nothing is applied until it passes held-out tests and the user approves it (9.9, 9.10).

Don't:
- Conclude "the agent made a mistake".
- Group by error message or feedback text.
- Rewrite a whole skill from one failure, or touch two surfaces in one proposal.
- Add a rule to a producer's always-on context or to `AGENTS.md`.
- Edit a skill without seeing it fail first.
- Accept a change because the triggering case now passes.
- Apply any edit yourself, or propose one from an attribution the user rejected.
- Copy client words, names or product details into a global edit.

## Steps

1. List the attributions in the brief, with cause, origin agent and confidence.
2. Group by mechanism. Rank groups by severity times count; repeat causes (`causes` in the scorecard) first.
3. For each group: five whys to a condition; pick the surface and scope; draft the edit as a diff.
4. Held-in: run the origin step on each case in the group without and with the edit (a scratch copy, never the products repo). Record pass counts and the excuses.
5. Write each proposal in the format of `templates/learning/retro-proposal.md`.

## Self-check

- [ ] Is every proposal one edit to one surface, with a scope?
- [ ] Does each conclusion name a condition to change, not an agent's mistake?
- [ ] Are the groups by mechanism, with no two groups sharing one?
- [ ] Was each held-in case run red before and green after, with the excuses recorded?
- [ ] Did a judgement miss become a reviewer check, and a mechanical one a script check?
- [ ] Is nothing applied?

## Adversarial reviewer

- Find a proposal that touches more than one surface, or has no scope.
- Find a conclusion that blames an agent instead of naming a condition.
- Find two groups with the same mechanism.
- Check a red baseline was recorded before each edit.
- Check the held-out cases were not in the producer's brief and did not regress.
- Check the held-in cases improved.
- Find a rule added to a producer's always-on context or to `AGENTS.md`.
- Find a proposal built on an attribution the user rejected, or below 0.8 and unconfirmed.
- Find a global edit that carries a client's words, names or product details.
- Check the new check or rule would have caught the original failure.
