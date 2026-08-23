---
name: r8-analyzer
description: Audit Android R8 and ProGuard configuration, existing Configuration Analyzer reports, broad keep rules, and library consumer rules. Use for read-only R8 configuration analysis or when deciding whether a risky AGP or R8 upgrade is justified; do not use for general Flutter artifact-size measurement.
---

# R8 Analyzer

## Outcome

Produce an evidence-backed, read-only assessment of the current R8 configuration.
Separate verified report metrics from static keep-rule findings and from changes
that still require a release build or runtime regression testing.

Do not upgrade AGP, replace R8, edit keep rules, or run a release build merely to
make this skill's preferred analysis path available. Those actions require the
user's request and the project's own build and release guidance.

## Establish The Current Path

1. Read the nearest project instructions and inspect the Android Gradle files,
   version catalog, `gradle.properties`, build types, and app-owned ProGuard files.
2. Record the current AGP/R8 versions and whether minification, code shrinking,
   resource shrinking, and R8 full mode are enabled for the relevant variant.
3. Prefer existing analyzer or release artifacts before running Gradle:
   - AGP 9.3 or later standalone report:
     `<module>/build/reports/r8/r8-config-analyzer-<variant>.html`
   - Report from a regular optimized build:
     `<module>/build/outputs/mapping/<variant>/configanalyzer.html`
   - Existing `configuration.txt`, `seeds.txt`, `usage.txt`, `mapping.txt`, and
     `r8-metadata.dat` under the matching variant's build outputs.
4. Verify current analyzer requirements and output paths against the official
   [R8 Configuration Analyzer documentation](https://developer.android.com/topic/performance/app-optimization/r8-configuration-analyzer)
   before relying on version thresholds, because AGP and R8 behavior can change.

## Generate A Report Only When Authorized

If the request and project rules authorize the exact Gradle operation:

- For AGP 9.3 or later, prefer the standalone task:

  ```bash
  ./gradlew :app:analyzeReleaseR8Config
  ```

- For AGP 9.2 or earlier with R8 9.3.7-dev or later, the current official
  fallback generates HTML directly during an R8-enabled build:

  ```bash
  ./gradlew assembleRelease \
    -Dcom.android.tools.r8.dumpkeepradiushtmltodirectory="$PWD/tmp/r8analysis"
  ```

Use the real module and variant names. Track the command until it and its child
processes exit. Do not claim success from a partial Gradle yield. Do not run the
fallback build when release builds are outside the user's authorization.

This skill intentionally does not require protobuf conversion helpers. Current
supported analyzer paths produce an HTML report directly. If only a protobuf
artifact exists, report that the quantitative path is unavailable instead of
inventing scores or reconstructing an unverified schema.

## Analyze

From an HTML report, capture the shrinking, optimization, and obfuscation scores,
the widest keep rules, their origins, blocked classes/fields/methods, unused or
identical rules, and subsumed rules. Treat these percentages as optimizer
availability metrics, not APK/AAB byte savings.

When no supported report exists, perform a heuristic audit:

- Check app-owned rules for package-wide `-keep`, broad member retention,
  `allowshrinking`/`allowoptimization` opportunities, global disable flags, and
  rules for removed dependencies.
- Trace library rules to merged release configuration or dependency artifacts.
  Do not assume an app rule is redundant merely because a modern library often
  ships consumer rules.
- Treat rules owned by AGP or third-party libraries as upstream facts. Prefer an
  upstream fix or a controlled filtering experiment over silently copying and
  deleting consumer rules.
- For reflection, JNI, serialization, dependency injection, deep links, and SDK
  initialization, identify the runtime path that a proposed narrowing could
  break and the focused test needed before changing the rule.

Static inspection may rank suspicious rules, but it must not fabricate analyzer
scores, Store download savings, or proof that a release build still works.

## Report

Lead with:

- current evidence and its exact variant/path;
- whether the result is quantitative or heuristic;
- configuration findings ordered by likely value and regression risk;
- the smallest safe next experiment, expected measurement, and required tests;
- missing release, device, SDK, or Store evidence.

Keep package-byte estimates separate from R8 configuration scores. If an app-size
baseline, artifact diff, or Store download estimate becomes the main task, route
that work to `flutter-app-size`.
