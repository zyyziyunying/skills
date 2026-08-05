---
name: flutter-best-layout
description: Design, implement, review, or fix Flutter UI layouts by choosing simple widget patterns and flexible constraints. Use for pages, components, responsive layouts, overflow problems, translating screenshots or Figma designs into Flutter, and related app-style layout previews.
---

# Flutter Best Layout

## Result

Build the UI with the simplest Flutter composition that expresses its content and interaction. Prefer natural or flexible sizing, standard widgets, and the constraints supplied by the real parent. Add fixed dimensions, breakpoints, nesting, or custom layout only when they carry clear design meaning.

Treat this skill as guidance, not a workflow or checklist. Decide from the target UI and surrounding project code.

## Think in Flutter Relationships

Remember: constraints go down, sizes go up, and parents position children. Identify the main direction, what may grow, what should wrap or scroll, and what truly overlaps; then choose the smallest useful pattern.

## Widget Palette

- Flow and remaining space: `Row`, `Column`, `Flex`, `Expanded`, `Flexible`, `Spacer`.
- Wrapping and alignment: `Wrap`, `Align`, `Center`, `Padding`, `SizedBox`.
- Meaningful bounds and proportions: `ConstrainedBox`, `FractionallySizedBox`, `AspectRatio`.
- True overlap: `Stack`, `Positioned`.
- Scrolling: `SingleChildScrollView` for small finite content, `ListView` or `GridView` for repeated content, and `CustomScrollView` with slivers for mixed sections sharing one scroll.
- Available space: `LayoutBuilder` for local parent constraints; `MediaQuery` for window, safe-area, keyboard, and text-scaling facts.
- Page and interaction structure: `Scaffold`, `SafeArea`, and the appropriate Material or Cupertino controls.

## Keep the High-Loss Boundaries

Apply only the boundaries relevant to the task:

- Let local parent constraints drive reusable components. Do not assume screen width when a component may be placed in a narrower parent.
- Treat screenshot or Figma dimensions as design evidence, not automatically as a fixed canvas. Use fixed width or height when the size is genuinely meaningful; do not freeze dynamic text, forms, panels, or pages with `SizedBox` when natural sizing, flex, wrapping, bounds, or scrolling expresses the intent.
- Prefer one clear scroll owner per axis. Resolve unbounded constraints by understanding the parent and intended scrolling behavior; do not default to nested scrollables or `shrinkWrap: true` merely to silence an error.
- Use `Stack` for real overlap, not to reproduce ordinary flowing content with coordinates.
- Preserve interaction semantics. Prefer real buttons, fields, list items, and selection controls over a painted shape plus `GestureDetector`; add `Semantics` when a custom interaction is justified.
- Validate the variation most likely to break the chosen layout, then report only what was actually observed. A screenshot, mock, or Web preview proves that rendered state and viewport, not native behavior, live data, or every device.

## Use Project Facts Without Ceremony

Follow applicable project instructions and the nearest declared source of truth for behavior, design, and validation. Inspect nearby components, theme tokens, and existing helpers before inventing new ones. Resolve or disclose a missing fact only when it could materially change the result; do not manufacture broad discovery, matrices, or documents for a simple layout change.

## Optional References

- Read [layout-patterns.md](references/layout-patterns.md) when the main composition, scroll ownership, or bounded-axis behavior is unclear.
- Read [responsive-layout.md](references/responsive-layout.md) when available space, overflow, design-frame translation, or fixed sizing needs more thought.
- Read [preview-workflow.md](references/preview-workflow.md) only when the user or project asks for an app-style preview or `LAYOUT-PREVIEW.md` decision.

Load only the reference that helps with the current problem. No reference is a gate.
