---
name: "playwright-interactive"
description: "Persistent browser and Electron interaction through the `node_repl` JavaScript tool for fast iterative UI debugging with reusable Playwright handles."
---

# Playwright interactive

Use a persistent Playwright session for iterative web or Electron debugging that benefits from reusing handles. Prefer the sibling `playwright` skill for one-shot terminal browser work when available.

## Capability and dependency contract

Inspect the tools actually exposed in the session for a real `node_repl` JavaScript tool. If absent, use a tool discovery/search facility only if one is available to discover it. Do not assume `tool_search` exists.

If `node_repl` remains unavailable, use the terminal Playwright workflow for supported browser tasks, or a provided browser/CUA tool through its documented API when it fits the task. CUA JavaScript is not a Node REPL: do not run the imports, bindings, or Playwright snippets from this skill there. If no available tool supports the required Electron or persistent-runtime inspection, report that specific limit and complete any independent checks that remain possible.

Once available, use the Node REPL JavaScript tool for the session. `js_reset` destroys handles; reserve it for a stuck runtime. Run from a workspace owning compatible `playwright` (and, for Electron, `electron`) dependencies. Read [runtime setup](references/runtime-setup.md) before bootstrap: it covers read-only import checks, reuse, authorized temporary harnesses, and dependency mutation boundaries. Do not install into the target repository by default.

## Session lifecycle

- Bootstrap once; reuse top-level bindings and one named handle per relevant surface. In Node REPL use reusable `var` bindings. For a closed or stale handle, verify ownership, close any still-live resource, then clear and recreate that handle.
- Use explicit viewports for reproducible web QA. Read [web sessions](references/web-session.md) to create desktop/mobile contexts, or native-window mode when OS sizing/DPI is relevant. Close the old context before changing viewport mode. Choose dimensions based on the target, not the example values.
- Treat Electron as native-window by default. Read [Electron sessions](references/electron-session.md) for launch and restart. Use `electronApp.evaluate(...)` for main-process inspection or purpose-built diagnostics.
- Reload existing web contexts or the Electron window after renderer-only changes. Relaunch Electron after main-process, preload, startup changes, or uncertain process ownership.
- Keep needed dev servers in tracked persistent TTY sessions using the project's normal start command. Confirm the port responds before navigation. Track task-owned processes and harness paths; bounded launch/inspection commands need timeouts and a wall-clock watchdog. A yielded session is not completion.
- At task end, read [cleanup and recovery](references/cleanup-and-recovery.md), close task-owned browser/Electron resources and stop task-owned servers. Verify exit rather than assuming a swallowed close error means success. Retain a server only when requested, with ownership and stopping conditions stated. Before terminating an uncertain process, verify its PID/PGID, command, workspace, and start time; do not use broad process kills.

## QA proportional to the change

Keep a compact inventory of affected user requirements, implemented behaviors, and claims to make in the final response. Map those claims to evidence. For a narrow fix, check the changed behavior and nearby regression risks; for a new or broadly changed interface, cover the critical user flow and relevant controls/states. Select exploratory cases from plausible failure modes rather than a fixed scenario count. Expand only when failures or uncertainty justify it.

Use real user controls (click, keyboard, touch, drag) for functional signoff and confirm the visible result. For affected reversible controls, check the change and return state. `page.evaluate(...)` and `electronApp.evaluate(...)` can inspect or stage state but do not substitute for user-input validation.

For visible changes, inspect the affected states separately from functional checks, including the initial viewport and any relevant dense, post-interaction, or moving state. Check clipping, overlays, contrast, and motion where applicable. Prefer viewport screenshots; full-page captures can aid debugging. Read [screenshot guidance](references/screenshots.md) before model-bound captures or coordinate follow-up, CSS-pixel normalization, or Electron screenshots.

Capture final evidence from the exact state evaluated. Report unverified behavior plainly; do not claim broad signoff from a narrow check.
