# templates

Files meant to be copied into your own product folders or config. Everything here is MIT ([LICENSE](LICENSE)).

- `aidev-po.local.example.json`: the shape of `aidev-po.local.json` (gitignored, at the repo root), which records where your products repo is. `po` writes it for you after you pick a location; `python3 scripts/products-dir.py --set PATH` does the same by hand.

Stage templates arrive in a later PR.
