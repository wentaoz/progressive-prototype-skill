# Figma output workflow

Produce a native Figma design that remains easy to inspect and edit at screen, region, component, and token level.

## Prerequisites

Load `figma-use` and `figma-generate-design` before every `use_figma` operation. Load `figma-create-new-file` before creating a file. Require a connected Figma MCP server and edit access.

If the user supplies a design URL, use its file key. Otherwise resolve the authenticated plan and create a design file named after the product. Do not create a file if the user requested review only.

## Inspect before writing

Enumerate pages and inspect existing screens, instances, variables, text styles, and effect styles. Prefer existing file conventions. If no representative screen exists, search linked design-system libraries broadly for components, variables, and styles before creating local foundations.

Never modify a remote or existing source component. Import and instantiate it. When no suitable system exists, create only the local foundations required by the confirmed screens.

## Organize a new file

Create or reuse these pages:

1. `00 Overview` — product snapshot, flow map, assumptions, and decisions
2. `01 Foundations` — local variables, text styles, and components that are actually used
3. `02 Prototype` — flow sections containing separate screen and state frames

If an unrelated page already owns one of these names, append ` (Progressive Prototype)` rather than taking it over. Mark owned pages and nodes with shared plugin data.

Use namespace `progressivePrototype` with these keys:

- `kind`: `page`, `flow`, `screen`, `state`, `region`, `component`, or `interaction-note`
- `semanticId`: `F-##`, `S-##`, a region ID, or `I-##`
- `sourceVersion`: the prototype updated date or revision identifier

## Build editable foundations

- Reuse imported component instances, variables, text styles, and effect styles first.
- For missing local controls, create component sets with purposeful variants such as state, emphasis, or size.
- Expose user-facing labels through component text properties.
- Bind fills, strokes, spacing, and radii to scoped variables where supported.
- Keep all text as Text nodes and load fonts before edits.
- Do not detach instances to make ordinary copy changes.

## Build screens progressively

- Create every inventoried screen as its own top-level Frame inside the relevant flow Section.
- Name frames `S-## / Screen name / State`.
- Build outline screens with semantically named layers and user-facing primary actions, not visible designer labels or polished UI.
- Build confirmed screens section by section with Auto Layout containers and component instances.
- Tile the primary path left to right with fixed visible gaps. Put Loading, Empty, Error, Permission, and Recovery frames in a second row below their owning Default frame.
- Keep all destinations visible. Represent runtime overlays as separate tiled state Frames for review.
- Put only end-user-facing text inside each screen Frame. Keep screen names, raw state/fidelity labels, IDs, decision rationale, business rules, and prototype explanations in Figma layer names, shared data, or external annotations.
- Set semantic shared data on screen frames and major regions.
- Return every created or mutated node ID from each call.

## Annotate interactions

Create separate sibling annotation Frames beside or below the related screen. Name them `I-## / Trigger / Destination`, set `kind=interaction-note`, and include trigger, precondition, result, failure, and recovery as editable Text. Never append an annotation Frame as a child of a user-facing screen.

Use native reactions only as a supplement for the core flow and material recovery paths. Prefer `ON_CLICK` navigation, overlays, and component `CHANGE_TO` reactions. Do not create interactions for decorative or deferred controls. Keep destinations within the tiled page, ensure every reaction matches an `I-##` note, and never add a hidden destination.

## Never flatten the final output

Do not use a captured webpage, screenshot, SVG import, or `generate_figma_design` result as the final screen. For a running web app, a capture may be used only as a temporary visual reference. Rebuild the deliverable with native Frames, Text, Instances, Variables, Styles, and Reactions, then remove the capture.

## Update safely

Locate owned nodes first through shared plugin data and then by semantic naming. Inspect the affected subtree before mutation. Preserve unrelated nodes and user styling. Add missing states or regions beside the current screen instead of recreating its parent Section. Save a version-history checkpoint before a structural update when supported.

## Validate

Use metadata and targeted read-only scripts to verify:

- one owned frame for every `S-##` screen;
- no screen root is an Image, Vector, Group, or single-child bitmap wrapper;
- detailed screens contain Auto Layout Frames, editable Text, and component Instances;
- repeated local controls remain Components or Instances;
- shared variables or imported design-system bindings exist;
- any native reactions exactly match the external interaction notes;
- semantic shared data is present and unique.
- every screen and material state has a non-overlapping canvas position and is visible without presentation playback;
- every action transition has an external `I-##` note with a valid destination or explicit terminal/stay result;
- no interaction note or internal design explanation is a descendant of a screen Frame;
- every Text descendant inside a screen is justified as user-facing copy.

Use screenshots of the full tiled flow plus each detailed screen and material state. Check copy hygiene, note placement, clipping, overlap, hierarchy, and readability. Compare reactions against notes and fail validation on orphan frames, dead ends, or contradictory destinations. Fix only the broken subtree and revalidate.
