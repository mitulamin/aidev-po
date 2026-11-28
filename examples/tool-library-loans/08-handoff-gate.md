# 08b — Engineering Handoff & Gate PR Brief: Lantern Lane Tool Library — Loans & Reservations

> Fictional demo. Lantern Lane Tool Library, its people and its data are invented for the aidev-po worked example.

- **Product slug**: `tool-library-loans`
- **Target Engineering Repo**: TBD (the volunteer build team has not set one up yet)
- **Source FSD**: `08-fsd.md`
- **Register**: `.po/register.jsonl`
- **Handoff Target**: `ai-sdlc-loop` coordinator (`/plan`)
<!-- TRACE_RESERVE: item_id_prefix=HND; trace_file=.po/traces.jsonl; fields=item_id,run,stage,agent,step,skill_versions,template_versions,upstream_ids,evidence_tag,register_refs -->

## 1. Handoff Readiness Gate

- [x] `fsd-reviewer`: `Verdict: PASS` (zero P0/P1 findings), first on 2026-11-03 and again after rerun RR-001 on 2026-11-12
- [x] `evidence-auditor`: `Verdict: PASS` (zero untagged or unsourced claims)
- [x] `challenger`: all challenges resolved or recorded as decisions
- [x] `.po/register.jsonl`: zero `open` or `surfaced` blockers or high-urgency questions (`scripts/register.py list --open`)

## 2. Brief for `ai-sdlc-loop` `/plan`

- **Goal (`HND-001`)**: let a volunteer-run tool library lend, hold and remind without paper cards, so overdue loans fall to 4 or fewer a month (`FSD-001` to `FSD-004`).
- **Users & Actors (`HND-002`)**: members, desk volunteers, the coordinator and the treasurer (`ACT-006`, `ACT-007`, `ACT-008`, `ACT-012`).
- **Scope — Slice 1 Only (`HND-003`)**: `US-001` to `US-008`, `REQ-001` to `REQ-008`, `NFR-001` to `NFR-009`. The late-return rule flags members for the coordinator's review and never suspends automatically (`REQ-004`, `REQ-008`).
- **Authoritative Spec Path**: `tool-library-loans/08-fsd.md` in the products repo

## 3. Locked Decisions (Do Not Override Downstream)

| Decision ID | Choice | Who Decided | Why | Register ID |
| --- | --- | --- | --- | --- |
| `DEC-001` | Loans, reservations and reminders; not a membership system | `user` | The pain is unseen and overdue tools | `r-20261005141500-2012` |
| `DEC-003` | Own logins; no shared desk account | `user` | Every loan shows who recorded it | `r-20261014145000-2027` |
| `DEC-004` | Holds last 48 hours, then release automatically | `user` | A weekend, without tying tools up | `r-20261016145000-2034` |
| `DEC-005` | Build the catalogue, not a shared calendar (challenger overruled) | `user` | The calendar failed in spring 2025 | `r-20261020150100-2040` |
| `DEC-006` | Release 1 is Slice 1 | `user` | Fits the appetite | `r-20261020150300-2042` |
| `DEC-007` | Only the coordinator waives deposits | `user` | Agreed at the workshop | `r-20261028150100-204d` |
| `DEC-009` | Email only in Release 1 | `user` | SMS parked until email gaps are known | `r-20261103100100-2060` |

The correction from rerun RR-001 is register decision `r-20261112090500-2069`: the system never suspends anyone by itself.

## 4. Explicit Non-Goals (Do Not Build)

| Park ID | Excluded Capability | Reason | Revisit Trigger |
| --- | --- | --- | --- |
| `PARK-001` | Online deposits | Cash works | More than 5 cash discrepancies in a quarter |
| `PARK-002` | SMS reminders | Unknown need, per-message cost | More than 20% of members without email after import |
| `PARK-003` | Member self-edit | Rare changes | More than 10 change requests in a month |
| `PARK-004` | Barcode labels | Large one-off job | Median check-out over 2 minutes in month one |
| `PARK-005` | Condition photos | Rare disputes | More than 3 damage disputes in a quarter |
| `PARK-006` | Delivery | New process and insurance | Funder asks, or 10 member requests in a season |
| `PARK-007` | Offline mode | One short Wi-Fi drop seen | Wi-Fi out over 5 minutes on two Saturdays in a month |
| `PARK-009` | Second site | One site | The board agrees a second site |

## 5. Numbered Acceptance Criteria Index (Given/When/Then)

- `AC-001`, `AC-002` (`US-001`); `AC-003`, `AC-004` (`US-002`); `AC-005`, `AC-006` (`US-003`); `AC-007` (`US-004`); `AC-008`, `AC-009` (`US-005`); `AC-010` (`US-006`); `AC-011`, `AC-014` (`US-007`); `AC-012`, `AC-013` (`US-008`). Full text in `08-fsd.md` §5.1.

## 6. Gate PR Plan (Requires Explicit User OK)

- **Proposed branch in target repo**: `docs/fsd-tool-library-loans`
- **Files to include in Gate PR**: `08-fsd.md`, `08-handoff-gate.md`
- **User approval to open Gate PR**: `PENDING USER OK` (the board approved the spend on 2026-11-04; the coordinator will say when the build team has a repo). Never push or open a PR without explicit user approval.

## Assumptions and open questions

=== REGISTER REQUESTS ===
None.
=== END REGISTER REQUESTS ===
