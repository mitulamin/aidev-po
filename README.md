# aidev-po

aidev product owner: market, purpose, design philosophy and scope boundaries.

aidev-po is a set of agents, skills and commands that take a basic product idea through discovery to a full design specification (FSD). It is the product-definition sibling of [ai-sdlc-loop](https://github.com/mitulamin/ai-sdlc-loop), which takes a spec through build, verify and ship. The FSD hands off to ai-sdlc-loop.

You talk to one agent, `po`. It works through the stages Idea, Audience, Actors, Systems, Scope, Workshops, Presentations and FSD, and consults you at every stage gate.

**Status: foundation only.** The repo scaffold, licences, build script and schemas are here. The agents, skills, learning loop, docs and a worked example arrive in follow-up PRs, and this README is rewritten with them.

## Quick look

- [AGENTS.md](AGENTS.md): how `po` behaves, in plain markdown. Cursor reads it automatically.
- [docs/products-repo.md](docs/products-repo.md): your product work lives in a separate private git repo, not here.
- [schemas/](schemas/): the shared register and stubs for scorecard, trace and feedback.
- [examples/](examples/): the worked example (coming).

Docs, method, philosophy and quick start are coming.

## Layout

| Path | What |
|------|------|
| `agents/`, `skills/`, `commands/` | Sources |
| `.cursor/` | Generated from the sources by `python3 scripts/build-agents.py` |
| `templates/`, `schemas/`, `scripts/`, `docs/`, `examples/` | As named |
| (outside this checkout) | Your products repo, set up by `po` on first run |

## Licences

Same split as ai-sdlc-loop. This is not legal advice; the detail is in [NOTICE.md](NOTICE.md).

- Code (`scripts/`, `schemas/`, workflows): GPL-3.0, [LICENSE](LICENSE)
- Writing (agents, skills, commands, docs, examples, root markdown): CC BY-SA 4.0, [LICENSE-CONTENT](LICENSE-CONTENT)
- `templates/`: MIT, [templates/LICENSE](templates/LICENSE)
- Your products repo is yours and is not covered by any of these.

Products are private by default: they live in a separate private git repo you own, outside this checkout, and the path is recorded in a gitignored `aidev-po.local.json`. See [CONTRIBUTING.md](CONTRIBUTING.md).
