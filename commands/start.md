---
name: start
description: "Start or continue work with po: find the products repo, list products, continue one or start a new one."
---

Act as `po`. Follow `AGENTS.md`, section "What `po` does on every start". Text after the command, if any, names the product to continue or the idea to start.

If no products repo is recorded yet, this command starts the one-time setup: ask where it should live (suggest `~/aidev-products`, `~/Documents/aidev-products` or `../aidev-products`), and with the user's OK run `python3 scripts/products-dir.py --set <path> --init` (plain `git init`, initial commit, no remote). Then ask whether they want it on GitHub: if yes, a private repo (`gh repo create <name> --private --source . --push` when `gh` is ready, otherwise manual steps from `docs/products-repo.md`); if no, they can add a remote later with `git remote add origin <url>`. Never push unless asked. On later runs, use the recorded path without asking again.
