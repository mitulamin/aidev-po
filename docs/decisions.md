---
title: Decisions
---

# Decisions

Product decisions for aidev-po, newest first. Each entry records what was decided, why, and what it replaces. Entries are not rewritten; a later decision supersedes an earlier one by ID.

## DEC-002: aidev-po and ai-sdlc-loop share one register taxonomy so handoffs work in both directions

- **Date:** 27 November 2026
- **Decided by:** Mitul Amin (Shravi Limited)
- **Status:** Accepted
- **Area:** Register format and the handoff to and from ai-sdlc-loop
- **Replaces:** aidev-po's own register shape, which used `stage` where ai-sdlc-loop uses `phase`, `by: "user"` where it uses `"human"`, left out `blocker`, and added types, statuses and fields ai-sdlc-loop's checker rejects. ai-sdlc-loop's `scripts/register.py check` failed on every aidev-po register, so the gate bundle could only carry a copy that ai-sdlc-loop could not check and aidev-po could not take back.

### Decision

aidev-po and [ai-sdlc-loop](https://github.com/mitulamin/ai-sdlc-loop) use one register taxonomy. Where ai-sdlc-loop's register contract (`data/agent-contract.json`, `register`) already defines something, it is the shared baseline and aidev-po follows it. aidev-po keeps its stages by writing them in the shared `phase` field, not in a parallel field. What aidev-po needs and ai-sdlc-loop lacks is an optional, documented **aidev-po extension** that both checkers accept. A register can then go to ai-sdlc-loop in the gate bundle and come back with engineering's entries, and pass both checkers either way.

### Mapping

| What | Before (aidev-po) | Now (shared) |
|------|-------------------|--------------|
| Where a line belongs | `stage`, one of the eight stages | `phase`, any non-empty string. aidev-po writes its stage (`idea` ... `fsd`); ai-sdlc-loop writes `Plan`, `Design`, ... or `all` |
| Who answered | `by: "user"` | `by: "human"` (baseline) |
| Blockers | not allowed; a high-urgency question instead | `blocker` type and `[BLOCKER: ...]` block line (baseline); open blockers come first and hold the gate |
| `decision`, `feedback`, `attribution` types | aidev-po only | aidev-po extension |
| `decided`, `superseded` statuses | aidev-po only | aidev-po extension |
| `item_ids`, `record` fields | aidev-po only | aidev-po extension (`record` required for feedback and attribution) |
| `id`, `ts`, `impact`, `urgency`, `via`, `note`, `answer`, `recommendation`, block delimiters | already the same | unchanged |
| Default path | `.po/register.jsonl` | unchanged (ai-sdlc-loop's default is `.ai-sdlc/register.jsonl`; the handoff passes `--register`) |

Feedback severities (P0 to P3), evidence tags and item IDs are not register fields, so they do not cross in the register; they stay in aidev-po's trace, feedback and attribution files.

### What changes

- `schemas/register.schema.json` and `scripts/register.py` follow the shared baseline plus the extension (`x-extension` in the schema). `--stage` becomes `--phase` on `register.py add`, `ingest`, `update` and `list`.
- `scripts/register.py merge --from <bundle>/register.jsonl` brings ai-sdlc-loop's entries back into the product register: it appends only lines the product lacks, and writes nothing if any line fails. `po` shows entries whose `phase` is not a stage as engineering's questions and blockers, and the user decides which are feedback.
- `scripts/register.py migrate --write` rewrites a register written before this decision (`stage` to `phase`, `by: "user"` to `"human"`). It is the one change to a register that is not an append. The worked example and the test fixtures are migrated.
- `tests/test_shared_register.py` runs a vendored copy of ai-sdlc-loop's checker (`tests/vendor/ai-sdlc-loop/`) on every aidev-po register, runs aidev-po's checker on lines ai-sdlc-loop writes, round-trips a register through a gate bundle, and fails if the two taxonomies drift.
- ai-sdlc-loop accepts the extension through a change to its contract (`register.extensions`, schema 1.2.0) proposed in [mitulamin/ai-sdlc-loop#29](https://github.com/mitulamin/ai-sdlc-loop/pull/29). Until that merges, ai-sdlc-loop's released checker passes the baseline lines of an aidev-po register but not its decision, feedback and attribution lines.

### Why

The handoff is only as good as what crosses it. Locked decisions have to reach ai-sdlc-loop's coordinator in a form its tools read, and engineering's questions about the spec have to come back to the product owner in a form aidev-po's tools read. Two near-identical formats with different field names break both directions for no gain. A shared baseline with a named, optional extension keeps each tool free to add what it needs without forking the format.

### Follow-up

- Re-pin `tests/vendor/ai-sdlc-loop/` to ai-sdlc-loop main once [ai-sdlc-loop#29](https://github.com/mitulamin/ai-sdlc-loop/pull/29) merges.

## DEC-001: Say who decides before an undoable change ships

- **Date:** 27 November 2026
- **Decided by:** Mitul Amin (Shravi Limited)
- **Status:** Accepted
- **Area:** Scope boundary for skill changes
- **Refines and generalises:** retro proposal P-1 from the worked example (`examples/.po/retro/retro-20261118-01/`), where a late-returns rule (three late returns leading to the member being spoken to or suspended) had been written as an automatic suspension.

### Decision

When a rule creates an undoable change, meaning a change that is not repairable by the person it lands on, there must be clarity on who the decision maker is before the change ships, not after.

Being repairable by an operator (for example, an admin) is acceptable to a certain extent. But if harm is done to a user, that is still harm even if an admin can repair it, so there must be a decision on who gets to make that call.

### What changes

P-1 triggered on a narrow case: a policy that applies a sanction or changes a person's rights. This decision replaces that narrow harm or deletion trigger with a broader one: any change that the person it lands on cannot undo themselves. For such a rule, skills and reviewers must record who decides (the system or a named actor). If the inputs do not say, they raise a `[QUESTION: ...]` rather than writing an automatic rule.

### Why

Operator repair does not undo the harm the user already experienced. Naming the decision maker up front makes the call deliberate and traceable instead of an accident of how a rule was phrased.

### Follow-up

Update `skills/c4-context-eventstorming/SKILL.md` and its matching reviewer check from the P-1 wording to the undoable-change trigger.
