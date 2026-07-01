---
name: "playwright-interactive"
description: "Persistent browser and Electron interaction through the `node_repl` JavaScript tool for fast iterative UI debugging with reusable Playwright handles."
---

# Playwright Interactive Skill

Use this skill when the task needs a persistent Playwright session across multiple iterations, especially for local web or Electron apps where reusing the same browser, page, or app window saves time.

Prefer the sibling `playwright` skill for one-shot browser automation from the terminal. Use this skill only when you want to keep handles alive between edits, reload the same surface repeatedly, or inspect renderer and Electron state interactively.

## Tool contract

- This skill assumes access to the `node_repl` JavaScript execution tool.
- If the current tool list does not already expose the `node_repl` `js` tool, use `tool_search` to load it before continuing.
- Use the `js` tool as the main execution surface.
- Treat `js_reset` as a recovery tool, not routine cleanup. Resetting the runtime destroys your Playwright handles.
- Run the JavaScript setup from the same workspace that owns the local `playwright` dependency and, for Electron apps, the local `electron` dependency.

## Preconditions

- Work from the target app workspace, not an unrelated parent directory.
- Keep any required dev server running in a persistent TTY session.
- Use short JS cells that do one thing at a time.
- Reuse top-level bindings instead of redeclaring them.

## One-time setup

Run these commands from the target workspace:

```bash
test -f package.json || npm init -y
npm install playwright
# Web-only, for headed Chromium or mobile emulation:
# npx playwright install chromium
# Electron-only, and only if the target workspace is the app itself:
# npm install --save-dev electron
node -e "import('playwright').then(() => console.log('playwright import ok')).catch((error) => { console.error(error); process.exit(1); })"
```

If you switch to a different workspace later, repeat setup there.

## Core workflow

1. Write a compact QA inventory before interacting with the app.
2. Bootstrap the shared Playwright bindings once.
3. Start or confirm the dev server in a persistent TTY session if the app needs one.
4. Launch the correct runtime and keep reusing the same handles.
5. After each code change, reload for renderer-only work or relaunch when process ownership changed.
6. Run functional QA with normal user inputs.
7. Run a separate visual QA pass.
8. Capture final artifacts only after you are looking at the exact state you want to sign off on.
9. Run cleanup only when the task is actually finished.

## QA inventory

Before testing, capture three things in a short checklist:

- The user-visible requirements in the prompt.
- The controls, states, or behaviors you actually implemented.
- The claims you expect to make in the final response.

Everything in any of those lists must map to at least one functional check, and every visible claim must map to at least one visual check.

Also add at least two short exploratory scenarios that could expose fragile behavior.

## References

Read only what you need:

- Read `references/screenshots.md` when you need model-bound screenshots, CSS-pixel normalization, viewport-fit validation, or Electron-specific screenshot capture guidance.

## Bootstrap

Run this once in the `node_repl` JS tool:

```javascript
var chromium;
var electronLauncher;
var browser;
var context;
var page;
var mobileContext;
var mobilePage;
var electronApp;
var appWindow;

try {
  ({ chromium, _electron: electronLauncher } = await import("playwright"));
  console.log("Playwright loaded");
} catch (error) {
  throw new Error(
    `Could not load playwright from the current node_repl workspace. Run the setup commands from this workspace first. Original error: ${error}`
  );
}
```

Binding rules:

- Use `var` for shared top-level Playwright handles so later JS cells can reuse them.
- If a handle looks stale, set that binding to `undefined` and rerun the relevant setup cell.
- Prefer one named handle per surface you care about (`page`, `mobilePage`, `appWindow`) over rediscovering pages every time.

## Shared helpers

