# Electron sessions

Requires the bindings in [runtime setup](runtime-setup.md). Launch through `_electron.launch(...)` so the session owns the process. Ensure a required renderer dev server is responding before launch.

## Start or reuse an Electron session

Set `ELECTRON_ENTRY` to `.` when the current workspace is the Electron app and `package.json` already points `main` at the correct entry file.

```javascript
var ELECTRON_ENTRY = ".";

if (appWindow?.isClosed()) appWindow = undefined;

if (!appWindow && electronApp) {
  await electronApp.close();
  electronApp = undefined;
}

electronApp ??= await electronLauncher.launch({
  args: [ELECTRON_ENTRY],
});

appWindow ??= await electronApp.firstWindow();

console.log("Loaded Electron window:", await appWindow.title());
```

If the app process looks stale, inspect its ownership and state; close it and verify exit before clearing `electronApp` and `appWindow` and relaunching. A close failure requires recovery, not discarding the handle.

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
await electronApp.close();
electronApp = undefined;
appWindow = undefined;

electronApp = await electronLauncher.launch({
  args: [ELECTRON_ENTRY],
});

appWindow = await electronApp.firstWindow();
console.log("Relaunched Electron window:", await appWindow.title());
```
