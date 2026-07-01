# Flutter UI Preview Workflow

Use this reference when a Flutter UI task needs to move beyond a static layout specimen and into an app-style preview: real route, real theme/shell, real repository/use-case/DTO path, mock data at the API transport or narrowest external adapter boundary, and Web preview checks.

## Workflow

Treat the work as a UI delivery pipeline:

1. Design input: collect screenshot, Figma/CSS export, product description, existing page, or target route.
2. Layout brief: define user task, content priority, scroll owner, constraints, responsive behavior, and state coverage.
3. `LAYOUT-PREVIEW.md`: create, update, or skip the lightweight preview contract according to the trigger tiers below.
4. Real route preview: use the app's real route when available; avoid creating scenario-only routes.
5. Mock data: provide local responses through a mock API transport/gateway, or through the narrowest external adapter for non-API data.
6. Web preview: when project guidance or the current user request explicitly
   allows it, reuse or ownership-safely clean up an existing same-project
   web-server before running the approved preview entry and opening the target
   route.
7. Ready check: let the developer judge the UI, aided by route, fixture, session, cache, mock-hit, and loading facts.
8. Screenshot/layout review: inspect compact, medium, and wide viewports.
9. Validation: run allowed static checks and focused tests.
10. Evidence: report screenshots/viewport notes, fixture changes, checks run, and remaining device/backend risks.

## Command Boundary

Use the Flutter command tiers for preview work:

- Default allowed: static reading, code edits, `dart analyze`,
  `flutter analyze`, and targeted `dart test` / `flutter test test/...`
  commands.
- Conditionally allowed: `flutter test integration_test`,
  `flutter run -d web-server`, hot reload, and screenshot/preview checks only
  when the nearest `AGENTS.md`, `TEST.md`, `LOCAL.md`, or current user request
  explicitly allows the exact command.
- Separate confirmation required: real device or simulator install/run,
  `flutter build`, release/package work, store/account/payment flows, and
  mutable backend-state flows.

## Web-Server Lifecycle

This workflow must not leak Flutter Web preview servers. Before any allowed
`flutter run -d web-server`, run stale-preview discovery and decide whether to
reuse, stop, or start:

```sh
screen -ls
pgrep -af 'flutter|dart|frontend_server|web-server'
lsof -nP -iTCP -sTCP:LISTEN
```

Rules:

Discovery is broad; action is ownership-scoped. Classify discovered entries as
current-task-owned, same-project reusable, same-project stale/conflicting, or
unowned/unrelated before acting. Ignore self-matches from the discovery commands.

- Match existing previews by project path, command, entrypoint, screen/session
  name, listening port, parent/child relationship, and current-task records when
  those facts are available.
- For candidate PIDs, perform a second pass before classifying them:
  `ps -o pid,ppid,pgid,etime,rss,vsz,command -p <pid>`, parent/child tree inspection,
  and `lsof -nP -p <pid>` or equivalent cwd/listening-port checks.
- Reuse a live same-project preview when it serves the required entrypoint and
  route. Same-project does not mean current-task-owned.
- Stop current-task-owned previews automatically. Stop same-project
  stale/conflicting previews only when ownership or inactivity is clear enough to
  make the action safe; otherwise leave them running, report them as unowned, or
  ask for confirmation.
- If a same-project stale/conflicting/unowned preview cannot be reused or safely
  stopped, do not start another `flutter run -d web-server`. Skip preview or ask
  the user to choose after reporting the existing PID/PGID, port, command, and
  ownership uncertainty. Treat this as a blocking unresolved cleanup risk for
  preview, especially when there is memory pressure or a port conflict.
- Do not blindly allocate a new port when a same-project preview is already
  running.
- Do not start `flutter run -d web-server` with detached `screen`, `nohup`, bare
  `&`, `disown`, `setsid`, or equivalent hidden background wrappers. Use a
  current-task foreground child process or a managed current-task-owned preview
  runner with an explicit cleanup guard. If the user asks for detached
  operation, do not run it under this preview workflow; ask them to manage that
  process outside the task or choose a non-detached preview.
- When starting a preview, record the PID, process group ID, port, project path,
  and exact startup command in task-local notes or final evidence. The preview
  must run under a non-detached, current-task-owned dedicated process
  group/session, or a controlled wrapper that creates or owns an equivalent
  dedicated process group/session and can terminate all descendants. If that
  cannot be established, do not start preview. Do not leave stale process IDs as
  durable `LAYOUT-PREVIEW.md` facts.
