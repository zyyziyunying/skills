# Flutter UI Preview Workflow

Use this reference only when the user or project needs an app-style UI preview, a `LAYOUT-PREVIEW.md`, mock preview data, or a live Flutter Web preview. It is not part of ordinary layout work.

## Decide Whether a Preview Document Helps

- Read an existing target-local `LAYOUT-PREVIEW.md` before preview work.
- Create one for a new previewable page or flow when route, state, mock, or judgment instructions need to be shared.
- Update it when route parameters, fixture data, mock boundaries, bypasses, ready cues, or relevant viewport expectations change.
- Skip it for small visual or local layout changes that do not change how the UI is reached or judged.

Project instructions and existing owner documents remain authoritative. Keep the document short enough to describe the current preview, not the history of building it.

## Prefer a Representative Preview

- Use the real app shell, theme, route, and page when practical.
- Replace the narrowest unstable external boundary with deterministic preview data.
- Keep production network, payment, account mutation, and unrelated native SDK behavior out of a local layout preview unless the user explicitly authorizes them.
- Make the ready check prove the expected route, data, and state are visible; a merely nonblank page is weak evidence.

Useful `LAYOUT-PREVIEW.md` facts include:

- target page and route;
- entry parameters and preview state;
- fixture, mock, cache, session, or SDK bypass boundary;
- launch command when the project allows it;
- visible cues that show the preview is ready;
- relevant viewport checks and remaining runtime or device risks.

## Manage a Live Preview Safely

Before starting another Flutter Web preview, inspect whether the same project already has a suitable preview process or listening port. Reuse it when it serves the required entry and state.

Start a new preview only when project instructions or the user allow the command. Keep it in a foreground or otherwise task-owned managed process so its descendants can be cleaned up reliably. Do not stop unrelated or uncertain processes.

At task end, stop processes started and owned by the current task. Report what was reused, started, stopped, or intentionally left running, along with any unresolved port or ownership conflict.

## Report the Evidence Boundary

State which route, state, data, and viewport were actually checked. A Web or mock preview demonstrates only that preview path; it does not prove native SDK behavior, real storefront data, purchases, backend mutation, or real-device layout.
