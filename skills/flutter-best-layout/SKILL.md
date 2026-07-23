---
name: flutter-best-layout
description: Plan, review, preview, refactor, and implement high-quality Flutter UI layouts. Use when creating, reviewing, fixing, or translating Flutter UI, including responsive/adaptive layout, overflow and constraint reasoning, Figma or screenshot implementation, fixed design canvas adaptation, screen/window sizing, dialog/sheet/media/list/grid/form/master-detail surfaces, layout review/refactor, LAYOUT-PREVIEW.md, app-style Web preview, or API mock data for UI checks.
---

# Flutter Best Layout

## Core Rule

Start from the user task, content hierarchy, and parent constraints before choosing widgets. Flutter layout is constraints down, sizes up, and parent positions; use the nearest parent constraints as the layout truth for local components.

Treat a UI draft's width and height as a reference viewport by default, not as the runtime canvas. Ordinary pages must lay out against the actual logical viewport and parent constraints so they remain usable on narrower, wider, shorter, and taller devices. Use project helpers such as `context.screenWidth` and `context.screenHeight`, or `MediaQuery.sizeOf(context)`, for decisions owned by a viewport-filling page or route; use `LayoutBuilder` for a component, panel, or embedded page whose allocated size can differ from the screen.

Do not recreate the draft by fixing the whole page to its reference width/height and then centering, clipping, uniformly scaling, or fitting it. Fixed design dimensions are allowed only for genuinely fixed-format media or compositions, or when the user/project explicitly requires a fixed canvas.

Do not treat Flutter UI work as a reflexive `Column`, `Row`, `LayoutBuilder`, breakpoint, fixed Figma pixel, or fake-repository exercise. First derive the layout and preview contract, then choose the smallest widget and preview structure that satisfies it.

## Goal Gate

Before loading optional project docs or reference files, identify a concrete layout target: a file, page, route, component, screenshot/Figma node, overflow symptom, viewport, or user workflow.

If no concrete target exists, read only the required skill and project instructions needed to ask a safe question, then ask for the target or audit scope. Do not load layout references, architecture docs, owner READMEs, preview docs, or broad code context just because the task is layout-related.

Treat requests such as "check the whole app", "audit all layout", or "look over the UI" as broad audits, not as concrete targets. For broad audits or multi-page work, propose the first bounded evidence slice and ask for scope or budget confirmation before reading large optional docs, architecture docs, many owner READMEs, or broad code context.

## Project Context Gate

After identifying a concrete target in an existing repository, read `references/layout-context-roadmap.md` and complete its discovery and Context Receipt before implementing, reviewing, or refactoring layout.

- Search from the target toward the project root for the nearest `LAYOUT-CONTEXT.md`. When present, read it completely and follow every source it marks required for the target; the roadmap is navigation, not a substitute for the owning design, test, product, goal, or module documents.
- When no project layout entry exists, follow the reference's fallback discovery through project instructions, design facts, validation/device facts, product scope, current goals, nearest owner docs, and target-adjacent layout utilities.
- Do not start layout edits while the reference viewport, supported runtime range, relevant real-device/runtime evidence, parent constraints, or validation boundary is still being guessed from a screenshot or physical pixels. Resolve the fact, make a narrow reversible assumption and disclose it, or ask when the choice would materially change the result.
- Keep the receipt internal for a narrow task. Share it for broad work, ambiguous evidence, structural changes, or whenever a missing fact affects scope.

## Required Context

Before implementing or reviewing layout in an existing repo:

- Complete the Project Context Gate; reading only `LAYOUT-CONTEXT.md` is insufficient when it routes to authoritative sources.
- Inspect nearby pages, components, theme tokens, spacing, colors, radius, typography, navigation, and surface conventions.
- Prefer existing app widgets, design-system helpers, and local layout utilities over introducing new patterns.
- If a module has an owner README, `SPEC.md`, design doc, or goal source of truth for UI behavior, read it before changing durable behavior.
- Keep `DESIGN.md` for UI rules, visual standards, and design facts. Use `LAYOUT-PREVIEW.md` for route, mock data boundary, bypass, ready, viewport, and preview evidence instructions when app-style preview is relevant.
- Treat project scope tables as routing guides, not a command to read every listed document. Prefer nearest owner docs and target-adjacent code over full architecture docs unless the task spans structure, routing, ownership, app shell boundaries, or no nearer owner can be found.
- If translating from Figma/CSS, record the draft viewport separately from the target viewport range. Treat fixed pixels as design intent, not literal Flutter constraints, unless the element is demonstrably fixed-format.
- Inspect project viewport helpers such as `context.screenWidth`, `context.screenHeight`, safe-area extensions, and spacing/layout tokens before inventing a parallel responsive abstraction.

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
5. Constraint model: Separate the draft/reference viewport from the supported runtime viewport range. Define which dimensions are intrinsic, fixed-format, flexible, fractional, or min/max bounded, plus safe-area constraints for fragile elements.
6. Adaptive behavior: Decide how the compact, medium, wide, and short-height cases use their actual available space: reflow, wrap, scroll, clamp, add columns, reveal side panels, increase density, preserve readable width, or keep the same structure.
7. State coverage: Account for loading, empty, error, long text, localization, text scale, keyboard, insets, and unavailable media.
8. Interaction model: Account for touch targets, keyboard traversal where relevant, gestures, scrolling, focus, and primary actions. Anything styled like a link, button, restore action, purchase action, or disclosure must either be a real interactive affordance with semantics or be called out as a prototype shortcut.

