#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
publish_dir="$repo_root/skills"
tmp_dir="$repo_root/.sync-published-skills"

rm -rf "$tmp_dir"
mkdir -p "$tmp_dir"

for skill_md in "$repo_root"/*/SKILL.md; do
  [ -e "$skill_md" ] || continue
  skill_dir="$(dirname "$skill_md")"
  skill_name="$(basename "$skill_dir")"

  case "$skill_name" in
    skills|scripts|.*)
      continue
      ;;
  esac

  if [ -e "$skill_dir/.private-skill" ]; then
    continue
  fi

  mkdir -p "$tmp_dir/$skill_name"
  rsync -a --exclude ".DS_Store" "$skill_dir/" "$tmp_dir/$skill_name/"
done

rm -rf "$publish_dir"
mv "$tmp_dir" "$publish_dir"

printf 'Synced %s skills into %s\n' "$(find "$publish_dir" -mindepth 2 -maxdepth 2 -name SKILL.md | wc -l | tr -d ' ')" "$publish_dir"
