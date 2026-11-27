# 02 — Audience: <Product Name>

- **Product slug**: `<slug>`
- **Stage**: `audience`
- **Status**: `draft` | `gate-approved`
- **Run ID**: `<run-id>`
- **Register**: `.po/register.jsonl`
<!-- TRACE_RESERVE: item_id_prefix=AUD; trace_file=.po/traces.jsonl; fields=item_id,run,stage,agent,step,skill_versions,template_versions,upstream_ids,evidence_tag,register_refs -->

## 1. Target Segments & Early Adopters

| ID | Segment | Early-Adopter Characteristics | Frequency & Trigger | Current Spend / Cost of Problem | Evidence Tag & Source | Upstream IDs |
| --- | --- | --- | --- | --- | --- | --- |
| `AUD-001` | Primary segment | ... | ... | ... | `[Stated / Assumed — ...]` | `IDEA-006` |

## 2. Mom Test Evidence & Last Real Instance Log

| ID | Segment | Real Past Instance (When / Context / Action Taken) | Current Workaround & Switching Friction | What They Already Tried / Paid For | Evidence Tag & Source | Upstream IDs |
| --- | --- | --- | --- | --- | --- | --- |
| `AUD-002` | `AUD-001` | ... | ... | ... | `[Stated / Validated / Assumed — ...]` | `AUD-001`, `IDEA-003` |

*Note: Any simulated user exploration to spot blind spots MUST be recorded in Section 4 and tagged `[Simulated]` — never here.*

## 3. Expanded Opportunity Solution Tree

- **Desired Outcome (`AUD-003`)**: `<refined measurable outcome>` (upstream: `IDEA-014`)
  - **Opportunity (`AUD-004`)**: `<validated/assumed customer pain>` (upstream: `IDEA-015`)
    - **Sub-opportunity (`AUD-005`)**: ...
      - **Candidate Solution 1 (`AUD-006`)**: ...
      - **Candidate Solution 2 (`AUD-007`)**: ...
      - **Fastest Assumption Test (`AUD-008`)**: ...

## 4. Discovery & Validation Plan (Incl. `[Simulated]` Gap Checks If Used)

| ID | Hypothesis / Gap | Research Method (Mom Test Interview / Observation / Data) | Pass / Falsify Criterion | Tag | Upstream IDs |
| --- | --- | --- | --- | --- | --- |
| `AUD-009` | ... | ... | ... | `[Assumed]` / `[Simulated]` | `AUD-002` |

## 5. Stage Exit Criteria (Given/When/Then)

- `AC-AUD-001`: Given `<segment/evidence>`, When `<check>`, Then `<verifiable outcome>`.

## 6. Decision Sheet (Locked)

| Decision ID | Choice | Who Decided | Why | Register ID |
| --- | --- | --- | --- | --- |
| `DEC-002` | ... | `user` / `po` | ... | `r-...` |

## 7. Parked Items & Explicit Non-Goals

| Park ID | Item | Why It Can Wait | Revisit Trigger | Register ID |
| --- | --- | --- | --- | --- |
| `PARK-002` | ... | ... | `<concrete event/metric>` | `r-...` |

## Assumptions and open questions

=== REGISTER REQUESTS ===
None.
=== END REGISTER REQUESTS ===
