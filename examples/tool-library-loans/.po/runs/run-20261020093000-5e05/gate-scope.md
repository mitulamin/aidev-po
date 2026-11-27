# Stage Gate Report: Lantern Lane Tool Library — Scope

> Fictional demo for the aidev-po worked example. This is the gate as held on 2026-10-20. `SCP-010` was rebuilt by rerun RR-001; see `.po/runs/run-20261112093000-9c09/gate-scope.md`.

- **Product slug**: `tool-library-loans`
- **Stage**: `scope`
- **Run ID**: `run-20261020093000-5e05`
- **Date (UTC)**: `2026-10-20T15:10:00Z`

## 1. Stage Artefact Produced

- **Artefact**: `05-scope.md`
- **Summary**:
  - Appetite: within the £6,000 grant, live before 2027-03-01 (`SCP-001`).
  - Impact map `SCP-002` to `SCP-004`; Must items `SCP-005` to `SCP-011` (Slice 1); Slice 2 `SCP-012`, `SCP-013`.
  - As written then, `SCP-010` was "Must: automatic 30-day suspension", carried from `SYS-012`.

## 2. Fresh-Context Verdicts

| Check | Agent | Verdict | Findings File | Notes |
| --- | --- | --- | --- | --- |
| Stage Review | `scope-reviewer` | `PASS` | this report | P2 on `SCP-011`: name the duplicates hotspot and who clears it. Fixed as `SCP-011` rev 2. |
| Evidence Audit | `evidence-auditor` | `PASS` | this report | P3 on `SCP-012`: slice placement rests on an open question. Retagged Stated at the gate (rev 2) from the answer to `r-20261020113001-203b`. |
| PO Challenge | `challenger` | `3 challenges` | this report | See below. |

## 3. Challenger Items & Overrules

| Challenge ID | Challenge Summary | Resolution | Decision / Register ID |
| --- | --- | --- | --- |
| `CH-SCOPE-001` | Cheaper Route: a shared calendar plus mail-merge reminders from the spreadsheet, no build; trial four weeks first. | **Overruled by the user**: the calendar was tried in spring 2025 and failed after six weeks. Recorded as DEC-005. | `r-20261020123000-203e` → `r-20261020150100-2040` |
| `CH-SCOPE-002` | Assumption Map: the import assumes clean data. | Accepted & Fixed: `SCP-011` rev 2 depends on the coordinator merging duplicates (`SYS-013`). | `r-20261016113002-2031` |
| `CH-SCOPE-003` | Pre-Mortem: volunteers drift back to paper if the tablet is slow. | Accepted: tested at the volunteer workshop; `r-20261020113000-203a` stays open. | `r-20261020113000-203a` |

## 4. Open Register Items & Outliner Q&A Rounds

Gate, round 1 (five questions; the challenge first, because the rest of the scope depends on it):

| Register ID | Type | Question / Assumption | User Decision / Answer | Status |
| --- | --- | --- | --- | --- |
| `r-20261020123000-203e` | `question` | CH-SCOPE-001: trial a shared calendar and mail-merge for four weeks first? (Recommended by the challenger: trial it. Park: not offered, the build decision depends on it.) | "No. We tried a shared calendar in spring 2025 … Build the catalogue." Overrule recorded as DEC-005 (`r-20261020150100-2040`, by user). | `answered` |
| `r-20261020150300-2042` | `decision` | Release 1 is Slice 1, `SCP-005` to `SCP-011` (recommended). | Agreed. DEC-006. | `decided` |
| `r-20261020113001-203b` | `question` | Waiting list (recommended: Slice 2). | Slice 2. | `answered` |
| `r-20261020113002-203c` | `question` | Condition photos at check-in (recommended: no; Park). | Park. PARK-005, trigger: more than 3 damage disputes in a quarter. | `answered` |
| `r-20261020113003-203d` | `question` | Delivery or collection (recommended: no; Park). | Park. PARK-006, trigger: the funder asks, or 10 members ask in a season. | `answered` |

Still open: `r-20261020113000-203a` (volunteers keep using the tablet after month one).

Not asked, and found later by AT-001: nobody asked whether the coordinator wants `SCP-010`'s suspension to be automatic. Scope only passed on what Systems had written.

## 5. Gate Decision & Products-Repo Commit

- **User Gate Decision**: `APPROVE & ADVANCE`
- **Next Stage**: `workshops`
- **Products-Repo Commit**: `User OK: Yes` — `tool-library-loans: complete scope stage — appetite, impact map, Slice 1; overrule CH-SCOPE-001`

## Assumptions and open questions

=== REGISTER REQUESTS ===
None.
=== END REGISTER REQUESTS ===
