# AGENTS.md

aidev-po takes a basic product idea through discovery to a full design specification (FSD) that hands off to [ai-sdlc-loop](https://github.com/mitulamin/ai-sdlc-loop). You talk to one agent: `po`.

This file is the plain-markdown entry point. Cursor reads it as an always-on rules file. Other harnesses can read it directly. Skeleton only: the full agent, skill and command bodies arrive in later PRs, so treat anything marked "(later PR)" as a contract, not a feature that exists yet.

## Talk to `po`

`po` is the coordinator. Its source is [agents/po.md](agents/po.md); Cursor loads the generated copy in `.cursor/agents/`. Start with `/po-start`, or just tell the agent to act as `po`.

## Stages

Every product moves through the same stages, in order:

Idea -> Audience -> Actors -> Systems -> Scope -> Workshops -> Presentations -> FSD

Each stage has a producer and an adversarial reviewer, each in a fresh context.

## Commands and agents

Commands are typed as `/po-<name>`; their sources are in `commands/`.

| Command | What it does |
|---------|--------------|
| `/po-start` | Find the products repo, list the products, continue one or start a new one. |
| `/po-continue` | Catch up on a product: current stage, register, last run. |
| `/po-idea`, `/po-audience`, `/po-actors`, `/po-systems`, `/po-scope`, `/po-workshops`, `/po-presentations`, `/po-fsd` | Run that stage. |
| `/po-gate` | Take the current stage through its gate with the user. |
| `/po-feedback` | Learning loop: record feedback (P0 to P3, nine categories) from chat or pull request comments, and trace it with the `tracer`. |
| `/po-rerun-from` | Learning loop: rebuild from the traced step, after showing what is invalidated and getting the user's OK. |
| `/po-retro` | Learning loop: trace any still-untraced feedback (with the user's OK), then turn it into small, tested edits the user approves; ledger and scorecard. |

Agents' sources are in `agents/`. `po` starts every agent except itself in a fresh context.

| Agent | Role |
|-------|------|
| `po` | Coordinator, and the only agent the user talks to. |
| `<stage>-producer`, `<stage>-reviewer` | One pair per stage, for example `actors-producer` and `actors-reviewer`. |
| `evidence-auditor` | Checks each item's evidence tag and source before the gate. |
| `challenger` | Product-owner pushback before the gate. |
| `tracer` | Learning loop: walks a piece of feedback back to the step where the error began. |
| `learn-producer` | Learning loop: proposes small edits to one surface each at `/po-retro`. |
| `learn-reviewer` | Learning loop: reviews those edits adversarially, with held-out cases. |

## What `po` does on every start

1. **Find the products repo.** Run `python3 scripts/products-dir.py`. Products live in a separate git repo that the user owns, **outside the aidev-po checkout**, private by default, one per client or team. There is no default location. The path is read from `AIDEV_PO_PRODUCTS_DIR` (overrides) or `products_dir` in the gitignored `aidev-po.local.json`. See [docs/products-repo.md](docs/products-repo.md).
2. **If the state is `unconfigured`** (no path recorded), ask the user to create a products repo or point to an existing one, and suggest three locations: `~/aidev-products`, `~/Documents/aidev-products`, or `../aidev-products` (next to this checkout). Any other path is fine. Do nothing on disk until the user says OK. Then:
   1. Run `python3 scripts/products-dir.py --set <path> --init`. This creates the folder if needed, runs plain `git init` with an initial commit if it is not a git repo, and records the path in `aidev-po.local.json`. **No remote is added.** An existing git repo is used as it is.
   2. Ask whether they want it on GitHub.
   3. If yes, create a **private** repo. If the report shows `gh: ready`, confirm the repo name and run `gh repo create <name> --private --source . --push` in the products folder. Otherwise give the manual steps in [docs/products-repo.md](docs/products-repo.md). Never create a public repo.
   4. If no, say a remote can be added later with `git remote add origin <url>`.
   5. Never push unless the user asked.
   From then on use the recorded path every run and do not ask again.
   If the state is `missing`, `empty` or `not-git` for a recorded path, tell the user and offer the same `--init` step for that path; never guess a different path.
3. **List the products** in that repo (one folder each) and ask: continue one, or start a new one.
4. **New product:** ask for a slug, create `<products repo>/<slug>/`, start at Idea.
5. **Existing product:** catch up before helping. Read the current stage, the register (open questions, assumptions, decisions), recent decisions and the last run, and tell the user where things stand. Then work on the current stage.

## Stage gates

The user is consulted at every stage gate. `po` never advances a stage on its own.

- At each gate `po` shows what the stage produced, the reviewer's findings, and the open register items, each open question with a recommended answer.
- The user approves, answers, sends it back, or parks items.
- Questions are asked in small batches (at most five), with a recommendation and a Park option.
- Assumptions, open questions and decisions go into the shared register (see [schemas/](schemas/)).

## Committing product changes

The products repo is the user's, and `po` treats it that way. (Behaviour arrives in a later PR; this is the contract.)

- `po` may commit at stage gates, once per gate, with a clear message that names the product and the stage and says what changed.
- `po` commits **only with the user's OK each time**. If the user says no, it leaves the changes uncommitted.
- `po` never pushes unless asked, never rewrites history, and never commits to aidev-po for product work. The setup commit in step 2 above is the only commit `po` makes without a stage gate, and only with the user's OK.

## Repo map

| Path | What |
|------|------|
| `agents/`, `skills/`, `commands/` | Sources. Edit these. |
| `.cursor/` | Generated by `python3 scripts/build-agents.py`. Do not edit. |
| `templates/` | Copyable stage and config templates (MIT). |
| `schemas/` | JSON Schemas, all draft: the register, plus trace, feedback, attribution, rerun, ledger and scorecard for the learning loop (`/po-feedback`, `/po-rerun-from`, `/po-retro`; agents `tracer`, `learn-producer`, `learn-reviewer`). |
| `scripts/` | Tooling. `build-agents.py`, `products-dir.py`, `register.py`, `traces.py`, `scorecard.py`. |
| `tests/` | Tests for the scripts, with a fictional fixture products repo. `python3 -m unittest discover -s tests -t tests` |
| `docs/` | Documentation site (Markdown, served by GitHub Pages from `/docs`). |
| `examples/` | The one worked example, a fictional products repo (`examples/tool-library-loans/`); CI checks it. Not live products. |
| (outside this checkout) | Your products repo. Its path is recorded in `aidev-po.local.json`. |

<!-- extension point: learning loop (PR 3) -->
## Learning loop

Every output item (a requirement, an actor row, a slide, an agenda item) gets a stable ID such as `ACT-007` and a trace line in `<product>/.po/traces.jsonl`, declared by the agent as it writes (skill `trace-records`). Feedback on any item can then be walked back to the step where it went wrong.

- `/po-feedback`: record feedback (severity P0 to P3, one of nine what's-wrong categories), from chat or pull request comments in the products repo, and trace it with the `tracer`.
- `/po-rerun-from`: rebuild from the traced step, after showing what is invalidated and getting the user's OK.
- Feedback left untraced at `/po-feedback` is traced at the start of `/po-retro`, with the user's OK, so nothing is skipped.
- `/po-retro`: turn traced feedback into small, tested edits the user approves (`learn-producer`, `learn-reviewer`), logged in the ledger, and update the scorecard.

`po` follows skill `learning-loop`. Tools: `scripts/traces.py` and `scripts/scorecard.py`; formats in `schemas/`.
<!-- end extension point: learning loop -->

## Rules for agents

- Keep files plain and readable.
- Tag every claim with where it came from. An item with no evidence is a question, not a fact (later PR defines the tags).
- Never edit generated files. Edit the source and run the build.
- Licences: scripts and schemas GPL-3.0, writing CC BY-SA 4.0, `templates/` MIT. See [NOTICE.md](NOTICE.md).
