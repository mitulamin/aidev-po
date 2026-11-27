# commands

Command sources, one markdown file per command, with `name` and `description` front matter. `scripts/build-agents.py` turns each into a Cursor slash command, `/po-<name>`, that only runs when the user types it.

| Command source | Slash command | Purpose |
| --- | --- | --- |
| [start.md](start.md) | `/po-start` | Start or continue work with `po` (detect/init/clone products repo, list products) |
| [continue.md](continue.md) | `/po-continue` | Catch up on an existing product and resume its current stage |
| [gate.md](gate.md) | `/po-gate` | Run adversarial review, evidence audit, challenger, layered Q&A, and gated commit |
| [idea.md](idea.md) | `/po-idea` | Enter/run the `idea` stage |
| [audience.md](audience.md) | `/po-audience` | Enter/run the `audience` stage |
| [actors.md](actors.md) | `/po-actors` | Enter/run the `actors` stage |
| [systems.md](systems.md) | `/po-systems` | Enter/run the `systems` stage |
| [scope.md](scope.md) | `/po-scope` | Enter/run the `scope` stage |
| [workshops.md](workshops.md) | `/po-workshops` | Enter/run the `workshops` stage |
| [presentations.md](presentations.md) | `/po-presentations` | Enter/run the `presentations` stage |
| [fsd.md](fsd.md) | `/po-fsd` | Enter/run the `fsd` stage and `ai-sdlc-loop` handoff gate |

Learning-loop commands (`/po-feedback`, `/po-rerun-from`, `/po-retro`) arrive in PR 3.
