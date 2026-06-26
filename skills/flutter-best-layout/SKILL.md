---
name: flutter-best-layout
description: Manual-only guide for planning, reviewing, previewing, and implementing high-quality Flutter UI flows and layouts, including LAYOUT-PREVIEW.md, app-style Web preview, and API mock data for UI checks. Use only when the user explicitly invokes $flutter-best-layout.
---

# Flutter Best Layout

## Core Rule

Design the UI flow before choosing widgets. Do not treat Flutter UI work as a reflexive `Column`, `Row`, `LayoutBuilder`, breakpoint, or fake-repository exercise. First derive the layout and preview contract, then choose the smallest widget and preview structure that satisfies it.

Scale the depth of analysis to the task. For a small overflow fix, identify the scroll owner and constraints. For a new page or major UI rewrite, complete the full layout brief. For a real app page that should be checked in Web preview, define or update `LAYOUT-PREVIEW.md` according to the trigger tiers below before wiring mock data or changing code broadly.

## Required Context

Before implementing or reviewing layout in an existing repo:

- Read the nearest project instructions such as `AGENTS.md`.
- Inspect nearby pages, components, theme tokens, spacing, colors, radius, typography, navigation, and surface conventions.
- Prefer existing app widgets, design-system helpers, and local layout utilities over introducing new patterns.
- If a module has an owner README, `SPEC.md`, design doc, or goal source of truth for UI behavior, read it before changing durable behavior.
- Keep `DESIGN.md` for UI rules, visual standards, and design facts. Use `LAYOUT-PREVIEW.md` for route, mock data boundary, bypass, ready, viewport, and preview evidence instructions when app-style preview is relevant.
- If translating from Figma/CSS, treat fixed pixels as design intent, not literal Flutter constraints.

## Layout Brief

Before writing UI code, derive these decisions. Keep them internal for simple tasks; share a concise plan when the work is broad, ambiguous, or user-facing.

1. User task: Identify the main thing the user is trying to do or understand.
2. Content priority: Decide what must be visible first, what can scroll, and what can be deferred.
3. Surface type: Classify the screen as reading/detail, form, feed/list, grid/gallery, master-detail, media, dashboard, tool/workspace, dialog, sheet, or hybrid.
4. Scroll ownership: Choose exactly one primary scroll owner per axis. Decide which regions are fixed, sticky, or independently scrollable.
5. Constraint model: Define width, height, aspect-ratio, min/max, and safe-area constraints for fragile elements.
6. Adaptive behavior: Decide whether wider space should add columns, reveal side panels, increase density, preserve readable width, or keep the same layout.
7. State coverage: Account for loading, empty, error, long text, localization, text scale, keyboard, insets, and unavailable media.
8. Interaction model: Account for touch targets, keyboard traversal where relevant, gestures, scrolling, focus, and primary actions.

## UI Delivery Workflow

For new UI, screenshot/Figma restoration, or app-style preview work, treat the task as a UI delivery pipeline:

1. Design input: understand the screenshot, Figma/CSS, product description, existing page, or target route.
2. Layout brief: decide task, priority, surface type, scroll owner, constraints, responsive behavior, and states.
3. Preview contract: if this is a real app page or flow, create, update, or skip `LAYOUT-PREVIEW.md` according to the trigger tiers.
4. Real route preview: prefer the app's real route and shell over scenario-only routes.
5. Mock data: prefer the API transport/gateway boundary; for non-API pages, use the narrowest external data source or adapter boundary.
6. Web preview: use the project-allowed `main_preview.dart` or approved web-server path.
7. Ready check: rely on developer judgment, aided by route, fixture, session, cache, mock-hit, and loading facts.
8. Screenshot/layout review: inspect compact, medium, and wide viewports.
9. Validation: run allowed static checks and focused tests.
10. Evidence: report screenshots or observations, fixture changes, checks, and remaining risks.

Use `references/preview-workflow.md` when the task involves `LAYOUT-PREVIEW.md`, `main_preview.dart`, app-style Web preview, mock data, Dart raw JSON responses, SDK/service bypasses, or ready-check evidence.

## LAYOUT-PREVIEW.md Trigger Tiers

- Must create or update: new page or flow, screenshot/Figma restoration, app-style preview, real route/params/mock/bypass changes, multi-state UI work, or broad structural layout changes.
- Optional update: existing preview docs where a local UI change affects ready facts, fixture data, viewport evidence, or a medium-risk layout branch.
- Skip: tiny copy, color, spacing, icon, format, or local overflow fixes that do not change route, mock data, state reachability, scroll ownership, or responsive behavior.

## Pattern Selection