```javascript
var resetWebHandles = function () {
  context = undefined;
  page = undefined;
  mobileContext = undefined;
  mobilePage = undefined;
};

var ensureWebBrowser = async function () {
  if (browser && !browser.isConnected()) {
    browser = undefined;
    resetWebHandles();
  }

  browser ??= await chromium.launch({ headless: false });
  return browser;
};

var reloadWebContexts = async function () {
  for (const currentContext of [context, mobileContext]) {
    if (!currentContext) continue;
    for (const p of currentContext.pages()) {
      await p.reload({ waitUntil: "domcontentloaded" });
    }
  }
  console.log("Reloaded existing web tabs");
};
```

Default posture:

- Keep each JS cell short and focused on one interaction burst.
- Reuse the existing top-level bindings instead of redeclaring them.
- If you need isolation, open a new page or context inside the same browser instead of resetting the whole runtime.
- For Electron, use `electronApp.evaluate(...)` only for main-process inspection or purpose-built diagnostics.

## Session mode selection

For web apps, use an explicit viewport by default.

- Use an explicit viewport for routine iteration, breakpoint checks, reproducible screenshots, and most visual QA.
- Use native-window mode (`viewport: null`) only for a separate pass when you need to validate launched window size, OS DPI behavior, or browser chrome interactions.
- Treat Electron as native-window by default.
- When switching between explicit viewport and native-window modes, close the old page and context first instead of trying to reuse them.

## Start or reuse a web session

### Desktop web context

```javascript
var TARGET_URL = "http://127.0.0.1:3000";

if (page?.isClosed()) page = undefined;

await ensureWebBrowser();
context ??= await browser.newContext({
  viewport: { width: 1600, height: 900 },
});
page ??= await context.newPage();

await page.goto(TARGET_URL, { waitUntil: "domcontentloaded" });
console.log("Loaded:", await page.title());
```

If `context` or `page` is stale, set `context = page = undefined` and rerun the cell.

### Mobile web context

```javascript
var MOBILE_TARGET_URL = typeof TARGET_URL === "string"
  ? TARGET_URL
  : "http://127.0.0.1:3000";

if (mobilePage?.isClosed()) mobilePage = undefined;

await ensureWebBrowser();
mobileContext ??= await browser.newContext({
  viewport: { width: 390, height: 844 },
  isMobile: true,
  hasTouch: true,
});
mobilePage ??= await mobileContext.newPage();

await mobilePage.goto(MOBILE_TARGET_URL, { waitUntil: "domcontentloaded" });
console.log("Loaded mobile:", await mobilePage.title());
```

If `mobileContext` or `mobilePage` is stale, set `mobileContext = mobilePage = undefined` and rerun the cell.

### Native-window web pass

```javascript
var TARGET_URL = "http://127.0.0.1:3000";

await ensureWebBrowser();

await page?.close().catch(() => {});
await context?.close().catch(() => {});
page = undefined;
context = undefined;

context = await browser.newContext({ viewport: null });
page = await context.newPage();

await page.goto(TARGET_URL, { waitUntil: "domcontentloaded" });
console.log("Loaded native window:", await page.title());
```

## Start or reuse an Electron session

Set `ELECTRON_ENTRY` to `.` when the current workspace is the Electron app and `package.json` already points `main` at the correct entry file.

```javascript
var ELECTRON_ENTRY = ".";

if (appWindow?.isClosed()) appWindow = undefined;

if (!appWindow && electronApp) {
  await electronApp.close().catch(() => {});
  electronApp = undefined;
}

electronApp ??= await electronLauncher.launch({
  args: [ELECTRON_ENTRY],
});

appWindow ??= await electronApp.firstWindow();

console.log("Loaded Electron window:", await appWindow.title());
```

If the app process looks stale, set `electronApp = appWindow = undefined` and rerun the cell.

## Reuse sessions during iteration

Keep the same session alive whenever you can.

Web renderer reload:

```javascript
await reloadWebContexts();
```

Electron renderer-only reload:

```javascript
await appWindow.reload({ waitUntil: "domcontentloaded" });
console.log("Reloaded Electron window");
```

Electron restart after main-process, preload, or startup changes:

