#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd -P "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
skill_source_dir="${SKILL_LINK_SOURCE_DIR:-$repo_root/skills}"
local_root="${LOCAL_SKILL_ROOT:-$HOME/.agents/skills}"
codex_root="${CODEX_SKILL_ROOT:-$HOME/.codex/skills}"

if [ ! -d "$skill_source_dir" ]; then
  printf 'Missing skill source directory: %s\n' "$skill_source_dir" >&2
  exit 1
fi

skill_source_dir="$(cd -P -- "$skill_source_dir" && pwd -P)"

mkdir -p "$local_root"
mkdir -p "$codex_root"

local_root="$(cd -P -- "$local_root" && pwd -P)"
codex_root="$(cd -P -- "$codex_root" && pwd -P)"

if [ "$local_root" = "$codex_root" ]; then
  printf 'Skill roots must resolve to different directories: %s\n' "$local_root" >&2
  exit 1
fi

desired_names=()
desired_dirs=()
for skill_dir in "$skill_source_dir"/*; do
  [ -d "$skill_dir" ] || continue
  [ -f "$skill_dir/SKILL.md" ] || continue

  skill_name="$(basename "$skill_dir")"
  desired_names+=("$skill_name")
  desired_dirs+=("$skill_dir")
done

is_desired_skill() {
  local candidate="$1"
  local desired_index
  local desired_name
  for ((desired_index = 0; desired_index < desired_count; desired_index++)); do
    desired_name="${desired_names[$desired_index]}"
    if [ "$candidate" = "$desired_name" ]; then
      return 0
    fi
  done
  return 1
}

resolved_link_target() {
  local link_path="$1"
  local link_target
  local target_path
  local target_parent
  local target_name
  link_target="$(readlink "$link_path")"
  case "$link_target" in
    /*) target_path="$link_target" ;;
    *) target_path="$(dirname "$link_path")/$link_target" ;;
  esac

  target_parent="$(dirname "$target_path")"
  target_name="$(basename "$target_path")"
  if target_parent="$(cd -P -- "$target_parent" 2>/dev/null && pwd -P)"; then
    printf '%s/%s\n' "$target_parent" "$target_name"
  else
    printf '%s\n' "$target_path"
  fi
}

is_stale_repo_managed_local_link() {
  local local_link="$1"
  local local_target
  local target_skill_name
  [ -L "$local_link" ] || return 1
  local_target="$(resolved_link_target "$local_link")"
  [ "$(dirname "$local_target")" = "$skill_source_dir" ] || return 1
  target_skill_name="$(basename "$local_target")"
  ! is_desired_skill "$target_skill_name"
}

# Validate every desired destination before removing or replacing any link.
desired_count="${#desired_names[@]}"
for ((index = 0; index < desired_count; index++)); do
  skill_name="${desired_names[$index]}"
  local_link="$local_root/$skill_name"
  codex_link="$codex_root/$skill_name"

  if [ -e "$local_link" ] && [ ! -L "$local_link" ]; then
    printf 'Refusing to replace non-symlink local skill: %s\n' "$local_link" >&2
    exit 1
  fi

  if [ -e "$codex_link" ] && [ ! -L "$codex_link" ]; then
    printf 'Refusing to replace non-symlink Codex skill: %s\n' "$codex_link" >&2
    exit 1
  fi
done

stale_local_links=()
for link_path in "$local_root"/*; do
  [ -L "$link_path" ] || continue
  link_target="$(resolved_link_target "$link_path")"
  if [ "$(dirname "$link_target")" = "$skill_source_dir" ]; then
    skill_name="$(basename "$link_target")"
    if ! is_desired_skill "$skill_name"; then
      stale_local_links+=("$link_path")
    fi
  fi
done

stale_codex_links=()
for link_path in "$codex_root"/*; do
  [ -L "$link_path" ] || continue
  link_target="$(resolved_link_target "$link_path")"
  link_parent="$(dirname "$link_target")"
  if [ "$link_parent" = "$skill_source_dir" ]; then
    skill_name="$(basename "$link_target")"
    if ! is_desired_skill "$skill_name"; then
      stale_codex_links+=("$link_path")
    fi
  elif [ "$link_parent" = "$local_root" ]; then
    skill_name="$(basename "$link_target")"
    if [ ! -e "$link_target" ] || {
      ! is_desired_skill "$skill_name" &&
        is_stale_repo_managed_local_link "$link_target"
    }; then
      stale_codex_links+=("$link_path")
    fi
  fi
done

stale_codex_count="${#stale_codex_links[@]}"
for ((index = 0; index < stale_codex_count; index++)); do
  link_path="${stale_codex_links[$index]}"
  rm "$link_path"
done

stale_local_count="${#stale_local_links[@]}"
for ((index = 0; index < stale_local_count; index++)); do
  link_path="${stale_local_links[$index]}"
  rm "$link_path"
done

count=0
for ((index = 0; index < desired_count; index++)); do
  skill_name="${desired_names[$index]}"
  skill_dir="${desired_dirs[$index]}"
  local_link="$local_root/$skill_name"
  codex_link="$codex_root/$skill_name"

  if [ -L "$local_link" ]; then
    rm "$local_link"
  fi
  ln -s "$skill_dir" "$local_link"

  if [ -L "$codex_link" ]; then
    rm "$codex_link"
  fi
  ln -s "$local_link" "$codex_link"

  count=$((count + 1))
done

printf 'Linked %s skills into %s\n' "$count" "$local_root"
printf 'Linked %s skills into %s via %s\n' "$count" "$codex_root" "$local_root"
