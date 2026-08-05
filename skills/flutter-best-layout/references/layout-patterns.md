# Flutter Layout Patterns

Use these as options, not prescriptions. Choose the tree that most clearly explains the UI.

## Match the Relationship

- Sequential content: `Column` or `Row`.
- A child consumes remaining flex space: `Expanded` or `Flexible`.
- Siblings may reflow: `Wrap`.
- Elements intentionally overlap: `Stack` and, when needed, `Positioned`.
- Small finite content may exceed the viewport: `SingleChildScrollView`.
- Repeated or potentially large content: `ListView` or `GridView`.
- Headers, lists, grids, and collapsing regions share a scroll: `CustomScrollView` with slivers.
- A component changes composition according to its allocated space: `LayoutBuilder` at that component boundary.

## Recognize Common Shapes

- Detail, reading, or form: natural vertical flow; add scrolling when it can grow; use a meaningful `maxWidth` on wide parents.
- Feed or list: one lazy collection as the main scroll owner.
- Gallery: a lazy grid with useful tile width or aspect ratio, rather than a fixed column count copied from one screenshot.
- Header, body, bottom action: `Column`, an `Expanded` scrollable body, and a safe bottom action.
- Compact versus wide: keep one composition until extra space enables a genuinely better structure such as master-detail.
- Media: preserve meaningful proportions with `AspectRatio` and `BoxFit`; keep ordinary content in normal flow.
- Dialog or sheet: let short content size naturally; bound and scroll growing content; account for keyboard and safe area.

## Diagnose Bounded and Unbounded Axes

Find which parent supplies finite space before adding a wrapper.

- A vertical lazy list inside a bounded `Column` usually needs `Expanded` or another meaningful height bound.
- Do not use `Expanded` or `Flexible` on the same unbounded axis inside `SingleChildScrollView`.
- When a header and lazy collection scroll together, prefer one sliver-based scroll owner over nested vertical scrollables.
- Reserve `shrinkWrap` for a deliberately small nested collection; it is not a general constraint fix.

## Keep Structure Meaningful

Prefer `Padding` over an otherwise empty `Container`. Add decoration only where decoration exists. Place `LayoutBuilder` where composition changes, not around every child. Extract a widget when it has meaning, behavior, or repeated structure—not merely to shorten a build method.
