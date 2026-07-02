---
name: flutter-best-layout
description: Plan, review, preview, refactor, and implement high-quality Flutter UI layouts. Use when creating, reviewing, fixing, or translating Flutter UI, including responsive/adaptive layout, overflow and constraint reasoning, Figma or screenshot implementation, fixed design canvas adaptation, screen/window sizing, dialog/sheet/media/list/grid/form/master-detail surfaces, layout review/refactor, LAYOUT-PREVIEW.md, app-style Web preview, or API mock data for UI checks.
---

# Flutter Best Layout

## Core Rule

Start from the user task, content hierarchy, and parent constraints before choosing widgets. Flutter layout is constraints down, sizes up, and parent positions; use the nearest parent constraints as the layout truth for local components.

Do not treat Flutter UI work as a reflexive `Column`, `Row`, `LayoutBuilder`, breakpoint, fixed Figma pixel, or fake-repository exercise. First derive the layout and preview contract, then choose the smallest widget and preview structure that satisfies it.

## Required Context

Before implementing or reviewing layout in an existing repo:

- Read the nearest project instructions such as `AGENTS.md`.
- Inspect nearby pages, components, theme tokens, spacing, colors, radius, typography, navigation, and surface conventions.
- Prefer existing app widgets, design-system helpers, and local layout utilities over introducing new patterns.
- If a module has an owner README, `SPEC.md`, design doc, or goal source of truth for UI behavior, read it before changing durable behavior.
- Keep `DESIGN.md` for UI rules, visual standards, and design facts. Use `LAYOUT-PREVIEW.md` for route, mock data boundary, bypass, ready, viewport, and preview evidence instructions when app-style preview is relevant.
- If translating from Figma/CSS, treat fixed pixels as design intent, not literal Flutter constraints.

## Command Boundary

Use the shared Flutter command tiers for layout work:

- Default allowed: static reading, code edits, `dart analyze`, `flutter analyze`, and targeted `dart test` or `flutter test test/...` commands.
- Conditionally allowed: `flutter test integration_test`, `flutter run -d web-server`, hot reload, and screenshot/preview checks only when the nearest `AGENTS.md`, `TEST.md`, `LOCAL.md`, or current user request explicitly allows the exact command.
- Separate confirmation required: real device or simulator install/run, `flutter build`, release/package work, store/account/payment flows, and mutable backend-state flows.

Prefer code reasoning, widget tests, and project-approved Web preview for layout confidence before asking for device/runtime validation. Before any allowed `flutter run -d web-server`, read `references/preview-workflow.md` and follow its reuse, ownership, cleanup, and final reporting rules.

## Layout Brief

For a small overflow fix, identify the scroll owner and constraints. For a new page or major UI rewrite, derive these decisions before writing UI code:

1. User task: Identify the main thing the user is trying to do or understand.
2. Content priority: Decide what must be visible first, what can scroll, and what can be deferred.
3. Surface type: Classify the screen as form/flow, media-heavy, list/grid, checkout/purchase panel, dialog/sheet, master-detail, reading/detail, dashboard, tool/workspace, or hybrid.
4. Scroll ownership: Choose exactly one primary scroll owner per axis. Decide which regions are fixed, sticky, or independently scrollable.
5. Constraint model: Define width, height, aspect ratio, min/max, and safe-area constraints for fragile elements.
6. Adaptive behavior: Decide whether wider space should add columns, reveal side panels, increase density, preserve readable width, or keep the same structure.
7. State coverage: Account for loading, empty, error, long text, localization, text scale, keyboard, insets, and unavailable media.
8. Interaction model: Account for touch targets, keyboard traversal where relevant, gestures, scrolling, focus, and primary actions.

Keep the brief internal for narrow changes. Share a concise plan when the work is broad, ambiguous, user-facing, or likely to change structure.

## Reference Routing

- Read `references/responsive-layout.md` when the task involves responsive/adaptive layout, overflow, Figma or screenshot implementation, fixed design canvas adaptation, layout review/refactor, breakpoints, `MediaQuery`, `LayoutBuilder`, text scale, localization, keyboard, safe areas, or compact/medium/wide behavior.
- Read `references/layout-patterns.md` when creating a new screen, translating a design, making a structural layout change, or choosing the primary surface pattern, scroll owner, constraint model, and adaptive strategy.
- Read `references/layout-pitfalls.md` when reviewing generated UI, fixing overflow, changing nested scrollables, handling orientation/large-screen constraints, or implementing non-trivial layout.
- Read `references/preview-workflow.md` when the task involves `LAYOUT-PREVIEW.md`, `main_preview.dart`, app-style Web preview, mock data, Dart raw JSON responses, SDK/service bypasses, or ready-check evidence.

For broad UI work, load the responsive, pattern, and pitfall references together. For a narrow review or overflow-only task, load the responsive reference first and add pitfalls if the code shows scroll, inset, text, media, or viewport risk.

## UI Delivery Workflow

For new UI, screenshot/Figma restoration, layout refactor, or app-style preview work:

1. Understand the screenshot, Figma/CSS, product description, existing page, or target route.
2. Complete the layout brief and classify the surface before choosing widgets.
3. Choose the primary pattern and scroll owner; introduce breakpoints only for real structure changes.
4. Translate fixed design sizes into aspect ratios, min/max constraints, padding, natural height, and scroll behavior.
5. Implement with local constraints at the component boundary; do not scatter global screen-width guesses through leaves.
6. If this is a real app page or flow, create, update, or skip `LAYOUT-PREVIEW.md` according to the trigger tiers.
7. Validate with allowed static checks, targeted tests, and project-approved preview evidence.

## LAYOUT-PREVIEW.md Trigger Tiers

- Must create or update: new page or flow, screenshot/Figma restoration, app-style preview, real route/params/mock/bypass changes, multi-state UI work, or broad structural layout changes.
- Optional update: existing preview docs where a local UI change affects ready facts, fixture data, viewport evidence, or a medium-risk layout branch.
- Skip: tiny copy, color, spacing, icon, format, or local overflow fixes that do not change route, mock data, state reachability, scroll ownership, or responsive behavior.

## Validation

Before finishing:

- Run allowed static checks unless project instructions, user constraints, or missing dependencies explicitly defer them.
- Inspect the changed code against `references/responsive-layout.md` and `references/layout-pitfalls.md`.
- Verify compact, medium, and wide behavior by code reasoning, widget tests, or screenshots when available.
- Verify loading, empty, error, long text, localization, text scale, keyboard, and inset behavior when relevant.
- For app-style preview, verify `LAYOUT-PREVIEW.md` identifies the route, mock data boundary, bypasses, fixture version, expected data IDs, auth/session source, cache isolation or cleanup, expected mock hit count, viewports, and evidence. Confirm ready check is not just "page is nonblank."
- If a web-server preview was used, report preview reuse/start/stop/remaining-process evidence from `references/preview-workflow.md`.
- State any real-device, simulator, build, backend, native SDK, or payment validation that remains deferred to the user.
