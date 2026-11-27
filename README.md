# aidev-po

![Status: Alpha](https://img.shields.io/badge/status-alpha-FF6B35)

> [!WARNING]
> This project is a work in progress and is considered alpha. It has not been fully tested yet.

aidev-po is a set of agents, skills and commands that take a basic product idea through discovery to a full design specification (FSD). It is the product-definition sibling of [ai-sdlc-loop](https://github.com/mitulamin/ai-sdlc-loop), which takes a spec through build, verify and ship. The FSD hands off to ai-sdlc-loop.

You talk to one agent, `po`. It works through the stages Idea, Audience, Actors, Systems, Scope, Workshops, Presentations and FSD, and consults you at every stage gate.

Browse the docs site: [https://mitulamin.github.io/aidev-po/](https://mitulamin.github.io/aidev-po/) (served from [docs/](docs/) on `main`).

## Status

The repo is built in pull requests: the foundation (licences, scaffold, build script, schemas, products-repo detection) first, then the stage agents and skills, then the learning loop, then the docs, then a worked example. This README and [docs/](docs/) describe how aidev-po is designed to work. Where a page describes behaviour that has not landed yet, treat it as the contract the build follows. The worked example will be a fictional demo in [examples/](examples/), not a real client product.

## What it aims to do

1. Turn a rough idea into a specification a build team (human or AI) can plan from: problem, outcome, audience, actors, systems, scope and non-goals, testable requirements, quality requirements, decisions and open questions.
2. Keep evidence visible. Every item is tagged Stated, Inferred, Assumed, Simulated or Validated, and an item with no evidence is a question, not a fact.
3. Challenge assumptions like a real product owner, and record it when you overrule.
4. Put the human in charge at every gate. `po` recommends; you decide.
5. Learn from every run. Feedback on any output is traced back to where it first went wrong, and becomes a small, tested, human-approved edit.

See [Philosophy](docs/philosophy.md) for the thinking behind this, and [How it fits](docs/how-it-fits.md) for how it relates to aidev, ai-sdlc-loop, aidev-platform and the governance platform, and what it does and does not do.

## How it works

`po` is a coordinator. It does not do the stage work itself: for each stage it starts a producer in a fresh context, then an adversarial reviewer in another, and brings the result to you at the gate with the open questions, at most five at a time, each with a recommended answer and a Park option.

| Stage | Main techniques |
|-------|-----------------|
| Idea | Problem framing, Jobs to be Done and the Mom Test, Lean Canvas, opportunity solution tree |
| Audience | Mom Test evidence log, segments and early adopters, value proposition canvas, validation plan |
| Actors | Power/interest stakeholder map, actor profiles, roles and permissions |
| Systems | C4 context (and containers if needed), integration register, EventStorming flow and hotspots, glossary and bounded contexts |
| Scope | Appetite, impact mapping, story mapping, MoSCoW, non-goals |
| Workshops | Planned by AI, run by a person; synthesis written back to the register |
| Presentations | PR/FAQ, narrative memo, decision-led stakeholder presentation outline |
| FSD | ISO/IEC/IEEE 29148 outline, INVEST, Given/When/Then, EARS, ISO/IEC 25010; handoff by gate PR |

More in [Method](docs/method.md), [Stages](docs/stages.md) and [Learning loop](docs/learning-loop.md). The research behind the choices, with sources, is in [Research](docs/research.md).

## Quick start

```
git clone https://github.com/mitulamin/aidev-po.git
cd aidev-po
```

Open the folder in Cursor and run `/po-start` (every command starts with `/po-`: `/po-continue`, `/po-gate`, `/po-idea` to `/po-fsd`, and `/po-feedback`, `/po-rerun-from`, `/po-retro` for the learning loop), or tell your agent to follow [AGENTS.md](AGENTS.md) and act as `po`. `po` finds your products repo, lists your products, and asks whether to continue one or start a new one. Full steps in [docs/quick-start.md](docs/quick-start.md).

## Your products live in their own repo

Product work does not live here. It lives in a **separate git repo that you own, always outside this checkout, private by default**, one per client or team. There is no default location.

If none is set up, `po` says so and suggests `~/aidev-products`, `~/Documents/aidev-products` or `../aidev-products`. Once you choose, and only with your OK, it runs `git init` with an initial commit (no remote), and saves the path in `aidev-po.local.json` (gitignored). `AIDEV_PO_PRODUCTS_DIR` overrides it. It then asks whether you want the repo on GitHub: if you say yes, it creates a **private** repo with `gh repo create <name> --private --source . --push` (or gives you the manual steps); if you say no, nothing else happens and you can add a remote later. `po` commits at stage gates only with your OK each time, and otherwise pushes only when you ask. Details in [docs/products-repo.md](docs/products-repo.md).

## Layout

| Path | What |
|------|------|
| `agents/`, `skills/`, `commands/` | Sources |
| `.cursor/` | Generated from the sources by `python3 scripts/build-agents.py` |
| `templates/` | Copyable stage and config templates (MIT) |
| `schemas/` | JSON Schemas: register, plus stubs for trace, feedback and scorecard |
| `scripts/` | Tooling |
| `docs/` | The documentation site (GitHub Pages, Markdown) |
| `examples/` | The one worked example, a fictional demo (not live products) |

Your products repo is not part of this checkout.

## Licences

Same split as ai-sdlc-loop. This is not legal advice; the detail is in [NOTICE.md](NOTICE.md).

- Code (`scripts/`, `schemas/`, workflows): GPL-3.0, [LICENSE](LICENSE)
- Writing (agents, skills, commands, docs, examples, root markdown): CC BY-SA 4.0, [LICENSE-CONTENT](LICENSE-CONTENT)
- `templates/`: MIT, [templates/LICENSE](templates/LICENSE)
- Your products repo is yours and is not covered by any of these.

See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute.
