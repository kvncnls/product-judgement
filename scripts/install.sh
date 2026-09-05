#!/usr/bin/env sh
# Install the Product Judgement Skills into any agent that reads SKILL.md folders.
#
# Claude Code, Cursor, and Codex can install this repository as a plugin instead;
# see the Install section of README.md. Use this script for project-scoped setups,
# for agents without a plugin system, or when you want plain symlinks you control.

set -eu

SKILLS="focal compass flywheel soul product-judgement"
ALL_SKILLS="$SKILLS"
ROOT=$(CDPATH= cd -P "$(dirname "$0")/.." && pwd -P)
MARKER_NAME=".product-judgement-install"

agents=""
scope="user"
project_dir=$(pwd -P)
project_arg=""
mode="link"
action="install"
selected=""
install_home=${HOME-}
temp_root=${TMPDIR:-/tmp}
hash_tool=""
move_mode=""
move_no_clobber=0
failures=0
active_stage=""
active_backup=""
active_destination=""

usage() {
  cat <<'USAGE'
Usage: scripts/install.sh [options]

  --agent NAME     claude | codex | cursor | gemini | opencode | all
                   Repeatable. Default: every agent detected on this machine.
  --skill NAME     Repeatable. Default: all five Skills.
  --scope SCOPE    user | project                     (default: user)
  --project DIR    Project root for --scope project   (default: current directory)
  --copy           Copy the Skill folders instead of symlinking them.
  --uninstall      Remove recognized installations.
  --list           Print the target directories and exit.
  -h, --help       Show this message.

Symlinks are the default so git pull in this repository updates every agent at once.
Existing entries are preserved unless they are a canonical link to the source Skill
or an unmodified copy carrying this script's provenance marker.
USAGE
}

error() {
  echo "install.sh: $*" >&2
}

die() {
  error "$1"
  exit "${2:-2}"
}

detect_move_mode() {
  [ -n "$move_mode" ] && return 0

  move_help=$(mv --help 2>&1 || :)
  case "$move_help" in
    *--no-target-directory*|*" -T "*|*" -T,"*|*"[-finT]"*)
      move_mode=target
      move_help_has_no_clobber "$move_help" && move_no_clobber=1
      return 0
      ;;
  esac

  move_help=$(mv -h 2>&1 || :)
  case "$move_help" in
    *"usage: mv "*|*"usage: mv["*|*"[-hv]"*|*"--no-dereference"*)
      move_mode=nofollow
      move_help_has_no_clobber "$move_help" && move_no_clobber=1
      return 0
      ;;
  esac

  move_mode=unsupported
}

move_help_has_no_clobber() {
  case "$1" in
    *--no-clobber*|*"-n,"*|*"[-"*"n"*"]"*) return 0 ;;
    *) return 1 ;;
  esac
}

safe_move() {
  detect_move_mode
  case "$move_mode" in
    target)
      [ "$move_no_clobber" -eq 1 ] || return 125
      mv -T -n "$1" "$2"
      ;;
    nofollow)
      [ "$move_no_clobber" -eq 1 ] || return 125
      mv -h -n "$1" "$2"
      ;;
    *) return 125 ;;
  esac
}

entry_identity() {
  identity_value=$(stat -f '%d:%i' "$1" 2>/dev/null) || identity_value=""
  case "$identity_value" in
    ""|*[!0123456789:]*) ;;
    *) printf '%s\n' "$identity_value"; return 0 ;;
  esac

  identity_value=$(stat -c '%d:%i' "$1" 2>/dev/null) || return 1
  case "$identity_value" in
    ""|*[!0123456789:]*) return 1 ;;
    *) printf '%s\n' "$identity_value" ;;
  esac
}

restore_backup_entry() {
  backup_entry=$1
  backup_destination=$2
  [ -e "$backup_entry" ] || [ -L "$backup_entry" ] || return 1
  [ ! -e "$backup_destination" ] && [ ! -L "$backup_destination" ] || return 1
  backup_identity=$(entry_identity "$backup_entry") || return 1
  safe_move "$backup_entry" "$backup_destination" || return 1
  restored_identity=$(entry_identity "$backup_destination") || return 1
  [ "$restored_identity" = "$backup_identity" ]
}

