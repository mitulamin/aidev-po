# 04 — Systems & Domain Flow: <Product Name>

- **Product slug**: `<slug>`
- **Stage**: `systems`
- **Status**: `draft` | `gate-approved`
- **Run ID**: `<run-id>`
- **Register**: `.po/register.jsonl`
<!-- TRACE_RESERVE: item_id_prefix=SYS; trace_file=.po/traces.jsonl; fields=item_id,run,stage,agent,step,skill_versions,template_versions,upstream_ids,evidence_tag,register_refs -->

## 1. C4 Level 1 — System Context

```text
[Actor ACT-002] --(protocol/intent)--> [System Under Design] --(API/protocol)--> [External System]
```

| ID | Element | Type (System / Actor / External System) | Owner | Protocol / Data Exchanged | Trust Boundary & Failure Fallback | Evidence Tag & Source | Upstream IDs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SYS-001` | Core Product System | System | Product Team | ... | ... | `[Inferred — ...]` | `IDEA-008` |
| `SYS-002` | External System X | External System | ... | ... | Timeout / retry / fallback | `[Stated / Assumed — ...]` | `ACT-001` |

## 2. C4 Level 2 — Container Overview (Only If Needed for Scope / Risk)

| ID | Container | Responsibility | Key Interfaces | Evidence Tag & Source | Upstream IDs |
| --- | --- | --- | --- | --- | --- |
| `SYS-003` | `N/A` or Container | ... | ... | ... | `SYS-001` |

## 3. Process EventStorming Flow

| ID | Step | Actor (`ACT-NNN`) | Command (Imperative) | Aggregate / Invariant | Domain Event (Past Tense) | Policy / Reaction | External System | Evidence Tag & Source | Upstream IDs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SYS-004` | 1 | `ACT-002` | `Submit...` | `<invariant>` | `...Submitted` | Whenever `...Submitted`, then `...` | `-` | `[Inferred / Assumed — ...]` | `ACT-002`, `SYS-001` |

## 4. EventStorming Hotspots (Unknowns, Risks, Conflicts)

| ID | Hotspot | Impacted Step / System | Linked Register ID | Upstream IDs |
| --- | --- | --- | --- | --- |
| `SYS-005` | ... | `SYS-004` | `r-...` | `SYS-004` |

## 5. Stage Exit Criteria (Given/When/Then)

- `AC-SYS-001`: Given `<system boundary/event>`, When `<trigger or external failure>`, Then `<observable behaviour>`.

## 6. Decision Sheet (Locked)

| Decision ID | Choice | Who Decided | Why | Register ID |
| --- | --- | --- | --- | --- |
| `DEC-004` | ... | `user` / `po` | ... | `r-...` |

## 7. Parked Items & Explicit Non-Goals

| Park ID | Item | Why It Can Wait | Revisit Trigger | Register ID |
| --- | --- | --- | --- | --- |
| `PARK-004` | ... | ... | `<concrete event/metric>` | `r-...` |

## Assumptions and open questions

=== REGISTER REQUESTS ===
None.
=== END REGISTER REQUESTS ===
