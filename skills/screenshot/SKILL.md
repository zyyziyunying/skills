---
name: "screenshot"
description: "Use when the user explicitly asks for a desktop or system screenshot (full screen, specific app or window, or a pixel region), or when tool-specific capture capabilities are unavailable and an OS-level capture is needed."
---


# Screenshot capture

Prefer an available tool's own capture capability for its surface, such as a browser or design tool. Use OS capture for an explicit desktop/system screenshot or when an integrated capture tool cannot show the requested content. Check the actual tools and their supported APIs rather than assuming a particular connector exists.

## Save and inspect

1. Save to the user's specified path when provided.
2. For a user-requested screenshot without a path, use the OS default screenshot location.
3. For the agent's own inspection, use the temporary directory.

Use the bundled helper for the current OS; resolve its path from this skill's actual location. The helper prints one path per capture. Multiple matching windows/displays produce multiple paths with suffixes. Inspect each relevant output with the image viewer before describing its contents. Preserve raw captures; manipulate them only when needed or requested. Report the saved paths to the user.

## Platform routing

Read only the current platform's procedure before capture:

- [macOS and Linux](references/macos-linux.md): Python helper, app/window selection, regions, multi-display behavior, Linux prerequisites. On macOS, run the Screen Recording permission preflight once before app/window capture. It uses a temporary Swift module cache to reduce redundant permission prompts.
- [Windows](references/windows.md): PowerShell helper, active window, region, and supplied window handles.
- [Direct OS fallbacks](references/os-fallbacks.md): only when the bundled helper cannot run; select the current OS's commands and follow the same save-location rules.

## Recovery

For macOS no-match results, list windows for the app, confirm visibility, and retry with a discovered window ID. On Linux, check the available capture tools; region capture requires `scrot` or ImageMagick `import`. Use the platform reference for supported flags.

If capture, Swift module-cache access, or saving to the required location is blocked by sandbox permissions, use the environment's supported permission escalation for the specific command. If unavailable or rejected, report the concrete limitation instead of implying a capture succeeded or silently changing the requested destination. Keep captures scoped to the requested surface.
