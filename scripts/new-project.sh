#!/usr/bin/env bash
# Set up a project folder for aidev-po: create it if it is missing, run a plain git init if it has
# none, and install aidev-po into it. Adds to an existing project without changing what is there.
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd -P)"
installer="$root/scripts/install-harness.py"
default_harness="cursor"
use_page="https://mitulamin.github.io/aidev-po/bootstrap.html"

usage() {
  cat <<EOF
Usage: scripts/new-project.sh [--harness <name>] [--overlay <dir>] <target-dir>

Installs aidev-po into <target-dir> for the harness (default: $default_harness) and
registers it alongside any tool already there, such as ai-sdlc-loop, without changing,
reordering or overwriting their files.

  <target-dir> missing   it is created, git init is run, and aidev-po is installed. Nothing else is.
  <target-dir> empty     git init is run if there is no repository, and aidev-po is installed.
  <target-dir> has files aidev-po is added on. No git init is run, and existing files are never
                         overwritten: a clash stops the run before anything is written.

Running it again is safe: files already up to date are skipped and nothing changes.
It never writes MCP configuration, hooks, editor settings or AGENTS.md, never adds a git
remote, and never commits. Nothing is written outside <target-dir>.

Harnesses (default: $default_harness; layouts in data/harnesses.json):
EOF
  if command -v python3 >/dev/null 2>&1; then
    python3 "$installer" --list | while IFS=$'\t' read -r id name; do
      printf '  %-16s %s\n' "$id" "$name"
    done
  else
    echo "  (install python3 to list and use the harnesses)"
  fi
  cat <<EOF

--overlay <dir>: also copy the files under <dir> into the project, never over an existing file.
It is the generic extension point and does nothing unless given (or AIDEV_PO_BOOTSTRAP_OVERLAY is set).

Guide: $use_page
EOF
}

harness="$default_harness"
overlay=()
args=()
while [ $# -gt 0 ]; do
  case "$1" in
    -h|--help) usage; exit 0 ;;
    --harness)
      if [ $# -lt 2 ]; then echo "--harness needs a name" >&2; echo >&2; usage >&2; exit 1; fi
      harness="$2"; shift 2 ;;
    --harness=*) harness="${1#--harness=}"; shift ;;
    --overlay)
      if [ $# -lt 2 ]; then echo "--overlay needs a folder" >&2; echo >&2; usage >&2; exit 1; fi
      overlay=(--overlay "$2"); shift 2 ;;
    --overlay=*) overlay=(--overlay "${1#--overlay=}"); shift ;;
    --) shift; args+=("$@"); break ;;
    -*) echo "Unknown option: $1" >&2; echo >&2; usage >&2; exit 1 ;;
    *) args+=("$1"); shift ;;
  esac
done
set -- ${args[@]+"${args[@]}"}

if [ $# -ne 1 ]; then
  usage >&2
  exit 1
fi
target="$1"

command -v python3 >/dev/null 2>&1 || { echo "aidev-po needs python3 to install itself." >&2; exit 1; }
command -v git >/dev/null 2>&1 || { echo "aidev-po needs git to set up the project's repository." >&2; exit 1; }
if ! [[ "$harness" =~ ^[a-z0-9-]+$ ]] || ! python3 "$installer" --validate "$harness"; then
  echo "Unknown harness: $harness" >&2
  echo >&2
  usage >&2
  exit 1
fi

if [ -e "$target" ] && [ ! -d "$target" ]; then
  echo "$target exists and is not a folder" >&2
  exit 1
fi

created=""
if [ ! -d "$target" ]; then
  mkdir -p "$target"
  created="yes"
fi
target="$(cd "$target" && pwd -P)"
case "$target/" in
  "$root"/*) echo "$target is inside the aidev-po checkout itself, so I have not changed anything. Choose a place outside it." >&2
             [ -z "$created" ] || rmdir "$target" 2>/dev/null || true
             exit 1 ;;
esac

fresh=""
if [ -z "$(ls -A "$target")" ]; then fresh="yes"; fi

if ! python3 "$installer" "$target" "$harness" ${overlay[@]+"${overlay[@]}"}; then
  [ -z "$created" ] || rmdir "$target" 2>/dev/null || true
  exit 1
fi

# Plain git init only for a folder that was missing or empty and has no repository; branch main, no commits, no remote.
if [ -n "$fresh" ] || [ -n "$created" ]; then
  if [ ! -e "$target/.git" ]; then
    git -C "$target" init -q
    git -C "$target" symbolic-ref HEAD refs/heads/main
    echo "Ran git init in $target (branch main, nothing committed, no remote)."
  fi
elif [ ! -e "$target/.git" ]; then
  echo "$target is not a git repository and I left it that way, as it already had files."
fi

if [ -n "$created" ]; then
  echo "Created $target with the $harness harness."
fi
echo "Next: open the project in Cursor and type /po-start. po will ask where your products repo lives. Guide: $use_page"
