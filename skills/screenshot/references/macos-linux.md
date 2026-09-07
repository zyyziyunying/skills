# macOS and Linux capture

Resolve `<path-to-skill>` to this skill's actual directory.

## macOS permission preflight (reduce repeated prompts)

On macOS, run the preflight helper once before window/app capture. It checks
Screen Recording permission, explains why it is needed, and requests it in one
place.

The helpers route Swift's module cache to `$TMPDIR/codex-swift-module-cache`
to avoid extra sandbox module-cache prompts.

```bash
bash <path-to-skill>/scripts/ensure_macos_permissions.sh
```

To avoid multiple sandbox approval prompts, combine preflight + capture in one
command when possible:

```bash
bash <path-to-skill>/scripts/ensure_macos_permissions.sh && \
python3 <path-to-skill>/scripts/take_screenshot.py --app "Codex"
```

For Codex inspection runs, keep the output in temp:

```bash
bash <path-to-skill>/scripts/ensure_macos_permissions.sh && \
python3 <path-to-skill>/scripts/take_screenshot.py --app "<App>" --mode temp
```

Use the bundled scripts to avoid re-deriving OS-specific commands.

## macOS and Linux (Python helper)

Run the helper from the repo root:

```bash
python3 <path-to-skill>/scripts/take_screenshot.py
```

Common patterns:

- Default location (user asked for "a screenshot"):

```bash
python3 <path-to-skill>/scripts/take_screenshot.py
```

- Temp location (Codex visual check):

```bash
python3 <path-to-skill>/scripts/take_screenshot.py --mode temp
```

- Explicit location (user provided a path or filename):

```bash
python3 <path-to-skill>/scripts/take_screenshot.py --path output/screen.png
```

- App/window capture by app name (macOS only; substring match is OK; captures all matching windows):

```bash
python3 <path-to-skill>/scripts/take_screenshot.py --app "Codex"
```

- Specific window title within an app (macOS only):

```bash
python3 <path-to-skill>/scripts/take_screenshot.py --app "Codex" --window-name "Settings"
```

- List matching window ids before capturing (macOS only):

```bash
python3 <path-to-skill>/scripts/take_screenshot.py --list-windows --app "Codex"
```

- Pixel region (x,y,w,h):

```bash
python3 <path-to-skill>/scripts/take_screenshot.py --mode temp --region 100,200,800,600
```

- Focused/active window (captures only the frontmost window; use `--app` to capture all windows):

```bash
python3 <path-to-skill>/scripts/take_screenshot.py --mode temp --active-window
```

- Specific window id (use --list-windows on macOS to discover ids):

```bash
python3 <path-to-skill>/scripts/take_screenshot.py --window-id 12345
```

The script prints one path per capture. When multiple windows or displays match, it prints multiple paths (one per line) and adds suffixes like `-w<windowId>` or `-d<display>`. View each path sequentially with the image viewer tool, and only manipulate images if needed or requested.

### Workflow examples

- "Take a look at <App> and tell me what you see": capture to temp, then view each printed path in order.

```bash
bash <path-to-skill>/scripts/ensure_macos_permissions.sh && \
python3 <path-to-skill>/scripts/take_screenshot.py --app "<App>" --mode temp
```

- "The design from Figma is not matching what is implemented": use a Figma MCP/skill to capture the design first, then capture the running app with this skill (typically to temp) and compare the raw screenshots before any manipulation.

### Multi-display behavior

An explicit output path is a base name when multiple captures match; the helper may add window/display suffixes. If the task requires exactly one file at the exact requested name, resolve the intended display, window, or region from the request and available supported capture APIs before capturing. Do not claim a suffixed multi-display file satisfies that exact-name requirement. Ordinary multi-display captures can return all actual paths without an extra question.

- On macOS, full-screen captures save one file per display when multiple monitors are connected.
- On Linux and Windows, full-screen captures use the virtual desktop (all monitors in one image); use `--region` to isolate a single display when needed.

### Linux prerequisites and selection logic

The helper automatically selects the first available tool:

1) `scrot`
2) `gnome-screenshot`
3) ImageMagick `import`

If none are available, ask the user to install one of them and retry.

Coordinate regions require `scrot` or ImageMagick `import`.

`--app`, `--window-name`, and `--list-windows` are macOS-only. On Linux, use
`--active-window` or provide `--window-id` when available.
