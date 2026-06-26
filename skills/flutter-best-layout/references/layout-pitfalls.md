# Flutter Layout Pitfalls

Use this reference for any layout review, generated UI review, overflow fix, nested-scrollable change, or non-trivial layout implementation.

## Scroll Ownership

Bad signs:

- A `SingleChildScrollView` wraps a `Column` that contains `ListView`, `GridView`, or another large scrollable.
- `shrinkWrap: true` is used to silence layout errors without proving the list is small.
- Multiple vertical scrollables compete in the same gesture region.

Better approaches:

- Use one lazy scroll owner with slivers for mixed page content.
- Keep fixed chrome outside the scroll owner.
- Use nested scroll only when both scroll regions have a clear, bounded purpose.

## Unbounded Constraints

Bad signs:

- Flex children appear inside an unbounded scroll direction.
- Lazy scrollables are placed in `Column` without `Expanded`, `Flexible`, or explicit height.
- Widgets rely on parent size that is infinite in the active axis.

Better approaches:

- Put scrollables in `Expanded` when they fill remaining space.
- Use `SizedBox`, `ConstrainedBox`, or slivers to provide bounds.
- Move mixed content into a single `CustomScrollView`.

## Hard-Coded Dimensions

Bad signs:

- Heights copied from a mockup for text-heavy or localized content.
- Buttons, cards, images, or headers have fixed sizes without min/max reasoning.
- Layout breaks when text scale, validation errors, or longer data appears.

Better approaches:

- Prefer natural sizing, loose constraints, min/max constraints, padding, and aspect ratios before fixed dimensions.
- Reserve fixed dimensions only for genuinely fixed-format UI.
- Define overflow, wrapping, and max-line behavior explicitly.

## Expensive Measurement and Scaling Hacks

Bad signs:

- `IntrinsicHeight` or `IntrinsicWidth` is used inside long lists, grids, repeated cards, or deeply nested layout.
- `FittedBox`, `Transform.scale`, or text scaling wrappers are used to hide overflow instead of designing wrapping, scrolling, or constraints.
- Post-frame measurement, `GlobalKey` size reads, or layout callbacks are used to drive ordinary responsive layout.
- Layout fixes depend on measuring rendered children instead of expressing constraints in the parent.

Better approaches:

- Express the intended bounds with `Expanded`, `Flexible`, `AspectRatio`, `ConstrainedBox`, slivers, or max widths before reaching for intrinsic measurement.
- Use intrinsic widgets only for small, bounded, low-frequency surfaces where the cost and behavior are intentional.
- Fix text and action overflow with wrapping, max lines, priority rules, overflow menus, or responsive reflow rather than shrinking the entire child.

## Breakpoints and Orientation

Bad signs:

- Layout switches because the device is a phone/tablet instead of because available space changed.
- Orientation is used as a proxy for width.
- `600` is used as a magic breakpoint without explaining what changes at that size.

Better approaches:

- Use parent constraints from `LayoutBuilder` where the layout boundary matters.
- Use breakpoints only when the UI structure meaningfully changes.
- Prefer continuous sizing, max widths, and max grid extents when they fit the problem.

## Wide-Screen Behavior

Bad signs:

- A narrow phone layout is simply centered on a large screen when extra space could improve the task.
- Text and forms stretch across the whole window.
- Dense pages become decorative card grids with poor scanability.

Better approaches:

- Preserve readable width for text and forms.
- Add supporting panes, detail views, filters, or denser grids only when they improve use.
- Use master-detail or split panes for selection-heavy flows.

## Keyboard, Insets, and Safe Areas

Bad signs:

- Primary actions are covered by the keyboard.
- Bottom sheets ignore gesture navigation or safe-area padding.
- Focused fields can be hidden during validation.

Better approaches:

- Account for `MediaQuery.viewInsetsOf(context).bottom` when keyboard affects the surface.
- Wrap fixed bottom regions with `SafeArea`.
- Keep form content scrollable enough to reveal focused fields and errors.

## Text and Localization

Bad signs:

- Constrained rows contain long text without `Expanded`, wrapping, max lines, or overflow.
- Labels assume English length.
- Large text scale causes button or card overflow.

Better approaches:

- Decide whether text wraps, truncates, or moves to a second line.
- Use `Expanded` around flexible text in rows.
- Test with long strings and larger text scale in reasoning or local UI checks when available.

## Media and Aspect Ratios

Bad signs:

- Remote images decide layout size after loading.
- Grid tiles resize based on text or image dimensions.
- Overlays cover key content or system insets.

Better approaches:

- Use `AspectRatio` or fixed constraints for media slots.
- Keep placeholders and error states the same geometry as loaded content.
- Use explicit `BoxFit` and clipping decisions.

## Stack and Overlay Layouts

Bad signs:

- `Stack` positions controls over content without reserving tappable or readable space.
- Positioned elements use magic offsets that fail on insets or text scale.
- Overlay actions intercept scroll or focus unexpectedly.

Better approaches:

- Use safe-area-aware positioning.
- Reserve content padding for overlays when the underlying content scrolls.
- Prefer normal layout flow unless overlay behavior is truly needed.

## Finish Checklist

Before finishing a layout change, verify:

- One primary scroll owner per axis is clear.
- Compact, medium, and wide constraints have intentional behavior.
- Loading, empty, error, and long-content states fit the same layout contract.
- Keyboard and safe-area behavior is accounted for when relevant.
- Images and fixed-format elements have stable geometry.
- Intrinsic measurement, `FittedBox`, and post-frame measurement hacks are absent or explicitly justified.
- Wide screens either add useful structure or preserve comfortable content width.
- Any remaining device/runtime validation is explicitly deferred.
