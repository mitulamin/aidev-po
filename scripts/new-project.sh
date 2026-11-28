#!/usr/bin/env bash
# Set up a project folder for aidev-po: create it if it is missing, run a plain git init unless told
# not to, and install aidev-po into it. Adds to an existing project without changing what is there.
# This script does not ask questions. A folder that already has files needs --yes (or
# AIDEV_PO_BOOTSTRAP_YES=1). --git-init and --no-git-init choose git init; the default is to
# initialise a folder that is not already a repository.
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd -P)"
installer="$root/scripts/install-harness.py"
default_harness="cursor"
use_page="https://mitulamin.github.io/aidev-po/bootstrap.html"

usage() {
  cat <<EOF
Usage: scripts/new-project.sh [--harness <name>] [--overlay <dir>] [--yes] [--git-init | --no-git-init] <target-dir>

Installs aidev-po into <target-dir> for the harness (default: $default_harness) and
registers it alongside any tool already there, such as ai-sdlc-loop, without changing,
reordering or overwriting their files. It does not ask questions.

  <target-dir> missing   it is created and aidev-po is installed. Nothing else is.
  <target-dir> empty     aidev-po is installed.
  <target-dir> has files in a terminal you are asked first; the default answer is no.
                         Without a terminal, pass --yes or set AIDEV_PO_BOOTSTRAP_YES=1.
                         Otherwise nothing is written.
                         Existing files are never overwritten: a clash stops the run before
                         anything is written. A file aidev-po installed that you have edited
                         stops the run, names the file, and writes nothing.

  Not already a git repo  git init is run (branch main, nothing committed, no remote)
                         unless you pass --no-git-init or set AIDEV_PO_BOOTSTRAP_GIT_INIT=0.
                         That is the default when nobody is asked. In a terminal the question
                         defaults to yes. --git-init asks for that default explicitly.
                         A folder that is already a repository is left on its current branch.

Running it again is safe once --yes is passed: files already up to date are skipped and nothing changes.
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
yes_flag=0
git_mode=""
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
    --yes) yes_flag=1; shift ;;
    --git-init)
      [ -z "$git_mode" ] || { echo "Use only one of --git-init and --no-git-init." >&2; exit 1; }
      git_mode=yes; shift ;;
    --no-git-init)
      [ -z "$git_mode" ] || { echo "Use only one of --git-init and --no-git-init." >&2; exit 1; }
      git_mode=no; shift ;;
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

case "${AIDEV_PO_BOOTSTRAP_YES:-}" in
  1|yes|true|YES|Yes) yes_flag=1 ;;
esac
case "${AIDEV_PO_BOOTSTRAP_GIT_INIT:-}" in
  "") ;;
  1|yes|true|YES|Yes)
    [ "$git_mode" != no ] || { echo "AIDEV_PO_BOOTSTRAP_GIT_INIT conflicts with --no-git-init." >&2; exit 1; }
    git_mode=yes ;;
  0|no|false|NO|No)
    [ "$git_mode" != yes ] || { echo "AIDEV_PO_BOOTSTRAP_GIT_INIT conflicts with --git-init." >&2; exit 1; }
    git_mode=no ;;
  *) echo "AIDEV_PO_BOOTSTRAP_GIT_INIT must be 1 or 0." >&2; exit 1 ;;
esac

if [ -e "$target" ] && [ ! -d "$target" ]; then
  echo "$target exists and is not a folder" >&2
  exit 1
fi

# Resolve without creating, so a refusal leaves the disk untouched.
target="$(python3 -c 'import os, sys
p = os.path.abspath(sys.argv[1])
parent = os.path.dirname(p)
print(os.path.join(os.path.realpath(parent), os.path.basename(p)) if os.path.isdir(parent) else p)' "$target")"
case "$target/" in
  "$root"/*)
    echo "$target is inside the aidev-po checkout itself, so I have not changed anything. Choose a place outside it." >&2
    exit 1 ;;
esac

if [ -d "$target" ] && [ -n "$(ls -A "$target")" ] && [ "$yes_flag" != 1 ]; then
  if [ -t 0 ]; then
    printf 'There are files in %s. Are you sure you want me to work in this folder? [y/N] ' "$target"
    if ! IFS= read -r answer; then
      echo
      echo "Stopped without changing anything."
      exit 0
    fi
    case "$answer" in
      y|Y|yes|YES|Yes) ;;
      *) echo "Stopped without changing anything."; exit 0 ;;
    esac
  else
    echo "There are files in $target. Re-run with --yes or AIDEV_PO_BOOTSTRAP_YES=1 to install into this folder. Nothing was written." >&2
    exit 1
  fi
fi

want_init=0
if [ ! -e "$target/.git" ]; then
  if [ "$git_mode" = yes ]; then
    want_init=1
  elif [ "$git_mode" = no ]; then
    want_init=0
  elif [ -t 0 ]; then
    printf "This folder isn't a Git repository. Initialise one? [Y/n] "
    if ! IFS= read -r answer; then
      echo
      answer=""
    fi
    case "$answer" in
      n|N|no|NO|No) want_init=0 ;;
      *) want_init=1 ;;
    esac
  else
    want_init=1
  fi
fi

created=""
if [ ! -d "$target" ]; then
  mkdir -p "$target"
  created="yes"
fi

if ! python3 "$installer" "$target" "$harness" ${overlay[@]+"${overlay[@]}"}; then
  [ -z "$created" ] || rmdir "$target" 2>/dev/null || true
  exit 1
fi

if [ "$want_init" = 1 ] && [ ! -e "$target/.git" ]; then
  git -C "$target" init -q
  git -C "$target" symbolic-ref HEAD refs/heads/main
  echo "Ran git init in $target (branch main, nothing committed, no remote)."
elif [ ! -e "$target/.git" ]; then
  echo "Left $target without a Git repository."
fi

if [ -n "$created" ]; then
  echo "Created $target with the $harness harness."
fi
echo "Next: open the project in Cursor and type /po-start. po will ask where your products repo lives. Guide: $use_page"
