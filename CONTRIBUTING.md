# Contributing

Open a pull request against `main`. Keep changes small and focused, and keep files plain and readable.

## Which licence your contribution is under

By contributing, you agree your contribution is licensed on the same split as the repo. This is not legal advice. The detail is in [NOTICE.md](NOTICE.md).

- Scripts, schemas and workflow tooling are under GPL-3.0 ([LICENSE](LICENSE)).
- Writing is under CC BY-SA 4.0 ([LICENSE-CONTENT](LICENSE-CONTENT)). That covers agent, skill and command sources, docs, examples and the root markdown files.
- Everything under `templates/` is MIT ([templates/LICENSE](templates/LICENSE)).
- Do not add material you cannot license that way. Borrowed files keep their own licence and attribution.

## Products are private by default

Never commit real product work to this repo. Products live in a separate git repo you own, outside this checkout (its path is recorded in the gitignored `aidev-po.local.json`). See [docs/products-repo.md](docs/products-repo.md). The worked example lives in `examples/`, and only an example written for this purpose, with nothing confidential in it, belongs there.

## Generated files

`.cursor/` is generated. Edit the sources in `agents/`, `skills/` and `commands/`, then run:

```
python3 scripts/build-agents.py
```

CI runs `python3 scripts/build-agents.py --check` and fails if a generated file is stale.
