# 07 — Presentations (PR/FAQ & Deck Outline): <Product Name>

- **Product slug**: `<slug>`
- **Stage**: `presentations`
- **Status**: `draft` | `gate-approved`
- **Run ID**: `<run-id>`
- **Register**: `.po/register.jsonl`
<!-- TRACE_RESERVE: item_id_prefix=PRS; trace_file=.po/traces.jsonl; fields=item_id,run,stage,agent,step,skill_versions,template_versions,upstream_ids,evidence_tag,register_refs -->

## 1. Working Backwards Press Release (<= 1 Page)

- **Headline (`PRS-001`)**: `<Target customer> can now <core outcome> without <old pain>` `[Inferred — SCP-002]`
- **Sub-headline (`PRS-002`)**: ...
- **Dateline & Launch Summary (`PRS-003`)**: `<City, Launch Date>` — ... (strictly Slice 1 capabilities only)
- **Problem Paragraph (`PRS-004`)**: ... `[Stated / Validated — AUD-002]`
- **Solution Paragraph (`PRS-005`)**: ... `[Inferred — SCP-002, SYS-001]`
- **Leader Quote (`PRS-006`)**: "..." `[Assumed — r-...]`
- **Customer Quote (`PRS-007`)**: "..." `[Simulated — illustrative launch quote based on IDEA-003; NOT customer validation]`
- **Call to Action (`PRS-008`)**: ...

## 2. Customer / External FAQ

| ID | Question | Answer (Slice 1 Reality Only) | Evidence Tag & Source | Upstream IDs |
| --- | --- | --- | --- | --- |
| `PRS-009` | Who is this for and how do I start? | ... | `[Inferred — AUD-001]` | `AUD-001`, `SCP-002` |
| `PRS-010` | What does it NOT do yet? | ... (cite Explicit Non-Goals) | `[Stated — PARK-005]` | `PARK-005` |

## 3. Internal / Stakeholder FAQ (Hard Questions)

| ID | Hard Question (Economics, Adoption, Ops, Security, Challenger Risks) | Candid Answer | Evidence Tag & Source | Upstream IDs |
| --- | --- | --- | --- | --- |
| `PRS-011` | What happens if nothing is built? | ... | `[Stated / Assumed — IDEA-002]` | `IDEA-002` |
| `PRS-012` | What is the top failure mode and unit-cost/ops risk? | ... | `[Assumed — r-...]` | `SYS-002` |

## 4. Narrative Memo (High-Power Stakeholders)

*Short-form memo for high-power stakeholders (`Manage Closely` / `Keep Satisfied` in `03-actors.md`). Every claim cites a register or artefact ID.*

- **Decision Requested (`PRS-013`)**: `<decision and options>` `[Inferred — DEC-..., SCP-003]`
- **Problem & Cost of Status Quo (`PRS-014`)**: ... `[Stated / Validated — IDEA-001, AUD-002]`
- **Recommended Slice 1 & Appetite (`PRS-015`)**: ... `[Stated / Inferred — SCP-001, SCP-003]`
- **Explicit Non-Goals & Top Risks (`PRS-016`)**: ... `[Stated / Assumed — PARK-005, r-...]`

## 5. Stakeholder Presentation Outline (Tailored to Power/Interest Map)

*Decision-led: one decision per deck, answer first, tailored per audience from the same source material.*

| Slide | Title | Target Audience (`ACT-NNN`) | Decision & Answer-First Key Point | Upstream IDs |
| --- | --- | --- | --- | --- |
| `PRS-017` | 1. Decision & Problem Cost | `ACT-001` | **Answer first**: ... | `IDEA-001`, `AUD-002` |
| `PRS-018` | 2. Target Audience & Stakeholders | `ACT-001` | ... | `AUD-001`, `ACT-001` |
| `PRS-019` | 3. Slice 1 Scope, Appetite & Non-Goals | `ACT-001` | ... | `SCP-001`, `SCP-003`, `PARK-005` |
| `PRS-020` | 4. Risks, Economics & Gate Ask | `ACT-001` | ... | `PRS-012`, `DEC-...` |

## 6. Decision Sheet (Locked)

| Decision ID | Choice | Who Decided | Why | Register ID |
| --- | --- | --- | --- | --- |
| `DEC-007` | ... | `user` / `po` | ... | `r-...` |

## 7. Parked Items & Explicit Non-Goals

| Park ID | Item | Why It Can Wait | Revisit Trigger | Register ID |
| --- | --- | --- | --- | --- |
| `PARK-007` | ... | ... | `<concrete event/metric>` | `r-...` |

## Assumptions and open questions

=== REGISTER REQUESTS ===
None.
=== END REGISTER REQUESTS ===
