---
title: Decisions
---

# Decisions

Product decisions for aidev-po, newest first. Each entry records what was decided, why, and what it replaces. Entries are not rewritten; a later decision supersedes an earlier one by ID.

## DEC-001: Say who decides before an undoable change ships

- **Date:** 27 November 2026
- **Decided by:** Mitul Amin (Shravi Limited)
- **Status:** Accepted
- **Area:** Scope boundary for skill changes
- **Refines and generalises:** retro proposal P-1 from the worked example (`examples/tool-library-loans/.po/retro/retro-20261118-01/`), where a late-returns rule (three late returns leading to the member being spoken to or suspended) had been written as an automatic suspension.

### Decision

When a rule creates an undoable change, meaning a change that is not repairable by the person it lands on, there must be clarity on who the decision maker is before the change ships, not after.

Being repairable by an operator (for example, an admin) is acceptable to a certain extent. But if harm is done to a user, that is still harm even if an admin can repair it, so there must be a decision on who gets to make that call.

### What changes

P-1 triggered on a narrow case: a policy that applies a sanction or changes a person's rights. This decision replaces that narrow harm or deletion trigger with a broader one: any change that the person it lands on cannot undo themselves. For such a rule, skills and reviewers must record who decides (the system or a named actor). If the inputs do not say, they raise a `[QUESTION: ...]` rather than writing an automatic rule.

### Why

Operator repair does not undo the harm the user already experienced. Naming the decision maker up front makes the call deliberate and traceable instead of an accident of how a rule was phrased.

### Follow-up

Update `skills/c4-context-eventstorming/SKILL.md` and its matching reviewer check from the P-1 wording to the undoable-change trigger.
