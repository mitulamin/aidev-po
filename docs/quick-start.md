---
title: Quick start
---

# Quick start

You need git, Python 3, and an AI coding agent. Cursor is the first-class harness; any harness that reads plain `AGENTS.md` can work too.

## 1. Get aidev-po

```
git clone https://github.com/mitulamin/aidev-po.git
cd aidev-po
```

The generated agents in `.cursor/` are committed, so there is nothing to build to use it. (Only if you change a source in `agents/`, `skills/` or `commands/`, run `python3 scripts/build-agents.py`.)

## 2. Set up your products repo

Your product work does not live in aidev-po. It lives in a **separate git repo that you own, outside the aidev-po checkout, private by default**, one per client or team.

You do not need to do this by hand. The first time you run `po` with nothing configured, it says so and suggests a location: `~/aidev-products`, `~/Documents/aidev-products`, or `../aidev-products` (next to the checkout). You pick one, and `po`:

- with your OK, runs `git init` there with an initial commit (no remote at this point),
- saves the path in `aidev-po.local.json` (gitignored), so it does not ask again,
- then asks once whether you want the repo on GitHub. If you say yes, it creates a **private** repo and pushes with `gh repo create <name> --private --source . --push` (or gives you the manual steps if `gh` is not ready). If you say no, nothing else happens and you can add a remote later with `git remote add origin <url>`.

`AIDEV_PO_PRODUCTS_DIR` overrides the saved path. You can also do the setup yourself with `python3 scripts/products-dir.py --set <path> --init`. Apart from that GitHub yes, `po` never pushes unless you ask. Details, including cloning an existing products repo, are on [Your products repo](products-repo.md).

To see what aidev-po currently finds:

```
python3 scripts/products-dir.py
```

## 3. Talk to `po`

Open the folder in Cursor and run `/po-start`, or tell the agent "act as `po`". In another harness, tell it to follow `AGENTS.md` and act as `po`.

`po` then:

- lists the products in your products repo and asks: continue one, or start a new one;
- for a **new** product, asks for a short slug, creates `<products repo>/<slug>/` and starts at Idea;
- for an **existing** product, catches up first (current stage, register, recent decisions, last run) and tells you where things stand before it helps.

### Commands

Every command starts with `/po-`. Cursor generates one per command source, and each one just asks `po` to do the thing.

| Command | What it does |
|---------|--------------|
| `/po-start` | Start or continue: find the products repo (first-run setup if needed), list products, continue one or start a new one |
| `/po-continue` | Catch up on an existing product (stage, register, decisions, open questions, last run) and resume its current stage |
| `/po-gate` | Run the current stage's reviewer, evidence audit and challenger, then consult you and optionally commit on approval |
| `/po-idea`, `/po-audience`, `/po-actors`, `/po-systems`, `/po-scope`, `/po-workshops`, `/po-presentations`, `/po-fsd` | Run or re-run that stage through `po` |
| `/po-feedback`, `/po-rerun-from`, `/po-retro` | The [learning loop](learning-loop.md): give feedback, rebuild from the traced step, turn findings into reviewed edits |

You can also just talk to `po` in plain words; the commands are shortcuts. In a harness without slash commands, ask `po` for the same thing by name.

## 4. Work through the gates

At every stage gate (`/po-gate` runs it) you see what was produced, what the reviewer found, and the open questions (at most five at a time, each with a recommended answer and a Park option). Approve, answer, send back, or park. See [Method](method.md) and [Stages](stages.md).

## 5. Commits

`po` may commit your product changes at stage gates, once per gate, with a clear message naming the product and stage. It does so **only with your OK each time**. Say no and it leaves the changes for you. It never pushes unless you ask (the one exception is the GitHub yes at setup), and never rewrites history.

## 6. Give feedback

Use `/po-feedback` on anything that is wrong, or comment on the artefact in a pull request. Then `/po-rerun-from` to rebuild from the traced step, and `/po-retro` to turn the findings into reviewed edits. See [Learning loop](learning-loop.md).

## 7. Hand off

When the FSD gate PR is approved, hand it to ai-sdlc-loop as the brief for planning. See [How it fits](how-it-fits.md).

## See a worked example

A fictional demo product will live under [examples/](https://github.com/mitulamin/aidev-po/tree/main/examples) in the aidev-po repo, written for this purpose with nothing confidential in it. It is not a live product and not a real client case. Your own products go in your private products repo, not in `examples/`.

## Not working yet?

Some commands and agents arrive in later pull requests (see the status note on the [home page](index.md)). Until then `po` follows `AGENTS.md`: it finds the products repo, offers init or clone, lists products and consults you at gates.
