---
name: pr-faq-presentations
description: "Use during the Presentations stage to craft a Working Backwards PR/FAQ (Press Release, Customer FAQ, Internal FAQ) and stakeholder presentation outline aligned with locked scope."
licence: CC-BY-SA-4.0
---

# PR/FAQ and Stakeholder Presentations

Test product clarity and narrative coherence from the customer's perspective before writing the full FSD, using Amazon's Working Backwards PR/FAQ plus a tailored stakeholder deck outline.

## When to use

During the `presentations` stage after `scope` and `workshops` are aligned.

## Producer: dos and don'ts

Do:
- Write a crisp **Press Release** (<=1 page, `PRS-NNN`) dated at launch:
  - Headline & sub-headline naming the target customer and core benefit
  - Summary paragraph (what launches, for whom, key outcome)
  - Problem paragraph (grounded in `[Stated]`/`[Validated]` pain, no hype)
  - Solution paragraph (how it works at a high level, bounded to Scope Slice 1)
  - Leader quote (why this matters) and realistic Customer quote (grounded in JTBD, tagged `[Simulated]` as an illustrative launch quote!)
  - Call to Action (how a customer starts)
- Write both **External/Customer FAQ** and **Internal/Stakeholder FAQ**:
  - Address the hardest real objections: pricing/economics, adoption friction, operational burden, security/compliance, technical feasibility, non-goals, and challenger risks
  - Tag every metric, claim, and quote with its evidence tag (marking illustrative Press Release customer quotes explicitly `[Simulated]`)
- Write a **Narrative Memo** for high-power stakeholders (`Manage Closely` / `Keep Satisfied`) and a decision-led **Stakeholder Presentation Outline** (one decision per deck, answer first, tailored per audience from the same source material) mapped to `ACT-NNN`, citing a register or artefact ID for every claim

Don't:
- Promise capabilities in the Press Release that were marked Won't / Non-Goal in `scope`
- Write marketing fluff or hide known risks/trade-offs from the Internal FAQ
- Pass an illustrative Press Release quote off as `[Validated]` customer testimony

## Steps

1. Pull locked scope (Slice 1 Musts + Non-Goals), JTBD, UVP, and workshop outcomes.
2. Draft the 1-page Press Release (tagging the illustrative launch quote `[Simulated]`).
3. Draft Customer FAQ and Internal FAQ tackling challenger risks and open trade-offs.
4. Build the Stakeholder Presentation Outline mapped to high-power/high-interest stakeholders.

## Self-check

- [ ] Is every capability described in the PR/FAQ strictly within Scope Slice 1 and consistent with Non-Goals?
- [ ] Is the illustrative launch quote explicitly tagged `[Simulated]` and every factual claim tagged with its real evidence source?
- [ ] Does the Internal FAQ directly answer the toughest challenger risks, cost/ops questions, and dependencies?

## Adversarial reviewer

- Fail (`P1`) if the PR/FAQ promises any capability excluded in `scope` Non-Goals or Won'ts.
- Fail (`P0`/`P1`) if an illustrative customer quote or projected metric is tagged `[Stated]` or `[Validated]` instead of `[Simulated]`/`[Assumed]`.
- Flag softball Internal FAQs that dodge pricing, adoption risk, compliance, or operational load.
