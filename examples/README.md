# examples

One worked example of aidev-po output: **Lantern Lane Tool Library — Loans & Reservations** (`tool-library-loans/`).

> **Fictional demo.** The tool library, its coordinator, volunteers, members, board and funder are invented. So are the commit SHAs in the records (`a1b2c3d`, `c0ffee1`), the products-repo pull request URL, and the held-out runs in the retro, which are described rather than recorded. Items tagged `Simulated` (`AUD-013`, `PRS-007`) are labelled as such and are not evidence. The skill and template versions in the trace lines are real aidev-po commits from when the example was written.

Examples are not live products. Your own products belong in your private products repo, never here. See [docs/products-repo.md](../docs/products-repo.md).

## What it is

`examples/` is laid out as a products repo with one product, exactly as `po` would leave it:

```text
examples/
  .po/                          products-repo level
    ledger.jsonl                every learned edit proposed at /po-retro: accepted, rejected or deferred
    scorecard.json              measures by run, repeat causes, and skill scores
    preferences.md              this client's preferences (one added by the retro)
    retro/retro-20261118-01/    brief, held-out pool, proposals and diffs, held-out results, reviews, report
  tool-library-loans/
    01-idea.md … 08-fsd.md      the eight stage files, from templates/
    08-handoff-gate.md          the handoff brief for ai-sdlc-loop /plan
    inputs/, workshops/         the source notes that Stated and Validated items cite
    .po/
      state.json                current stage, completed stages, last run
      register.jsonl            questions, assumptions, decisions, feedback and attribution lines
      traces.jsonl              one line per item written or reviewed
      feedback.jsonl            FB-001 and FB-002
      attributions.jsonl        AT-001 (three lines: tracer, replay, user verdict)
      reruns.jsonl              RR-001 (planned, approved, done, committed)
      tracer/FB-001-AT-001.md   the tracer's report
      runs/<run-id>/            gate reports; the systems run also has its brief, report, review, evidence audit and challenge
```

The product: a volunteer-run tool library replaces paper loan cards and a shared spreadsheet with a small web app for availability, 48-hour holds, desk check-out and email reminders. It went through all eight stages between 2026-10-05 and 2026-11-03.

The example has 183 items, each with a stable ID and a trace record:

| IDs | Stage |
| --- | --- |
| `IDEA` | Idea |
| `AUD` | Audience |
| `ACT` | Actors |
| `SYS` | Systems |
| `SCP` | Scope |
| `WKS` | Workshops |
| `PRS` | Presentations |
| `FSD`, `US`, `AC`, `REQ`, `NFR` | FSD |
| `HND` | Handoff |
| `DEC`, `PARK` | Decisions and parked items at every gate |

## What to look for

- **Evidence tags used honestly.** The items are tagged Stated (84), Inferred (71), Assumed (22), Validated (4) and Simulated (2). Every Assumed item relies on a register assumption. `AUD-003` was first tagged Stated on an assumption; the audience reviewer failed it, and rev 2 is Validated from the desk notes (`grep AUD-003 examples/tool-library-loans/.po/traces.jsonl`).
- **An overruled challenge.** At Scope the challenger proposed a shared calendar and mail-merge instead of a build (`CH-SCOPE-001`). The coordinator overruled it, because the calendar had already been tried and had failed, and the overrule is recorded as decision `DEC-005` (`05-scope.md` and the scope gate report).
- **Question rounds of at most five questions.** Each gate report lists its rounds. Every question has a recommended answer, and most offer Park with a revisit trigger (`PARK-001` to `PARK-009`).
- **Assumptions.** Some are settled by evidence: "desk volunteers will record loans on a tablet" (`r-20261005104003-200e`) was dismissed by `WKS-004`. Others, such as "volunteers will keep using the tablet after the first month" (`r-20261020113000-203a`), are still open at handoff.

## The learning loop, end to end

1. **The error.** At Systems, the EventStorming step turned the house rule "three late returns in a year and you lose borrowing for a month" into an automatic policy (`SYS-012` rev 1). Scope (`SCP-010`), the board deck (`PRS-013`) and the FSD (`US-007`, `AC-011`, `REQ-004`) passed it on faithfully.
2. **Feedback.** On 2026-11-10 the coordinator ran `/po-feedback REQ-004 P1 …`, which recorded FB-001: P1, `misunderstood-intent`, in her own words.
3. **Trace.** The tracer walked `traces.jsonl` from `REQ-004` back to `SYS-012`. Its attribution AT-001 names:
   - The origin, the carriers and the cause (`unsupported-inference`).
   - A confidence of 0.65, with two alternatives (the idea step dropping "I always have a word with them first", at 0.3; no question about who applies house rules, at 0.2).
   - The reviewer that should have caught it (evidence-auditor).

   A replay in a scratch copy raised the confidence to 0.8, and the user confirmed it.
