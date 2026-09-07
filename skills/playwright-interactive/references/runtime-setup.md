# Runtime setup

Read after confirming a real `node_repl` tool is available. The code in this reference is for that runtime, not CUA.

## One-time setup

Start with a read-only dependency check from the target workspace:

```bash
node -e "import('playwright').then(() => console.log('playwright import ok')).catch((error) => { console.error(error); process.exit(1); })"
# Electron tasks only:
node -e "import('electron').then(() => console.log('electron import ok')).catch((error) => { console.error(error); process.exit(1); })"
```

If the import succeeds, reuse that installation. Do not reinstall it.

If a dependency is missing, do not run `npm init`, `npm install`, or a browser download in the target workspace by default:

1. Reuse a compatible task-owned runtime or dependency installation when one is already available.
2. Otherwise, when the task already authorizes the required local writes and dependency download, create a task-specific temporary harness outside the target repository, install the dependency there, and attach the JavaScript runtime to that harness. Keep the exact harness path so it can be cleaned up when the task ends.
3. If the target workspace itself must own the dependency, or the temporary harness cannot satisfy module or Electron resolution, change `package.json`, a lockfile, or `node_modules` only within the user's authorized scope; ask only if that necessary mutation is not already authorized. Treat `npx playwright install chromium` as a download and cache mutation that also requires appropriate task authorization.

When switching workspaces, repeat the read-only import check. Never repeat installation automatically.

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
    `Could not load playwright from the current node_repl workspace. Run the dependency preflight and use a workspace or authorized temporary harness that owns the dependency. Original error: ${error}`
  );
}
```

Binding rules:

- Use `var` for shared top-level Playwright handles so later JS cells can reuse them.
- If a handle looks stale, verify the resource is closed or close it before clearing the binding and rerunning setup. A disconnected browser can leave a process running: inspect tracked ownership and resolve it before launching a replacement.
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
    throw new Error("Browser disconnected. Verify task-owned process exit before clearing browser and web handles and relaunching.");
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
