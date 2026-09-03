#!/usr/bin/env sh
# Install the Product Judgement Skills into any agent that reads SKILL.md folders.
#
# Claude Code, Cursor, and Codex can install this repository as a plugin instead;
# see the Install section of README.md. Use this script for project-scoped setups,
# for agents without a plugin system, or when you want plain symlinks you control.

set -eu

SKILLS="focal compass flywheel soul product-judgement"
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

agents=""
scope="user"
project_dir=$(pwd)
mode="link"
action="install"
selected=""

usage() {
  cat <<'USAGE'
Usage: scripts/install.sh [options]

  --agent NAME     claude | codex | cursor | gemini | opencode | all
                   Repeatable. Default: every agent detected on this machine.
  --skill NAME     Repeatable. Default: all five Skills.
  --scope SCOPE    user | project                     (default: user)
  --project DIR    Project root for --scope project   (default: current directory)
  --copy           Copy the Skill folders instead of symlinking them.
  --uninstall      Remove Skills this script installed.
  --list           Print the target directories and exit.
  -h, --help       Show this message.

Symlinks are the default so `git pull` in this repository updates every agent at once.
USAGE
}

# Resolve an agent's skills directory for the active scope.
skills_dir() {
  case "$1" in
    claude)   [ "$scope" = user ] && echo "$HOME/.claude/skills"  || echo "$project_dir/.claude/skills" ;;
    cursor)   [ "$scope" = user ] && echo "$HOME/.cursor/skills"  || echo "$project_dir/.cursor/skills" ;;
    codex)    [ "$scope" = user ] && echo "$HOME/.agents/skills"  || echo "$project_dir/.agents/skills" ;;
    gemini)   [ "$scope" = user ] && echo "$HOME/.gemini/skills"  || echo "$project_dir/.gemini/skills" ;;
    opencode) [ "$scope" = user ] && echo "$HOME/.opencode/skills" || echo "$project_dir/.opencode/skills" ;;
    *) echo "install.sh: unknown agent '$1'" >&2; exit 2 ;;
  esac
}

# An agent counts as present if its CLI is on PATH or its config directory exists.
detect_agents() {
  found=""
  command -v claude      >/dev/null 2>&1 || [ -d "$HOME/.claude" ]   && found="$found claude"
  command -v codex       >/dev/null 2>&1 || [ -d "$HOME/.codex" ]    && found="$found codex"
  command -v cursor-agent >/dev/null 2>&1 || [ -d "$HOME/.cursor" ]  && found="$found cursor"
  command -v gemini      >/dev/null 2>&1 || [ -d "$HOME/.gemini" ]   && found="$found gemini"
  command -v opencode    >/dev/null 2>&1 || [ -d "$HOME/.opencode" ] && found="$found opencode"
  echo "$found"
}

while [ $# -gt 0 ]; do
  case "$1" in
    --agent)     agents="$agents $2"; shift 2 ;;
    --skill)     selected="$selected $2"; shift 2 ;;
    --scope)     scope="$2"; shift 2 ;;
    --project)   project_dir=$(CDPATH= cd -- "$2" && pwd); shift 2 ;;
    --copy)      mode="copy"; shift ;;
    --uninstall) action="uninstall"; shift ;;
    --list)      action="list"; shift ;;
    -h|--help)   usage; exit 0 ;;
    *) echo "install.sh: unknown option '$1'" >&2; usage >&2; exit 2 ;;
  esac
done

case "$scope" in
  user|project) ;;
  *) echo "install.sh: --scope must be 'user' or 'project'" >&2; exit 2 ;;
esac

case " $agents " in
  *" all "*) agents="claude codex cursor gemini opencode" ;;
esac

if [ -z "$(echo "$agents" | tr -d ' ')" ]; then
  agents=$(detect_agents)
  if [ -z "$(echo "$agents" | tr -d ' ')" ]; then
    echo "install.sh: no supported agent detected; pass --agent NAME" >&2
    exit 1
  fi
  echo "Detected:$agents"
fi

[ -n "$(echo "$selected" | tr -d ' ')" ] && SKILLS="$selected"

for skill in $SKILLS; do
  [ -f "$ROOT/$skill/SKILL.md" ] || { echo "install.sh: no such Skill '$skill'" >&2; exit 2; }
done

for agent in $agents; do
  target=$(skills_dir "$agent")

  if [ "$action" = list ]; then
    echo "$agent	$target"
    continue
  fi

  [ "$action" = install ] && mkdir -p "$target"
  [ -d "$target" ] || continue

  for skill in $SKILLS; do
    dest="$target/$skill"

    if [ "$action" = uninstall ]; then
      if [ -L "$dest" ] || [ -d "$dest" ]; then
        rm -rf "$dest"
        echo "removed  $dest"
      fi
      continue
    fi

    # Replace whatever is there so re-running the script is a clean repair.
    rm -rf "$dest"
    if [ "$mode" = copy ]; then
      cp -R "$ROOT/$skill" "$dest"
      echo "copied   $dest"
    else
      ln -s "$ROOT/$skill" "$dest"
      echo "linked   $dest -> $ROOT/$skill"
    fi
  done
done

[ "$action" = install ] && echo "Done. Restart your agent so it reloads Skill metadata."
exit 0
