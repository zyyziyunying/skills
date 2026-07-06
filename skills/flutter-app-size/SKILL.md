---
name: flutter-app-size
description: Measure, analyze, and reduce Flutter release artifact size for APK, Android App Bundle, IPA, and desktop builds. Use when the user asks about Flutter app size, build size, download size, App Size Tool reports, `--analyze-size`, `--split-debug-info`, obfuscation, asset/package bloat, iOS App Thinning, or size regression comparisons.
---

# Flutter App Size

## Overview

Use this skill to establish a reproducible release-size baseline, inspect the generated code-size report, apply targeted reductions, and compare before/after evidence. Treat upload package size, installed size, and user download size as different measurements.

## Command Boundary

Flutter size work usually requires release builds. Before running any `flutter build` command, confirm that the current user request or project instructions explicitly allow that exact build target and any requested build flags. If the project has `AGENTS.md`, `TEST.md`, `LOCAL.md`, release docs, signing notes, or CI packaging guidance, read the nearest relevant file before building.

Never run store submission, account, payment, production distribution, provisioning-profile mutation, certificate mutation, or credential-handling steps. For iOS App Thinning, default to providing the Xcode export steps only. Run a local non-submission IPA/archive/App Thinning workflow only when the user explicitly authorizes that exact action and the project guidance allows it; do not change signing assets, upload to App Store Connect, or operate store accounts. If the task turns into release packaging or signing ownership, hand off to `flutter-release-packager`.

## Triage

Identify these facts before measuring or changing code:

1. Target platform: `apk`, `appbundle`, `ios`, `linux`, `macos`, or `windows`.
2. Distribution path: direct APK, Play Store/App Store, internal QA, desktop installer, or local artifact.
3. Goal: establish baseline, investigate a regression, reduce below a threshold, compare branches, or prepare release evidence.
4. Constraints: available SDKs, signing/export requirements, CI-only builds, and whether obfuscation or split debug info is acceptable.

If any missing fact can change the measurement method, exact build target, build flags, signing/export requirements, SDK availability, CI-only constraint, or permission to run a release build, ask a concise question before running build commands.

## Measurement Workflow

Use release-mode measurements only. Debug builds and `flutter run` artifacts are not representative.

1. Capture the starting state: branch/commit, Flutter version if easy to get, target platform, build command, artifact path, and any known size target.
2. Generate a size analysis report with the matching command:

```bash
flutter build apk --analyze-size
flutter build appbundle --analyze-size
flutter build ios --analyze-size
flutter build linux --analyze-size
flutter build macos --analyze-size
flutter build windows --analyze-size
```

3. Locate the generated `*-code-size-analysis_*.json` file under `build/`.
4. Open DevTools with `dart devtools`, then use the App Size Tool to inspect the JSON report.
5. Prefer concrete findings from the treemap, dominator tree, package/library grouping, and diff view over broad guesses.
6. After each optimization, regenerate the same report with the same target and compare it with the baseline in the DevTools diff view.

## iOS Size Estimates

For iOS, do not rely on the `.app` bundle size as the end-user download estimate. When accurate user-facing estimates matter, build an IPA and generate an App Thinning Size Report through Xcode:

```bash
flutter build ipa --export-method development
```

Then use Xcode distribution/export to select all compatible device variants, strip Swift symbols when appropriate, export the IPA, and inspect `App Thinning Size Report.txt`. Treat these as instructions unless the user explicitly authorizes local execution. Even with authorization, keep the workflow non-submission and do not mutate signing assets or accounts.

## Android Download And Install Estimates

For Android, distinguish local artifacts from user-facing estimates:

- Local APK/AAB sizes and `--analyze-size` reports are useful for breakdowns, regressions, and relative comparisons.
- Accurate download and install estimates require Play Console app size reporting or a user-provided Play Console report. Do not upload binaries, operate Play Console, or change store settings from this skill unless the user explicitly moves the task to a release-packaging workflow.
- When Play Console data is unavailable, report the local artifact size and code-size findings clearly as local evidence, not as the expected end-user download size.

## Reduction Playbook

Choose reductions based on report evidence:

- Split debug info and obfuscate release builds when acceptable for the project:

```bash
flutter build appbundle --obfuscate --split-debug-info=release-symbols/appbundle/<build-id>/
```

- Preserve the `--split-debug-info` output so crash symbolication remains possible. Prefer a project-approved archive path or CI artifact path; avoid leaving the only copy under `build/` unless the pipeline immediately archives it. Report the saved symbol path in the final evidence.
- When comparing obfuscation or split-debug-info changes, generate a matching optimized size report with the same target/flavor plus the changed flags:

```bash
flutter build appbundle --analyze-size --obfuscate --split-debug-info=release-symbols/appbundle/<build-id>/
```

- Compress or replace large image/audio/video assets only after checking where they are used and whether quality constraints exist.
- Remove unused assets, fonts, generated files, packages, and platform plugins only after verifying no route, flavor, localization, or dynamic lookup depends on them.
- For direct Android APK distribution, consider ABI splits such as `flutter build apk --split-per-abi` when that matches the release channel. Do not equate a universal APK or AAB upload size with end-user download size.
- Keep icon tree shaking enabled unless the project deliberately disabled it for dynamic icon use.
- Use conditional imports, deferred imports, platform-specific packages, and platform gates when the report shows code that should not ship to a target. Validate the result with a size diff instead of assuming the compiler removed it.
- For large dependencies, inspect whether a lighter package, narrower import, feature flag, or lazy/deferred loading strategy fits the product requirements.

## Validation

After changes:

1. Re-run a matching release-size measurement command: keep the same target, flavor, entrypoint, and environment, then add only the optimization flags or changes being compared.
2. Compare baseline and new JSON reports in the DevTools App Size Tool diff view.
3. Run the project-approved static checks and targeted tests for touched code.
4. Report artifact paths, JSON report paths, before/after sizes, major contributors, changed files, and any residual uncertainty.

If the size did not improve, stop and re-check the report before applying unrelated optimizations.

## Constraints

- Do not measure app size from debug builds, IDE play buttons, hot reload, or simulator install footprints.
- Do not assume upload size equals download size; app stores and devices can split by ABI, density, architecture, and device variant.
- Always pass a real directory to `--split-debug-info`.
- Do not remove assets, packages, or platform code purely because they look large; tie removals to report evidence and code references.
- Do not change signing, bundle identifiers, store metadata, provisioning profiles, or release channels while doing size work unless the user explicitly asks.
