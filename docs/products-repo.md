---
title: Your products repo
---

# Your products repo

aidev-po is the tooling. Your product work (ideas, audiences, registers, decisions, workshops, the FSD) lives somewhere else: a **separate git repo that you own, always outside the aidev-po checkout, private by default**. This keeps client work out of a public repo and gives it its own history.

One products repo per client or team. Each product is a folder in it:

```
<products repo>/
├── <product-slug>/
│   ├── ...stage files...
│   └── .po/            # register, traces, feedback (shapes in schemas/)
└── <another-product-slug>/
```

aidev-po has no default location inside its own checkout, and nothing under it is ever committed to aidev-po. The only worked example, a fictional demo, lives in `examples/` in aidev-po and is not a live product.

## Where aidev-po looks

First match wins.

1. Environment variable `AIDEV_PO_PRODUCTS_DIR`. It overrides everything else.
2. `products_dir` in `aidev-po.local.json` at the aidev-po root. This file is gitignored and is where `po` remembers your choice. You can write it yourself (copy `templates/aidev-po.local.example.json`).
3. Nothing set. `po` asks you to choose a location (below).

A relative path is resolved from the aidev-po root; `~` is expanded.

## When nothing is set

`po` says so and suggests one of three locations, and you pick one or give your own:

| Suggestion | Meaning |
|------------|---------|
| `~/aidev-products` | In your home folder |
| `~/Documents/aidev-products` | In your Documents folder |
| `../aidev-products` | Next to your aidev-po checkout |

Once you choose, `po` saves the path as `products_dir` in `aidev-po.local.json`, so it does not ask again. Set `AIDEV_PO_PRODUCTS_DIR` if you want a different path for one shell or machine.

## Set it up

`po` offers each step and waits for your answer. You can also do it yourself.

### New products repo (the default)

At the chosen path, `po` offers to:

1. `git init` a new repo, and
2. make an initial commit,

and that is all. **No remote is created by default.** The repo is local until you decide otherwise.

By hand:

```
git init ~/aidev-products
cd ~/aidev-products
git commit --allow-empty -m "Initial commit"
```

### Optional: a private GitHub remote

`po` then asks whether you want a private GitHub repo for it. If you say yes and the GitHub CLI (`gh`) is installed and signed in, `po` can create it as **private**:

```
gh repo create your-org/acme-products --private --source ~/aidev-products --remote origin
```

That creates the repo and adds the `origin` remote. It does not push. (Do not add `--push` unless you want that.) It is never created public.

No `gh`, or you prefer the website? Create an empty **private** repo yourself, then:

```
git -C ~/aidev-products remote add origin git@github.com:your-org/acme-products.git
```

### If you decline, add a remote later

Saying no is fine. Whenever you want a remote, create a private repo and run the `git remote add origin ...` line above. Nothing else changes.

### Pushing

**`po` never pushes unless you ask.** Creating a remote and pushing are separate steps. When you want to push, ask `po` or run `git push -u origin HEAD` yourself.

### Existing remote

If the products repo already exists elsewhere, clone it into a missing or empty folder instead of starting a new one:

```
git clone git@github.com:your-org/acme-products.git ~/aidev-products
```

`po` offers this too and asks for the URL. Then, as above, `po` records the path in `aidev-po.local.json`.

## Commits

After the initial commit, `po` may commit product changes at stage gates, once per gate, with a clear message that names the product and stage, **only with your OK each time**. If you prefer to commit yourself, say no and it leaves the working tree for you. It never rewrites history and never commits product work to aidev-po.

## Licence

Your products repo is not covered by aidev-po's licences. See [NOTICE.md](https://github.com/mitulamin/aidev-po/blob/main/NOTICE.md).
