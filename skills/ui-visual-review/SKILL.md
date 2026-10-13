---
name: ui-visual-review
description: Inspect rendered UI across relevant viewports and states, check layout and interactions, and deliver annotated screenshot evidence. Use for visual QA, responsive layout review, and screenshot acceptance of existing web or app interfaces. Do not use for screenshot capture alone, designing a new UI, or unit/widget test authoring alone.
---

# UI Visual Review

Deliver inspectable evidence of the actual interface, with findings tied to the
page, state, and constraints observed. Keep the review proportional to the change.

## Establish the Review Context

- Read applicable project instructions and the nearest maintained design, test,
  and page documentation. Read an existing preview guide when relevant. Derive
  expected behavior from those sources or the user, not from current output alone.
- Obtain the target entry, representative states, ready cues, supported sizes,
  first-screen requirements, and permitted execution scope from the project.
  Do not require particular filenames or create preview documents by default.
- Honor user-specified sizes and project defaults. Otherwise choose representative
  narrow, ordinary, and wide viewports for the interface; add short windows,
  breakpoint neighbors, long/localized text, text scaling, keyboard pressure,
  safe areas, or orientation changes only where they expose relevant risks.
  State consequential assumptions; no universal phone-size matrix is required.
- Use existing scoped authorization without asking again. This skill grants no
  permission to start devices, build releases, or access live accounts, backends,
  payments, or other external state. Resolve only missing authorization needed
  for the actual next action; continue independent permitted checks.

## Use a Representative Preview

Reuse the real page, shell, theme, fonts, and assets. Replace unstable external
dependencies at a narrow boundary with existing local fixtures or mocks when
available. Do not substitute a separately drawn HTML mockup for the app under review.

Reuse a suitable existing preview serving the intended entry and state. If an
authorized new process is needed, state the command, target, and purpose first;
prefer a loopback listener for a local server. Keep an observable process session.
At completion, stop only processes started by this task and verify their children
exit, unless the user asked to retain the preview. Report a retained preview's URL
and status; do not terminate a reused or uncertain process.

Use available, documented browser or app tools. Honor the user's or project's
browser preference. When precise viewport control or capture is unavailable,
use a capable permitted tool and explain the substitution. If none is available,
report the limitation rather than inventing results or automatically installing tools.

Before capture, verify visible cues for the intended route, data, and state;
check fonts, images, and other required resources have loaded. A nonblank screen,
loading indicator, or arbitrary delay does not establish readiness. For animation,
capture a representative state and identify the phase when it affects interpretation.

## Inspect Actual Constraints and Behavior

- Set and verify each actual viewport in logical/CSS pixels. Account for toolbars,
  embedded frames, fixed chrome, and the content's real bounds. Record DPR only
  when relevant; physical screen pixels and outer-window size are not content
  constraints. Resizing a screenshot does not test responsive layout.
- Reset scroll and relevant fixture state for comparable captures. Inspect required
  first-screen content and primary actions before scrolling. For long content or
  constrained states, separately check scroll reachability and fixed-control
  obstruction. Reaching an action after scrolling does not prove a first-screen
  requirement; natural lists need not fit entirely on screen.
- Inspect screenshots yourself for clipping, overlap, unreadable text, unintended
  wrapping, image distortion, safe-area conflicts, and deviations from the supplied
  design. Use available console/runtime logs to corroborate overflow and resource
  errors; quiet logs alone do not prove the UI is correct.
- Exercise relevant local interactions where permitted. When resizing is in scope,
  check retention of input, selections, and ongoing operations. Label simulated
  insets, keyboard space, text scale, language, and other non-default parameters;
  absence of an inset is not evidence that the interface handles it.
- Report observed defects with size, state, expected behavior, and evidence. Fix
  them when the task includes repair, then repeat affected checks. In review-only
  work, report findings without changing product code. Turn important confirmed
  defects into behavior-focused regression tests when the task warrants it;
  screenshots do not replace interaction or business tests.

For Flutter, preview actual Flutter widgets with the project's entry and fixtures.
Verify browser viewport and Flutter content constraints separately when chrome or
embedding changes available space. Use existing preview support for `MediaQuery`
insets and text scaling; Web defaults do not validate native keyboard or safe areas.
Take commands and flags from the project, not from another repository's setup.

## Deliver Evidence

Save screenshots to the requested destination, otherwise a local temporary or
existing ignored directory. Inspect the final images and display them directly
when supported, labeling page, state, actual viewport, and relevant simulation
parameters. Use absolute paths for local image embeds. Supply first-screen viewport
captures for first-screen requirements; full-page or scrolled images are supplemental.
Include a reachable preview when live interaction is useful and it remains available.

Summarize checked scope, concrete findings, and untested conditions. Distinguish
executed observations, simulations, static reasoning, and user acceptance. Never
record human approval before it happens. A Web/mock screenshot supports only the
rendered state and constraints inspected; it does not establish native platform
views, media, permissions, keyboard behavior, live transactions, or release behavior.
Retain any project-required native verification as outstanding until evidenced.

Follow the project's evidence ownership for durable records. Keep run history out
of reusable skill instructions and preview configuration; do not create a goal or
new documentation hierarchy merely to store screenshots.