Keep the brief internal for narrow changes. Share a concise plan when the work is broad, ambiguous, user-facing, or likely to change structure.

## Reference Routing

- Load references progressively. Start with the one reference that matches the target and add more only when the artifact or risk requires it.
- Read `references/layout-context-roadmap.md` for every concrete implementation, review, or refactor target in an existing repository; it is the mandatory project-fact discovery step, not an optional layout-pattern reference.
- Read `references/responsive-layout.md` when the task involves responsive/adaptive layout, overflow, Figma or screenshot implementation, fixed design canvas adaptation, layout review/refactor, breakpoints, `MediaQuery`, `LayoutBuilder`, text scale, localization, keyboard, safe areas, or compact/medium/wide behavior.
- Read `references/layout-patterns.md` when creating a new screen, translating a design, making a structural layout change, or choosing the primary surface pattern, scroll owner, constraint model, and adaptive strategy.
- Read `references/layout-pitfalls.md` when code or design evidence shows nested scrollables, unbounded constraints, hard-coded height/width risk, orientation/large-screen risk, keyboard/inset/safe-area risk, text/localization risk, media aspect-ratio risk, Stack/overlay collision risk, or when a non-trivial layout needs final risk review.
- Read `references/preview-workflow.md` when the task involves `LAYOUT-PREVIEW.md`, `main_preview.dart`, app-style Web preview, mock data, Dart raw JSON responses, SDK/service bypasses, or ready-check evidence.

Do not load responsive, pattern, and pitfall references together just because the task is broad. If broad UI work has no concrete target, stop at the Goal Gate. If it has a concrete target, read the first matching reference, inspect the target, then decide whether another reference is justified.

## UI Delivery Workflow

For new UI, screenshot/Figma restoration, layout refactor, or app-style preview work:

1. Complete the Project Context Gate, then understand the screenshot, Figma/CSS, product description, existing page, or target route. Record the source draft size as reference evidence and identify the actual target viewport range from project facts rather than the draft alone.
2. Classify source images and screenshots as pure media/background, reference-only, or UI that must be rebuilt. Do not place an image that still contains rebuilt live UI under final widgets unless the result is explicitly prototype-only and disclosed.
3. Complete the layout brief and classify the surface before choosing widgets.
4. Choose the primary pattern and scroll owner; introduce breakpoints only for real structure changes.
5. Translate design sizes into intrinsic sizes, aspect ratios, flexible/fractional space, bounded values, min/max constraints, padding, natural height, reflow, and scroll behavior. Do not multiply every draft coordinate by one global scale factor.
6. Implement decisions owned by a viewport-filling page or route from the actual logical viewport, using the project's `context.screenWidth`/`screenHeight` helpers or `MediaQuery` when appropriate. Implement reusable/local components, panels, and embedded pages from their parent constraints; pass down a deliberate layout mode or value instead of making leaves guess from global screen width.
7. If this is a real app page or flow, create, update, or skip `LAYOUT-PREVIEW.md` according to the trigger tiers.
8. Validate with allowed static checks, targeted tests, and project-approved preview evidence.

## LAYOUT-PREVIEW.md Trigger Tiers

- Must create or update: new page or flow, screenshot/Figma restoration, app-style preview, real route/params/mock/bypass changes, multi-state UI work, or broad structural layout changes.
- Optional update: existing preview docs where a local UI change affects ready facts, fixture data, viewport evidence, or a medium-risk layout branch.
- Skip: tiny copy, color, spacing, icon, format, or local overflow fixes that do not change route, mock data, state reachability, scroll ownership, or responsive behavior.

## Validation

Before finishing:

- Run allowed static checks unless project instructions, user constraints, or missing dependencies explicitly defer them.
- Reconcile the Context Receipt with the delivered result: state which authoritative project sources and actual viewport/device facts informed the layout, which validation sizes or device classes were checked, and which evidence remains deferred. Do not claim responsive coverage from the design viewport alone.
- Apply this core layout gate before deciding whether more reference reading is needed: the draft size is not used as a fixed page canvas; actual viewport/parent constraints drive layout; one scroll owner per axis; no fragile fixed dimensions; compact/medium/wide and relevant short-height behavior considered; text scale/localization considered; keyboard/insets/safe areas considered; loading/empty/error states considered; and interactive affordances backed by real semantics or explicitly disclosed as prototype shortcuts.
- Inspect the changed code against `references/responsive-layout.md` or `references/layout-pitfalls.md` only when those references were loaded for the task or when the core layout gate exposes unresolved risk.
- For screenshot/Figma UI with CTA, price, legal, forms, or purchase panels, smoke tests that only prove text exists are not layout validation.
- Verify compact, medium, and wide behavior by code reasoning, widget tests, or screenshots when available. For a draft-based implementation, validation at only the draft viewport is insufficient; include at least one narrower or shorter case and one wider case relevant to the product.
- Verify loading, empty, error, long text, localization, text scale, narrow width, short height, keyboard, semantics, and inset behavior when relevant.
- For app-style preview, follow `references/preview-workflow.md` and confirm the ready check is not just "page is nonblank."
- If a web-server preview was used, report preview reuse/start/stop/remaining-process evidence required by `references/preview-workflow.md`.
- If visual fidelity required prototype shortcuts such as screenshot UI used as background, fake status bars, empty callbacks, hard-coded purchase data, or non-interactive visual links, report them explicitly instead of presenting the UI as production-complete.
- State any real-device, simulator, build, backend, native SDK, or payment validation that remains deferred to the user.
