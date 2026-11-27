# Held-out pool for retro-20261118-01

> Fictional demo for the aidev-po worked example. Kept out of the brief: `learn-producer` never sees this file.

This is the first retro in this products repo, so the ledger has no earlier confirmed cases. aidev-po's worked example (`examples/tool-library-loans`) is this product, so the held-out cases are the systems-stage items of this product that the feedback does not touch, and that any fix for FB-001 could break.

| Case | Stage, step | Why it is a good test |
|------|-------------|-----------------------|
| `tool-library-loans/SYS-008` automatic hold release | systems, 3-event-storming | A policy that is correctly automatic (DEC-004, r-20261016145000-2034). An edit that makes every policy ask "who decides?" must still let this one be automatic. |
| `tool-library-loans/SYS-010` automatic reminders | systems, 3-event-storming | Another correct automatic policy, Inferred from scope rather than Stated. Tests that the edit does not treat "Inferred and automatic" as "unsupported". |
| `tool-library-loans/SYS-009` deposit rule at check-out | systems, 3-event-storming | A rule a person applies at the desk, Stated from r-20261005090900-2005. Tests that the edit does not add questions where the actor is already known. |

Pass means: the step writes the item with the same meaning as the approved rev, and raises no new question the user already answered.
