# [Project Name] GENERATION

Date: [YYYY-MM-DD]
Status: current generated-file fact source
Scope: `[project/path]`

This document owns generated-file rules for [project].

## Current Generated Content

[List committed generated outputs or state that none exist.]

## Ignored Generated Content

[List ignored build/generated/cache outputs.]

## Generators

For each generator, document:

1. Source files.
2. Generated output paths.
3. Command or IDE action.
4. Whether Codex may run the command.
5. Whether outputs are committed or ignored.
6. Required validation after regeneration.

## Command Boundary

Default allowed:

- Static reading and project-owned code or documentation edits.
- Generator dry-run or validation commands that do not write outside the
  project, when documented above.
- [Fast deterministic lint, schema, or targeted test commands.]

Conditionally allowed when `AGENTS.md`, `TEST.md`, `LOCAL.md`, this document,
or the current user request explicitly allows the exact command:

- Documented generators that modify project-owned generated outputs.
- [Integration, preview, browser, container, or expensive validation.]

Requires separate confirmation:

- Release, deployment, signing, publishing, or production changes.
- Account, payment, private-data, real-device, or mutable external-state flows.

## Change Rules

[State source-first editing, no hand edits to generated outputs, and doc update expectations.]
