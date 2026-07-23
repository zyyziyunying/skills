# Flutter Responsive Layout

Use this reference when implementing, reviewing, or refactoring Flutter UI where available space, overflow, fixed design dimensions, Figma/screenshot adaptation, text scale, keyboard, safe areas, or compact/medium/wide behavior matters.

## Contents

- [Decision Model](#decision-model)
- [Measurement Boundary](#measurement-boundary)
- [Translating a Reference Draft](#translating-a-reference-draft)
- [Breakpoints](#breakpoints)
- [Surface Classification](#surface-classification)
- [Fixed Design Canvas](#fixed-design-canvas)
- [Anti-Patterns](#anti-patterns)
- [Code Review Checklist](#code-review-checklist)
- [Default Layout Gate](#default-layout-gate)
- [Refactor Checklist](#refactor-checklist)
- [Short Patterns](#short-patterns)

## Decision Model

Use Flutter's layout contract as the first principle:

- Constraints go down.
- Sizes go up.
- Parents position children.

The actual logical viewport is the layout truth for a top-level page or route that fills it. The parent constraint is the layout truth for a local component, panel, or embedded page. A child can choose a size only inside the box its parent allows, and the parent still decides where the child sits. A Figma frame or screenshot size is reference evidence, not a third source of runtime constraints.

Use the measurement boundary that owns the decision:

- At a viewport-filling page or route boundary, use project helpers such as `context.screenWidth` and `context.screenHeight`, or `MediaQuery.sizeOf(context)`, to respond to the actual logical viewport.
- At a reusable section, component, panel, or embedded-page boundary, use `LayoutBuilder` or constraints supplied by the parent because it may receive less space than the screen.
- For a genuinely fixed-format illustration, artboard, media slot, game scene, diagram, or canvas, preserve its internal coordinate system inside responsive outer bounds.

For every responsive decision, answer:

1. What is the user trying to do here?
2. Which parent owns this region's available width and height?
3. Which content must remain visible, and which content can wrap, scroll, collapse, or move?
4. Does the structure really change, or only spacing, max width, density, or tile count?
5. Which facts came from the reference draft, and how should each one behave when the runtime viewport differs?

## Measurement Boundary

Use these APIs by responsibility, not by habit:

- Project helpers such as `context.screenWidth` and `context.screenHeight`: preferred when the project already defines them and the decision belongs to a viewport-filling page/route or the whole window. Use them for responsive outer page padding, readable-width bounds, top-level composition, or short-height handling; do not use them when navigation chrome, panes, dialogs, or another parent allocate a smaller region, and do not use them to freeze the page at the draft size.
- `MediaQuery.sizeOf(context)`: the framework equivalent for whole-window or route-level facts, such as whether a scaffold can show a permanent navigation pane. Do not use it inside a reusable card, panel, or list item when the parent may allocate less space than the window.
- `MediaQuery.paddingOf(context)`: safe-area facts for top/bottom chrome, overlays, dialogs, sheets, and fixed actions.
- `MediaQuery.viewInsetsOf(context)`: keyboard and system inset facts for forms, bottom sheets, fixed checkout actions, and focused fields that must remain reachable.
- `LayoutBuilder`: local parent constraints at the boundary where a section or component must choose structure. Put it around the region that changes, not around every leaf.

Avoid using device model, hardware class, physical pixels, or orientation as ordinary layout truth. Do not reject `screenWidth` categorically: it is appropriate viewport-level layout truth when it exposes the space owned by the decision. The anti-pattern is using global width inside a local component or embedded page that may be narrower than the window, or treating one reference width as if every device had that canvas. Physical pixels matter for platform/display adapters, image processing, camera/canvas math, or exact media output, not for ordinary widget layout.

## Translating a Reference Draft

Assume the draft is a reference unless the user or project explicitly calls it a fixed canvas.

Classify each measurement before implementation:

| Draft evidence | Runtime translation |
| --- | --- |
| Page/frame width and height | Replace with actual logical viewport and safe-area/inset facts. Never force the page back to the draft frame. |
| Content margins and gutters | Use project spacing tokens, compact/medium/wide values, or bounded interpolation based on actual available width. |
| Full-width regions | Use the available parent width, not the draft pixel width. |
| Cards, forms, reading columns | Use natural width on compact screens and a justified `maxWidth` on wider screens. |
| Hero/media rectangles | Preserve meaningful aspect ratio while bounding width/height and choosing an intentional `BoxFit`. |
| Rows of content | Wrap, scroll, reflow, or change column count when children no longer have usable width. |
| Vertical placement | Prefer normal flow, flexible space, slivers, and scroll. Treat short height and keyboard insets as first-class cases. |
| Typography | Use theme/type tokens and respect `TextScaler`; do not scale all font sizes from draft width. |
| Icons, touch targets, hairlines | Usually keep semantic/design-token sizes stable unless the design system explicitly defines responsive variants. |
| Fixed-format artboard coordinates | Keep the internal coordinate system only inside responsive outer constraints; use scale-down/crop behavior deliberately. |

Do not mechanically apply `draftValue * actualWidth / draftWidth` to every coordinate. That reproduces a uniformly scaled screenshot, makes height and text behavior fragile, and often fails on different aspect ratios. Prefer actual constraints plus bounded values, `Expanded`/`Flexible`, `FractionallySizedBox`, `AspectRatio`, `ConstrainedBox`, wrapping, and intentional structural branches.

## Breakpoints

A breakpoint is justified only when it names a real structural change:

- List route and detail route become master-detail.
- Bottom navigation becomes rail/navigation pane.
- Filter drawer becomes persistent side panel.
- One-column checkout becomes order summary plus form.
- Grid adds columns because tile width remains useful.

Name thresholds after the structure they enable, such as `detailPaneMinWidth`, `persistentFilterMinWidth`, or `orderSummaryAsideMinWidth`. Do not add generic `600`, `840`, `tablet`, `desktop`, or `largeScreen` branches unless the project already owns those tokens and the structure behind them is documented.

Prefer continuous constraints when the structure is unchanged:

- `ConstrainedBox` and `Align` for readable form/text width.
- `SliverGridDelegateWithMaxCrossAxisExtent` for responsive grids.
- `AspectRatio` plus `BoxFit` for stable media.
- `Flexible`/`Expanded` only after deciding which region owns remaining space.
- Padding and spacing that scale by design tokens or bounded interpolation only when the project already uses that pattern.

Treat compact, medium, and wide as validation buckets. They are not magic numbers by themselves.

## Surface Classification

Classify the page before selecting a layout pattern:

| Surface | Responsive decision |
| --- | --- |
| Form/flow | Preserve readable width, keyboard reachability, validation errors, and primary action visibility. Wider space usually centers or splits supportive content only when it helps completion. |
| Media-heavy | Keep media geometry stable with aspect ratio, safe overlays, and predictable controls. Text/action regions should not cover important media. |
| List/grid | Use one lazy scroll owner. Lists preserve row readability; grids add columns by max tile extent or a documented structural threshold. |
| Checkout/purchase panel | Keep price, terms, errors, and primary action visible and resilient to long strings. Prefer natural height, min constraints, and local overflow rules over fixed-height panels. |
| Dialog/sheet | Bound max width and max height, keep header/actions stable, make content scroll when necessary, and account for keyboard and safe areas. |
| Master-detail | Compact screens navigate between list and detail; wide screens show both only when each pane has usable width. |
| Reading/detail | Preserve comfortable line length. Extra width may add related content, metadata, or actions only when useful. |
| Dashboard/tool | Increase density or reveal panels only when it improves scanning or work. Keep command/work regions bounded and predictable. |

## Fixed Design Canvas

Fixed design dimensions are the exception. They are valid only when the user/project explicitly requires a fixed canvas or the thing is genuinely fixed-format:

- Artboards, diagrams, illustrations, game scenes, maps, media previews, or branded compositions may use proportional `scaleDownToFit` behavior inside bounded constraints.
- Media slots can preserve design ratios with `AspectRatio`, `FittedBox(fit: BoxFit.scaleDown)` around the fixed-format child, or explicit max constraints.
- The fixed-format child should have a clear design size and should not contain ordinary editable text, form fields, validation errors, or purchase decisions that need platform text behavior.

For text, forms, checkout/purchase panels, error states, and localized content:

- Prefer natural height.
- Use min/max constraints, padding, wrapping, max lines, overflow menus, and scroll.
- Let the primary scroll owner handle growth.
- Test with long strings, larger text scale, and keyboard/viewInsets in reasoning or widget tests.

Do not center, clip, letterbox, or scale an entire ordinary page to make a screenshot fit. Translate the design into Flutter constraints and state behavior, and let the page use the actual logical viewport.

For screenshot or Figma-image restoration, classify each source asset before implementation:

- Pure media/background: can be used as an image slot or fixed-format scene.
- Reference-only: should guide rebuilt Flutter layout but not ship as visible UI.
- Contains UI to rebuild: status bars, text, buttons, prices, legal links, panels, or controls must be rebuilt as Flutter widgets. Do not leave the old UI in the image and cover it with blur, wash, or duplicate widgets unless the result is explicitly prototype-only and reported as such.

## Anti-Patterns

Treat these as review blockers unless the code has a narrow, documented reason:

- Entire page wrapped in `FittedBox`, `Transform.scale`, or a custom text-scale clamp to hide overflow.
- Ordinary page fixed to the Figma/screenshot frame width or height, leaving smaller devices clipped and larger devices letterboxed or underused.
- Every coordinate derived from one `actualWidth / draftWidth` scale factor, including text and vertical positions.
- Fixed `SizedBox(height: ...)` around text, forms, purchase panels, validation errors, or localized content.
- `SingleChildScrollView` plus `Column` plus `ListView`/`GridView` with casual `shrinkWrap: true`.
- `Positioned` controls with magic offsets that ignore safe area, keyboard, text scale, or dynamic content.
- Global `screenWidth` or `MediaQuery.sizeOf(context).width` used inside local components that should respond to parent constraints. Page-level use remains valid.
- Device model, physical pixel width, or orientation checks used as default widget-structure decisions.
- Breakpoints copied as `600`/`840` without naming the structural change.
- Remote images or loaded media dimensions allowed to decide page geometry.
- Long price, title, SKU, legal, or localized strings placed in rows without `Expanded`, wrapping, max lines, or explicit overflow behavior.
- Screenshot/Figma images that still contain the same live UI being rebuilt, then hide the old UI with blur, opacity, local masking, or overlay widgets.
- Live text, price, CTA, legal links, restore actions, forms, or purchase panels placed in `Stack`/`Positioned` regions without a collision strategy for long content, large text, safe areas, and short heights.
- Underlined, colored, chevroned, or button-like text that has no tap handler, focus path, semantic action, disabled state, or explicit prototype disclosure.

## Code Review Checklist

Check these before approving or finishing a layout change:

- Layout truth: Does each responsive branch use local parent constraints or a justified route-level window fact?
- Reference status: Is the draft viewport treated as reference evidence, with the actual logical viewport driving the page? If a fixed canvas remains, is its exception explicit and bounded?
- Scroll owner: Is there one primary scroll owner per axis, with lazy lists/grids kept lazy?
- Source assets: Are screenshot/Figma images separated into clean media assets versus UI that must be rebuilt as Flutter widgets?
- Safe area: Are fixed top/bottom chrome, overlays, sheets, dialogs, and actions safe-area aware?
- Keyboard/viewInsets: Can focused fields, validation errors, purchase actions, and sheet actions remain reachable?
- Text scale and localization: Do labels, buttons, prices, legal text, and errors survive longer strings and larger text?
- Fixed design sizes: Are artboard/media/illustration dimensions separated from text/form/purchase behavior?
- Semantic affordance: Are visual links, buttons, restore actions, and purchase actions real controls with labels, focus/tap behavior, and disabled or unavailable states?
- Compact/medium/wide: Is behavior intentional in all three validation buckets, even if no breakpoint exists?
- Viewport evidence: For draft-based work, was the layout checked beyond the draft size, including a narrower or shorter case and a wider case?
- States: Do loading, empty, error, unavailable media, and long-data states obey the same constraints?
- Breakpoints: Does each threshold name a structure, not a device class or magic number?
- Prototype shortcuts: Are fake status bars, empty callbacks, screenshot-contained UI, hard-coded purchase data, and non-interactive links reported instead of presented as production-complete?
- Validation boundary: Have default static checks or targeted widget tests run, and are device/simulator/run/build checks clearly deferred when they require confirmation?

## Default Layout Gate

For Flutter UI implementation or review, run the strongest layout checks allowed by the current task before escalating to run/build/device validation.

Default allowed checks:

- Static scan: inspect changed widgets for `RenderFlex` overflow risk, fixed dimensions around growing text, unbounded nested scrollables, route-level `MediaQuery` leaking into reusable leaves, whole-page scaling, and `Stack`/`Positioned` magic offsets.
- Draft scan: reject fixed page canvases and uniform draft-to-screen scaling unless the surface is explicitly fixed-format. Confirm the route consumes the actual logical viewport through project helpers or `MediaQuery`, while local components consume parent constraints.
- Constraint reasoning: identify the primary scroll owner per axis, the nearest parent constraint for each responsive branch, and compact/medium/wide behavior even when no breakpoint exists.
- Narrow and short viewport reasoning: verify primary content and actions remain reachable under narrow width and short height; fixed top/bottom actions must account for safe area, keyboard, and scroll reachability.
- Text scale and localization reasoning: check long labels, prices, legal text, errors, CJK or German-like expansion, multiline buttons, and larger text scale. Prefer natural height, wrapping, `Expanded`, max lines, overflow menus, or scroll over page-level scaling or clamping.
- Widget-test gate: when the project has a test harness and the task allows test edits, prefer targeted `flutter test test/...` cases with constrained surface size, larger text scaling, long fixture strings when injectable, semantics checks, and `tester.takeException()` for layout exceptions.
- Semantic affordance: verify tappable-looking controls are real `Button`, `InkWell`, link recognizer, semantic action, or a `GestureDetector` paired with `Semantics`/focus behavior, labels, adequate hit area, and disabled state when unavailable.
- Visual links without actions: flag underlined text, link colors, chevrons, card rows, icons, or CTA-looking surfaces that have no handler, route, callback, semantic action, or disabled explanation.
- Fixed `Stack` collision review: for every `Stack` with `Positioned`, overlays, badges, or fixed artboard geometry, reason through narrow width, short height, large text, safe area, and dynamic content. Use `AspectRatio`, bounds, wrapping, normal flow, pinned safe actions, or scroll instead of overlapping live text/actions.

Report before finishing:

- Checks run: static scan, analyze/test, widget test, screenshot, or code reasoning.
- Viewport buckets covered: compact, medium, wide, plus any short-height or narrow-width case that matters.
- Cases explicitly deferred: preview screenshots, web-server, simulator/device, build, backend, native SDK, payment, or production data validation.

## Refactor Checklist

Use this order when fixing a fragile responsive layout:

1. Classify the surface and identify the user's primary task.
2. Mark fixed regions, scroll regions, and the primary scroll owner per axis.
3. Move global width/orientation checks to the route boundary or replace them with a `LayoutBuilder` at the component boundary.
4. Replace fixed heights around growing content with padding, min/max constraints, wrapping, and scroll.
5. Consolidate nested scrollables into slivers or bound the inner scrollable for a specific reason.
6. Add safe-area and `viewInsets` handling for fixed actions, dialogs, sheets, and forms.
7. Give media and fixed-format content stable aspect ratios or scale-down bounds.
8. Convert visual links/buttons/restore actions into real controls or disclose prototype-only affordances.
9. Verify long strings, text scale, localization, semantic affordances, error states, and compact/medium/wide constraints.
10. Run allowed analyze/test commands; use widget tests for deterministic size/text/semantics cases when the project has a test harness.

## Short Patterns

### Page-Level Viewport Adaptation

Use the project's viewport helpers at a viewport-filling page boundary when they expose logical pixels. Keep content fluid on compact screens and bound it where unlimited width would hurt readability:

```dart
@override
Widget build(BuildContext context) {
  final screenWidth = context.screenWidth;
  final screenHeight = context.screenHeight;
  final horizontalPadding = (screenWidth * 0.05).clamp(12.0, 32.0).toDouble();
  final topPadding = (screenHeight * 0.025).clamp(12.0, 24.0).toDouble();

  return SafeArea(
    child: SingleChildScrollView(
      padding: EdgeInsets.fromLTRB(
        horizontalPadding,
        topPadding,
        horizontalPadding,
        24,
      ),
      child: Align(
        alignment: Alignment.topCenter,
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 720),
          child: const ProfileForm(),
        ),
      ),
    ),
  );
}
```

The draft may have been 390 logical pixels wide, but the page is not. The page consumes the actual viewport, uses bounded rather than unlimited proportional spacing, scrolls on short devices, and avoids an over-wide form on large windows. This does not imply scaling every size from screen width. If `ProfileForm` changes structure based on the width its parent gives it, put a `LayoutBuilder` inside that component rather than reading `screenWidth` again.

### Purchase Panel Height

Avoid fixing the whole panel height when price, legal text, errors, or buttons can grow:

```dart
// Before: hides long price/legal/error text.
SizedBox(
  height: 176,
  child: PurchasePanel(order: order),
)
```

Prefer a minimum height, natural growth, and local handling for the fragile text:

```dart
ConstrainedBox(
  constraints: const BoxConstraints(minHeight: 176, maxWidth: 520),
  child: Padding(
    padding: const EdgeInsets.all(16),
    child: Column(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Expanded(child: Text(order.title)),
            const SizedBox(width: 12),
            ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 150),
              child: FittedBox(
                fit: BoxFit.scaleDown,
                alignment: Alignment.centerRight,
                child: Text(order.formattedTotal),
              ),
            ),
          ],
        ),
        if (order.errorText != null)
          Padding(
            padding: const EdgeInsets.only(top: 8),
            child: Text(order.errorText!),
          ),
        const SizedBox(height: 16),
        FilledButton(onPressed: onPay, child: const Text('Pay')),
      ],
    ),
  ),
)
```

The `FittedBox` is limited to the price slot after the panel's real constraints are defined. It is not used to scale the page or panel.

### Local Structure Branch

Use `LayoutBuilder` where the parent allocates the region:

```dart
const detailPaneMinWidth = 900.0;

LayoutBuilder(
  builder: (context, constraints) {
    final showDetailPane = constraints.maxWidth >= detailPaneMinWidth;
    if (!showDetailPane) {
      return OrderList(onOpenOrder: openOrderRoute);
    }

    return Row(
      children: [
        const SizedBox(width: 360, child: OrderListPane()),
        const VerticalDivider(width: 1),
        Expanded(child: OrderDetailPane(orderId: selectedOrderId)),
      ],
    );
  },
)
```

The threshold is named for the detail pane, not for a device size.

### Fixed-Format Illustration

Use scale-down for an illustration or artboard, not for the surrounding page:

```dart
ConstrainedBox(
  constraints: const BoxConstraints(maxWidth: 360, maxHeight: 240),
  child: FittedBox(
    fit: BoxFit.scaleDown,
    child: SizedBox(
      width: 360,
      height: 240,
      child: EmptyStateIllustration(),
    ),
  ),
)
```