- Install the cleanup guard, timeout owner, and record container before creating
  the process, using `trap`, `finally`, a timeout wrapper, or equivalent
  task-owned cleanup guard. Immediately after spawn, capture PID/PGID, port, and
  command inside that guard. Cleanup must cover startup failure, failed PID/PGID
  capture, ready-check failure, browser/screenshot failure, user interrupt, and
  task end.
- At task end, stop only processes owned by the current task, then rerun the
  discovery commands. Use `kill -TERM -<pgid>` only after confirming that PGID
  is dedicated to the current-task preview. Use PID-tree cleanup only for
  discovery or emergency remediation, not as the normal launch contract. Use
  `kill -KILL` only for owned processes that remain after graceful termination.
  If owned processes remain after cleanup, keep cleaning or report preview
  cleanup as failed.
- The final report must state what preview was reused, what was started, what
  was stopped, and what same-project or Flutter/Dart/frontend_server/screen
  processes or listening ports remain, including unowned related entries that
  were intentionally not touched. For each related process, report PID, PPID,
  PGID, start/elapsed time, cwd/project path, entrypoint/full command, listening
  port, RSS/VSZ or equivalent memory evidence, ownership classification, and
  action taken. Summarize remaining Flutter/Dart/frontend_server/screen memory
  footprint when available. Mark cleanup failures explicitly.

## LAYOUT-PREVIEW.md Trigger Tiers

Use `LAYOUT-PREVIEW.md` when it improves shared understanding of how to reach and judge the UI. Do not turn it into paperwork for tiny edits.

Must create or update:

- New page, new flow, screenshot/Figma restoration, or app-style preview.
- Real route, route params, mock API, external data source, SDK bypass, auth/session, cache, or ready-state behavior changes.
- Multi-state UI work where success, loading, empty, error, or long-content states need to be reachable.
- Structural layout changes that affect scroll ownership, responsive behavior, safe areas, keyboard/insets, or major first-screen priority.

Optional update:

- A preview document already exists and the change only adjusts expected evidence, viewport notes, fixture IDs, or debug facts.
- Medium-risk local layout changes where a short note would help the next UI pass.

Skip:

- Tiny copy, color, icon, spacing, or typography edits with no route, state, data, scroll, or responsive impact.
- Local overflow fixes that only change constraints inside one obvious owner and do not alter preview data.
- Pure formatting, import cleanup, or tests that do not change UI behavior.

## LAYOUT-PREVIEW.md Template

Keep this as a human-and-agent-readable document, not a complex runtime config. `DESIGN.md` should remain the home for UI rules, visual standards, and design facts; `LAYOUT-PREVIEW.md` should explain how to preview one page or flow.

```markdown
# <Page Or Flow> Layout Preview

## Page

- Target: <page name or flow name>
- Real route: `<route>`
- Entry params: `<ids, query, arguments, or none>`
- Main UI task: <what the user is trying to do or understand>

## Layout Brief

- Surface type: <form/list/grid/dashboard/media/detail/tool/hybrid>
- Content priority: <first-screen order>
- Scroll owner: <primary scroll owner per axis>
- Constraints: <width/height/aspect/safe-area rules>
- Responsive targets: compact <size>, medium <size>, wide <size>
- State coverage: <success/loading/empty/error/long content/keyboard/insets>

## Mock Data Boundary

- Primary boundary: <API transport/gateway or narrow external adapter>
- Non-API sources: <local DB/cache, SDK stream, local state source, or none>
- Fixture version: <human-readable version/date/hash>
- Expected data IDs: <ids that must appear, such as pet-001/order-123>
- Auth/session source: <anonymous/fake user/test token/local session seed>
- Cache isolation/cleanup: <fresh namespace/clear before launch/disabled/cache seed>

## Mock API

- `<METHOD> <path or endpoint>` -> `<Dart response provider>`
- `<METHOD> <path or endpoint>` -> `<Dart response provider>`

Notes:
- Response data may come from backend code, captured JSON, DTO/parser facts, or hand-written fake JSON.
- Response data must pass the real decode/DTO/parser path.
- Missing mock APIs must fail locally with method/path/query/body diagnostics.

## External Adapter Mock

- `<adapter/source>` -> `<fake response/stream/cache seed/no-op>`
- `<adapter/source>` -> `<fake response/stream/cache seed/no-op>`

Notes:
- Use this only when the page is not primarily driven by HTTP/API data.
- Mock the narrowest external boundary that still exercises real adapters, parsers, repositories, and page state.
- Examples include local DB/cache, SDK event streams, local session state, platform services, or generated local data sources.

## Bypass

- `<SDK/service/capability>`: <disabled/no-op/fake adapter/real>
- `<SDK/service/capability>`: <disabled/no-op/fake adapter/real>

## Preview Entry

- Entry file: `lib/main_preview.dart`
- Route to open: `<route>`
- Web target if allowed by project docs: `flutter run -t lib/main_preview.dart -d web-server`
- Process lifecycle: discover/reuse/cleanup per the Web-Server Lifecycle rules;
  keep PID/port records in task-local evidence, not as stale durable facts.

## Ready Check

Developer judgment is authoritative. Use debug facts only to avoid false positives:

- Route matched: <expected route>
- Fixture version: <expected version>
- Expected data IDs visible: <ids>
- Auth/session source: <expected source>
- Cache isolation/cleanup applied: <yes/no and how>
- Expected mock hit count: <number or per-endpoint counts>
- Mock hits visible/logged: <expected endpoints or adapters>
- Missing mock requests: none
- Loading state: gone or intentionally visible
- Key UI facts: <text, section, semantic node, or visual landmark>

## Evidence

- Viewports checked: <compact/medium/wide>
- Screenshots or notes: <paths or summary>
- Checks run: <format/analyze/test/manual browser check>
- Preview lifecycle: <task-local final report must list reused/started/stopped/
  remaining same-project or Flutter/Dart/frontend_server/screen processes with
  PID, PPID, PGID, start/elapsed time, cwd/project path, entrypoint/full command,
  listening port, RSS/VSZ or equivalent memory evidence, ownership
  classification, action taken, cleanup failures; do not preserve these transient
  process IDs as durable preview facts>
- Remaining risk: <device/backend/native SDK/pixel precision/etc.>
```

