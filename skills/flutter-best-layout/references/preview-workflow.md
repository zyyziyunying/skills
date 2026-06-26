# Flutter UI Preview Workflow

Use this reference when a Flutter UI task needs to move beyond a static layout specimen and into an app-style preview: real route, real theme/shell, real repository/use-case/DTO path, mock data at the API transport or narrowest external adapter boundary, and Web preview checks.

## Workflow

Treat the work as a UI delivery pipeline:

1. Design input: collect screenshot, Figma/CSS export, product description, existing page, or target route.
2. Layout brief: define user task, content priority, scroll owner, constraints, responsive behavior, and state coverage.
3. `LAYOUT-PREVIEW.md`: create, update, or skip the lightweight preview contract according to the trigger tiers below.
4. Real route preview: use the app's real route when available; avoid creating scenario-only routes.
5. Mock data: provide local responses through a mock API transport/gateway, or through the narrowest external adapter for non-API data.
6. Web preview: when project guidance allows it, run the approved web-server entry and open the target route in the browser.
7. Ready check: let the developer judge the UI, aided by route, fixture, session, cache, mock-hit, and loading facts.
8. Screenshot/layout review: inspect compact, medium, and wide viewports.
9. Validation: run allowed static checks and focused tests.
10. Evidence: report screenshots/viewport notes, fixture changes, checks run, and remaining device/backend risks.

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
- Record remaining real-device, native SDK, backend, or pixel-precision risks before finishing.