4. **Rerun.** `/po-rerun-from AT-001` planned RR-001 from `SYS-012`. `traces.py downstream SYS-012` gave the ten items to rebuild. The user took the narrower option and kept `FSD-004` and `HND-001`, which don't say "automatic". The rerun:
   - Rebuilt eight items and added `AC-014` and `REQ-008`.
   - Reopened four gates.
   - Committed once, with the user's OK.

   See `.po/runs/run-20261112093000-9c09/`.
5. **Retro.** `/po-retro` produced three proposals:
   - P-1, a global skill edit: deferred, since there is one case in one product. Later adopted: the maintainer applied it to `skills/c4-context-eventstorming/SKILL.md` with its trigger widened by DEC-001 to any change the person it lands on cannot undo themselves. The ledger shows this as a newer `LE-001` line (`accepted`, `applied`); the deferred line and the retro files are left as they were.
   - P-2, a client preference: accepted and applied.
   - P-3, a reviewer check: it regressed two held-out cases, the learn-reviewer failed it, and the ledger records it as rejected so it isn't proposed again.
6. **Scorecard.** `c4-context-eventstorming` has a harm flag from the systems run, so the verdict is the user's. `trace-records` points to keep.
7. **Still open.** FB-002 (P3, `wrong-for-audience`) came in from a products-repo pull request comment on slide `PRS-019` ("operators" should say "desk volunteers"). It came in on 2026-11-20, after the retro, and has no attribution yet. `python3 scripts/traces.py open-feedback --all --repo examples` lists it, and `/po-continue` shows it at catch-up. The next `/po-retro` traces it first (step 1): it lists FB-002, asks whether to trace it now, runs the tracer and asks you to confirm, and only then selects attributions for proposals. If you say no, FB-002 stays open and is offered again at the next retro.

To follow the trace yourself:

```bash
python3 scripts/traces.py chain REQ-004 --feedback FB-001 --dir examples/tool-library-loans
python3 scripts/traces.py locate 04-systems.md --quote FlagMemberForReview --dir examples/tool-library-loans
python3 scripts/traces.py downstream SYS-012 --dir examples/tool-library-loans
python3 scripts/scorecard.py measures --repo examples
python3 scripts/traces.py open-feedback --all --repo examples    # FB-002, untraced
```

## Checks

CI runs these on every pull request, and `tests/test_example.py` also validates every line against its schema:

```bash
python3 scripts/traces.py check --all --repo examples
for f in examples/*/.po/register.jsonl; do python3 scripts/register.py check --register "$f"; done
python3 scripts/scorecard.py check --repo examples
```

To change the example, edit it the way `po` edits a real product. Each changed item gets a new trace line (`scripts/traces.py add`), each answer or decision a register line (`scripts/register.py`), and then the checks above must still pass.

## As the held-out and reference case for /po-retro

`/po-retro` step 3 builds its held-out pool from confirmed cases already in the ledger and from the matching stages of this example. The learn-producer never sees them. To use it:

1. Pick the stage a proposal touches, for example `tool-library-loans` systems for an edit to `c4-context-eventstorming`. Choose items whose approved rev the edit could break, such as `SYS-008` and `SYS-010` (correctly automatic) or `SYS-009` (a person applies the rule). Write them to the retro's `heldout-pool.md`, never to the brief.
2. In a scratch git worktree of aidev-po, copy `examples/tool-library-loans` to a scratch folder. Run the affected step on it without the diff and then with it.
3. A case passes if the step writes the item with the meaning of its approved rev and asks nothing the register already answers. Record the counts and any regression in `heldout.md`.

This example's own retro (`.po/retro/retro-20261118-01/`) shows the whole loop, including a proposal rejected for held-out regressions. Its `heldout-pool.md` explains why its held-out cases come from the same product: it was the first retro, and the example is that product.

The example also serves as a reference for a finished product: what a complete stage file, gate report, trace chain and ledger look like.

## Try po against a copy

Run `po` on a copy outside aidev-po, never on `examples/` itself, and never commit products to aidev-po:

```bash
cp -r examples /tmp/demo-products
cd /tmp/demo-products && git init && git add -A && git commit -m "Demo products repo from the aidev-po worked example"
export AIDEV_PO_PRODUCTS_DIR=/tmp/demo-products
```

Then open aidev-po in Cursor and try, for example:

- `/po-continue tool-library-loans` to see the catch-up, with FB-002 open.
- `/po-feedback PRS-019 P3 …` or `/po-feedback --pr …` to take in feedback.
- `/po-rerun-from …` after a trace.
- `/po-retro` to run a retro on the copy: it offers to trace FB-002 first, since no attribution names it yet.

`po` commits to `/tmp/demo-products` only with your OK, and never pushes. Delete the folder when you are done.

## Licence

The example is writing, not code: CC BY-SA 4.0, as [NOTICE.md](../NOTICE.md) lists for `examples/` ([LICENSE-CONTENT](../LICENSE-CONTENT)).
