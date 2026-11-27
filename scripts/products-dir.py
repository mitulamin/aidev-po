#!/usr/bin/env python3
"""Find the products repo and report its state, so `po` can decide what to offer.

Usage:
  scripts/products-dir.py          print the state as key: value lines
  scripts/products-dir.py --json   print the state as JSON

Standard library only. Where the products repo lives, first match wins:

  1. the AIDEV_PO_PRODUCTS_DIR environment variable
  2. "products_dir" in aidev-po.local.json at the repo root (gitignored)
  3. products/ at the repo root (the default)

A relative path is resolved from the repo root; ~ is expanded. The path is a separate git
repo that the user owns, one per client or team. See docs/products-repo.md.

state is one of:
  missing      the path does not exist
  empty        the path exists and has no files
  not-git      the path has files but is not a git repo
  git-local    a git repo with no remote
  git-remote   a git repo with at least one remote

Exit code is 0 whenever the state was read, whatever the state is.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_VAR = "AIDEV_PO_PRODUCTS_DIR"
CONFIG = ROOT / "aidev-po.local.json"
DEFAULT = "products"


def resolve():
    if os.environ.get(ENV_VAR):
        return os.environ[ENV_VAR], f"env {ENV_VAR}"
    if CONFIG.exists():
        try:
            value = json.loads(CONFIG.read_text(encoding="utf-8")).get("products_dir")
        except (json.JSONDecodeError, OSError) as e:
            raise SystemExit(f"{CONFIG.name}: cannot read ({e})")
        if value:
            return value, CONFIG.name
    return DEFAULT, "default"


def git(path, *args):
    return subprocess.run(["git", "-C", str(path), *args], capture_output=True, text=True)


def inspect():
    raw, source = resolve()
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = ROOT / path
    state, remotes, branch, dirty = "missing", [], None, None
    if path.is_dir():
        entries = [p for p in path.iterdir() if p.name != ".DS_Store"]
        top = git(path, "rev-parse", "--show-toplevel")
        is_repo = top.returncode == 0 and Path(top.stdout.strip()).resolve() == path.resolve()
        if is_repo:
            remotes = git(path, "remote", "-v").stdout.splitlines()
            remotes = sorted({line.split()[1] for line in remotes if len(line.split()) >= 2})
            state = "git-remote" if remotes else "git-local"
            branch = git(path, "branch", "--show-current").stdout.strip() or None
            dirty = bool(git(path, "status", "--porcelain").stdout.strip())
        elif entries:
            state = "not-git"
        else:
            state = "empty"
    products = []
    if state.startswith("git") or state == "not-git":
        products = sorted(p.name for p in path.iterdir() if p.is_dir() and not p.name.startswith("."))
    return {"path": str(path), "source": source, "state": state, "remotes": remotes,
            "branch": branch, "uncommitted_changes": dirty, "products": products}


def main(argv):
    info = inspect()
    if "--json" in argv:
        print(json.dumps(info, indent=2))
    else:
        for key, value in info.items():
            print(f"{key}: {', '.join(value) if isinstance(value, list) else value}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
