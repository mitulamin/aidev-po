#!/usr/bin/env bash
# Bootstrap: install aidev-po into a project for Cursor. Run it from inside your checkout of aidev-po.
# It asks where the project is (or should be) and what to call it. A project that does not exist
# yet is created with a plain git init; a project that already has files, such as one set up with
# ai-sdlc-loop, gets aidev-po added alongside, and nothing already there is changed. Running it
# again changes nothing.
#
# Before you start, you need:
#   - Python 3 (this script checks for it and does not install it)
#   - Git (this script checks for it and does not install it)
#   - cURL, only if you download aidev-po with curl instead of git clone
#   - Cursor, signed in. If its cursor command is missing, you are told how to open the folder
#
# To skip the questions, pass the project folder as an argument, or set AIDEV_PO_BOOTSTRAP_LOCATION to
# home, documents, parent or the full path of an existing folder, and AIDEV_PO_BOOTSTRAP_NAME to the
# project's folder name.
set -euo pipefail

script="${BASH_SOURCE[0]}"
case "$script" in
  */*) root="$(cd "${script%/*}/.." && pwd -P)" ;;
  *) root="$(cd .. && pwd -P)" ;;
esac
use_page="https://mitulamin.github.io/aidev-po/bootstrap.html"
default_name="my-project"

stop() {
  printf '%s\n' "$@" >&2
  exit 1
}

target_arg=""
if [ $# -gt 0 ]; then
  case "$1" in
    -h|--help)
      cat <<EOT
Usage: ./scripts/bootstrap.sh [project-folder]

Run it from inside your checkout of aidev-po. It asks where the project is or
should be (your home folder, your Documents folder, or the folder next to this
one) and what to call it, then installs aidev-po into it for Cursor: the po
coordinator, its agents, skills and /po-* commands in .cursor/, an always-on
Cursor rule, and the scripts and templates they run in .aidev-po/.

If the folder does not exist it is created and git init is run (branch main,
nothing committed, no remote). If it already has files, for example a project
set up with ai-sdlc-loop, aidev-po is added alongside: nothing already there is
changed, reordered or overwritten, and AGENTS.md, .ai-sdlc/, MCP configuration,
hooks and editor settings are never touched. Run it again and nothing changes.

It never puts the project inside this checkout, does not create a GitHub
repository, add a remote or sign you up for anything, and opens Cursor if the
cursor command is available. Your products live in a separate git repo, not in
the project; po asks where on its first run.

You need Python 3 and Git. It does not install them.

To skip the questions, give the project folder as the argument, or set
AIDEV_PO_BOOTSTRAP_LOCATION to home, documents, parent or the full path of an
existing folder, and AIDEV_PO_BOOTSTRAP_NAME to the project's folder name.

For scripting, see scripts/new-project.sh, which this calls.
Guide: $use_page
EOT
      exit 0 ;;
    -*) stop "Unknown option: $1. Run ./scripts/bootstrap.sh --help." ;;
    *)
      [ $# -eq 1 ] || stop "bootstrap.sh takes one project folder at most. Run ./scripts/bootstrap.sh --help."
      target_arg="$1" ;;
  esac
fi

command -v git >/dev/null 2>&1 || stop \
  "Git is not installed, and this setup needs it to keep a history of your project." \
  "Install git from https://git-scm.com/downloads, then run this again."
command -v python3 >/dev/null 2>&1 || stop \
  "Python 3 is not installed, and this setup needs it to copy the project files." \
  "Install it from https://www.python.org/downloads/, then run this again."

resolve_dir() { (cd "$1" 2>/dev/null && pwd -P); }

inside_checkout() {
  case "$1/" in
    "$root"/*) return 0 ;;
  esac
  return 1
}

ask() {
  printf '%s ' "$1"
  if ! IFS= read -r answer; then
    echo
    stop "I did not get an answer, so I have stopped without changing anything." \
      "Run it again in a terminal, or pass the project folder, or set AIDEV_PO_BOOTSTRAP_LOCATION and AIDEV_PO_BOOTSTRAP_NAME (see --help)."
  fi
}

has_files() {
  [ -e "$1" ] && { [ ! -d "$1" ] || [ -n "$(ls -A "$1")" ]; }
}

confirm_add_on=1
if [ -n "$target_arg" ]; then
  target="$target_arg"
  confirm_add_on=0
else
  home_dir=""
  if [ -n "${HOME:-}" ] && [ -d "$HOME" ]; then home_dir="$(resolve_dir "$HOME")"; fi
  docs_dir=""
  if [ -n "$home_dir" ] && [ -d "$home_dir/Documents" ]; then docs_dir="$(resolve_dir "$home_dir/Documents")"; fi
  parent_dir="$(resolve_dir "$root/..")"

  location=""
  if [ -n "${AIDEV_PO_BOOTSTRAP_LOCATION:-}" ]; then
    want="$AIDEV_PO_BOOTSTRAP_LOCATION"
    case "$want" in
      home) location="$home_dir" ;;
      documents) location="$docs_dir" ;;
      parent) location="$parent_dir" ;;
      /*) location="$(resolve_dir "$want" || true)" ;;
      *) stop "AIDEV_PO_BOOTSTRAP_LOCATION must be home, documents, parent or the full path of an existing folder." ;;
    esac
    [ -n "$location" ] || stop "I cannot find the folder for AIDEV_PO_BOOTSTRAP_LOCATION=$want, so I have not changed anything."
    if inside_checkout "$location"; then
      stop "That place is inside the aidev-po folder itself, so I have not changed anything." \
        "Choose a place outside it."
    fi
  else
    labels=()
    places=()
    if [ -n "$home_dir" ]; then labels+=("Your home folder"); places+=("$home_dir"); fi
    if [ -n "$docs_dir" ]; then labels+=("Your Documents folder"); places+=("$docs_dir"); fi
    labels+=("The folder next to this download (one level up)")
    places+=("$parent_dir")
    while true; do
      echo
      echo "Where is the project, or where would you like it to be put?"
      for i in "${!places[@]}"; do
        printf '  %d) %s\n     %s\n' "$((i + 1))" "${labels[$i]}" "${places[$i]}"
      done
      if [ -z "$docs_dir" ]; then echo "  (There is no Documents folder here, so it is not on the list.)"; fi
      ask "Type a number and press Enter:"
      if [[ "$answer" =~ ^[0-9]+$ ]] && [ "$answer" -ge 1 ] && [ "$answer" -le "${#places[@]}" ]; then
        location="${places[$((answer - 1))]}"
        if inside_checkout "$location"; then
          echo "That place is inside the aidev-po folder itself, and a project cannot go there. Please pick another."
          continue
        fi
        break
      fi
      echo "Please type one of the numbers above."
    done
  fi

  valid_name='^[A-Za-z0-9][A-Za-z0-9._-]*$'
  explain_name="Please use letters, numbers, dashes or underscores, with no spaces, starting with a letter or number."
  if [ -n "${AIDEV_PO_BOOTSTRAP_NAME:-}" ]; then
    name="$AIDEV_PO_BOOTSTRAP_NAME"
    [[ "$name" =~ $valid_name ]] || stop "AIDEV_PO_BOOTSTRAP_NAME is not a good folder name. $explain_name"
    confirm_add_on=0
  else
    while true; do
      echo
      ask "What is the project's folder called? It is created if it does not exist. [$default_name]"
      name="${answer:-$default_name}"
      if ! [[ "$name" =~ $valid_name ]]; then
        echo "$explain_name"
        continue
      fi
      break
    done
  fi
  target="$location/$name"
fi

if has_files "$target" && [ "$confirm_add_on" = 1 ]; then
  echo
  echo "$target already has files. I will add aidev-po alongside them and change nothing that is already there."
  ask "Add aidev-po to it? [Y/n]"
  case "$answer" in
    ""|y|Y|yes|YES|Yes) ;;
    *) stop "Stopped without changing anything." ;;
  esac
fi

if ! out="$(bash "$root/scripts/new-project.sh" --harness cursor "$target" 2>&1)"; then
  printf '%s\n' "$out" >&2
  stop "" "Setup stopped before it finished. The messages above say why."
fi
printf '%s\n' "$out" | grep -v "^Next:" || true
target="$(resolve_dir "$target")"

echo
echo "aidev-po is ready in $target. Nothing was sent anywhere."
if command -v cursor >/dev/null 2>&1 && cursor "$target" >/dev/null 2>&1; then
  echo "Opening Cursor. Open the agent chat and type /po-start."
else
  echo "Next: open the folder $target in Cursor (File, then Open Folder), open the agent chat, and type /po-start."
fi
