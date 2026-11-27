---
title: How it fits
---

# How it fits, and where it stops

## The parts around aidev-po

Shravi sells and delivers consulting through a system with three parts.

| Part | What it is |
|------|------------|
| **Governance platform** | The governance side of the system: the rules, approvals and records that apply to the work. |
| **aidev-platform** | A Kubernetes platform with a contract that AI systems use to deploy dev, test and prod apps. |
| **aidev** | The AI software-engineering team in a box. It contains [ai-sdlc-loop](https://github.com/mitulamin/ai-sdlc-loop), the loop that takes a spec through build, verify and ship. |

**aidev-po is a sibling of ai-sdlc-loop, for product definition.** It sits upstream: it turns an idea into an FSD, and the FSD is the input ai-sdlc-loop plans from. The two share a way of working (coordinator, producer plus adversarial reviewer, register, learn loop, same licence split) so they can share tooling and habits.

```
 idea
  |
  v
 aidev-po  --- FSD via gate PR --->  ai-sdlc-loop  --->  built, verified, shipped
 (product definition)                (inside aidev)         |
                                                            v
                                          aidev-platform contract: dev / test / prod
```

### Handoff to ai-sdlc-loop

The FSD is handed over by a gate PR: the FSD goes up for approval by the user, and once approved it becomes the brief for ai-sdlc-loop's planning. aidev-po's job ends at an approved FSD. Acceptance criteria are written as Given/When/Then so ai-sdlc-loop can turn them into tests.

### aidev-platform in the Systems stage

For Shravi client work, the aidev-platform contract is a known external system. It appears on every system context diagram, so the FSD already accounts for how the thing will be deployed.

### Governance

Where the governance platform requires information from a product (for example compliance or data protection decisions), the FSD has a governance and data-protection section to hold it. What exactly the platform requires is not something these docs define.

## What aidev-po does

- Takes a rough idea and finds the problem underneath it.
- Works out the audience, the jobs they are trying to get done, every actor and every stakeholder.
- Maps the product's boundary: external systems, data flows, events, terms.
- Shapes scope: what is in the first release, what is out, and when to revisit.
- Plans workshops and writes up their results, and drafts the narrative (PR/FAQ, memo, decks).
- Writes the FSD, with testable requirements and quality requirements.
- Keeps a register of questions, assumptions and decisions, and tags every item with its evidence.
- Challenges your assumptions, and records it when you overrule.
- Learns from feedback, with a person approving every change.

## What aidev-po does not do

- **It does not build.** No code, no tests, no deployment. That is ai-sdlc-loop and aidev-platform.
- **It does not decide for you.** It recommends and you decide at each gate. It does not advance a stage on its own.
- **It does not replace talking to real people.** It prepares interviews and workshops and writes up the results. Simulated users are labelled Simulated and are never evidence. A need is Validated only when a real person confirmed it.
- **It does not run workshops.** AI plans them, a person runs them.
- **It does not invent facts to fill gaps.** A gap becomes a question.
- **It does not store your product work in this repo.** That lives in your private products repo. See [Your products repo](products-repo.md).
- **It does not push or rewrite history.** It commits at stage gates only with your OK, and never pushes unless asked.
- **It does not set governance policy.** It records what the governance platform requires; it does not define it.
- **It is not a project manager.** No plans, estimates or staffing. Scope uses an appetite you set, not a schedule it invents.