## Dart Mock API Table

Keep the Dart API table minimal. Do not build a scenario registry unless the app proves it needs one. The table maps real API requests to response providers; capabilities such as path parameters, query matching, body matching, pagination, uploads, and error envelopes should be added only when the backend endpoint needs them.

Conceptual shape:

```dart
final previewMockApi = MockApiTable()
  ..get('/app/v1/bootstrap', (_) => jsonResponse(bootstrapReadyJson))
  ..get('/app/v1/pets/pet-001/space', (_) => jsonResponse(petSpaceReadyJson))
  ..get(
    '/app/v1/pets/pet-001/space/runtime-manifest',
    (_) => jsonResponse(runtimeManifestReadyJson),
  );
```

Raw JSON strings are the preferred daily-editing form because they resemble backend responses, pass through `jsonDecode` and real DTO parsers, and are hot-reload friendly:

```dart
const petSpaceReadyJson = r'''
{
  "data": {
    "pet_id": "pet-001",
    "name": "Momo",
    "status": "ready"
  }
}
''';
```

Rules:

- Return API-shaped raw JSON strings or response bodies, not view models or widget data.
- Let real decode, envelope parsing, DTO parsing, and repository code run.
- Allow hand-written fake responses when they match backend or parser facts.
- Keep captured backend JSON as reference evidence when useful; do not require JSON files to be packaged as Flutter assets for day-to-day preview.
- Missing routes must fail locally with a clear diagnostic. Do not silently call the real network.

## External Data Source Mock

The main path is still API transport mock. If a page has no API boundary, mock the narrowest external data source or adapter boundary instead of inventing fake repositories across the app. The goal is still the same: reach the real page through the real route while replacing only the unstable outside world.

Good boundaries:

- Local DB/cache gateway seeded with preview rows.
- SDK stream adapter returning a fake stream payload.
- Local session/auth source returning a preview user.
- Platform service adapter returning no-op or deterministic data.

Avoid:

- View-model injection that bypasses decode, adapter, repository, or page state.
- Many named scenarios whose entry route, state setup, and fake repositories drift from real app behavior.
- Silent fallback to production network, persistent old cache, or ambient user session.

## main_preview.dart

Use a separate preview entry when the project supports app-style preview. It should:

- Start the real app shell and theme.
- Reuse the real route map.
- Inject only the mock API transport/gateway, narrow external adapter mocks, and explicit SDK/service bypasses.
- Provide a lightweight debug overlay for route, fixture version, expected data ID, auth/session, cache namespace/cleanup, mock hit/missing counts, and loading facts.
- Avoid page-specific UI logic and alternate route maps.

## Validation Notes

- Use browser screenshots for layout judgment; do not replace visual review with large hard-coded widget tests.
- Ready check is primarily developer judgment. Debug overlay facts should prevent obvious false positives, not become a full automation platform.
- Guard against stale UI by recording fixture version, expected data IDs, auth/session source, cache isolation or cleanup, and expected mock hit counts.
- Guard against stale preview servers by running lifecycle discovery before
  launch and after cleanup, and by reporting any remaining web-server,
  frontend_server, Dart, Flutter, screen session, or listening port.
- Record remaining real-device, native SDK, backend, or pixel-precision risks before finishing.
