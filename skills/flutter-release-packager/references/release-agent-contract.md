# Flutter Release Agent Contract

Use a release agent contract when a Flutter project has repeatable release packaging steps that should be safe for agents to inspect and run. `PACKAGING.md` is the human-readable source of truth; the contract is the machine-readable execution surface linked from that document. The contract lives in the app repository because package identities, signing files, release scripts, environment names, upload policy, and evidence paths are project facts.

## Recommended Path

```text
tool/release_console/agent-contract.json
```

Use another path only when the project already has a release tooling convention. Link that path from `PACKAGING.md`; let `AGENTS.md` point readers to `PACKAGING.md` instead of duplicating packaging details.

## Field Model

Keep the contract explicit and boring. Prefer strings, booleans, arrays, and command arrays over prose.

- `schemaVersion`: integer contract version. New contracts use version 2; the
  helper retains version 1 compatibility for legacy contracts that predate Git
  identity, release records, exact target commands, and grouped evidence.
- `projectKind`: usually `flutter-app`, `flutter-package`, or `flutter-plugin`.
- `versionSource`: where the package version comes from, such as `pubspec.yaml version`, CI build metadata, or a release file.
- `releaseConsole`: local release-console protocol used by the generic helper.
- `status`: optional extra non-mutating discovery commands.
- `dirtyWorktreePolicy`: `block`, `block-store-release`, `warn`, or `allow`.
- `gitIdentity`: named/clean branch requirements, branch/tag templates, whether tags must reach an approved remote, and the separate-push-confirmation boundary.
- `releaseRecords`: optional manifest-draft, annotated-tag, append, and remote-tag-push command arrays used after a successful build.
- `stripEnvironmentPrefixes`: environment variable prefixes that must be removed from the parent shell before starting the release console.
- `secretRedaction`: key names, environment prefixes, path fields, or log patterns that must be redacted.
- `targets`: supported package targets.

The `releaseConsole` object should describe:

- `startCommand`: exact command array to start the local console.
- `startupUrlPattern`: regex whose first capture group is the complete absolute
  `http://` or `https://` local console URL, including the query string when it
  carries the auth token. Use non-capturing groups for other regex structure;
  relative, non-HTTP, empty, or unmatched first-group values are invalid.
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
- `releaseLine`: stable line such as `store` or `daily`.
- `branchTemplate`: exact named-branch shape for this target.
- `requiredFiles`: file paths that must exist before running the target.
- `requiredEnvFiles`: env/config files that must exist and be validated.
- `options`: optional typed parameter schema for agent-supplied build options.
- `allowedOptions`: compatibility allowlist for parameters an agent may pass. If `options` exists, keep `allowedOptions` in sync with the option names.
- `forbiddenOptions`: parameters an agent must not pass, usually because the project owns them elsewhere.
- `upload`: whether upload is unsupported, optional, required, which option names trigger upload, whether wait options exist, whether a condition must be true, and whether separate confirmation is required.
- `evidence`: log labels, manifest paths, artifact paths, symbol paths, upload status/log labels, and fields that should appear in final summaries.

Each `options` entry should define:

- `name`: payload key accepted by the release console.
- `type`: `boolean`, `string`, or `path`.
- `default`: default value when omitted, when the project has a documented default.
- `allowedValues`: valid string values for enum-like parameters.
- `forcedValue`: value fixed by the target that agents must not override.
- `description`: concise human-readable purpose.

The `upload` object should define:

- `supported`: whether this target can upload to an external service.
- `optional` or `required`: whether upload is selectable or mandatory for this target.
- `triggerOptions`: boolean payload keys that request upload, such as `iosUploadAfterBuild`.
- `waitOptions`: boolean payload keys that wait for remote processing after upload.
- `condition`: optional `{ "option": "...", "equals": "..." }` guard that must be satisfied before upload can run.
- `requiresSeparateConfirmation`: keep `true` unless project rules explicitly allow build confirmation to include upload.

The `evidence` object may define any `*Labels` arrays. Common labels are `artifactLabels`, `flutterOutputLabels`, `manifestLabels`, `symbolLabels`, `artifactsDirLabels`, `releaseRecordLabels`, `uploadStatusLabels`, and `uploadLogLabels`. When `requiredForSuccess: true`, define `requiredLabelGroups` as the `*Labels` keys that must each contribute at least one final log value. This applies to internal and store targets alike; keep conditional upload groups out of the required set unless upload itself is mandatory.

When present, `releaseRecords` should define:

- `draftLabels`: log labels that expose the generated record draft.
- `tagCommand`: creates or verifies the annotated local package tag for `--event-file`.
- `appendCommand`: verifies the tag and idempotently appends the draft.
- `pushCommand`: required when `gitIdentity.tagPushRequired=true`; pushes and re-verifies the tag on the approved remote.

The helper uses separate `record --confirm-record` and `push-tag --confirm-push` commands. A build or Store-upload confirmation never authorizes either Git mutation.

## Rules

- Use schema version 2 for new contracts. Version 2 requires each target's
  `platform`, `releaseLine`, `branchTemplate`, `command`, and complete
  `requiredLabelGroups` when evidence is required. Version 1 remains readable
  for existing projects, where those newer fields are optional and legacy
  required evidence means at least one non-empty configured label.
- When `gitIdentity` is present, the helper enforces its named/clean posture and
  the target's exact branch template before contacting the release console.
- Do not store secrets in the contract.
- Do not include absolute machine-local secret paths in the contract.
- Keep upload behavior explicit. Uploads should require a second confirmation unless the project rules clearly say otherwise.
- Treat `block` as absolute. Do not add a generic user override for a project-declared dirty-worktree block.
- Keep local tag/append and remote tag push separately confirmable. Required remote push must never run automatically.
- Fail closed for unknown schema versions, unknown options, malformed option/upload/evidence schema, and invalid secret redaction regex patterns.
- Keep the version source explicit. If `pubspec.yaml` owns the release version, forbid ad hoc version overrides.
- Keep release-console protocols in the project repo, not in a public generic skill, when the protocol is project-specific.
- Update `PACKAGING.md` when the release target set, version source, signing posture, or upload policy changes.
