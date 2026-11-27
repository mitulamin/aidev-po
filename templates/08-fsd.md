# 08 — Functional Specification Document (FSD): <Product Name>

- **Product slug**: `<slug>`
- **Stage**: `fsd`
- **Standard**: One-Page PRD + ISO/IEC/IEEE 29148 + INVEST/Given-When-Then/EARS + ISO/IEC 25010
- **Status**: `draft` | `gate-approved`
- **Run ID**: `<run-id>`
- **Register**: `.po/register.jsonl`
<!-- TRACE_RESERVE: item_id_prefixes=FSD,US,REQ,NFR,AC; trace_file=.po/traces.jsonl; fields=item_id,run,stage,agent,step,skill_versions,template_versions,upstream_ids,evidence_tag,register_refs -->

---

## Part 0 — One-Page PRD (Executive Summary)

- **Problem (`FSD-001`)**: ... `[Stated / Validated — IDEA-001, AUD-002]`
- **Target Audience & Actors (`FSD-002`)**: ... `[Stated / Inferred — AUD-001, ACT-001]`
- **Desired Outcome & Success Metrics (`FSD-003`)**: ... `[Assumed / Validated — AUD-003]`
- **Solution Summary — Slice 1 Only (`FSD-004`)**: ... `[Inferred — SCP-002]`
- **Explicit Non-Goals (`FSD-005`)**: ... (list `PARK-NNN` with revisit triggers)
- **Key Risks & Dependencies (`FSD-006`)**: ...
- **Locked Decisions Summary (`FSD-007`)**: cite `DEC-001`..`DEC-008`

---

## 1. Purpose & Scope

- **1.1 Product Identification & Purpose (`FSD-008`)**: ...
- **1.2 System Boundaries (`FSD-009`)**: In-scope (Slice 1) vs Out-of-scope (Non-Goals).

## 2. Product Perspective

- **2.1 System Context (`FSD-010`)**: reference `04-systems.md` (`SYS-001`..`SYS-004`).
- **2.2 External Interfaces & Failure Modes (`FSD-011`)**: protocols, auth, timeouts, fallbacks.
- **2.3 Operational & Deployment Constraints (`FSD-012`)**: ...

## 3. User Characteristics & Roles

| Actor ID | Role | Goals & Context | Permissions / Forbidden Actions | Evidence Tag & Source | Upstream IDs |
| --- | --- | --- | --- | --- | --- |
| `ACT-002` | ... | ... | ... | ... | `03-actors.md` |

## 4. Constraints, Assumptions & Dependencies

| ID | Type (`Constraint` / `Assumption` / `Dependency`) | Statement | Register ID | Evidence Tag |
| --- | --- | --- | --- | --- |
| `FSD-013` | ... | ... | `r-...` | `[Stated / Assumed]` |

## 5. Specific Functional Requirements & INVEST User Stories

### 5.1 User Stories (INVEST) & Acceptance Criteria (Given/When/Then)

#### `US-001`: `<Story Title>`
- **Story**: As `<ACT-NNN>`, I want `<capability>`, so that `<outcome>`.
- **Upstream**: `SCP-002`, `SYS-004` | **Evidence**: `[Inferred / Stated — ...]`
- **INVEST check**: Independent / Negotiable / Valuable / Estimable / Small / Testable (`PASS`)
- **Acceptance Criteria**:
  - `AC-001`: Given `<precondition>`, When `<trigger>`, Then `<observable outcome>`.
  - `AC-002`: Given `<invalid/edge state>`, When `<trigger>`, Then `<observable error handling>`.

### 5.2 System & Edge-Case Requirements (EARS)

| ID | EARS Pattern | Requirement (`The system shall ...` / `When ...` / `While ...` / `If ... then ...` / `Where ...`) | Evidence Tag & Source | Upstream IDs |
| --- | --- | --- | --- | --- |
| `REQ-001` | Event-driven | When `<trigger>`, the `<system>` shall `<response>`. | `[Inferred — SYS-004]` | `US-001`, `SYS-004` |
| `REQ-002` | Unwanted behaviour | If `<error/timeout>`, then the `<system>` shall `<safe fallback>`. | `[Inferred — SYS-002]` | `SYS-002` |

### 5.3 Data & Information Requirements

The information the system keeps, receives or sends: what each entity holds, where it comes from, who may see or change it, and how long it is kept. Use the Glossary terms.

| ID | Entity / Information | Key Fields & Meaning | Source & Owner | Access (who reads / writes) | Retention & Deletion | Evidence Tag & Source | Upstream IDs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `FSD-014` | `<entity>` | ... | `<SYS-NNN / ACT-NNN>` | ... | `<period, or N/A — reason>` | `[Stated / Inferred — ...]` | `SYS-...`, `ACT-...` |

## 6. Non-Functional Requirements — ISO/IEC 25010 Quality Matrix

| ID | ISO 25010 Characteristic | Target Metric & Condition (or `N/A — reason`) | Verification Method | Evidence Tag & Source | Upstream IDs |
| --- | --- | --- | --- | --- | --- |
| `NFR-001` | Functional Suitability | ... | ... | ... | ... |
| `NFR-002` | Performance Efficiency | ... | ... | ... | ... |
| `NFR-003` | Compatibility | ... | ... | ... | ... |
| `NFR-004` | Interaction Capability / Usability | ... | ... | ... | ... |
| `NFR-005` | Reliability | ... | ... | ... | ... |
| `NFR-006` | Security | ... | ... | ... | ... |
| `NFR-007` | Maintainability | ... | ... | ... | ... |
| `NFR-008` | Flexibility / Portability | ... | ... | ... | ... |
| `NFR-009` | Safety | `N/A — ...` or target | ... | ... | ... |

## 7. Verification & Traceability Matrix

| Upstream ID | FSD Item (`US` / `REQ` / `NFR`) | Acceptance / Verification (`AC-NNN` / Method) | Evidence Tag |
| --- | --- | --- | --- |
| `SCP-002` | `US-001`, `REQ-001` | `AC-001`, `AC-002` | `[Inferred]` |

## 8. Decision Sheet (Locked)

| Decision ID | Choice | Who Decided | Why | Register ID |
| --- | --- | --- | --- | --- |
| `DEC-008` | ... | `user` / `po` | ... | `r-...` |

## 9. Parked Items & Explicit Non-Goals

| Park ID | Item | Why It Can Wait | Revisit Trigger | Register ID |
| --- | --- | --- | --- | --- |
| `PARK-008` | ... | ... | `<concrete event/metric>` | `r-...` |

## 10. Definitions / Glossary

Pull terms from the Systems stage Glossary & Bounded Contexts (`04-systems.md`), keeping their definitions; add a term only for a word this FSD introduces, and raise a `[QUESTION: ...]` if it conflicts with the Systems glossary.

| ID | Term | Definition | Synonyms to Avoid | Bounded Context | Upstream IDs |
| --- | --- | --- | --- | --- | --- |
| `FSD-015` | ... | ... | ... | ... | `SYS-...` |

## Assumptions and open questions

=== REGISTER REQUESTS ===
None.
=== END REGISTER REQUESTS ===
