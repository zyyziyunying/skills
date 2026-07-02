# Flutter Responsive Layout

Use this reference when implementing, reviewing, or refactoring Flutter UI where available space, overflow, fixed design dimensions, Figma/screenshot adaptation, text scale, keyboard, safe areas, or compact/medium/wide behavior matters.

## Contents

- [Decision Model](#decision-model)
- [Measurement Boundary](#measurement-boundary)
- [Breakpoints](#breakpoints)
- [Surface Classification](#surface-classification)
- [Fixed Design Canvas](#fixed-design-canvas)
- [Anti-Patterns](#anti-patterns)
- [Code Review Checklist](#code-review-checklist)
- [Refactor Checklist](#refactor-checklist)
- [Short Patterns](#short-patterns)

## Decision Model

Use Flutter's layout contract as the first principle:

- Constraints go down.
- Sizes go up.
- Parents position children.

The parent constraint is the layout truth for a local component. A child can choose a size only inside the box its parent allows, and the parent still decides where the child sits. Treat whole-window data as route-level context, not as a substitute for local constraints.

For every responsive decision, answer:

1. What is the user trying to do here?
2. Which parent owns this region's available width and height?
3. Which content must remain visible, and which content can wrap, scroll, collapse, or move?
4. Does the structure really change, or only spacing, max width, density, or tile count?

## Measurement Boundary

Use these APIs by responsibility, not by habit:

- `MediaQuery.sizeOf(context)`: whole-window or route-level facts, such as whether a scaffold can show a permanent navigation pane. Do not use it inside a reusable card, panel, or list item when the parent may allocate less space than the window.
- `MediaQuery.paddingOf(context)`: safe-area facts for top/bottom chrome, overlays, dialogs, sheets, and fixed actions.
- `MediaQuery.viewInsetsOf(context)`: keyboard and system inset facts for forms, bottom sheets, fixed checkout actions, and focused fields that must remain reachable.
- `LayoutBuilder`: local parent constraints at the boundary where a section or component must choose structure. Put it around the region that changes, not around every leaf.

Avoid using device model, hardware class, physical pixels, orientation, or global `screenWidth` as ordinary layout truth. Physical pixels matter for platform/display adapters, image processing, camera/canvas math, or exact media output, not for deciding whether a Flutter widget should be a row or column.

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

Fixed design dimensions are valid only when the thing is genuinely fixed-format:

- Artboards, diagrams, illustrations, game scenes, maps, media previews, or branded compositions may use proportional `scaleDownToFit` behavior inside bounded constraints.
- Media slots can preserve design ratios with `AspectRatio`, `FittedBox(fit: BoxFit.scaleDown)` around the fixed-format child, or explicit max constraints.
- The fixed-format child should have a clear design size and should not contain ordinary editable text, form fields, validation errors, or purchase decisions that need platform text behavior.

For text, forms, checkout/purchase panels, error states, and localized content:

- Prefer natural height.
- Use min/max constraints, padding, wrapping, max lines, overflow menus, and scroll.
- Let the primary scroll owner handle growth.
- Test with long strings, larger text scale, and keyboard/viewInsets in reasoning or widget tests.

Do not scale an entire page to make a screenshot fit. Translate the design into Flutter constraints and state behavior.

## Anti-Patterns

Treat these as review blockers unless the code has a narrow, documented reason:

- Entire page wrapped in `FittedBox`, `Transform.scale`, or a custom text-scale clamp to hide overflow.
- Fixed `SizedBox(height: ...)` around text, forms, purchase panels, validation errors, or localized content.
- `SingleChildScrollView` plus `Column` plus `ListView`/`GridView` with casual `shrinkWrap: true`.
- `Positioned` controls with magic offsets that ignore safe area, keyboard, text scale, or dynamic content.
- Global `screenWidth` or `MediaQuery.sizeOf(context).width` used inside local components that should respond to parent constraints.
- Device model, physical pixel width, or orientation checks used as default widget-structure decisions.
- Breakpoints copied as `600`/`840` without naming the structural change.
- Remote images or loaded media dimensions allowed to decide page geometry.
- Long price, title, SKU, legal, or localized strings placed in rows without `Expanded`, wrapping, max lines, or explicit overflow behavior.

## Code Review Checklist

Check these before approving or finishing a layout change:

- Layout truth: Does each responsive branch use local parent constraints or a justified route-level window fact?
- Scroll owner: Is there one primary scroll owner per axis, with lazy lists/grids kept lazy?
- Safe area: Are fixed top/bottom chrome, overlays, sheets, dialogs, and actions safe-area aware?
- Keyboard/viewInsets: Can focused fields, validation errors, purchase actions, and sheet actions remain reachable?
- Text scale and localization: Do labels, buttons, prices, legal text, and errors survive longer strings and larger text?
- Fixed design sizes: Are artboard/media/illustration dimensions separated from text/form/purchase behavior?
- Compact/medium/wide: Is behavior intentional in all three validation buckets, even if no breakpoint exists?
- States: Do loading, empty, error, unavailable media, and long-data states obey the same constraints?
- Breakpoints: Does each threshold name a structure, not a device class or magic number?
- Validation boundary: Have default static checks or targeted widget tests run, and are device/simulator/run/build checks clearly deferred when they require confirmation?

## Refactor Checklist

Use this order when fixing a fragile responsive layout:

1. Classify the surface and identify the user's primary task.
2. Mark fixed regions, scroll regions, and the primary scroll owner per axis.
3. Move global width/orientation checks to the route boundary or replace them with a `LayoutBuilder` at the component boundary.
4. Replace fixed heights around growing content with padding, min/max constraints, wrapping, and scroll.
5. Consolidate nested scrollables into slivers or bound the inner scrollable for a specific reason.
6. Add safe-area and `viewInsets` handling for fixed actions, dialogs, sheets, and forms.
7. Give media and fixed-format content stable aspect ratios or scale-down bounds.
8. Verify long strings, text scale, localization, error states, and compact/medium/wide constraints.
9. Run allowed analyze/test commands; use widget tests for deterministic size/text cases when the project has a test harness.

## Short Patterns

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
