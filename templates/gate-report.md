# Stage Gate Report: <Product Name> — <Stage>

- **Product slug**: `<slug>`
- **Stage**: `<idea | audience | actors | systems | scope | workshops | presentations | fsd>`
- **Run ID**: `<run-id>`
- **Date (UTC)**: `<YYYY-MM-DDTHH:MM:SSZ>`
<!-- TRACE_RESERVE: run_summary_for_pr3; fields=run,stage,agent,verdicts,register_refs -->

## 1. Stage Artefact Produced

- **Artefact**: `<01-idea.md ...>`
- **Summary**: `<3-5 concise bullets>`

## 2. Fresh-Context Verdicts

| Check | Agent | Verdict | Findings File | Notes |
| --- | --- | --- | --- | --- |
| Stage Review | `<stage>-reviewer` | `PASS / FAIL` | `.po/runs/<run-id>/<stage>-review.md` | ... |
| Evidence Audit | `evidence-auditor` | `PASS / FAIL` | `.po/runs/<run-id>/<stage>-evidence.md` | ... |
| PO Challenge | `challenger` | `N challenges` | `.po/runs/<run-id>/<stage>-challenge.md` | ... |

## 3. Challenger Items & Overrules

| Challenge ID | Challenge Summary | Resolution (`Accepted & Fixed` / `Overruled -> Decision` / `Parked`) | Decision / Register ID |
| --- | --- | --- | --- |
| `CH-...-001` | ... | ... | `r-...` |

## 4. Open Register Items & Outliner Q&A Rounds

| Register ID | Type | Question / Assumption | User Decision / Answer | Status |
| --- | --- | --- | --- | --- |
| `r-...` | `question` | ... | ... | `answered` / `decided` / `surfaced` |

## 5. Gate Decision & Products-Repo Commit

- **User Gate Decision**: `APPROVE & ADVANCE` | `REVISE STAGE` | `HOLD`
- **Next Stage**: `<next stage or HANDOFF>`
- **Products-Repo Commit**: `User OK: Yes / No` — `<commit sha & message, or left uncommitted per user>`

## Assumptions and open questions

=== REGISTER REQUESTS ===
None.
=== END REGISTER REQUESTS ===