cleanup() {
  if [ -n "$active_stage" ]; then
    rm -rf "$active_stage" 2>/dev/null || :
    active_stage=""
  fi
  if [ -n "$active_backup" ]; then
    # An interrupt can arrive after the owned destination was moved aside but
    # before its staged replacement lands. Restore it when the original path
    # is still free; otherwise leave the rollback directory discoverable.
    if [ -n "$active_destination" ] && ! has_path "$active_destination" && has_path "$active_backup/entry"; then
      restore_backup_entry "$active_backup/entry" "$active_destination" 2>/dev/null || :
    fi
    if ! has_path "$active_backup/entry"; then
      rmdir "$active_backup" 2>/dev/null || :
    else
      error "original destination retained in '$active_backup/entry'"
    fi
    active_backup=""
    active_destination=""
  fi
}

trap cleanup EXIT
trap 'cleanup; exit 129' HUP
trap 'cleanup; exit 130' INT
trap 'cleanup; exit 143' TERM

has_path() {
  [ -e "$1" ] || [ -L "$1" ]
}

list_contains() {
  case " $1 " in
    *" $2 "*) return 0 ;;
    *) return 1 ;;
  esac
}

known_agent() {
  case "$1" in
    claude|codex|cursor|gemini|opencode|all) return 0 ;;
    *) return 1 ;;
  esac
}

known_skill() {
  case "$1" in
    focal|compass|flywheel|soul|product-judgement) return 0 ;;
    *) return 1 ;;
  esac
}

require_value() {
  option=$1
  [ "$#" -ge 2 ] || die "$option requires a value" 2
  case "$2" in
    --*) die "$option requires a value" 2 ;;
  esac
}

skills_dir() {
  case "$1" in
    claude)
      if [ "$scope" = user ]; then printf '%s\n' "$install_home/.claude/skills"; else printf '%s\n' "$project_dir/.claude/skills"; fi
      ;;
    cursor)
      if [ "$scope" = user ]; then printf '%s\n' "$install_home/.cursor/skills"; else printf '%s\n' "$project_dir/.cursor/skills"; fi
      ;;
    codex)
      if [ "$scope" = user ]; then printf '%s\n' "$install_home/.agents/skills"; else printf '%s\n' "$project_dir/.agents/skills"; fi
      ;;
    gemini)
      if [ "$scope" = user ]; then printf '%s\n' "$install_home/.gemini/skills"; else printf '%s\n' "$project_dir/.gemini/skills"; fi
      ;;
    opencode)
      if [ "$scope" = user ]; then printf '%s\n' "$install_home/.config/opencode/skills"; else printf '%s\n' "$project_dir/.opencode/skills"; fi
      ;;
    *) die "unknown agent '$1'" 2 ;;
  esac
}

detect_agents() {
  found=""
  if command -v claude >/dev/null 2>&1 || { [ "$scope" = user ] && [ -d "$install_home/.claude" ]; } || { [ "$scope" = project ] && [ -d "$project_dir/.claude" ]; }; then
    found="$found claude"
  fi
  if command -v codex >/dev/null 2>&1 || { [ "$scope" = user ] && [ -d "$install_home/.codex" ]; } || { [ "$scope" = project ] && [ -d "$project_dir/.agents" ]; }; then
    found="$found codex"
  fi
  if command -v cursor-agent >/dev/null 2>&1 || { [ "$scope" = user ] && [ -d "$install_home/.cursor" ]; } || { [ "$scope" = project ] && [ -d "$project_dir/.cursor" ]; }; then
    found="$found cursor"
  fi
  if command -v gemini >/dev/null 2>&1 || { [ "$scope" = user ] && [ -d "$install_home/.gemini" ]; } || { [ "$scope" = project ] && [ -d "$project_dir/.gemini" ]; }; then
    found="$found gemini"
  fi
  if command -v opencode >/dev/null 2>&1 || { [ "$scope" = user ] && { [ -d "$install_home/.config/opencode" ] || [ -d "$install_home/.opencode" ]; }; } || { [ "$scope" = project ] && [ -d "$project_dir/.opencode" ]; }; then
    found="$found opencode"
  fi
  printf '%s\n' "$found"
}

canonical_existing() {
  CDPATH= cd -P "$1" 2>/dev/null && pwd -P
}

canonical_parent() {
  candidate=$(dirname "$1")
  while [ ! -d "$candidate" ]; do
    next=$(dirname "$candidate")
    [ "$next" != "$candidate" ] || return 1
    candidate=$next
  done
  canonical_existing "$candidate"
}

