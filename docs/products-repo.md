# Your products repo

aidev-po is the tooling. Your product work (ideas, audiences, registers, decisions, workshops, the FSD) lives somewhere else: a **separate git repo that you own, private by default**. This keeps client work out of a public repo and gives it its own history.

One products repo per client or team. Each product is a folder in it:

```
<products repo>/
├── <product-slug>/
│   ├── ...stage files...
│   └── .po/            # register, traces, feedback (shapes in schemas/)
└── <another-product-slug>/
```

## Where aidev-po looks

First match wins. `scripts/products-dir.py` reports what it found.

1. Environment variable `AIDEV_PO_PRODUCTS_DIR`
2. `products_dir` in `aidev-po.local.json` at the repo root (gitignored; copy `templates/aidev-po.local.example.json`)
3. `products/` at the repo root (the default)

A relative path is resolved from the aidev-po root; `~` is expanded. The default `products/` is ignored by this repo's `.gitignore`. If you point `products_dir` at another path inside this checkout, add that path to `.git/info/exclude`. A path outside the checkout needs nothing.

## Set it up

Start a new products repo:

```
git init products
```

Or use an existing remote (the target folder must be missing or empty):

```
git clone git@github.com:your-org/your-products.git products
```

Or keep it elsewhere and point at it:

```
git clone git@github.com:your-org/acme-products.git ~/work/acme-products
echo '{ "products_dir": "~/work/acme-products" }' > aidev-po.local.json
```

Create the remote as **private** unless you mean otherwise.

You do not have to run these yourself. When `po` finds no products repo, it offers to run `git init` or a clone for you and waits for your answer.

## Commits

`po` may commit product changes at stage gates, with a clear message per gate, **only with your OK each time**. It never pushes unless you ask. If you prefer to commit yourself, say no and it will leave the working tree for you.

## Why `products/` has no README

`git clone` needs an empty or missing target folder, so no file is tracked under `products/` in aidev-po. This page is the mount note.

## Licence

Your products repo is not covered by aidev-po's licences. See [NOTICE.md](../NOTICE.md).
