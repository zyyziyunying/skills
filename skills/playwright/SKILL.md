---
name: "playwright"
description: "Use when the task requires automating a real browser from the terminal (navigation, form filling, snapshots, screenshots, data extraction, UI-flow debugging) via `playwright-cli` or the bundled wrapper script."
---


# Playwright CLI

Drive a real browser with `playwright-cli`, preferably through the bundled wrapper. Use CLI automation for this workflow; create `@playwright/test` files only when the user requests them.

## Runtime and path

Check `command -v npx` before using the wrapper. If missing, inspect available runtimes or a supported browser tool before requiring installation. Use any alternative tool through its own documented API. If no compatible runtime exists, explain the missing Node.js/npm prerequisite; do not prescribe a global CLI install as necessary.

Resolve `PWCLI` to this skill's actual installed location, for example:

```bash
export PWCLI="${CODEX_HOME:-$HOME/.codex}/skills/playwright/scripts/playwright_cli.sh"
"$PWCLI" --help
```

The wrapper uses `npx --yes --package @playwright/cli playwright-cli`; its first use may download a package and write to npm's cache. Respect task authorization and network permissions. A global installation is optional; reuse it if the repository already standardizes on one.

## Interaction loop

```bash
"$PWCLI" open https://example.com --headed
"$PWCLI" snapshot
# Replace e3 with an element ref observed in that snapshot.
"$PWCLI" click e3
"$PWCLI" snapshot
```

Always obtain a snapshot before using element refs. Snapshot again after navigation, tab switches, menus/modals, significant DOM changes, or a stale-ref failure. Never invent live refs. For commands described but not executed, placeholders such as `eX` should be explicitly identified.

Prefer explicit commands over `eval`/`run-code`; do not bypass snapshot ref requirements with code. Use `--headed` when visual inspection helps. Scope checks and artifacts to the requested flow and relevant risks. Store repo artifacts under `output/playwright/` unless the user or project specifies another location.

## References and lifecycle

- Read [CLI reference](references/cli.md) for exact command syntax, options, tabs, and artifact commands beyond the basic loop.
- Read [workflow reference](references/workflows.md) for forms, extraction, traces, configuration, named sessions, or troubleshooting. Choose only the relevant workflow and re-snapshot points.
- Track sessions and processes started by this task. Close the task-owned browser session when finished using the CLI's documented close command. Apply command timeouts and a wall-clock watchdog where a command may hang; confirm process exit after interruption or cleanup. Do not close unrelated user sessions.
