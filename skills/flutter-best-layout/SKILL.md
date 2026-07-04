---
name: flutter-best-layout
description: Plan, review, preview, refactor, and implement high-quality Flutter UI layouts. Use when creating, reviewing, fixing, or translating Flutter UI, including responsive/adaptive layout, overflow and constraint reasoning, Figma or screenshot implementation, fixed design canvas adaptation, screen/window sizing, dialog/sheet/media/list/grid/form/master-detail surfaces, layout review/refactor, LAYOUT-PREVIEW.md, app-style Web preview, or API mock data for UI checks.
---

# Flutter Best Layout

## Core Rule

Start from the user task, content hierarchy, and parent constraints before choosing widgets. Flutter layout is constraints down, sizes up, and parent positions; use the nearest parent constraints as the layout truth for local components.

Do not treat Flutter UI work as a reflexive `Column`, `Row`, `LayoutBuilder`, breakpoint, fixed Figma pixel, or fake-repository exercise. First derive the layout and preview contract, then choose the smallest widget and preview structure that satisfies it.

## Goal Gate

Before loading optional project docs or reference files, identify a concrete layout target: a file, page, route, component, screenshot/Figma node, overflow symptom, viewport, or user workflow.

If no concrete target exists, read only the required skill and project instructions needed to ask a safe question, then ask for the target or audit scope. Do not load layout references, architecture docs, owner READMEs, preview docs, or broad code context just because the task is layout-related.

Treat requests such as "check the whole app", "audit all layout", or "look over the UI" as broad audits, not as concrete targets. For broad audits or multi-page work, propose the first bounded evidence slice and ask for scope or budget confirmation before reading large optional docs, architecture docs, many owner READMEs, or broad code context.

## Required Context

Before implementing or reviewing layout in an existing repo:

- Read the nearest project instructions such as `AGENTS.md`.
- Inspect nearby pages, components, theme tokens, spacing, colors, radius, typography, navigation, and surface conventions.
- Prefer existing app widgets, design-system helpers, and local layout utilities over introducing new patterns.
- If a module has an owner README, `SPEC.md`, design doc, or goal source of truth for UI behavior, read it before changing durable behavior.
- Keep `DESIGN.md` for UI rules, visual standards, and design facts. Use `LAYOUT-PREVIEW.md` for route, mock data boundary, bypass, ready, viewport, and preview evidence instructions when app-style preview is relevant.
- Treat project scope tables as routing guides, not a command to read every listed document. Prefer nearest owner docs and target-adjacent code over full architecture docs unless the task spans structure, routing, ownership, app shell boundaries, or no nearer owner can be found.
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
8. Interaction model: Account for touch targets, keyboard traversal where relevant, gestures, scrolling, focus, and primary actions. Anything styled like a link, button, restore action, purchase action, or disclosure must either be a real interactive affordance with semantics or be called out as a prototype shortcut.

Keep the brief internal for narrow changes. Share a concise plan when the work is broad, ambiguous, user-facing, or likely to change structure.

## Reference Routing

- Load references progressively. Start with the one reference that matches the target and add more only when the artifact or risk requires it.
- Read `references/responsive-layout.md` when the task involves responsive/adaptive layout, overflow, Figma or screenshot implementation, fixed design canvas adaptation, layout review/refactor, breakpoints, `MediaQuery`, `LayoutBuilder`, text scale, localization, keyboard, safe areas, or compact/medium/wide behavior.
- Read `references/layout-patterns.md` when creating a new screen, translating a design, making a structural layout change, or choosing the primary surface pattern, scroll owner, constraint model, and adaptive strategy.
- Read `references/layout-pitfalls.md` when code or design evidence shows nested scrollables, unbounded constraints, hard-coded height/width risk, orientation/large-screen risk, keyboard/inset/safe-area risk, text/localization risk, media aspect-ratio risk, Stack/overlay collision risk, or when a non-trivial layout needs final risk review.
- Read `references/preview-workflow.md` when the task involves `LAYOUT-PREVIEW.md`, `main_preview.dart`, app-style Web preview, mock data, Dart raw JSON responses, SDK/service bypasses, or ready-check evidence.

Do not load responsive, pattern, and pitfall references together just because the task is broad. If broad UI work has no concrete target, stop at the Goal Gate. If it has a concrete target, read the first matching reference, inspect the target, then decide whether another reference is justified.

## UI Delivery Workflow

For new UI, screenshot/Figma restoration, layout refactor, or app-style preview work:

1. Understand the screenshot, Figma/CSS, product description, existing page, or target route.
2. Classify source images and screenshots as pure media/background, reference-only, or UI that must be rebuilt. Do not place an image that still contains rebuilt live UI under final widgets unless the result is explicitly prototype-only and disclosed.
3. Complete the layout brief and classify the surface before choosing widgets.
4. Choose the primary pattern and scroll owner; introduce breakpoints only for real structure changes.
5. Translate fixed design sizes into aspect ratios, min/max constraints, padding, natural height, and scroll behavior.
6. Implement with local constraints at the component boundary; do not scatter global screen-width guesses through leaves.
7. If this is a real app page or flow, create, update, or skip `LAYOUT-PREVIEW.md` according to the trigger tiers.
8. Validate with allowed static checks, targeted tests, and project-approved preview evidence.

## LAYOUT-PREVIEW.md Trigger Tiers

- Must create or update: new page or flow, screenshot/Figma restoration, app-style preview, real route/params/mock/bypass changes, multi-state UI work, or broad structural layout changes.
- Optional update: existing preview docs where a local UI change affects ready facts, fixture data, viewport evidence, or a medium-risk layout branch.
- Skip: tiny copy, color, spacing, icon, format, or local overflow fixes that do not change route, mock data, state reachability, scroll ownership, or responsive behavior.

## Validation

Before finishing:

- Run allowed static checks unless project instructions, user constraints, or missing dependencies explicitly defer them.
- Apply this core layout gate before deciding whether more reference reading is needed: one scroll owner per axis, bounded parent constraints, no fragile fixed dimensions, compact/medium/wide behavior considered, text scale/localization considered, keyboard/insets/safe areas considered, loading/empty/error states considered, and interactive affordances backed by real semantics or explicitly disclosed as prototype shortcuts.
- Inspect the changed code against `references/responsive-layout.md` or `references/layout-pitfalls.md` only when those references were loaded for the task or when the core layout gate exposes unresolved risk.
- For screenshot/Figma UI with CTA, price, legal, forms, or purchase panels, smoke tests that only prove text exists are not layout validation.
- Verify compact, medium, and wide behavior by code reasoning, widget tests, or screenshots when available.
- Verify loading, empty, error, long text, localization, text scale, narrow width, short height, keyboard, semantics, and inset behavior when relevant.
- For app-style preview, follow `references/preview-workflow.md` and confirm the ready check is not just "page is nonblank."
- If a web-server preview was used, report preview reuse/start/stop/remaining-process evidence required by `references/preview-workflow.md`.
- If visual fidelity required prototype shortcuts such as screenshot UI used as background, fake status bars, empty callbacks, hard-coded purchase data, or non-interactive visual links, report them explicitly instead of presenting the UI as production-complete.
- State any real-device, simulator, build, backend, native SDK, or payment validation that remains deferred to the user.
