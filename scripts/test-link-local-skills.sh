#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
link_script="$repo_root/scripts/link-local-skills.sh"
skill_source_dir="$repo_root/skills"
test_root="$(mktemp -d "${TMPDIR:-/tmp}/link-local-skills-test.XXXXXX")"
test_root="$(cd -P -- "$test_root" && pwd -P)"

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
  "$aliased_local_real/git-commit-helper" ] || \
    fail 'Codex link did not canonicalize the configured local root path'

relative_work="$test_root/relative-work"
mkdir -p "$relative_work"
(
  cd "$relative_work"
  LOCAL_SKILL_ROOT="relative-local" \
    CODEX_SKILL_ROOT="relative-codex" \
    "$link_script" >"$test_root/relative-roots.out"
)

relative_local="$relative_work/relative-local"
relative_codex="$relative_work/relative-codex"
[ -e "$relative_codex/git-commit-helper/SKILL.md" ] || \
  fail 'relative roots produced a broken second-hop Codex link'
[ "$(readlink "$relative_codex/git-commit-helper")" = \
  "$relative_local/git-commit-helper" ] || \
    fail 'relative roots were not canonicalized before linking'

fixture_source="$test_root/fixture-source"
first_skill='active-a'
last_skill='active-z'
stale_skill='stale-skill'
mkdir -p "$fixture_source/$first_skill" \
  "$fixture_source/$last_skill" \
  "$fixture_source/$stale_skill"
touch "$fixture_source/$first_skill/SKILL.md" \
  "$fixture_source/$last_skill/SKILL.md"

conflict_local="$test_root/conflict-local"
conflict_codex="$test_root/conflict-codex"
mkdir -p "$conflict_local" "$conflict_codex"
ln -s "$test_root/original-local-target" "$conflict_local/$first_skill"
ln -s "$test_root/original-codex-target" "$conflict_codex/$first_skill"

stale_source_dir="$fixture_source/$stale_skill"
ln -s "$stale_source_dir" "$conflict_local/$stale_skill"
ln -s "$conflict_local/$stale_skill" "$conflict_codex/$stale_skill"
mkdir "$conflict_codex/$last_skill"

if SKILL_LINK_SOURCE_DIR="$fixture_source" \
  LOCAL_SKILL_ROOT="$conflict_local" \
  CODEX_SKILL_ROOT="$conflict_codex" \
  "$link_script" >"$test_root/conflict.out" 2>&1; then
  fail 'late non-symlink conflict was accepted'
fi

grep -Fq 'Refusing to replace non-symlink Codex skill' \
  "$test_root/conflict.out" || fail 'late conflict failure was not explained'
[ "$(readlink "$conflict_local/$first_skill")" = \
  "$test_root/original-local-target" ] || \
    fail 'late conflict partially replaced an earlier local link'
[ "$(readlink "$conflict_codex/$first_skill")" = \
  "$test_root/original-codex-target" ] || \
    fail 'late conflict partially replaced an earlier Codex link'
[ -L "$conflict_local/$stale_skill" ] || \
  fail 'late conflict partially removed a stale local link'
[ -L "$conflict_codex/$stale_skill" ] || \
  fail 'late conflict partially removed a stale Codex link'

stale_local="$test_root/stale-local"
stale_codex="$test_root/stale-codex"
mkdir -p "$stale_local" "$stale_codex"
ln -s "$stale_source_dir" "$stale_local/$stale_skill"
ln -s "$stale_local/$stale_skill" "$stale_codex/$stale_skill"
unmanaged_source="$test_root/unmanaged-source"
mkdir "$unmanaged_source"
ln -s "$unmanaged_source" "$stale_local/unmanaged-skill"
ln -s "$stale_local/unmanaged-skill" "$stale_codex/unmanaged-skill"
ln -s "$fixture_source/$first_skill" \
  "$stale_local/manual-git-alias"
ln -s "$stale_local/manual-git-alias" \
  "$stale_codex/manual-git-alias"

SKILL_LINK_SOURCE_DIR="$fixture_source" \
  LOCAL_SKILL_ROOT="$stale_local" \
  CODEX_SKILL_ROOT="$stale_codex" \
  "$link_script" >"$test_root/stale-existing-directory.out"

[ ! -L "$stale_local/$stale_skill" ] || \
  fail 'source directory without SKILL.md left a stale local link behind'
[ ! -L "$stale_codex/$stale_skill" ] || \
  fail 'source directory without SKILL.md left a stale Codex link behind'
[ -L "$stale_local/unmanaged-skill" ] || \
  fail 'stale cleanup removed an unmanaged local skill link'
[ -L "$stale_codex/unmanaged-skill" ] || \
  fail 'stale cleanup removed an unmanaged Codex skill link'
[ -L "$stale_local/manual-git-alias" ] || \
  fail 'stale cleanup removed a valid local alias to a managed skill'
[ -L "$stale_codex/manual-git-alias" ] || \
  fail 'stale cleanup removed a valid Codex alias to a managed skill'

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
printf 'PASS: canonicalized configured root aliases during stale-link cleanup\n'
printf 'PASS: canonicalized relative roots before creating second-hop links\n'
printf 'PASS: rejected a late conflict before any link mutation\n'
printf 'PASS: removed links to a source directory without SKILL.md\n'
printf 'PASS: preserved valid unmanaged skill links\n'
printf 'PASS: preserved aliases to current managed skills\n'
printf 'PASS: linked %s skills across distinct roots\n' "$expected_count"