path_within() {
  candidate=$1
  base=$2
  [ "$candidate" = "$base" ] && return 0
  [ "$base" = "/" ] && return 0
  case "$candidate" in
    "$base"/*) return 0 ;;
    *) return 1 ;;
  esac
}

source_path() {
  canonical_existing "$ROOT/$1"
}

source_path_is_canonical() {
  source_skill=$1
  source_expected="$ROOT/$source_skill"
  [ -d "$source_expected" ] && [ ! -L "$source_expected" ] || return 1
  source_canonical=$(canonical_existing "$source_expected") || return 1
  [ "$source_canonical" = "$source_expected" ]
}

source_is_safe() {
  source=$1
  root_real=$(canonical_existing "$ROOT") || return 1
  path_within "$source" "$root_real" || return 1
  [ "$source" != "$root_real" ] || return 1
}

target_path_is_safe() {
  target=$1
  if has_path "$target"; then
    [ -d "$target" ] || { error "target '$target' exists but is not a directory"; return 1; }
    target_real=$(canonical_existing "$target") || { error "cannot resolve target '$target'"; return 1; }
  else
    target_parent=$(canonical_parent "$target") || { error "cannot resolve the parent of target '$target'"; return 1; }
    target_real="$target_parent/$(basename "$target")"
  fi

  for check_skill in $ALL_SKILLS; do
    check_source=$(source_path "$check_skill") || { error "cannot resolve source Skill '$check_skill'"; return 1; }
    if path_within "$target_real" "$check_source"; then
      error "refusing target '$target': it resolves inside source Skill '$check_source'"
      return 1
    fi
  done
}

prepare_target() {
  target=$1
  if ! has_path "$target"; then
    target_parent=$(canonical_parent "$target") || { error "cannot resolve the parent of target '$target'"; return 1; }
    for check_skill in $ALL_SKILLS; do
      check_source=$(source_path "$check_skill") || { error "cannot resolve source Skill '$check_skill'"; return 1; }
      if path_within "$target_parent" "$check_source"; then
        error "refusing target '$target': its parent resolves inside source Skill '$check_source'"
        return 1
      fi
    done
    if ! mkdir -p "$target"; then
      error "cannot create target '$target'"
      return 1
    fi
  fi
  target_path_is_safe "$target"
}

resolve_link() {
  link=$1
  link_target=$(readlink "$link") || return 1
  case "$link_target" in
    /*) resolved=$link_target ;;
    *) resolved="$(dirname "$link")/$link_target" ;;
  esac
  canonical_existing "$resolved"
}

destination_path_is_safe() {
  dest=$1
  source_link=0
  if [ -L "$dest" ]; then
    if candidate=$(resolve_link "$dest" 2>/dev/null); then
      for check_skill in $ALL_SKILLS; do
        check_source=$(source_path "$check_skill") || continue
        [ "$candidate" = "$check_source" ] && source_link=1
      done
    else
      candidate="$(canonical_parent "$dest")/$(basename "$dest")" || { error "cannot resolve destination '$dest'"; return 1; }
    fi
  elif [ -d "$dest" ]; then
    candidate=$(canonical_existing "$dest") || { error "cannot resolve destination '$dest'"; return 1; }
  else
    candidate="$(canonical_parent "$dest")/$(basename "$dest")" || { error "cannot resolve destination '$dest'"; return 1; }
  fi

  for check_skill in $ALL_SKILLS; do
    check_source=$(source_path "$check_skill") || { error "cannot resolve source Skill '$check_skill'"; return 1; }
    if path_within "$candidate" "$check_source" && [ "$source_link" -eq 0 ]; then
      error "refusing destination '$dest': it resolves inside source Skill '$check_source'"
      return 1
    fi
  done
}

source_symlinks_are_safe() {
  source_root=$1
  source_entries=$(find "$source_root" -type l -print 2>/dev/null) || return 1
  [ -n "$source_entries" ] || return 0

  while IFS= read -r source_link_path; do
    [ -n "$source_link_path" ] || continue
    source_link_target=$(resolve_link "$source_link_path" 2>/dev/null) || {
      error "source Skill '$source_root' contains an unresolved symlink '$source_link_path'"
      return 1
    }
    if ! path_within "$source_link_target" "$source_root"; then
      error "source Skill '$source_root' contains symlink '$source_link_path' outside the selected Skill"
      return 1
    fi
  done <<EOF
$source_entries
EOF
}

if command -v shasum >/dev/null 2>&1; then
  hash_tool=shasum
elif command -v sha256sum >/dev/null 2>&1; then
  hash_tool=sha256sum
else
  hash_tool=cksum
fi

digest_file() {
  digest_output=""
  case "$hash_tool" in
    shasum)
      digest_output=$(shasum -a 256 "$1") || return 1
      printf '%s\n' "${digest_output%% *}"
      ;;
    sha256sum)
      digest_output=$(sha256sum "$1") || return 1
      printf '%s\n' "${digest_output%% *}"
      ;;
    cksum)
      set -- $(cksum "$1") || return 1
      printf '%s:%s\n' "$1" "$2"
      ;;
    *) return 1 ;;
  esac
}

temporary_file() {
  mktemp "$temp_root/product-judgement.XXXXXX"
}

directory_fingerprint() {
  directory=$1
  output=$2
  : > "$output" || return 1
  entries_file=$(temporary_file) || return 1
  if ! find "$directory" ! -path "$directory" ! -path "$directory/$MARKER_NAME" -print > "$entries_file" 2>/dev/null; then
    rm -f "$entries_file" 2>/dev/null || :
    return 1
  fi
  if ! entries=$(LC_ALL=C sort "$entries_file"); then
    rm -f "$entries_file" 2>/dev/null || :
    return 1
  fi
  rm -f "$entries_file" 2>/dev/null || return 1
  [ -n "$entries" ] || return 0

  while IFS= read -r item; do
    [ -n "$item" ] || continue
    relative=${item#"$directory"/}
    if [ -L "$item" ]; then
      link_target=$(readlink "$item") || return 1
      printf 'L\t%s\t%s\n' "$relative" "$link_target" >> "$output" || return 1
    elif [ -d "$item" ]; then
      printf 'D\t%s\n' "$relative" >> "$output" || return 1
    elif [ -f "$item" ]; then
      file_digest=$(digest_file "$item") || return 1
      printf 'F\t%s\t%s\n' "$relative" "$file_digest" >> "$output" || return 1
    else
      return 1
    fi
  done <<EOF
$entries
EOF
}

directory_digest() {
  signature=$(temporary_file) || return 1
  if ! directory_fingerprint "$1" "$signature"; then
    rm -f "$signature" 2>/dev/null || :
    return 1
  fi
  if ! signature_digest=$(digest_file "$signature"); then
    rm -f "$signature" 2>/dev/null || :
    return 1
  fi
  rm -f "$signature" 2>/dev/null || return 1
  printf '%s\n' "$signature_digest"
}

marker_value() {
  key=$1
  marker=$2
  case "$key" in
    version) sed -n 's/^version=//p' "$marker" ;;
    kind) sed -n 's/^kind=//p' "$marker" ;;
    skill) sed -n 's/^skill=//p' "$marker" ;;
    source) sed -n 's/^source=//p' "$marker" ;;
    content) sed -n 's/^content=//p' "$marker" ;;
    *) return 1 ;;
  esac
}

copy_marker_digest() {
  dest=$1
  skill=$2
  source=$3
  marker="$dest/$MARKER_NAME"

  [ -f "$marker" ] && [ ! -L "$marker" ] || return 1
  [ "$(sed -n '1p' "$marker")" = "# Product Judgement installer metadata" ] || return 1
  [ "$(marker_value version "$marker")" = 1 ] || return 1
  [ "$(marker_value kind "$marker")" = copy ] || return 1
  [ "$(marker_value skill "$marker")" = "$skill" ] || return 1
  [ "$(marker_value source "$marker")" = "$source" ] || return 1
  expected=$(marker_value content "$marker")
  case "$expected" in
    ""|*[!0123456789abcdef:]*) return 1 ;;
  esac
  expected_marker=$(printf '# Product Judgement installer metadata\nversion=1\nkind=copy\nskill=%s\nsource=%s\ncontent=%s\n' "$skill" "$source" "$expected")
  actual_marker=$(cat "$marker") || return 1
  [ "$actual_marker" = "$expected_marker" ] || return 1
  printf '%s\n' "$expected"
}

copy_is_intact() {
  dest=$1
  expected=$2
  actual=$(directory_digest "$dest") || return 1
  [ "$actual" = "$expected" ]
}

destination_kind() {
  dest=$1
  skill=$2
  source=$3

  if ! has_path "$dest"; then
    printf '%s\n' absent
    return 0
  fi
  if [ -L "$dest" ]; then
    if resolved=$(resolve_link "$dest" 2>/dev/null) && [ "$resolved" = "$source" ]; then
      printf '%s\n' link
    else
      printf '%s\n' unowned
    fi
    return 0
  fi
  if [ -d "$dest" ] && expected=$(copy_marker_digest "$dest" "$skill" "$source" 2>/dev/null); then
    if copy_is_intact "$dest" "$expected"; then
      printf '%s\n' copy
    else
      printf '%s\n' modified
    fi
    return 0
  fi
  printf '%s\n' unowned
}

write_marker() {
  destination=$1
  skill=$2
  source=$3
  content_digest=$4
  marker="$destination/$MARKER_NAME"
  if ! {
    printf '%s\n' '# Product Judgement installer metadata'
    printf '%s\n' 'version=1'
    printf '%s\n' 'kind=copy'
    printf 'skill=%s\n' "$skill"
    printf 'source=%s\n' "$source"
    printf 'content=%s\n' "$content_digest"
  } > "$marker"; then
    error "cannot write provenance marker '$marker'"
    return 1
  fi
}

discard_stage() {
  if [ -n "$active_stage" ]; then
    rm -rf "$active_stage" 2>/dev/null || :
    active_stage=""
  fi
}

stage_install() {
  skill=$1
  source=$2
  target=$3
  stage_parent=$(mktemp -d "$target/.product-judgement-stage.XXXXXX") || { error "cannot create a staging directory under '$target'"; return 1; }
  active_stage=$stage_parent
  stage_entry="$stage_parent/$skill"

  if ! source_path_is_canonical "$skill"; then
    error "source Skill '$skill' changed to an alias while being staged"
    discard_stage
    return 1
  fi
  if ! source_symlinks_are_safe "$source"; then
    error "source Skill '$skill' changed to include an unsafe symlink while being staged"
    discard_stage
    return 1
  fi

  if [ "$mode" = copy ]; then
    source_before=$(directory_digest "$source") || { error "cannot fingerprint source Skill '$source'"; discard_stage; return 1; }
    if ! cp -R "$source" "$stage_entry"; then
      error "cannot stage a copy of Skill '$skill'"
      discard_stage
      return 1
    fi
    [ -d "$stage_entry" ] && [ ! -L "$stage_entry" ] || { error "staged copy of Skill '$skill' is not a directory"; discard_stage; return 1; }
    source_symlinks_are_safe "$stage_entry" || { error "staged copy of Skill '$skill' contains an unsafe symlink"; discard_stage; return 1; }
    staged_digest=$(directory_digest "$stage_entry") || { error "cannot verify staged copy of Skill '$skill'"; discard_stage; return 1; }
    [ "$staged_digest" = "$source_before" ] || { error "staged copy of Skill '$skill' failed content verification"; discard_stage; return 1; }
    source_after=$(directory_digest "$source") || { error "cannot recheck source Skill '$source'"; discard_stage; return 1; }
    source_path_is_canonical "$skill" || { error "source Skill '$skill' changed to an alias while being staged"; discard_stage; return 1; }
    source_symlinks_are_safe "$source" || { error "source Skill '$skill' changed to include an unsafe symlink while being staged"; discard_stage; return 1; }
    [ "$source_after" = "$source_before" ] || { error "source Skill '$skill' changed while it was being staged; destination preserved"; discard_stage; return 1; }
    staged_digest=$source_after
    write_marker "$stage_entry" "$skill" "$source" "$source_after" || { discard_stage; return 1; }
  else
    staged_digest=""
    if ! ln -s "$source" "$stage_entry"; then
      error "cannot stage a link for Skill '$skill'"
      discard_stage
      return 1
    fi
    source_path_is_canonical "$skill" || { error "source Skill '$skill' changed to an alias while being staged"; discard_stage; return 1; }
    source_symlinks_are_safe "$source" || { error "source Skill '$skill' changed to include an unsafe symlink while being staged"; discard_stage; return 1; }
  fi
  staged_identity=$(entry_identity "$stage_entry") || { error "cannot identify staged Skill '$skill'"; discard_stage; return 1; }
  staged_entry=$stage_entry
}

owned_entry_matches() {
  owned_entry=$1
  owned_skill=$2
  owned_source=$3
  owned_kind=$4
  [ "$(destination_kind "$owned_entry" "$owned_skill" "$owned_source")" = "$owned_kind" ]
}

staged_destination_matches() {
  verify_destination=$1
  verify_kind=$2
  verify_source=$3
  verify_identity=$4
  verify_digest=$5
  actual_identity=$(entry_identity "$verify_destination") || return 1
  [ "$actual_identity" = "$verify_identity" ] || return 1

  case "$verify_kind" in
    link)
      [ -L "$verify_destination" ] || return 1
      resolved_destination=$(resolve_link "$verify_destination" 2>/dev/null) || return 1
      [ "$resolved_destination" = "$verify_source" ]
      ;;
    copy)
      [ -d "$verify_destination" ] && [ ! -L "$verify_destination" ] || return 1
      actual_digest=$(directory_digest "$verify_destination") || return 1
      [ "$actual_digest" = "$verify_digest" ]
      ;;
    *) return 1 ;;
  esac
}

recover_nested_stage() {
  recovery_destination=$1
  recovery_stage=$2
  recovery_identity=$3
  recovery_kind=$4
  recovery_digest=$5
  [ -d "$recovery_destination" ] && [ ! -L "$recovery_destination" ] || return 0

  recovery_nested="$recovery_destination/$(basename "$recovery_stage")"
  nested_identity=$(entry_identity "$recovery_nested" 2>/dev/null) || return 0
  [ "$nested_identity" = "$recovery_identity" ] || return 0
  if [ "$recovery_kind" = copy ]; then
    nested_digest=$(directory_digest "$recovery_nested" 2>/dev/null) || return 0
    [ "$nested_digest" = "$recovery_digest" ] || return 0
  fi
  safe_move "$recovery_nested" "$recovery_stage" 2>/dev/null || :
}

replace_staged() {
  dest=$1
  target=$2
  skill=$3
  source=$4
  expected_kind=$5
  stage_entry=$6
  expected_identity=$7
  expected_digest=$8
  backup_parent=""

  current_kind=$(destination_kind "$dest" "$skill" "$source")
  if [ "$current_kind" != "$expected_kind" ]; then
    error "destination '$dest' changed while it was being staged; destination preserved"
    return 1
  fi

  if [ "$expected_kind" = absent ]; then
    if has_path "$dest"; then
      error "destination '$dest' changed while it was being staged; destination preserved"
      return 1
    fi
  elif ! has_path "$dest"; then
    error "destination '$dest' disappeared while it was being staged; destination preserved"
    return 1
  fi

  if ! source_path_is_canonical "$skill"; then
    error "source Skill '$skill' changed to an alias while being staged; destination preserved"
    return 1
  fi
  if ! source_symlinks_are_safe "$source"; then
    error "source Skill '$skill' changed to include an unsafe symlink while being staged; destination preserved"
    return 1
  fi
  if [ "$mode" = copy ]; then
    source_recheck=$(directory_digest "$source") || {
      error "cannot recheck source Skill '$source'; destination preserved"
      return 1
    }
    [ "$source_recheck" = "$expected_digest" ] || {
      error "source Skill '$skill' changed while it was being staged; destination preserved"
      return 1
    }
  fi

  if has_path "$dest"; then
    backup_parent=$(mktemp -d "$target/.product-judgement-backup.XXXXXX") || { error "cannot create a rollback directory under '$target'"; return 1; }
    active_backup=$backup_parent
    active_destination=$dest
    if ! safe_move "$dest" "$backup_parent/entry"; then
      error "cannot move owned destination '$dest' aside; destination preserved"
      return 1
    fi
    if ! owned_entry_matches "$backup_parent/entry" "$skill" "$source" "$expected_kind"; then
      error "destination changed while it was being moved; destination preserved"
      if restore_backup_entry "$backup_parent/entry" "$dest"; then
        if rm -rf "$backup_parent" 2>/dev/null; then
          active_backup=""
          active_destination=""
        else
          error "destination restored; rollback directory retained"
        fi
      else
        error "original destination retained in '$backup_parent/entry'"
      fi
      return 1
    fi
  fi

  if safe_move "$stage_entry" "$dest"; then
    if ! staged_destination_matches "$dest" "$mode" "$source" "$expected_identity" "$expected_digest"; then
      recover_nested_stage "$dest" "$stage_entry" "$expected_identity" "$mode" "$expected_digest"
      error "staged Skill did not land at intended destination '$dest'; destination preserved"
    else
      if [ -n "$backup_parent" ]; then
        if ! owned_entry_matches "$backup_parent/entry" "$skill" "$source" "$expected_kind"; then
          error "original destination changed before rollback cleanup; original retained in '$backup_parent/entry'"
          rmdir "$(dirname "$stage_entry")" 2>/dev/null || :
          active_stage=""
          return 1
        fi
        if ! rm -rf "$backup_parent" 2>/dev/null; then
          error "cannot discard original destination backup; original retained in '$backup_parent/entry'"
          rmdir "$(dirname "$stage_entry")" 2>/dev/null || :
          active_stage=""
          return 1
        fi
        active_backup=""
        active_destination=""
      fi
      rmdir "$(dirname "$stage_entry")" 2>/dev/null || :
      active_stage=""
      return 0
    fi
  fi

  if [ -n "$backup_parent" ] && ! has_path "$dest" && restore_backup_entry "$backup_parent/entry" "$dest"; then
    if rm -rf "$backup_parent" 2>/dev/null; then
      active_backup=""
      active_destination=""
      error "cannot install staged Skill at '$dest'; destination restored"
    else
      error "cannot install staged Skill at '$dest'; destination restored and rollback directory retained"
    fi
  elif [ -n "$backup_parent" ]; then
    error "cannot install staged Skill at '$dest'; original retained in '$backup_parent/entry'"
  else
    error "cannot install staged Skill at '$dest'; destination preserved"
  fi
  return 1
}

remove_owned() {
  dest=$1
  target=$2
  skill=$3
  source=$4
  expected_kind=$5
  backup_parent=$(mktemp -d "$target/.product-judgement-backup.XXXXXX") || { error "cannot create a rollback directory under '$target'"; return 1; }
  current_kind=$(destination_kind "$dest" "$skill" "$source")
  if [ "$current_kind" != "$expected_kind" ]; then
    error "destination '$dest' changed before uninstall; destination preserved"
    rmdir "$backup_parent" 2>/dev/null || :
    return 1
  fi
  active_backup=$backup_parent
  active_destination=$dest
  if ! safe_move "$dest" "$backup_parent/entry"; then
    error "cannot move owned destination '$dest' aside; destination preserved"
    return 1
  fi
  if ! owned_entry_matches "$backup_parent/entry" "$skill" "$source" "$expected_kind"; then
    error "destination changed while being moved for uninstall; destination preserved"
    if restore_backup_entry "$backup_parent/entry" "$dest"; then
      if rm -rf "$backup_parent" 2>/dev/null; then
        active_backup=""
        active_destination=""
      else
        error "destination restored; rollback directory retained"
      fi
    else
      error "original destination retained in '$backup_parent/entry'"
    fi
    return 1
  fi
  if rm -rf "$backup_parent/entry"; then
    if rm -rf "$backup_parent" 2>/dev/null; then
      active_backup=""
      active_destination=""
      printf 'removed  %s\n' "$dest"
      return 0
    fi
    error "removed '$dest'; rollback directory retained"
    return 1
  fi

  if ! has_path "$dest" && restore_backup_entry "$backup_parent/entry" "$dest"; then
    if rm -rf "$backup_parent" 2>/dev/null; then
      active_backup=""
      active_destination=""
      error "cannot remove owned destination '$dest'; destination restored"
    else
      error "cannot remove owned destination '$dest'; destination restored and rollback directory retained"
    fi
  else
    error "cannot remove owned destination '$dest'; original retained in '$backup_parent/entry'"
  fi
  return 1
}

while [ "$#" -gt 0 ]; do
  option=$1
  case "$option" in
    --agent)
      require_value "$@"
      known_agent "$2" || die "unknown agent '$2'; expected claude, codex, cursor, gemini, opencode, or all" 2
      if ! list_contains "$agents" "$2"; then agents="$agents $2"; fi
      shift 2
      ;;
    --skill)
      require_value "$@"
      known_skill "$2" || die "unknown Skill '$2'; use one of focal, compass, flywheel, soul, or product-judgement" 2
      if ! list_contains "$selected" "$2"; then selected="$selected $2"; fi
      shift 2
      ;;
    --scope)
      require_value "$@"
      scope=$2
      shift 2
      ;;
    --project)
      require_value "$@"
      project_arg=$2
      shift 2
      ;;
    --copy)
      mode=copy
      shift
      ;;
    --uninstall)
      [ "$action" = install ] || die "--uninstall and --list cannot be combined" 2
      action=uninstall
      shift
      ;;
    --list)
      [ "$action" = install ] || die "--uninstall and --list cannot be combined" 2
      action=list
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      die "unknown option '$option'" 2
      ;;
  esac
done

case "$scope" in
  user|project) ;;
  *) die "--scope must be 'user' or 'project'" 2 ;;
esac

if [ "$scope" = user ] && [ -z "$install_home" ]; then
  die "HOME must be set for --scope user; use --scope project for an isolated install" 2
fi

if [ -n "$project_arg" ]; then
  [ -d "$project_arg" ] || die "--project directory '$project_arg' does not exist" 2
  project_dir=$(CDPATH= cd -P "$project_arg" && pwd -P) || die "cannot resolve --project directory '$project_arg'" 2
fi

if list_contains "$agents" all; then
  agents="claude codex cursor gemini opencode"
elif [ -z "$(printf '%s' "$agents" | tr -d ' ')" ]; then
  agents=$(detect_agents)
  if [ -z "$(printf '%s' "$agents" | tr -d ' ')" ]; then
    die "no supported agent detected; pass --agent NAME" 1
  fi
  echo "Detected:$agents"
fi

[ -n "$(printf '%s' "$selected" | tr -d ' ')" ] && SKILLS=$selected

for skill in $SKILLS; do
  source_path_is_canonical "$skill" || die "source Skill '$skill' is not the canonical directory in this repository" 2
  source=$(source_path "$skill") || die "no such Skill '$skill'" 2
  [ -f "$source/SKILL.md" ] || die "Skill '$skill' has no SKILL.md" 2
  source_is_safe "$source" || die "source Skill '$skill' resolves outside this repository" 2
  source_symlinks_are_safe "$source" || die "source Skill '$skill' contains an unsafe symlink" 2
  [ ! -e "$source/$MARKER_NAME" ] && [ ! -L "$source/$MARKER_NAME" ] || die "source Skill '$skill' uses reserved installer marker '$MARKER_NAME'" 2
done

if [ "$action" = list ]; then
  for agent in $agents; do
    printf '%s\t%s\n' "$agent" "$(skills_dir "$agent")"
  done
  exit 0
fi

for agent in $agents; do
  target=$(skills_dir "$agent")
  if [ "$action" = install ]; then
    if ! prepare_target "$target"; then failures=1; fi
  elif has_path "$target"; then
    if ! target_path_is_safe "$target"; then failures=1; fi
  fi
done

for agent in $agents; do
  target=$(skills_dir "$agent")
  [ -d "$target" ] || continue
  for skill in $SKILLS; do
    dest="$target/$skill"
    if ! destination_path_is_safe "$dest"; then
      failures=1
      continue
    fi
    source=$(source_path "$skill") || { failures=1; continue; }
    kind=$(destination_kind "$dest" "$skill" "$source")
    case "$kind" in
      unowned)
        error "refusing '$dest': existing entry is not a canonical link or marked copy installed by this script; preserve it or move it aside"
        failures=1
        ;;
      modified)
        error "refusing '$dest': copied Skill was modified; restore the original or remove it yourself before retrying"
        failures=1
        ;;
    esac
  done
done

[ "$failures" -eq 0 ] || exit 1

for agent in $agents; do
  target=$(skills_dir "$agent")
  [ -d "$target" ] || continue
  for skill in $SKILLS; do
    dest="$target/$skill"
    source=$(source_path "$skill") || { failures=1; continue; }
    kind=$(destination_kind "$dest" "$skill" "$source")

    if [ "$action" = uninstall ]; then
      case "$kind" in
        absent) continue ;;
        link|copy)
          if ! remove_owned "$dest" "$target" "$skill" "$source" "$kind"; then failures=1; fi
          ;;
        *)
          error "refusing '$dest': destination changed after preflight; preserve it"
          failures=1
          ;;
      esac
      continue
    fi

    needs_install=1
    if [ "$mode" = link ] && [ "$kind" = link ]; then
      needs_install=0
    elif [ "$mode" = copy ] && [ "$kind" = copy ]; then
      marker_digest=$(copy_marker_digest "$dest" "$skill" "$source") || marker_digest=""
      source_digest=$(directory_digest "$source") || source_digest=""
      [ -n "$marker_digest" ] && [ "$marker_digest" = "$source_digest" ] && needs_install=0
    fi

    if [ "$needs_install" -eq 0 ]; then
      echo "unchanged $dest"
      continue
    fi

    if ! stage_install "$skill" "$source" "$target"; then
      failures=1
      continue
    fi
    if replace_staged "$dest" "$target" "$skill" "$source" "$kind" "$staged_entry" "$staged_identity" "$staged_digest"; then
      if [ "$mode" = copy ]; then
        echo "copied   $dest"
      else
        echo "linked   $dest -> $source"
      fi
    else
      failures=1
      discard_stage
    fi
  done
done

[ "$failures" -eq 0 ] || exit 1
echo "Done. Restart your agent so it reloads Skill metadata."
exit 0
