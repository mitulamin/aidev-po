---
name: feedback-intake
description: "Use when the user gives feedback on any product output, by /po-feedback, by saying in chat that something is wrong, or by a pull request comment in the products repo. Records it against the right items with a severity (P0 to P3) and one of nine what's-wrong categories."
---

# Feedback intake

Feedback is captured the moment it is given and processed later in a batch (ai-sdlc-loop 9.11). Each piece becomes one feedback line, attached to the item IDs and revisions it is about, so the tracer can walk it back.

Format: `schemas/feedback.schema.json`. File: `<product>/.po/feedback.jsonl`. Each line also gets a register line of type `feedback` with `record` set to its ID.

## When to use

- The user runs `/po-feedback`.
- The user says, in any conversation with `po`, that an output is wrong, missing something or unclear. Offer to record it; do not argue first.
- The user asks `po` to take in comments from a pull request in the products repo.

## Severity

| | Meaning | Example |
|-|---------|---------|
| P0 | Blocks use. Acting on it would cause real harm or a wrong build. | A requirement that breaks a legal duty; a missing actor the whole flow depends on |
| P1 | Wrong. | A permission nobody granted |
| P2 | Weak. Right, but thin, vague or poorly argued. | A goal with no measure |
| P3 | Polish. | Wording, order, formatting |

## What's wrong: nine categories

| Category | Means | Example |
|----------|-------|---------|
| `wrong-or-invented` | States something nobody said, or something false. Includes invented content: a requirement, actor, figure or quote with no source. | "Admins can delete records": nobody said delete |
| `missing` | Leaves out an actor, system, requirement, risk, step or other item that should be there. | No practice owner in the actor list |
| `misunderstood-intent` | Recorded a different meaning from what the user said. | We said "tidy up", it wrote "delete" |
| `wrong-scope-or-priority` | In when it should be out, out when it should be in, or the wrong priority. | A Should written as a Must |
| `unclear-or-untestable` | Vague words, two requirements in one, no acceptance criteria, or a criterion nobody could test. | "The system shall be fast" |
| `inconsistent` | Contradicts another output, the glossary, or a locked decision. | The FSD says weekly, the decision says daily |
| `wrong-for-audience` | Right content, wrong tone, depth, language or format for its reader. | Jargon in the board deck |
| `process` | About how `po` worked, not one item. | Too many questions; a leading question; a skipped gate |
| `not-sure` | Feels wrong, the user cannot say why. | "Something's off with this slide" |

If two fit, take the earlier one in the list, except `not-sure`, which is used only when nothing else fits. `misunderstood-intent` beats `wrong-or-invented` when the user did say something and it was read wrongly.

## Steps

1. **Find the target.** Item IDs the user names; otherwise a quoted sentence (`python3 scripts/traces.py locate <file> --quote "<text>" --product <slug>`); otherwise a file and heading (level `section`), a file (`artefact`) or a run (`run`, for process feedback). If you cannot tell, show at most five candidate items and ask which.
2. **Record the revision.** Put each item's current `rev` in `target.item_revs`, so the feedback stays attached to the version it was about.
3. **Severity and category.** Use the user's if given. Otherwise propose both, with a one-line reason, and ask the user to confirm or change them in one short question. Never record a severity the user has not seen.
4. **Keep the words.** `text` is the user's words, verbatim. Put what it should say, if they said, in `expected`.
5. **Write it.** `python3 scripts/traces.py add feedback --product <slug> --json '{...}'` (it assigns the `FB-` ID), then its register line: `python3 scripts/register.py add --type feedback --record <FB-ID> --agent po --phase <stage of the target> --item-id <ID> ... --text "<the user's words>" --register <product>/.po/register.jsonl`.
6. **Hand on.** Offer to trace it now (the `tracer`); for P0 and P1 recommend yes. Fixing the output is `/po-rerun-from`; improving aidev-po is `/po-retro`.

## Pull request comments

The products repo is the user's and may be on GitHub. When asked to take in comments from a pull request there:

1. Read the review comments read-only, for example `gh api repos/<owner>/<repo>/pulls/<n>/comments`. Skip any whose `comment_id` is already in a feedback line.
2. A comment can start with a tag, for example `P1 missing: no practice owner`, or `[P2 unclear-or-untestable]`. Severity is any of P0 to P3; the category is a slug or its words from the table. Untagged comments get a proposed severity and category, confirmed by the user in batches of at most five.
3. The comment's path starts with the product folder. Find the item with `python3 scripts/traces.py locate <path inside the product> --line <line> --product <slug>`. If the file has changed since the comment's commit, locate by quoting the commented line instead.
4. Record each with `source` `pr-comment` and `pr` (url, comment_id, path, line, commit).
5. Never reply to, resolve or react to a comment unless the user asks.

The template `templates/learning/feedback-comment.md` shows users how to tag comments.

## Self-check

- [ ] Does each feedback line name the item IDs and revs it is about, or the run, file or section for wider feedback?
- [ ] Did the user see the severity and category before they were recorded?
- [ ] Is `text` the user's words, unchanged?
- [ ] Does each feedback line have a register line of type feedback pointing at it?
- [ ] For PR comments: is each comment taken in once, and was nothing posted back to the pull request?
