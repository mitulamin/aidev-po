---
title: Bootstrap
---

# Bootstrap: put aidev-po in a project

`scripts/bootstrap.sh` installs aidev-po into a project for Cursor. It is the sibling of [ai-sdlc-loop's bootstrap](https://mitulamin.github.io/ai-sdlc-loop/use.html): the same script names, the same environment-variable skip for the questions, the same layout of a `data/harnesses.json` and an `install-harness.py`, and the same promises. It differs in one important way: it can also add aidev-po to a project that already has files, such as one set up with ai-sdlc-loop, without changing any of them.

You do not need it to try aidev-po. Cloning the repo and running `/po-start` in it still works ([Quick start](quick-start.md)). Use bootstrap when you want `po` available inside a project of your own, next to other tools.

## What you need

Python 3 and Git (the script checks and does not install them), and Cursor, signed in. On Windows, use WSL.

## Run it

From inside your checkout of aidev-po:

```
./scripts/bootstrap.sh
```

It asks where the project is, or should be (your home folder, your Documents folder, or the folder next to the checkout), and what the project's folder is called. To skip the questions, give the folder as an argument, or set the environment variables:

```
./scripts/bootstrap.sh ~/work/my-project
AIDEV_PO_BOOTSTRAP_LOCATION=home AIDEV_PO_BOOTSTRAP_NAME=my-project ./scripts/bootstrap.sh
```

`AIDEV_PO_BOOTSTRAP_LOCATION` is `home`, `documents`, `parent` or the full path of an existing folder. For scripting, call the layer underneath directly:

```
scripts/new-project.sh [--harness cursor] [--overlay <dir>] <target-dir>
```

## What it does with the target

It finds out what the target is, and acts on that:

| Target | What happens |
|--------|--------------|
| Does not exist | The folder is created (parents included), `git init` is run (branch `main`, no commits, no remote), and only aidev-po is installed. |
| Exists and is empty | `git init` is run unless it is already a repository, and only aidev-po is installed. |
| Has files | aidev-po is added alongside. No `git init`. Nothing already there is changed, reordered or overwritten. |

It never puts the project inside the aidev-po checkout. It never creates a GitHub repository, adds a remote, commits or pushes.

## What it writes

All of it inside the target, and nothing else:

| Path | What |
|------|------|
| `.cursor/agents/` | `po`, the producers and reviewers, `evidence-auditor`, `challenger`, `tracer`. |
| `.cursor/skills/` | The skills and the `/po-*` commands (Cursor treats commands as skills). |
| `.cursor/rules/aidev-po-bootstrap.mdc` | A short always-on rule that points the agent at `po`. This is aidev-po's registration in Cursor's rules layer. |
| `.aidev-po/scripts/`, `schemas/`, `templates/`, `docs/` | The scripts, schemas and templates the agents run, and two reference pages. The agent and skill files already point at these paths. |
| `.aidev-po/install.json` | The registration manifest: the tool, the aidev-po commit it came from, and every file written with its SHA-256. |
| `.aidev-po/.gitignore` | Keeps `.aidev-po/aidev-po.local.json` (where your products repo is, on this machine) out of the project's git. |

It never writes MCP configuration, hooks, editor or Cursor settings, or `AGENTS.md`, and it never touches `.ai-sdlc/`, including `.ai-sdlc/register.jsonl`.

Two agents are installed under a different name: `learn-producer` and `learn-reviewer` become `po-learn-producer` and `po-learn-reviewer`, because ai-sdlc-loop installs agents with the first two names. The rename is always applied, so that either tool can be installed first.

## How it registers

Registration is a drop-in: aidev-po owns the files above and edits no file it did not create. There is no shared registry file to merge into, so there is nothing of another tool's to overwrite or reorder, and the order of installation does not matter.

Before it writes, it recognises other tools that are already registered, and says so (`Found ai-sdlc-loop already registered here ... Left untouched.`). Two formats are recognised:

- **legacy**: how ai-sdlc-loop registers today. Its always-on rule `.cursor/rules/ai-sdlc-bootstrap.mdc`, its `.ai-sdlc/` folder, or agents carrying its "Installed from ai-sdlc-loop" comment.
- **manifest**: a top-level `.<tool>/install.json` that names its tool. This is the format aidev-po itself uses (`convention: drop-in-registration/1`).

Recognising is for the message and for the tests; the guarantee that nothing of theirs changes comes from what aidev-po writes: only its own files, and it refuses to overwrite any existing file it did not write.

## Running it again

It is idempotent. A file already there with the same bytes is skipped. A file that an earlier aidev-po wrote, and that you have not edited, is updated to the new version; a file an earlier aidev-po wrote that is no longer part of it is removed if unedited. Any other existing file at a path aidev-po wants is a clash: it stops before writing anything and lists the files. Run it twice from the same checkout and the second run changes nothing, not even a modification time.

## Your products are separate

The project you bootstrap is not your products repo. Products live in a separate git repo that you own, outside the project, as before ([Your products repo](products-repo.md)). When installed, `products-dir.py` treats the whole project folder as the checkout it must stay out of: it refuses to record the project, or a folder inside it, as the products repo. The recorded path goes in `.aidev-po/aidev-po.local.json` (gitignored), and `AIDEV_PO_PRODUCTS_DIR` still overrides it. The `../aidev-products` suggestion is next to the project.

## Extension point

`--overlay <dir>` (or `AIDEV_PO_BOOTSTRAP_OVERLAY`) copies the files under `<dir>` into the project as well, never over an existing file or one of aidev-po's own, and lists them in `install.json`. It does nothing unless given. aidev-po knows nothing about what you put there.

## What is not covered

- Harnesses other than Cursor. `data/harnesses.json` has the shape for more; only Cursor's `.cursor/` is generated today.
- `/po-retro` proposes edits to aidev-po itself. In an installed project the copies in `.cursor/` and `.aidev-po/` are not a checkout, so make those edits in your aidev-po checkout and run bootstrap again to update.
- Updating is re-running bootstrap from a newer checkout.
