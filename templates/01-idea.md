# 01 — Idea: <Product Name>

- **Product slug**: `<slug>`
- **Stage**: `idea`
- **Status**: `draft` | `gate-approved`
- **Run ID**: `<run-id>`
- **Register**: `.po/register.jsonl`
<!-- TRACE_RESERVE: item_id_prefix=IDEA; trace_file=.po/traces.jsonl; fields=item_id,run,stage,agent,step,skill_versions,template_versions,upstream_ids,evidence_tag,register_refs -->

## 1. Problem Framing & Status Quo

| ID | Statement | Evidence Tag & Source | Upstream IDs |
| --- | --- | --- | --- |
| `IDEA-001` | Core problem observed | `[Stated / Assumed — source or r-...]` | `-` |
| `IDEA-002` | What happens if nothing is built (current manual workaround / cost) | `[Stated / Assumed — source or r-...]` | `IDEA-001` |

## 2. Jobs to Be Done (JTBD) & Mom Test Evidence

| ID | Job Type | When `<situation>`, I want to `<motivation>`, so I can `<outcome>` | Last Real Instance / Past Workaround | Evidence Tag & Source | Upstream IDs |
| --- | --- | --- | --- | --- | --- |
| `IDEA-003` | Functional | ... | ... | `[Stated / Assumed — ...]` | `IDEA-001` |
| `IDEA-004` | Emotional / Social | ... | ... | `[Assumed — r-...]` | `IDEA-003` |

## 3. Lean Canvas

| ID | Box | Content | Evidence Tag & Source | Upstream IDs |
| --- | --- | --- | --- | --- |
| `IDEA-005` | Problem (Top 1-3) & Existing Alternatives | ... | ... | `IDEA-001`, `IDEA-002` |
| `IDEA-006` | Customer Segments & Early Adopters | ... | ... | `IDEA-003` |
| `IDEA-007` | Unique Value Proposition & High-Level Concept | ... | ... | `IDEA-005`, `IDEA-006` |
| `IDEA-008` | Solution (Top 3 Capabilities) | ... | ... | `IDEA-005` |
| `IDEA-009` | Channels | ... | ... | `IDEA-006` |
| `IDEA-010` | Revenue Streams | ... | ... | `IDEA-006` |
| `IDEA-011` | Cost Structure | ... | ... | `IDEA-008` |
| `IDEA-012` | Key Metrics | ... | ... | `IDEA-007` |
| `IDEA-013` | Unfair Advantage | ... | ... | `IDEA-007` |

## 4. Initial Opportunity Solution Tree (Seed)

- **Desired Outcome (`IDEA-014`)**: `<measurable outcome + target>` `[Assumed — r-...]`
  - **Opportunity (`IDEA-015`)**: `<customer pain/need>` `[Stated / Assumed — ...]`
    - **Candidate Solution A (`IDEA-016`)**: ...
    - **Candidate Solution B (`IDEA-017`)**: ...
    - **Assumption Test (`IDEA-018`)**: ...

## 5. Riskiest Assumptions (Top 3)

1. `IDEA-019`: ... (`r-...`)
2. `IDEA-020`: ... (`r-...`)
3. `IDEA-021`: ... (`r-...`)

## 6. Stage Exit Criteria (Given/When/Then)

- `AC-IDEA-001`: Given `<context>`, When `<event>`, Then `<verifiable outcome>`.

## 7. Decision Sheet (Locked)

| Decision ID | Choice | Who Decided | Why | Register ID |
| --- | --- | --- | --- | --- |
| `DEC-001` | ... | `user` / `po` | ... | `r-...` |

## 8. Parked Items & Explicit Non-Goals

| Park ID | Item | Why It Can Wait | Revisit Trigger | Register ID |
| --- | --- | --- | --- | --- |
| `PARK-001` | ... | ... | `<concrete event/metric>` | `r-...` |

## Assumptions and open questions

=== REGISTER REQUESTS ===
None.
=== END REGISTER REQUESTS ===