Read `references/layout-patterns.md` and `references/layout-pitfalls.md` together when creating a new screen, translating a design, making a structural layout change, or performing a complex layout fix. Use patterns to choose the structure and pitfalls to constrain the implementation. For app-style preview, also read `references/preview-workflow.md`. For a narrow review or overflow-only task, read `references/layout-pitfalls.md` first and load patterns only if the structure needs to change.

Do not default to `600px => Row/Column`. Add breakpoints only when the information architecture changes at that size. Prefer continuous constraints, slivers, max widths, grids with max extents, and aspect ratios when they express the design better than discrete branching.

## Implementation Guidance

- Use `LayoutBuilder` at the boundary where parent constraints matter; avoid scattering width checks through leaf widgets.
- Use `MediaQuery.sizeOf`, `paddingOf`, and `viewInsetsOf` for window, safe-area, and keyboard facts when those facts are actually needed.
- Prefer `CustomScrollView` and slivers for pages that mix headers, lists, grids, and pinned/flexible regions.
- Use `Expanded` and `Flexible` only after deciding how remaining space should be distributed.
- Use `ConstrainedBox`, `FractionallySizedBox`, `AspectRatio`, `SizedBox`, and `Align` to make fragile dimensions explicit.
- Keep readable text and forms constrained on wide screens; do not let content stretch just because the window is wide.
- Keep media dimensions stable with aspect ratios and fit rules; do not allow images or videos to drive unpredictable page height.
- Keep primary actions reachable without covering content. For forms, account for keyboard and validation errors before finalizing the scroll model.
- Extract small private widgets when a branch or section has its own layout responsibility. Avoid creating abstractions that only rename a `Column`.

## App-Style Preview Guidance

- Prefer real routes, real app shell, real theme, real repository/use-case, and real DTO/parser paths.
- Use a separate `main_preview.dart` when the project supports preview entrypoints. It should inject mock API transport, the narrowest external data-source adapter mocks, and explicit SDK/service bypasses without owning page logic or alternate route maps.
- Keep mock API data simple. A Dart mock API table that maps endpoint/request entries to raw JSON response providers is enough until real backend interfaces require more.
- Let raw JSON responses pass through real decode, envelope parsing, DTO parsing, repository code, and page state. Do not jump straight to view models or widget data for convenience.
- Allow hand-written fake responses when they match backend code, interface facts, or parser requirements.
- Do not package JSON fixture files as the default daily UI preview path. Captured JSON may be kept as reference evidence, but Dart raw JSON strings or response providers are the hot-reload-friendly default.
- Missing mock APIs must fail locally with method/path/query/body diagnostics. Do not silently call the real network.
- Do not bind the workflow only to HTTP. For pages driven by local DB/cache, SDK streams, local state sources, or other non-API data, mock at the smallest external boundary that still exercises the real decode/adapter/page path.
- Use SDK/service bypasses only for non-API capabilities such as payment, push, media picker, permissions, native SDKs, and system services. Record them in `LAYOUT-PREVIEW.md`.

## Pitfall Check

Read `references/layout-pitfalls.md` for any layout review, generated UI review, overflow fix, nested-scrollable change, or non-trivial layout implementation. Skip it only for tiny text/style edits that cannot affect constraints, scrolling, insets, or content size.

Actively avoid:

- `SingleChildScrollView` wrapping a large `Column` that contains lazy lists.
- `ListView` or `GridView` inside another scroll view with casual `shrinkWrap: true`.
- Hard-coded heights copied from a design when content can grow.
- Device-type or orientation checks used as layout truth.
- Wide-screen pages that simply center a narrow phone layout when a richer structure is needed.
- Wide-screen pages that stretch reading/form content beyond useful width.
- `Stack` overlays that hide scrollable content, keyboard content, or accessibility focus.
- Text without max lines, wrapping, or overflow decisions in constrained UI.
- Placeholder/demo widgets in production UI unless the task is explicitly prototyping.

## Validation

Before finishing:

- Run allowed static checks unless project instructions, user constraints, or missing dependencies explicitly defer them.
- Inspect the changed code for overflow-prone combinations listed in `layout-pitfalls.md`.
- Verify the layout path for compact, medium, and wide constraints in code reasoning or screenshots if available.
- Verify loading, empty, error, long text, and keyboard/inset behavior when they are relevant.
- For app-style preview, verify `LAYOUT-PREVIEW.md` identifies the route, mock data boundary, bypasses, fixture version, expected data IDs, auth/session source, cache isolation or cleanup, expected mock hit count, viewports, and evidence. Confirm ready check is not just "page is nonblank."
- State any runtime or device validation that remains deferred to the user.
