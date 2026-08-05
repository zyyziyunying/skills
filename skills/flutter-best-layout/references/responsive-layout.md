# Flutter Responsive Layout

Responsive layout means using the space a parent actually provides. It does not require a framework, many breakpoints, or proportional scaling of an entire design.

## Consider the Simplest Useful Response

Let content size naturally first. Depending on the relationship, share space with flex, reflow with `Wrap`, add a meaningful minimum or maximum, preserve a real aspect ratio, or let growing content scroll. Change composition only when the current structure stops being useful. Use exact dimensions when they have a clear purpose.

This is a set of options, not a required sequence.

## Read the Right Space

- Use `LayoutBuilder` when a component depends on space assigned by its parent.
- Use `MediaQuery` for window-level facts such as safe areas, keyboard insets, and text scaling.
- Reuse project helpers when they already expose the same fact clearly.

A reusable component may be much narrower than the screen. Avoid global screen-width decisions inside it, and avoid `LayoutBuilder` when the normal widget tree already adapts without branching.

## Give Fixed Sizes Meaning

Fixed or minimum sizes fit intentional gaps, icons, touch targets, avatars, media slots, and fixed-format artboards. They are fragile around text, localization, forms, stateful panels, and page height.

Prefer a maximum for growing content:

```dart
ConstrainedBox(
  constraints: const BoxConstraints(maxWidth: 560),
  child: const ProfileForm(),
)
```

Do not copy a design frame into a dynamic container:

```dart
const SizedBox(width: 390, height: 640, child: ProfileForm())
```

When stable proportion belongs to the content, express that fact directly:

```dart
const AspectRatio(aspectRatio: 390 / 640, child: IllustrationArtboard())
```

## Translate Design Relationships

Treat screenshot and Figma dimensions as clues about hierarchy, spacing, alignment, and proportion. Keep ordinary content in flow, preserve media with `AspectRatio` or `BoxFit`, use `Stack` only for intended overlap, and constrain readable content on wide parents. Do not scale a whole page merely to hide overflow.

## Add Breakpoints for Structural Change

A breakpoint is useful when it enables a different structure: one column becomes two panes, a drawer becomes persistent navigation, list and detail coexist, or a grid gains a column while tiles remain usable. If only spacing changes, natural layout may already be enough.

## Check the Risk You Introduced

Select variations from the layout's assumptions instead of applying a universal device matrix: narrow width for a tight row, long or scaled text for dynamic content, keyboard inset for a form, wide parent for an adaptive composition, or empty/loading/error state when structure changes.

Record the viewport, state, and data source actually observed. Static inspection is reasoning evidence; a rendered screenshot or Web preview is evidence for that state and viewport; real-device and native behavior require their own checks.
