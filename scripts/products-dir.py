#!/usr/bin/env python3
"""Find the products repo, report its state, and record where it is.

Usage:
  scripts/products-dir.py                  print the state as key: value lines
  scripts/products-dir.py --json           print the state as JSON
  scripts/products-dir.py --set PATH       record PATH in aidev-po.local.json (products_dir)
  scripts/products-dir.py --set PATH --init  the same, and set up PATH as a git repo if it is not one: create the
                                           folder, run git init and make an empty initial commit. No remote is added.

Standard library only. Products live in a separate git repo outside the aidev-po checkout,
one per client or team. There is no default location; the user chooses one once. Where the
products repo is, first match wins:

  1. the AIDEV_PO_PRODUCTS_DIR environment variable (overrides the recorded path)
  2. "products_dir" in aidev-po.local.json at the repo root (gitignored)

If neither is set the state is "unconfigured" and `po` asks the user to create a products repo or
point to an existing one, offering the suggested paths printed below. `--set` and `--init` change
things on disk, so `po` runs them only after the user says yes. Nothing here adds a remote or
pushes: a remote is a separate question `po` asks afterwards (see docs/products-repo.md). The report
includes `gh`, whether the GitHub CLI is ready (installed and signed in), for that question.

A relative path is resolved from the aidev-po root; ~ is expanded. `--set` records a path as an
absolute path, or as typed if it starts with ~.

state is one of:
  unconfigured no path is set
  missing      the path does not exist
  empty        the path exists and has no files
  not-git      the path has files but is not a git repo
  git-local    a git repo with no remote (the normal state right after setup)
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
SUGGESTIONS = ["~/aidev-products", "~/Documents/aidev-products", str(ROOT.parent / "aidev-products")]


def read_config():
    if not CONFIG.exists():
        return {}
    try:
        return json.loads(CONFIG.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        raise SystemExit(f"{CONFIG.name}: cannot read ({e})")


def resolve():
    """Return (path as written, where it came from), or (None, None) if nothing is set."""
    if os.environ.get(ENV_VAR):
        return os.environ[ENV_VAR], f"env {ENV_VAR}"
    value = read_config().get("products_dir")
    if value:
        return value, CONFIG.name
    return None, None


def expand(raw):
    path = Path(raw).expanduser()
    return path if path.is_absolute() else ROOT / path


def git(path, *args):
    return subprocess.run(["git", "-C", str(path), *args], capture_output=True, text=True)


def is_repo_root(path):
    top = git(path, "rev-parse", "--show-toplevel")
    return top.returncode == 0 and Path(top.stdout.strip()).resolve() == path.resolve()


def gh_status():
    try:
        result = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True)
    except FileNotFoundError:
        return "not-installed"
    return "ready" if result.returncode == 0 else "not-signed-in"


def inspect():
    raw, source = resolve()
    info = {"path": None, "source": source, "state": "unconfigured", "remotes": [], "branch": None,
            "uncommitted_changes": None, "has_commits": None, "gh": gh_status(), "products": [], "suggestions": [str(expand(s)) for s in SUGGESTIONS]}
    if raw is None:
        return info
    path = expand(raw)
    info["path"] = str(path)
    if not path.is_dir():
        info["state"] = "missing"
        return info
    entries = [p for p in path.iterdir() if p.name != ".DS_Store"]
    if is_repo_root(path):
        remotes = git(path, "remote", "-v").stdout.splitlines()
        info["remotes"] = sorted({line.split()[1] for line in remotes if len(line.split()) >= 2})
        info["state"] = "git-remote" if info["remotes"] else "git-local"
        info["branch"] = git(path, "branch", "--show-current").stdout.strip() or None
        info["uncommitted_changes"] = bool(git(path, "status", "--porcelain").stdout.strip())
        info["has_commits"] = git(path, "rev-parse", "--verify", "HEAD").returncode == 0
    else:
        info["state"] = "not-git" if entries else "empty"
    if entries:
        info["products"] = sorted(p.name for p in path.iterdir() if p.is_dir() and not p.name.startswith("."))
    return info


def record(raw, init):
    path = expand(raw)
    if path.resolve() == ROOT.resolve():
        raise SystemExit("products repo cannot be the aidev-po checkout itself")
    if path.exists() and not path.is_dir():
        raise SystemExit(f"{path} exists and is not a folder")
    stored = raw if raw.startswith("~") else str(path)
    config = read_config()
    config["products_dir"] = stored
    CONFIG.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    print(f"recorded products_dir {stored} in {CONFIG.name}")
    if os.environ.get(ENV_VAR):
        print(f"note: {ENV_VAR} is set and overrides it", file=sys.stderr)
    if init:
        path.mkdir(parents=True, exist_ok=True)
        if is_repo_root(path):
            print(f"{path} is already a git repo")
        else:
            result = git(path, "init")
            if result.returncode:
                raise SystemExit(result.stderr.strip() or "git init failed")
            print(f"ran git init in {path}")
        if git(path, "rev-parse", "--verify", "HEAD").returncode:
            result = git(path, "commit", "--allow-empty", "-m", "Initialise products repo")
            if result.returncode:
                raise SystemExit("git init worked but the initial commit failed (set git user.name and user.email?): "
                                 + (result.stderr.strip() or result.stdout.strip()))
            print("made the initial commit; no remote added")


def main(argv):
    if "--set" in argv:
        i = argv.index("--set")
        if i + 1 >= len(argv) or argv[i + 1].startswith("--"):
            raise SystemExit("--set needs a path")
        record(argv[i + 1], "--init" in argv)
        return 0
    if "--init" in argv:
        raise SystemExit("--init goes with --set PATH")
    info = inspect()
    if "--json" in argv:
        print(json.dumps(info, indent=2))
    else:
        for key, value in info.items():
            print(f"{key}: {', '.join(value) if isinstance(value, list) else value}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
