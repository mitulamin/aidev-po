# 03 — Actors & Stakeholders: <Product Name>

- **Product slug**: `<slug>`
- **Stage**: `actors`
- **Status**: `draft` | `gate-approved`
- **Run ID**: `<run-id>`
- **Register**: `.po/register.jsonl`
<!-- TRACE_RESERVE: item_id_prefix=ACT; trace_file=.po/traces.jsonl; fields=item_id,run,stage,agent,step,skill_versions,template_versions,upstream_ids,evidence_tag,register_refs -->

## 1. Power / Interest Stakeholder Map

| ID | Stakeholder / Group | Role Type (Buyer / Decision Maker / Gatekeeper / User / Operator) | Power | Interest | Quadrant Strategy | Evidence Tag & Source | Upstream IDs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ACT-001` | ... | ... | High / Low | High / Low | Manage Closely / Keep Satisfied / Keep Informed / Monitor | `[Stated / Inferred / Assumed — ...]` | `AUD-001` |

## 2. Actor & User Profiles

| ID | Actor Name | Primary Goal(s) | Usage Context & Frequency | Tech Literacy / Accessibility / Device Constraints | Trust Level & Permission Boundary | Evidence Tag & Source | Upstream IDs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ACT-002` | ... | ... | ... | ... | ... | `[Stated / Inferred / Assumed — ...]` | `ACT-001`, `AUD-002` |

## 3. Roles, Permissions & Decision Rights

| ID | Actor ID | Can View | Can Create / Edit | Can Approve / Administer | Forbidden Actions | Evidence Tag & Source | Upstream IDs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ACT-003` | `ACT-002` | ... | ... | ... | ... | `[Inferred / Assumed — ...]` | `ACT-002` |

## 4. Stage Exit Criteria (Given/When/Then)

- `AC-ACT-001`: Given `<actor>`, When `<action>`, Then `<permission/boundary outcome>`.

## 5. Decision Sheet (Locked)

| Decision ID | Choice | Who Decided | Why | Register ID |
| --- | --- | --- | --- | --- |
| `DEC-003` | ... | `user` / `po` | ... | `r-...` |

## 6. Parked Items & Explicit Non-Goals

| Park ID | Item | Why It Can Wait | Revisit Trigger | Register ID |
| --- | --- | --- | --- | --- |
| `PARK-003` | ... | ... | `<concrete event/metric>` | `r-...` |

## Assumptions and open questions

=== REGISTER REQUESTS ===
None.
=== END REGISTER REQUESTS ===
