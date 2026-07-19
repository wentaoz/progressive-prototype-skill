# Pencil output workflow

Produce an editable `.pen` file as the visual alternative when Pencil is requested or Figma is unavailable.

## Prerequisites

Check `pencil version`, the latest registry version, and `pencil status` once per session. Require an authenticated Pencil user and Codex-capable agent configuration. Save output in the user's project or a `designs/` directory, never in a temporary directory.

Use Pencil MCP for structural reads and deterministic edits when the desktop editor is connected. Call `get_editor_state(include_schema: true)` before other Pencil MCP tools. Never read or grep an encrypted `.pen` file directly.

## Create

Pass the user's request unchanged as the CLI prompt. Attach `PROTOTYPE.md` and [visual-output-contract.md](visual-output-contract.md) as prompt files so the Pencil agent receives the semantic source and editability requirements without expanding the user's creative request.

Use this shape:

```bash
pencil --out designs/<product>.pen \
  --prompt "<exact user request>" \
  --prompt-file <path-to-PROTOTYPE.md> \
  --prompt-file <skill-directory>/references/visual-output-contract.md \
  --agent codex \
  --export designs/<product>.png \
  --export-scale 2
```

Tell the user generation can take several minutes. Show the exported preview after completion.

## Structure

- Create every screen as a separate top-level frame named `S-## / Screen name / State`.
- Keep all inventoried screens as editable outlines and only confirmed screens at mid fidelity.
- Tile the primary path left to right with visible gaps and place alternate/material states in a row below the owning screen. Never overlap or hide a destination.
- Use variables for shared visual values.
- Use reusable nodes and refs for repeated controls and regions.
- Keep text as text nodes and images as replaceable image fills on dedicated frames.
- Preserve `S-##` and region IDs in node names for later search and updates.
- Keep only end-user-facing copy inside screen frames. Put purpose, rationale, business rules, raw state/fidelity labels, IDs, and prototype explanations in metadata or separate external annotation frames.
- Create sibling annotation frames named `I-## / Trigger / Destination` with editable text for trigger, precondition, result, failure, and recovery. Never nest them inside screens.

If the active `.pen` schema has no native interaction or connection nodes, use the tiled state frames, external `I-##` notes, and action metadata as the interaction specification. Report that limitation instead of claiming the flow is natively clickable.

## Update

Use `--in` so Pencil reads the existing design instead of regenerating it. Pass the exact user change as the prompt and attach the updated `PROTOTYPE.md` plus the common visual contract.

When Pencil MCP is connected, prefer a targeted native node update for a local change. When only CLI is available, do not use the same path for `--in` and `--out`; write a sibling candidate, validate it, and retain the original until the candidate passes. For a structural change, write a versioned `<product>-vN.pen`, validate it, then update the Visual outputs row to the new file. Explicitly name affected `S-##` IDs in the user's approved change request; preserve every unrelated screen and reusable node.

Locate descendants by their owning `S-##` frame plus unique semantic names or metadata. Do not assume every internal descendant ID survives copying or reopening a `.pen` file unchanged.

## Validate with Pencil MCP

When the desktop editor is connected:

1. Read all top-level screen frames and reusable nodes in batched queries.
2. Confirm every inventoried `S-##` exists exactly once per intended state.
3. Confirm repeated controls use reusable nodes or refs.
4. Confirm every screen and material state is tiled, visible, and non-overlapping.
5. Read all Text descendants inside screen frames and remove internal/product/design explanations.
6. Confirm every actionable transition has a sibling `I-##` note with a valid visible destination or terminal/stay result.
7. Run `snapshot_layout` with `problemsOnly: true` for clipping and overlap.
8. Screenshot the full flow plus each detailed screen and material state.
9. After an update, compare unaffected top-level identities and named properties to confirm preservation. Treat descendant IDs as implementation details unless the reopened file proves them stable.

When only CLI is available, export and inspect the preview but report structural validation as unavailable. Do not infer native editability from the PNG alone.
