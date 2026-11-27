# commands

Command sources, one markdown file per command, with `name` and `description` front matter. `scripts/build-agents.py` turns each into a Cursor slash command, `/po-<name>`, that only runs when the user types it. More commands arrive in later PRs.