```javascript
await electronApp.close().catch(() => {});
electronApp = undefined;
appWindow = undefined;

electronApp = await electronLauncher.launch({
  args: [ELECTRON_ENTRY],
});

appWindow = await electronApp.firstWindow();
console.log("Relaunched Electron window:", await appWindow.title());
```

## Session checklist

- Bootstrap once, then keep the same handles alive across iterations.
- Launch the target runtime from the current workspace.
- Make the code change.
- Reload or relaunch using the correct path for that change.
- Update the QA inventory if exploration reveals another visible control, state, or claim.
- Re-run functional QA.
- Re-run visual QA.
- Capture final artifacts only after the current state is the one you are evaluating.

Reload decision:

- Renderer-only change: reload the existing page or Electron window.
- Main-process, preload, or startup change: relaunch Electron.
- New uncertainty about process ownership or startup code: relaunch instead of guessing.

## Functional QA

- Use real user controls for signoff: click, keyboard, touch, drag, or equivalent Playwright input APIs.
- Verify at least one end-to-end critical flow.
- Confirm the visible result of that flow, not only internal state.
- Cover every obvious visible control at least once before signoff.
- For reversible or stateful controls, verify the full cycle: initial state, changed state, and return state.
- After scripted checks pass, do a short exploratory pass using normal input instead of only the intended path.
- `page.evaluate(...)` and `electronApp.evaluate(...)` may inspect or stage state, but they do not count as signoff input.

## Visual QA

- Treat visual QA as separate from functional QA.
- Reuse the same QA inventory; do not invent a second implicit list.
- Inspect the initial viewport before scrolling.
- Verify each visible claim in the specific state where the user would perceive it.
- Inspect dense, post-interaction, or in-motion states when they matter.
- Treat clipping, cut-off regions, unstable overlays, weak contrast, or awkward motion as failures even when the underlying flow still works.
- Prefer viewport screenshots for signoff. Use full-page captures only as secondary debugging artifacts.
- Read `references/screenshots.md` when you need model-bound screenshots, CSS-pixel normalization, or explicit viewport-fit checks.

## Dev server

For local web debugging, keep the app running in a persistent TTY session. Do not rely on one-shot background commands from a short-lived shell.

Use the project's normal start command, for example:

```bash
npm start
```

Before `page.goto(...)`, verify the chosen port is listening and the app responds.

For Electron debugging, launch the app from the JS runtime through `_electron.launch(...)` so the same session owns the process. If the Electron renderer depends on a separate dev server, keep that server running in a persistent TTY session and then relaunch or reload the Electron app from the JS runtime.

## Cleanup

Only run cleanup when the task is actually finished:

```javascript
if (electronApp) {
  await electronApp.close().catch(() => {});
}

if (mobileContext) {
  await mobileContext.close().catch(() => {});
}

if (context) {
  await context.close().catch(() => {});
}

if (browser) {
  await browser.close().catch(() => {});
}

browser = undefined;
context = undefined;
page = undefined;
mobileContext = undefined;
mobilePage = undefined;
electronApp = undefined;
appWindow = undefined;

console.log("Playwright session closed");
```

## Common failure modes

- `Cannot find module 'playwright'`: run the one-time setup in the current workspace and verify the import before using the JS tool.
- Playwright package is installed but the browser executable is missing: run `npx playwright install chromium`.
- `page.goto: net::ERR_CONNECTION_REFUSED`: make sure the dev server is still running in a persistent TTY session, recheck the port, and prefer `http://127.0.0.1:<port>`.
- `electron.launch` hangs, times out, or exits immediately: verify the local `electron` dependency, confirm the `args` target, and make sure any renderer dev server is already running before launch.
- `Identifier has already been declared`: reuse the existing top-level bindings, choose a new name, or wrap the code in `{ ... }`. Use `js_reset` only when the runtime is genuinely stuck.
- Browser launch or network operations fail immediately: confirm the workspace really owns the required dependencies and that the JS runtime is attached to the intended project.
