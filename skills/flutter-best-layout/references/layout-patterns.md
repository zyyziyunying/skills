# Flutter Layout Patterns

Choose a pattern from the user task, content hierarchy, and scroll model. Combine patterns when needed, but keep one primary layout owner for each axis.

## Single-Column Detail or Reading Page

Use for profile/detail/settings/about/content pages where reading order matters more than density.

Structure:

- `Scaffold` with app bar or local header when navigation matters.
- `CustomScrollView` or `ListView` for the primary vertical scroll.
- Centered `ConstrainedBox` for readable content width on wide screens.
- Stable sections with local spacing, not nested cards around every section.

Prefer:

- `SliverToBoxAdapter` for mixed content.
- `SliverPadding` for page gutters.
- Max width around text and forms.

Avoid:

- Full-width paragraphs on tablets/desktops.
- A phone-only centered column when wide screens should reveal supporting content.

## Form or Checkout Page

Use for login, onboarding, edit profile, payment, settings forms, and flows with validation.

Structure:

- Primary scroll owner that survives keyboard insets.
- Constrained form width.
- Primary action either in scroll flow for short forms or pinned safely for transactional forms.
- Error text and validation states included in height planning.

Prefer:

- `MediaQuery.viewInsetsOf(context).bottom` when keyboard behavior affects layout.
- `SafeArea` around fixed actions.
- `AutofillGroup`, focus traversal, and meaningful input actions when appropriate.

Avoid:

- Fixed-height forms that break when validation messages appear.
- Submit buttons hidden behind keyboard.
- Independent scroll views inside field groups.

## Feed or List Page

Use for timelines, activity feeds, item lists, notifications, search results, and selectable rows.

Structure:

- One lazy scroll owner: usually `ListView.builder`, `CustomScrollView`, or slivers.
- Header/filter/search regions as slivers or fixed outer chrome, not nested scroll hacks.
- Empty/loading/error states that occupy intentional space.

Prefer:

- `SliverList` for mixed page chrome.
- Stable item extents only when content shape is predictable.
- Pull-to-refresh and pagination boundaries that respect the primary scroll owner.

Avoid:

- `SingleChildScrollView` plus `Column` plus `ListView.builder`.
- Blanket `shrinkWrap: true` for large or unknown lists.
- Rows with trailing actions that collapse long titles unpredictably.

## Grid or Gallery Page

Use when comparison and browsing matter: photos, products, selectable collections, cards.

Structure:

- Lazy grid with a clear tile aspect ratio.
- Max cross-axis extent when tiles should keep a preferred size.
- Explicit media fit and placeholder/error states.

Prefer:

- `SliverGridDelegateWithMaxCrossAxisExtent` for responsive tile counts.
- `AspectRatio` around media.
- Selection and hover/focus states sized into the tile.

Avoid:

- Fixed column counts copied from one screen size.
- Tiles whose text can resize the whole grid unpredictably.
- Unbounded images inside grid cells.

## Master-Detail

Use when wide screens should show a list and selected detail together, while compact screens navigate between them.

Structure:

- Compact: list route and detail route.
- Wide: list pane plus detail pane in one scaffold.
- Selection state shared outside the list item.

Prefer:

- A single breakpoint based on when both panes are useful.
- Constrained pane widths instead of equal splits by habit.
- Empty detail state when no item is selected.

Avoid:

- Rendering both panes on compact screens.
- Rebuilding unrelated pane state during selection changes.
- A sidebar wider than the useful list content.

## Media-Heavy Page

Use for image/video/story/camera/preview/detail pages where media is the anchor.

Structure:

- Reserve stable media space with `AspectRatio`, constraints, or viewport-relative bounds.
- Put controls in predictable overlays or below-media regions.
- Keep metadata/actions readable without covering important media content.

Prefer:

- Explicit `BoxFit` decisions.
- Safe-area-aware overlays.
- Placeholder/error media surfaces with the same geometry as loaded media.

Avoid:

- Letting remote image dimensions determine page geometry.
- Overlays that hide controls under system insets.
- Text blocks floating over busy media without contrast handling.

## Dashboard or Operational Screen

Use for dense, repeated decision-making surfaces: metrics, operations, CRM, admin, health, finance.

Structure:

- Prioritize scanning, comparison, and repeated action.
- Use restrained section grouping and consistent alignment.
- Increase density on wider screens only when it improves scanning.

Prefer:

- Data tables, split panes, compact filters, and clear status affordances.
- Breakpoints that add useful panels or columns.
- Consistent row heights and numeric alignment.

Avoid:

- Marketing-style hero layouts.
- Oversized cards for every metric.
- Decorative layout that reduces scan speed.

## Tool or Workspace

Use for editors, canvases, builders, inspectors, map views, and configuration tools.

Structure:

- Fixed toolbar or command region.
- Flexible work area.
- Optional side panel/inspector that appears only when space supports it.
- Clear drag, zoom, selection, and keyboard behavior when relevant.

Prefer:

- `Row`/`Column` with deliberate `Expanded` regions.
- Split panes with min/max widths.
- Canvas/work area that owns gestures without fighting parent scroll.

Avoid:

- Putting the primary work area inside decorative cards.
- Panels that can shrink below usable width.
- Gesture regions nested inside competing scrollables.

## Dialog and Bottom Sheet

Use for bounded tasks, confirmation, pickers, filters, and short creation flows.

Structure:

- Max width for dialogs and max height for sheets.
- Header and actions fixed when content can scroll.
- Internal scroll only for content, not the entire surface unless the task is short.

Prefer:

- `SafeArea` and keyboard-aware padding.
- `DraggableScrollableSheet` only when drag behavior is core to the UX.
- Clear cancellation and confirmation placement.

Avoid:

- Dialog content growing beyond viewport height.
- Bottom sheet actions hidden by keyboard or gesture nav.
- Nesting a full page scaffold inside a modal without need.
