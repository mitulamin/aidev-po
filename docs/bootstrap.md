---
title: Bootstrap
---

# Bootstrap: put aidev-po in a project

`scripts/bootstrap.sh` installs aidev-po into a project for Cursor. It is the sibling of [ai-sdlc-loop's bootstrap](https://mitulamin.github.io/ai-sdlc-loop/use.html): the same script names, the same environment-variable skip for the questions, the same layout of a `data/harnesses.json` and an `install-harness.py`, and the same promises. It differs in one important way: it can also add aidev-po to a project that already has files, such as one set up with ai-sdlc-loop, without changing any of them. It asks before it does that.

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
scripts/new-project.sh [--harness cursor] [--overlay <dir>] [--yes] [--git-init | --no-git-init] <target-dir>
```

`new-project.sh` does not ask questions. A folder that already has files needs `--yes` there too.

## Before it writes

Two checks run on every route: the wizard, a folder argument, the environment variables, and `new-project.sh`. Nothing is written until both have an answer.

**A folder that already has files.** The question is `There are files in <dir>. Are you sure you want me to work in this folder? [y/N]`. Enter or anything other than yes stops, and the folder is unchanged. The wizard asks this only in a terminal, with no folder argument and no `AIDEV_PO_BOOTSTRAP_LOCATION` or `AIDEV_PO_BOOTSTRAP_NAME`. `new-project.sh` asks the same question when it is run in a terminal. Every other run does not ask. Pass `--yes`, or set `AIDEV_PO_BOOTSTRAP_YES` to `1`, `yes` or `true`, or it stops and writes nothing. Answering no stops without writing and exits cleanly.

**A folder that is not a Git repository,** including one that does not exist yet and an empty one. The question is `This folder isn't a Git repository. Initialise one? [Y/n]`. Enter means yes. Yes runs `git init` (branch `main`, no commits, no remote). No leaves the folder without a repository and still installs. A folder that already has its own `.git` is not asked and is not re-initialised. Non-interactive runs do not ask. `--git-init` and `--no-git-init` choose, and so does `AIDEV_PO_BOOTSTRAP_GIT_INIT` (`1` or `0`). If you pass neither, the folder is initialised, the same as answering yes. Pass only one of the two flags. The same names and questions are the ones [ai-sdlc-loop](https://github.com/mitulamin/ai-sdlc-loop/pull/32) uses, with aidev-po's own environment-variable prefix.

## What it does with the target

| Target | What happens |
|--------|--------------|
| Does not exist | The folder is created (parents included). `git init` runs unless you answered no or passed `--no-git-init`. Only aidev-po is installed. |
| Exists and is empty | Same `git init` rule, unless it is already a repository. Only aidev-po is installed. |
| Has files | It stops unless you answered yes or passed `--yes` (or set `AIDEV_PO_BOOTSTRAP_YES`). Then aidev-po is added alongside. Nothing already there is changed, reordered or overwritten. `git init` runs only when the folder is not already a repository and you did not pass `--no-git-init`. |

It never puts the project inside the aidev-po checkout. It never creates a GitHub repository, adds a remote, commits or pushes.

## What it writes

All of it inside the target, as ordinary files. Nothing is a symlink, and the installed text does not point back at the aidev-po checkout to read agents, skills, rules, templates or scripts. A private repository created from the project stands on its own for that.

| Path | What |
|------|------|
| `.cursor/agents/` | `po`, the producers and reviewers, `evidence-auditor`, `challenger`, `tracer`. |
| `.cursor/skills/` | The skills and the `/po-*` commands (Cursor treats commands as skills). |
| `.cursor/rules/aidev-po-bootstrap.mdc` | A short always-on rule that points the agent at `po`. This is aidev-po's registration in Cursor's rules layer. |
| `.aidev-po/scripts/`, `schemas/`, `templates/`, `docs/`, `examples/` | The scripts, schemas, templates and two reference pages the agents run, and the worked example, copied in full. |
| `.aidev-po/LICENSE`, `LICENSE-CONTENT`, `NOTICE.md`, `templates/LICENSE` | The licence texts that already apply to those copies. See [Licences of the copy](#licences-of-the-copy). |
| `.aidev-po/install.json` | The registration manifest: the tool, the aidev-po commit it came from, and every file written with its SHA-256. The commit recorded there is how an installed `traces.py versions` stamps a run. It is not fetched to read the texts. |
| `.aidev-po/.gitignore` | Keeps `.aidev-po/aidev-po.local.json` (where your products repo is, on this machine) out of the project's git. |

It never writes MCP configuration, hooks, editor or Cursor settings, or `AGENTS.md`, and it never touches `.ai-sdlc/`, including `.ai-sdlc/register.jsonl`.

Two agents are installed under a different name: `learn-producer` and `learn-reviewer` become `po-learn-producer` and `po-learn-reviewer`, because ai-sdlc-loop installs agents with the first two names. The rename is always applied, so that either tool can be installed first.

## Licences of the copy

The install does not change any licence. GitHub shows this repository as GPL-3.0 because that is the licence of the code. The files the installer copies are not all under one licence:

| Copied files | Licence |
|--------------|---------|
| `.aidev-po/scripts/`, `.aidev-po/schemas/` | GPL-3.0 ([LICENSE](https://github.com/mitulamin/aidev-po/blob/main/LICENSE) in this repository; the text is copied to `.aidev-po/LICENSE`) |
| `.cursor/agents/`, `.cursor/skills/`, `.aidev-po/docs/`, `.aidev-po/examples/` | CC BY-SA 4.0, copyright Shravi Limited and contributors (copied to `.aidev-po/LICENSE-CONTENT`) |
| `.aidev-po/templates/`, `.cursor/rules/aidev-po-bootstrap.mdc` | MIT (copied to `.aidev-po/templates/LICENSE`) |

`.aidev-po/NOTICE.md` in the project states the same split. Making every copied text MIT would need those files relicensed in aidev-po first. This install does not do that.

## How it registers

Registration is a drop-in: aidev-po owns the files above and edits no file it did not create. There is no shared registry file to merge into, so there is nothing of another tool's to overwrite or reorder, and the order of installation does not matter.

Before it writes, it recognises other tools that are already registered, and says so (`Found ai-sdlc-loop already registered here ... Left untouched.`). Two formats are recognised:

- **legacy**: how ai-sdlc-loop registers today. Its always-on rule `.cursor/rules/ai-sdlc-bootstrap.mdc`, its `.ai-sdlc/` folder, or agents carrying its "Installed from ai-sdlc-loop" comment.
- **manifest**: a top-level `.<tool>/install.json` that names its tool. This is the format aidev-po itself uses (`convention: drop-in-registration/1`).

Recognising is for the message and for the tests; the guarantee that nothing of theirs changes comes from what aidev-po writes: only its own files, and it refuses to overwrite any existing file it did not write.

## Running it again

It is idempotent once the folder is confirmed with `--yes` or the question. A file already there with the same bytes is skipped. A file that an earlier aidev-po wrote, and that you have not edited, is updated to the new version; a file an earlier aidev-po wrote that is no longer part of it is removed if unedited. Any other existing file at a path aidev-po wants is a clash: it stops before writing anything and lists the files.

If you have edited a file aidev-po itself installed, the run stops before writing anything. It says it detected local edits to its own files, lists each edited path, and says it halted rather than overwrite them and that nothing was written. There is no `--force`.

Run it twice from the same checkout, with the folder confirmed the second time, and the second run changes nothing, not even a modification time.

## Your products are separate

The project you bootstrap is not your products repo. Products live in a separate git repo that you own, outside the project, as before ([Your products repo](products-repo.md)). When installed, `products-dir.py` treats the whole project folder as the checkout it must stay out of: it refuses to record the project, or a folder inside it, as the products repo. The recorded path goes in `.aidev-po/aidev-po.local.json` (gitignored), and `AIDEV_PO_PRODUCTS_DIR` still overrides it. The `../aidev-products` suggestion is next to the project.

That pointer is only where your products live. The agent, skill, rule, template and script texts are the copies in the project. The pointer is not used to read them.

A few records still name the aidev-po repository, and none of them is read to load those texts. `.aidev-po/install.json` stores the commit the copy came from, which `traces.py versions` uses as a stamp. Each schema's `$id` stays the identifier it has in aidev-po. `products-dir.py` credits aidev-po in the short README it writes when it creates a products repo. The worked example is copied as it stands, so its ledger still names the pull request where one demo edit landed.

## Extension point

`--overlay <dir>` (or `AIDEV_PO_BOOTSTRAP_OVERLAY`) copies the files under `<dir>` into the project as well, never over an existing file or one of aidev-po's own, and lists them in `install.json`. It does nothing unless given. aidev-po knows nothing about what you put there.

## What is not covered

- Harnesses other than Cursor. `data/harnesses.json` has the shape for more; only Cursor's `.cursor/` is generated today.
- `/po-retro` global edits in an installed project change the copies in `.cursor/` and `.aidev-po/`. They do not open an aidev-po checkout to read those texts. Editing the aidev-po repository itself, and sending a change upstream, is still a separate checkout: run bootstrap again from that checkout to refresh an install.
- Updating is re-running bootstrap from a newer checkout, with the folder confirmed.
