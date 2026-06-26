# Flutter Release Agent Contract

Use a release agent contract when a Flutter project has repeatable release packaging steps that should be safe for agents to inspect and run. `PACKAGING.md` is the human-readable source of truth; the contract is the machine-readable execution surface linked from that document. The contract lives in the app repository because package identities, signing files, release scripts, environment names, upload policy, and evidence paths are project facts.

## Recommended Path

```text
tool/release_console/agent-contract.json
```

Use another path only when the project already has a release tooling convention. Link that path from `PACKAGING.md` or `AGENTS.md`.

## Field Model

Keep the contract explicit and boring. Prefer strings, booleans, arrays, and command arrays over prose.

- `schemaVersion`: integer contract version.
- `projectKind`: usually `flutter-app`, `flutter-package`, or `flutter-plugin`.
- `versionSource`: where the package version comes from, such as `pubspec.yaml version`, CI build metadata, or a release file.
- `releaseConsole`: local release-console protocol used by the generic helper.
- `status`: optional extra non-mutating discovery commands.
- `dirtyWorktreePolicy`: `block-store-release`, `warn`, or `allow`.
- `stripEnvironmentPrefixes`: environment variable prefixes that must be removed from the parent shell before starting the release console.
- `secretRedaction`: key names, environment prefixes, path fields, or log patterns that must be redacted.
- `targets`: supported package targets.

The `releaseConsole` object should describe:

- `startCommand`: exact command array to start the local console.
- `startupUrlPattern`: regex whose first capture group is the local console URL.
- `auth`: `tokenQueryParameter` when the startup URL includes a query token.
- `statusEndpoint`: GET endpoint for non-mutating status.
- `buildEndpoint`: POST endpoint for starting a build.
- `jobEndpoint`: GET endpoint template for polling a job, using `{id}`.
- `cancelEndpoint`: optional POST endpoint template for cancellation.

Each target should describe:

- `id`: stable machine-readable target id.
- `label`: human-readable target name.
- `platform`: `android`, `ios`, `web`, or another Flutter-supported platform.
- `artifactType`: APK, AAB, IPA, web build, package archive, or project-specific artifact.
- `audience`: local QA, internal testing, closed testing, production, TestFlight, App Store, Play, or package consumers.
- `storeLike`: whether this target is external/store-facing and should enforce stricter checks.
- `command`: exact command array to run when the user confirms the build.
- `requiredFiles`: file paths that must exist before running the target.
- `requiredEnvFiles`: env/config files that must exist and be validated.
- `allowedOptions`: parameters an agent may ask for and pass.
- `forbiddenOptions`: parameters an agent must not pass, usually because the project owns them elsewhere.
- `upload`: whether upload is unsupported, optional, or required, plus whether separate confirmation is required.
- `evidence`: log labels, manifest paths, artifact paths, symbol paths, and fields that should appear in final summaries.

## Rules

- Do not store secrets in the contract.
- Do not include absolute machine-local secret paths in the contract.
- Keep upload behavior explicit. Uploads should require a second confirmation unless the project rules clearly say otherwise.
- Keep the version source explicit. If `pubspec.yaml` owns the release version, forbid ad hoc version overrides.
- Keep release-console protocols in the project repo, not in a public generic skill, when the protocol is project-specific.
- Update `PACKAGING.md` when the release target set, version source, signing posture, or upload policy changes.
