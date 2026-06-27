#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
skill_source_dir="$repo_root/skills"
local_root="${LOCAL_SKILL_ROOT:-$HOME/.agents/skills}"
codex_root="${CODEX_SKILL_ROOT:-$HOME/.codex/skills}"

if [ ! -d "$skill_source_dir" ]; then
  printf 'Missing skill source directory: %s\n' "$skill_source_dir" >&2
  exit 1
fi

mkdir -p "$local_root"
mkdir -p "$codex_root"

for link_path in "$local_root"/*; do
  [ -L "$link_path" ] || continue
  link_target="$(readlink "$link_path")"

  case "$link_target" in
    "$skill_source_dir"/*)
      if [ ! -e "$link_target" ]; then
        rm "$link_path"
      fi
      ;;
  esac
done

for link_path in "$codex_root"/*; do
  [ -L "$link_path" ] || continue
  link_target="$(readlink "$link_path")"

  case "$link_target" in
    "$local_root"/*|"$skill_source_dir"/*)
      if [ ! -e "$link_target" ]; then
        rm "$link_path"
      fi
      ;;
  esac
done

count=0
for skill_dir in "$skill_source_dir"/*; do
  [ -d "$skill_dir" ] || continue
  [ -f "$skill_dir/SKILL.md" ] || continue

  skill_name="$(basename "$skill_dir")"
  local_link="$local_root/$skill_name"
  codex_link="$codex_root/$skill_name"

  if [ -e "$local_link" ] && [ ! -L "$local_link" ]; then
    printf 'Refusing to replace non-symlink local skill: %s\n' "$local_link" >&2
    exit 1
  fi

  if [ -L "$local_link" ]; then
    rm "$local_link"
  fi
  ln -s "$skill_dir" "$local_link"

  if [ -e "$codex_link" ] && [ ! -L "$codex_link" ]; then
    printf 'Refusing to replace non-symlink Codex skill: %s\n' "$codex_link" >&2
    exit 1
  fi

  if [ -L "$codex_link" ]; then
    rm "$codex_link"
  fi
  ln -s "$local_link" "$codex_link"

  count=$((count + 1))
done

printf 'Linked %s skills into %s\n' "$count" "$local_root"
printf 'Linked %s skills into %s via %s\n' "$count" "$codex_root" "$local_root"
