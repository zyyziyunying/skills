# Layout Context Roadmap

Use this reference after a concrete Flutter layout target is known in an existing repository. It defines how to obtain project-specific design and device facts before making layout decisions.

## Discovery Order

1. Start at the target file or owning feature directory and walk toward the repository or workspace root.
2. Read every applicable project-instruction file encountered on that path, nearest first, such as nested `AGENTS.md` files. A nearer instruction overrides a parent only where they conflict; it does not cancel parent execution, validation, safety, or cross-workspace rules that still apply.
3. Look for the nearest applicable `LAYOUT-CONTEXT.md`.
4. If it exists, read it completely, then read every source it marks required for the target.
5. If it does not exist, use the fallback source map below.
6. Inspect the target, its parent composition, nearby components, theme/tokens, viewport and safe-area helpers, and nearest owner documentation.
7. Complete the Context Receipt before editing or approving layout.

Do not search sibling applications, archived documents, broad architecture trees, or unrelated feature docs unless project instructions or a discovered owner source routes there.

## Project Entry Contract

Treat `LAYOUT-CONTEXT.md` as a routing document, not a second design specification. A useful project entry identifies:

- authoritative project instructions and product scope;
- the design source that owns the reference viewport and visual rules;
- the validation source that owns real devices, runtime measurements, and allowed checks;
- current-goal and nearest-owner discovery rules;
- project viewport, spacing, safe-area, typography, and layout helpers;
- preview, mock, asset-generation, and runtime boundaries when applicable;
- the fields required in the Context Receipt.

Do not copy mutable device tables, design constants, validation status, or page behavior into the routing document. Link the owning source and state what must be extracted from it.

## Fallback Source Map

When no `LAYOUT-CONTEXT.md` exists, resolve these roles from project instructions and nearby files:

| Needed fact | Likely owner | Extract |
| --- | --- | --- |
| Execution boundaries | `AGENTS.md` or equivalent | Required reads, allowed commands, runtime/device restrictions |
| Product scope | `SPEC.md`, product brief, or current goal | Supported platforms, orientations, compatibility and non-goals |
| Design baseline | `DESIGN.md`, design system, Figma brief, or tokens | Reference viewport, typography, spacing, fixed-format exceptions |
| Device and validation facts | `TEST.md`, QA/device matrix, or test owner | Logical viewports, safe areas, DPR, text scale, keyboard and evidence rules |
| Current decisions | Active `goal.html`, plan, or issue | Confirmed behavior, deferred evidence, unresolved risks |
| Local behavior | Nearest maintained README or owner doc | Scroll owner, surface contract, state and interaction rules |
| Runtime helpers | Target-adjacent code and shared UI utilities | Viewport, safe-area, spacing, breakpoints and max-width conventions |

File names are conventions, not authority by themselves. Follow the repository's declared ownership and prefer the nearest maintained source.

## Context Receipt

Record these fields before implementation or review:

```text
Target:
User task and surface type:
Project instructions read:
Authoritative design source:
Reference draft/canvas:
Supported runtime viewport or parent-constraint range:
Authoritative device/validation source:
Relevant real devices or measured logical viewports:
Orientation, safe-area, keyboard and text-scale requirements:
Primary scroll owner:
Compact / medium / wide / short-height behavior:
Existing project layout helpers and tokens:
Nearest owner and current-goal sources:
Allowed validation:
Missing facts, assumptions and deferred evidence:
```

For a narrow fix, keep the receipt concise and internal. Surface it when the task is broad, the layout structure changes, sources conflict, or an assumption affects supported behavior.

## Start Gate

Do not begin layout edits while any of these are unresolved and material:

- the draft/reference viewport is being treated as the runtime canvas;
- physical pixels are being used to infer Flutter logical dimensions;
- the target's actual parent constraints or scroll owner are unknown;
- the project declares real-device or validation facts that have not been read;
- a current goal or nearest owner document may narrow the page behavior;
- an unavailable fact would change structure, supported devices, orientation, or acceptance criteria.

Use a narrow reversible assumption only when it does not materially change scope. Record it in the receipt and final handoff. Ask for direction when alternatives would produce meaningfully different behavior.

## Evidence Gate

Before completion:

1. Recheck the implementation against the authoritative design and owner sources.
2. Use logical viewport or parent constraints, not device names or physical pixels, as layout truth.
3. Validate the project-relevant compact, medium, wide, and short-height cases. Use actual project device facts when available instead of a generic device matrix.
4. Include safe area, keyboard/viewInsets, text scale, localization, loading/error/empty states, and fixed-format media where the surface exposes those risks.
5. Report the sources used, viewport/device cases checked, evidence type, and any real-device or runtime validation still deferred.

Passing only at the reference draft size is not responsive-layout evidence.
