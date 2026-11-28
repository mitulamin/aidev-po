---
name: ai-sdlc-loop-handoff
description: "Use at the end of the FSD stage to prepare the gate PR / handoff brief package so ai-sdlc-loop's coordinator can ingest the specification cold via /plan."
licence: CC-BY-SA-4.0
---

# Handoff to ai-sdlc-loop via Gate PR

Package the approved FSD, locked decisions, numbered Given/When/Then criteria, and EARS/NFR rules into a clean handoff brief and gate PR checklist for `ai-sdlc-loop`'s coordinator.

## When to use

At the final phase of the `fsd` stage, once `08-fsd.md` passes review and is ready for the FSD stage gate and handoff to engineering.

## Producer: dos and don'ts

Do:
- Create `08-handoff-gate.md` (`HND-NNN`) in the product folder as the self-contained entry brief for `ai-sdlc-loop` `/plan`
- Verify and include:
  - Exact link/path to `08-fsd.md` and upstream artefacts
  - Goal & One-Page PRD summary (Scope Slice 1 only)
  - Complete **Locked Decisions** table (`DEC-NNN`, register ID `r-...`, choice, rationale) — zero silent changes allowed downstream
  - Complete list of **Explicit Non-Goals** (`PARK-NNN` / `NG-NNN`) with revisit triggers so engineering does not accidentally build them
  - Numbered `AC-NNN` (`Given/When/Then`), `REQ-NNN` (EARS), and `NFR-NNN` (ISO 25010) summary/index for `ai-sdlc-loop`'s `1.2 spec-before-code` and `1.7 verifiable-goals`
  - **Gate PR checklist** for handing off into the target implementation repo (if a target engineering repo exists: propose opening a handoff PR into `docs/fsd/` or `specs/` there ONLY with user OK; otherwise prepare the gate bundle in the products repo for the user to link/open)
  - A copy of `.po/register.jsonl` in the gate bundle (for example `docs/fsd/<slug>/register.jsonl`), and the exact command to start planning with it: `/plan <bundle>/08-handoff-gate.md --register <bundle>/register.jsonl`. `--register` makes ai-sdlc-loop's coordinator read the locked decisions (entries of type `decision`, status `decided`), answers and open items from it and write its own entries there. Both tools use one register taxonomy (DEC-002 in `docs/decisions.md`), so the copy passes ai-sdlc-loop's checker and its entries pass aidev-po's. Pass the copy, never the product's own register: the bundle may live in an engineering repo, and the products repo stays private
- The way back: after an ai-sdlc-loop run, `po` merges the bundle's register into the product with `python3 scripts/register.py merge --from <bundle>/register.jsonl --register <product>/.po/register.jsonl`. Engineering's entries keep their ai-sdlc-loop `phase` (`Plan`, `Design`, ... or `all`); `po` shows them at catch-up and the user decides which are feedback (`/po-feedback`)
- Check `.po/register.jsonl` before handoff: zero unresolved P0/P1 findings, zero open blockers, and zero high-urgency open questions remain

Don't:
- Hand off with open blockers, unresolved `urgency: "high"` open questions, or failing `fsd-reviewer` / `evidence-auditor` verdicts
- Write register lines in a private shape for the bundle: the copy is the product register as it is, and must pass `scripts/register.py check` in both repos
- Push or open a PR in any external implementation repo without explicit user approval
- Omit Non-Goals or Locked Decisions (which causes `ai-sdlc-loop` to re-invent or violate product boundaries)

## Steps

1. Verify `08-fsd.md` passed `fsd-reviewer`, `evidence-auditor`, and `challenger` gate checks, and `.po/register.jsonl` has no open blockers and no unresolved high-urgency questions.
2. Generate `08-handoff-gate.md` from `templates/08-handoff-gate.md`.
3. Present the handoff package and Gate PR option to the user at the FSD gate (`po` asks user OK before creating/pushing any gate PR or committing).

## Self-check

- [ ] Are zero open blockers, zero high-urgency open questions and zero unresolved P0/P1 findings left in `.po/register.jsonl` / `08-fsd.md`?
- [ ] Does the bundle's register copy pass `python3 scripts/register.py check`?
- [ ] Does `08-handoff-gate.md` give `ai-sdlc-loop` everything needed for `/plan` cold (Goal, Slice 1, Locked Decisions, Non-Goals, numbered `AC-NNN` Given/When/Then, `REQ-NNN`, `NFR-NNN`)?
- [ ] Is the Gate PR action gated on explicit user OK?

## Adversarial reviewer

- Fail (`P0`/`P1`) if any open blocker or `urgency: "high"` open question in `.po/register.jsonl` remains unresolved at handoff.
- Fail (`P1`) if `08-handoff-gate.md` omits Locked Decisions, Explicit Non-Goals, or numbered `Given/When/Then` criteria.
- Fail (`P2`) if the `/plan` command in `08-handoff-gate.md` has no `--register` pointing at the register copy in the bundle, or points at the product's own `.po/register.jsonl`.
- Fail (`P1`) if any handoff claim contradicts `08-fsd.md` or `05-scope.md`.
