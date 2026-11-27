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

- offers to `git init` it and make an initial commit (no remote by default),
- optionally offers a **private** GitHub repo through `gh` (or shows the manual steps), which you can decline and add later with `git remote add origin <url>`,
- saves the path in `aidev-po.local.json` (gitignored), so it does not ask again.

`AIDEV_PO_PRODUCTS_DIR` overrides the saved path. `po` never pushes unless you ask. Details, including cloning an existing products repo, are on [Your products repo](products-repo.md).

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

## 4. Work through the gates

At every stage gate you see what was produced, what the reviewer found, and the open questions (at most five at a time, each with a recommended answer and a Park option). Approve, answer, send back, or park. See [Method](method.md) and [Stages](stages.md).

## 5. Commits

`po` may commit your product changes at stage gates, once per gate, with a clear message naming the product and stage. It does so **only with your OK each time**. Say no and it leaves the changes for you. It never pushes unless you ask, and never rewrites history.

## 6. Give feedback

Use `/feedback` on anything that is wrong, or comment on the artefact in a pull request. Then `/rerun-from` to rebuild from the traced step, and `/retro` to turn the findings into reviewed edits. See [Learning loop](learning-loop.md).

## 7. Hand off

When the FSD gate PR is approved, hand it to ai-sdlc-loop as the brief for planning. See [How it fits](how-it-fits.md).

## See a worked example

A fictional demo product will live under [examples/](https://github.com/mitulamin/aidev-po/tree/main/examples) in the aidev-po repo, written for this purpose with nothing confidential in it. It is not a live product and not a real client case. Your own products go in your private products repo, not in `examples/`.

## Not working yet?

Some commands and agents arrive in later pull requests (see the status note on the [home page](index.md)). Until then `po` follows `AGENTS.md`: it finds the products repo, offers init or clone, lists products and consults you at gates.
