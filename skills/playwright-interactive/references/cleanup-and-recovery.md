# Cleanup and recovery

## Cleanup

Close resources owned by this task when finished. Keep handles for any failed close so recovery can inspect the live resource; do not silently discard errors or report that all processes exited.

```javascript
var closeFailures = [];
for (const [label, resource] of [
  ["electronApp", electronApp],
  ["mobileContext", mobileContext],
  ["context", context],
  ["browser", browser],
]) {
  if (!resource) continue;
  try {
    await resource.close();
    if (label === "electronApp") electronApp = appWindow = undefined;
    if (label === "mobileContext") mobileContext = mobilePage = undefined;
    if (label === "context") context = page = undefined;
    if (label === "browser") browser = undefined;
  } catch (error) {
    closeFailures.push({ label, error: String(error) });
  }
}
console.log({ closeFailures });
```

Resolve any failures and verify task-owned process exit before clearing residual handles. Stop tracked dev-server sessions and clean up a task-created temporary harness when no longer needed. A successful API close does not verify an independently launched server or its descendants. On interruption, verify the exact PID/PGID, command, workspace, and start time before graceful termination, then confirm there are no descendants remaining. Retain only explicitly requested long-running processes, with ownership and stopping conditions reported.

## Common failure modes

- `Cannot find module 'playwright'`: repeat the read-only dependency check. Reuse an existing installation or use an authorized temporary harness; do not install into the target workspace by default.
- Playwright is installed but the browser executable is missing: reuse an available executable, or run `npx playwright install chromium` only when the task authorizes the download and cache mutation.
- `page.goto: net::ERR_CONNECTION_REFUSED`: make sure the dev server is still running in a persistent TTY session, recheck the port, and prefer `http://127.0.0.1:<port>`.
- `electron.launch` hangs, times out, or exits immediately: verify the local `electron` dependency, confirm the `args` target, and make sure any renderer dev server is already running before launch.
- `Identifier has already been declared`: reuse the existing top-level bindings, choose a new name, or wrap the code in `{ ... }`. Use `js_reset` only when the runtime is genuinely stuck.
- Browser launch or network operations fail immediately: confirm the workspace really owns the required dependencies and that the JS runtime is attached to the intended project.
