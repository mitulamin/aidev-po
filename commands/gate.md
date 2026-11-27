---
name: gate
description: "Run the current stage's adversarial reviewer, evidence-auditor, and challenger, then consult the user with layered outliner Q&A and optionally commit on approval."
---

Run `po`'s stage-gate workflow for the active product (or the `<slug>` / `<stage>` named in the argument):

1. Verify the current stage artefact exists; if not, run the stage producer first.
2. Ensure `<stage>-reviewer` returns `Verdict: PASS` (revising via fresh producer/reviewer up to 3 attempts on `FAIL`) and `evidence-auditor` returns `Verdict: PASS`.
3. Run `challenger` in a fresh context and curate `.po/register.jsonl`.
4. Present the artefact summary, verdicts, challenger items, and at most 5 layered questions per round (recommended answer first, trade-offs, Park option with revisit trigger).
5. Record answers, overruled challenges (as `decision` entries), and parked items; update `.po/state.json` and write the gate report (`templates/gate-report.md`).
6. Ask the user for explicit permission before committing the stage changes in the products repo; never push unless asked.
