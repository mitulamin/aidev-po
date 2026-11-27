# Your products repo

aidev-po is the tooling. Your product work (ideas, audiences, registers, decisions, workshops, the FSD) lives somewhere else: a **separate git repo that you own, outside the aidev-po checkout, private by default**. This keeps client work out of a public repo and gives it its own history.

One products repo per client or team. Each product is a folder in it:

```
<products repo>/
├── <product-slug>/
│   ├── ...stage files...
│   └── .po/            # register, traces, feedback (shapes in schemas/)
└── <another-product-slug>/
```

There is no default location. You choose one, once.

## First run

When `po` finds no products repo, it asks you to create one or point to an existing one, and suggests three places:

1. `~/aidev-products`
2. `~/Documents/aidev-products`
3. `../aidev-products` (next to your aidev-po checkout)

You can give any other path. Then, **only with your OK**, `po`:

1. Creates the folder if needed and runs a plain `git init` there, with an empty initial commit. **No remote is added.**
2. Records the path (see below).
3. Asks whether you want the repo on GitHub.

Doing it by hand is the same: `python3 scripts/products-dir.py --set ~/aidev-products --init`.

An existing git repo is used as it is: nothing is re-initialised, and no commit is made if it already has any. To use a remote you already have, clone it first, wherever you like, and give `po` that path:

```
git clone git@github.com:your-org/acme-products.git ~/aidev-products
```

## Put it on GitHub (optional)

`po` asks once, right after setup. It never pushes unless you ask.

**Yes.** The repo is created **private**. If the GitHub CLI is installed and signed in (`gh auth status`), `po` runs this in the products folder, after confirming the repo name with you:

```
gh repo create <name> --private --source . --push
```

That creates the private repo, adds it as `origin`, and pushes the initial commit. Otherwise `po` gives you these steps:

1. Create an empty **private** repository on GitHub (no README, no licence, no `.gitignore`).
2. In the products folder:

```
git remote add origin git@github.com:<you>/<name>.git
git push -u origin HEAD
```

**No.** Nothing else happens. You can add a remote any time later:

```
git remote add origin <url>
```

`po` never creates a remote on its own and never makes a public repo.

## Where the path is recorded

First match wins. `python3 scripts/products-dir.py` reports what it found.

1. Environment variable `AIDEV_PO_PRODUCTS_DIR`. It overrides the recorded path, so you can switch clients per shell.
2. `products_dir` in `aidev-po.local.json` at the aidev-po root. This file is gitignored. `po` writes it after you choose; you can also run `python3 scripts/products-dir.py --set PATH` (add `--init` to create the folder and `git init`), or copy `templates/aidev-po.local.example.json`.

After that, `po` uses the recorded path on every run and does not ask again. To move to another products repo, run `--set` with the new path or set the environment variable.

A relative path is resolved from the aidev-po root; `~` is expanded. If the path is inside the aidev-po checkout, add it to `.git/info/exclude`. A path outside needs nothing. `products/` at the root is ignored as a safety net, but it is not a default and is not looked at unless you point to it.

Why not a default inside the checkout? A repo inside a repo is easy to commit by mistake, `git clone` into a non-empty folder fails, and one checkout of aidev-po then ties you to one client. Outside, each products repo stands alone.

## Commits

`po` may commit product changes at stage gates, with a clear message per gate, **only with your OK each time**. It never pushes unless you ask. If you prefer to commit yourself, say no and it will leave the working tree for you.

## Licence

Your products repo is not covered by aidev-po's licences. See [NOTICE.md](../NOTICE.md).
