# templates

Files meant to be copied into your own product folders or config. Everything here is MIT ([LICENSE](LICENSE)).

Every stage template assigns stable IDs (`IDEA-NNN`, `AUD-NNN`, `ACT-NNN`, `SYS-NNN`, `SCP-NNN`, `WKS-NNN`, `PRS-NNN`, `FSD-NNN`, `US-NNN`, `REQ-NNN`, `NFR-NNN`, `AC-NNN`, `DEC-NNN`, `PARK-NNN`) and reserves trace metadata (`TRACE_RESERVE` comments and `Upstream IDs` / `Evidence Tag` columns) for the learning loop.

## Config & state

- `aidev-po.local.example.json`: the shape of `aidev-po.local.json` (gitignored, at the repo root), which records where your products repo is. `po` writes it for you after you pick a location; `python3 scripts/products-dir.py --set PATH` does the same by hand.
- `product-state.example.json`: copy to `<products-repo>/<slug>/.po/state.json` when initialising a new product.

## Stage artefact templates

| Template | Stage | Output file in `<products-repo>/<slug>/` |
| --- | --- | --- |
| [01-idea.md](01-idea.md) | `idea` | `01-idea.md` |
| [02-audience.md](02-audience.md) | `audience` | `02-audience.md` |
| [03-actors.md](03-actors.md) | `actors` | `03-actors.md` |
| [04-systems.md](04-systems.md) | `systems` | `04-systems.md` |
| [05-scope.md](05-scope.md) | `scope` | `05-scope.md` |
| [06-workshops.md](06-workshops.md) | `workshops` | `06-workshops.md` |
| [07-presentations.md](07-presentations.md) | `presentations` | `07-presentations.md` |
| [08-fsd.md](08-fsd.md) | `fsd` | `08-fsd.md` |
| [08-handoff-gate.md](08-handoff-gate.md) | `fsd` (handoff) | `08-handoff-gate.md` |
| [gate-report.md](gate-report.md) | all gates | `.po/runs/<run-id>/gate-<stage>.md` |
