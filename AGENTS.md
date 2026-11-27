# AGENTS.md

aidev-po takes a basic product idea through discovery to a full design specification (FSD) that hands off to [ai-sdlc-loop](https://github.com/mitulamin/ai-sdlc-loop). You talk to one agent: `po`.

This file is the plain-markdown entry point. Cursor reads it as an always-on rules file. Other harnesses can read it directly. Agent, skill and command sources live in this repo; Cursor loads the copies `python3 scripts/build-agents.py` writes under `.cursor/`.

## Talk to `po`

`po` is the coordinator. Its source is [agents/po.md](agents/po.md); Cursor loads the generated copy in `.cursor/agents/`. Start with `/po-start`, or just tell the agent to act as `po`.

## Stages

Every product moves through the same stages, in order:

Idea -> Audience -> Actors -> Systems -> Scope -> Workshops -> Presentations -> FSD

Each stage has a producer and an adversarial reviewer, each in a fresh context.

## Commands and agents

Commands are typed as `/po-<name>`; their sources are in `commands/`. `scripts/build-agents.py` turns each into `.cursor/skills/po-<name>/SKILL.md`, which Cursor runs only when the user types that command.

| Command | What it does |
|---------|--------------|
| `/po-start` | Find the products repo, list the products, continue one or start a new one. |
| `/po-continue` | Catch up on a product: current stage, register, last run, open feedback. |
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

1. **Find the products repo.** Run `python3 scripts/products-dir.py` (`po` uses `--json`). Products live in a separate git repo that the user owns, **outside the aidev-po checkout**, private by default, one per client or team. There is no default location, and no in-repo `products/` folder. The path is read from `AIDEV_PO_PRODUCTS_DIR` (overrides) or `products_dir` in the gitignored `aidev-po.local.json`. See [docs/products-repo.md](docs/products-repo.md).
2. **If the state is `unconfigured`** (no path recorded), ask the user to create a products repo or point to an existing one, and suggest three locations: `~/aidev-products`, `~/Documents/aidev-products`, or `../aidev-products` (next to this checkout). Any other path is fine. Do nothing on disk until the user says OK. Then:
   1. For a new or existing local folder, run `python3 scripts/products-dir.py --set <path> --init`. This creates the folder if needed, runs plain `git init` if it is not a git repo, makes an initial commit with a short `README.md` and `.gitignore`, and records the path in `aidev-po.local.json`. **No remote is added.** An existing git repo is used as it is. It refuses any path inside the aidev-po checkout. If git `user.name` or `user.email` is not set it stops without recording anything; `po` tells the user to run `git config --global user.name "Their Name"` and `git config --global user.email "them@example.com"`, then tries again.
   2. To use a private remote they already have, clone it (`git clone <url> <path>`) and record that path with `python3 scripts/products-dir.py --set <path>` (no `--init`).
   3. After a local init, ask whether they want it on GitHub.
   4. If yes, create a **private** repo. If the report shows `gh: ready`, confirm the repo name and run `gh repo create <name> --private --source . --push` in the products folder. Otherwise give the manual steps in [docs/products-repo.md](docs/products-repo.md). Never create a public repo.
   5. If no, say a remote can be added later with `git remote add origin <url>`.
   6. Never push unless the user asked.
   From then on use the recorded path every run and do not ask again.
   If the state is `missing`, `empty` or `not-git` for a recorded path, tell the user and offer the same `--init` step (or a clone into that path); never guess a different path.
3. **List the products** in that repo (one folder each) and ask: continue one, or start a new one. The repo is ready when the state is `git-local` or `git-remote`.
4. **New product:** ask for a short lowercase slug, create `<products repo>/<slug>/` and `<products repo>/<slug>/.po/`, triage depth (thin pass + one-page PRD, or full FSD) and let the user override it, copy `templates/product-state.example.json` to `.po/state.json` with `current_stage` set to `idea` and `depth` set to `thin` or `full`, and start at Idea. Every producer and reviewer brief states the depth.
5. **Existing product:** catch up before helping. Read `.po/state.json` (depth, current stage, completed stages, last run), the register (open questions, assumptions, decisions), the latest gate report, and open feedback, waiting attributions and unfinished reruns (`python3 scripts/traces.py open-feedback --catch-up --product <slug>`), and tell the user where things stand. Then work on the current stage.

## Stage gates

The user is consulted at every stage gate. `po` never advances a stage on its own.

- At each gate `po` shows what the stage produced, the reviewer's findings, the `evidence-auditor` and `challenger` results, and the open register items, each open question with a recommended answer.
- `python3 scripts/traces.py check --product <slug>` must pass before the gate. Errors go back to the producer; warnings are shown at the gate.
- The user approves, answers, sends it back, or parks items.
- Questions are asked in small batches (at most five), with a recommendation and a Park option.
- Assumptions, open questions and decisions go into the shared register (see [schemas/](schemas/)).

## Committing product changes

The products repo is the user's, and `po` treats it that way.

- `po` may commit at stage gates, once per gate, with a clear message that names the product and the stage and says what changed. It shows the changed files and the proposed message first.
- `po` commits **only with the user's OK each time**. If the user says no, it leaves the changes uncommitted.
- `po` never pushes unless asked, never rewrites history, and never commits product files into aidev-po. The setup commit in step 2 above is the only commit `po` makes without a stage gate, and only with the user's OK.
- An accepted `/po-retro` edit to aidev-po itself is a separate change, on a new branch, and only with the user's OK to commit. Client words and product names stay out of that commit.

## Repo map

| Path | What |
|------|------|
| `agents/` | Agent sources. Edit these. `po`, one producer and one reviewer per stage, plus `evidence-auditor`, `challenger`, `tracer`, `learn-producer` and `learn-reviewer`. |
| `skills/` | Skill sources, one `skills/<name>/SKILL.md` each: shared skills, stage skills, and the learning-loop skills (`trace-records`, `feedback-intake`, `learning-loop`, `learn-edits`). Edit these. |
| `commands/` | Command sources: `start`, `continue`, the eight stages, `gate`, `feedback`, `rerun-from`, `retro`. Edit these. |
| `.cursor/` | Generated by `python3 scripts/build-agents.py`. Agents go to `.cursor/agents/`. Skills and `/po-*` commands go to `.cursor/skills/` (`po-<name>/SKILL.md` for a command). Do not edit. |
| `templates/` | Copyable files (MIT): stage artefacts `01-idea.md` through `08-fsd.md`, `08-handoff-gate.md`, `gate-report.md`, `product-state.example.json`, `aidev-po.local.example.json`, and learning-loop formats in `templates/learning/`. |
| `schemas/` | JSON Schemas, all draft: `register`, `trace`, `feedback`, `attribution`, `rerun`, `ledger`, `scorecard`, `product-state`. |
| `scripts/` | `build-agents.py`, `products-dir.py`, `register.py`, `traces.py`, `scorecard.py`, `check-schemas.py`. |
| `tests/` | Tests for the scripts, and a fictional fixture products repo at `tests/fixtures/products-repo/`. `python3 -m unittest discover -s tests -t tests` |
| `docs/` | Documentation site (Markdown, GitHub Pages from `/docs`): philosophy, how it fits, method, stages, learning loop, products repo, quick start, research. |
| `examples/` | One worked example, laid out as a products repo: `examples/tool-library-loans/` and `examples/.po/` (ledger, scorecard, preferences, one retro). CI checks its traces, register and scorecard. Not live products. |
| `LICENSE`, `LICENSE-CONTENT`, `templates/LICENSE`, `NOTICE.md` | GPL-3.0 for `scripts/`, `schemas/`, `tests/` and `.github/workflows/`; CC BY-SA 4.0 for writing, including generated `.cursor/` files; MIT for `templates/`. |
| (outside this checkout) | The user's products repo. `python3 scripts/products-dir.py` reads `AIDEV_PO_PRODUCTS_DIR`, otherwise `products_dir` in gitignored `aidev-po.local.json`. There is no default path in this checkout. `.gitignore` ignores `/products/` and `/aidev-po.local.json`; `/products/` is only a safety net. |

## Learning loop

Every output item (a requirement, an actor row, a slide, an agenda item) gets a stable ID such as `ACT-007` and a trace line in `<product>/.po/traces.jsonl`, declared by the agent as it writes (skill `trace-records`). Feedback on any item can then be walked back to the step where it went wrong.

- `/po-feedback`: record feedback (severity P0 to P3, one of nine what's-wrong categories), from chat or pull request comments in the products repo, and trace it with the `tracer`.
- `/po-rerun-from`: rebuild from the traced step, after showing what is invalidated and getting the user's OK.
- Feedback left untraced at `/po-feedback` is traced at the start of `/po-retro`, with the user's OK, so nothing is skipped.
- `/po-retro`: turn traced feedback into small, tested edits the user approves (`learn-producer`, `learn-reviewer`), logged in the ledger, and update the scorecard.
- On catch-up, `po` also reports open feedback, attributions waiting on the user, and reruns that are not done.

`po` follows skill `learning-loop` (`skills/learning-loop/SKILL.md`) on every run. Tools: `scripts/traces.py` and `scripts/scorecard.py`; formats in `schemas/` and `templates/learning/`.

## Rules for agents

- Keep files plain and readable.
- Tag every claim with where it came from, using the tags in [skills/evidence-tags](skills/evidence-tags/SKILL.md): `Stated`, `Inferred`, `Assumed`, `Simulated`, `Validated`. An item with no evidence is a question, not a fact.
- Never edit generated files. Edit the source under `agents/`, `skills/` or `commands/` and run `python3 scripts/build-agents.py`.
- Licences: scripts, schemas and tests GPL-3.0, writing CC BY-SA 4.0, `templates/` MIT. See [NOTICE.md](NOTICE.md).
