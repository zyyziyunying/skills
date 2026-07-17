#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
link_script="$repo_root/scripts/link-local-skills.sh"
skill_source_dir="$repo_root/skills"
test_root="$(mktemp -d "${TMPDIR:-/tmp}/link-local-skills-test.XXXXXX")"

cleanup() {
  rm -rf -- "$test_root"
}
trap cleanup EXIT

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  exit 1
}

same_root="$test_root/same-root"
mkdir -p "$same_root"
ln -s "$skill_source_dir/removed-skill" "$same_root/stale-skill"

if LOCAL_SKILL_ROOT="$same_root" \
  CODEX_SKILL_ROOT="$same_root/." \
  "$link_script" >"$test_root/same-root.out" 2>&1; then
  fail 'path aliases resolving to the same root were accepted'
fi

grep -Fq 'Skill roots must resolve to different directories' \
  "$test_root/same-root.out" || fail 'same-root failure did not explain the conflict'
[ -L "$same_root/stale-skill" ] || fail 'same-root rejection removed an existing skill link'
[ ! -e "$same_root/git-commit-helper" ] || fail 'same-root rejection created a skill link'

aliased_local_real="$test_root/aliased-local-real"
aliased_local_root="$test_root/aliased-local-root"
aliased_codex_root="$test_root/aliased-codex-root"
mkdir -p "$aliased_local_real" "$aliased_codex_root"
ln -s "$aliased_local_real" "$aliased_local_root"
ln -s "$aliased_local_root/removed-skill" "$aliased_codex_root/stale-skill"

LOCAL_SKILL_ROOT="$aliased_local_root" \
  CODEX_SKILL_ROOT="$aliased_codex_root" \
  "$link_script" >"$test_root/aliased-local-root.out"

[ ! -L "$aliased_codex_root/stale-skill" ] || \
  fail 'aliased local root left a stale Codex link behind'
[ "$(readlink "$aliased_codex_root/git-commit-helper")" = \
  "$aliased_local_root/git-commit-helper" ] || \
  fail 'Codex link did not preserve the configured local root path'

local_root="$test_root/local-root"
codex_root="$test_root/codex-root"
LOCAL_SKILL_ROOT="$local_root" \
  CODEX_SKILL_ROOT="$codex_root" \
  "$link_script" >"$test_root/distinct-roots.out"

expected_count=0
for skill_dir in "$skill_source_dir"/*; do
  [ -d "$skill_dir" ] || continue
  [ -f "$skill_dir/SKILL.md" ] || continue

  skill_name="$(basename "$skill_dir")"
  [ -L "$local_root/$skill_name" ] || fail "missing local link for $skill_name"
  [ "$(readlink "$local_root/$skill_name")" = "$skill_dir" ] || \
    fail "incorrect local link target for $skill_name"
  [ -L "$codex_root/$skill_name" ] || fail "missing Codex link for $skill_name"
  [ "$(readlink "$codex_root/$skill_name")" = "$local_root/$skill_name" ] || \
    fail "incorrect Codex link target for $skill_name"
  expected_count=$((expected_count + 1))
done

grep -Fq "Linked $expected_count skills into $local_root" \
  "$test_root/distinct-roots.out" || fail 'distinct-root local summary was incorrect'
grep -Fq "Linked $expected_count skills into $codex_root via $local_root" \
  "$test_root/distinct-roots.out" || fail 'distinct-root Codex summary was incorrect'

printf 'PASS: rejected aliased same roots before link mutation\n'
printf 'PASS: preserved configured root aliases during stale-link cleanup\n'
printf 'PASS: linked %s skills across distinct roots\n' "$expected_count"
