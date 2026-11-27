# Proposals for retro-20261118-01

> Fictional demo for the aidev-po worked example. Round 2, written by a fresh `learn-producer` with the brief and `review-round1.md`. P-3 is kept below, marked withdrawn, so the ledger can record it.

## P-1: say who decides for any policy that applies a sanction

- **Scope:** global
- **Surface:** skill, `skills/c4-context-eventstorming/SKILL.md`
- **Mechanism:** a stated rule turned into an automatic sanction
- **Covers:** tool-library-loans/FB-001 via tool-library-loans/AT-001
- **Cause:** `unsupported-inference` at systems-producer, 3-event-storming

### Why (blameless)

1. Why did the FSD require an automatic suspension? Because every stage after Systems restated policy `SYS-012`.
2. Why did `SYS-012` say "automatic"? Because the policy form "Whenever X, then Y" names a command but not who issues it, and the step's inputs did not say.
3. Why did the inputs not say? Because no step before Systems asks who applies a rule, and the Systems step has no prompt to ask either.
4. The condition aidev-po can change: step 3 of the skill does not ask who decides when a policy sanctions a person.

### The edit

In step 3, for a policy that applies a sanction or changes a person's rights, record who decides (the system or a named actor); if the inputs do not say, raise a `[QUESTION: ...]` instead of writing an automatic policy. Diff: `P-1.diff`.

Judgement or mechanical: judgement, so it lives in the skill's step and the reviewer's check, not a script.

What would change without it: Systems keeps filling the actor gap in sanction policies with "automatic".

### Held-in

| Case | Without the edit | With the edit | Excuse the agent gave without it |
|------|------------------|---------------|----------------------------------|
| tool-library-loans/FB-001 | fail | pass | "Policies are written as automatic reactions, so the house rule becomes SuspendMember." |

Before: 0 of 1 pass. After: 1 of 1 pass.

## P-2: this client applies house rules in person

- **Scope:** client
- **Surface:** client-preference, `.po/preferences.md`
- **Mechanism:** a stated rule turned into an automatic sanction
- **Covers:** tool-library-loans/FB-001 via tool-library-loans/AT-001
- **Cause:** `unsupported-inference` at systems-producer, 3-event-storming

### Why (blameless)

1. to 3. As P-1.
4. The condition this client's preferences can change: nothing tells a producer that this client never automates sanctions, so every new product starts without it.

### The edit

Add to this client's preferences: house rules are applied by the coordinator in person; never specify an automatic sanction without a register decision naming who decides. Diff: `P-2.diff`.

Judgement or mechanical: judgement; `po` passes the preference into each brief.

What would change without it: until a global edit lands, this client's next product can repeat FB-001.

### Held-in

| Case | Without the edit | With the edit | Excuse the agent gave without it |
|------|------------------|---------------|----------------------------------|
| tool-library-loans/FB-001 | fail | pass | "Policies are written as automatic reactions, so the house rule becomes SuspendMember." |

Before: 0 of 1 pass. After: 1 of 1 pass.

## P-3 (withdrawn in round 2): evidence-auditor fails unstated automation

- **Scope:** global
- **Surface:** reviewer-check, `agents/evidence-auditor.md`
- **Mechanism:** a stated rule turned into an automatic sanction
- **Covers:** tool-library-loans/FB-001 via tool-library-loans/AT-001
- **Cause:** `unsupported-inference` at systems-producer, 3-event-storming

### The edit

Add a check: fail any Inferred item that adds automation (a system action with no actor) that its upstream items do not state. Diff: `P-3.diff`.

Held-in: before 0 of 1, after 1 of 1.

Withdrawn: `learn-reviewer` failed it in round 1 (held-out regressions on `SYS-008` and `SYS-010`; see `review-round1.md`). Narrowing it to "sanctions only" makes it the same as P-1 in a second place, so this round drops it rather than reworking it.

### Assumptions and open questions

=== REGISTER REQUESTS ===
None.
=== END REGISTER REQUESTS ===
