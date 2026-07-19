# Visual output contract

Apply this contract to both Figma and Pencil outputs.

## Semantic identity

- Keep `PROTOTYPE.md` as the product-semantics source.
- Give every screen and screen state a stable `S-## / Name / State` identity.
- Give important regions semantic IDs such as `S-01.header`, `S-01.content`, and `S-01.primary-action`.
- Preserve semantic IDs across renames and visual restyling.

## Progressive fidelity

- Create an editable outline for every screen in the inventory.
- Raise only the confirmed two or three screens to `detailed` mid fidelity on the first generation.
- Keep deferred screens visibly labeled and structurally present without invented copy or decoration.
- Represent component states through reusable variants or reusable nodes; represent material page states as separate screen frames.

## Native editability

- Keep screens as separate top-level frames, never one combined bitmap or vector.
- Keep text as editable text layers.
- Use layout containers instead of manually positioned piles of shapes.
- Use component instances or reusable references for repeated UI.
- Use variables or tokens for colors, spacing, radii, and other shared values.
- Name layers by purpose, not by generated shape type.
- Keep each major region independently selectable and replaceable.

## Screen copy boundary

- Put only end-user-facing copy, data, labels, validation, feedback, and necessary help inside screen frames.
- Never place page purpose, decision being tested, design rationale, assumptions, business rules, raw state/fidelity labels, IDs, or prototype instructions inside a screen. User-facing loading, empty, error, and success messages are allowed.
- Keep designer and product context in external annotation frames or notes. Metadata may remain hidden on nodes.
- Audit every text child of every screen before handoff. If a sentence explains the prototype rather than helping the product user complete the task, move it outside.

## Tiled canvas and interaction notes

- Tile every screen and material state on an open canvas with visible gaps; do not stack, overlap, hide, or require click-through to discover a destination.
- Arrange the primary flow left to right. Put alternate, error, loading, permission, and recovery states directly below their owning screen.
- Represent overlays, drawers, and modals as separate visible state frames in the review canvas even if the product will overlay them at runtime.
- Add external `I-##` interaction notes beside the related screen, never inside it. Record trigger, precondition, destination, failure, and recovery.
- Keep each note visually and structurally separate from screen content. Connectors are optional; the note text is authoritative.
- Native reactions may supplement the tiled documentation. They must match the notes and may not introduce hidden destinations.

## Logic completion

- Ensure every screen/state is reachable from a visible start and every non-terminal screen/state has an exit.
- Ensure branch labels are mutually understandable and collectively complete, or include an explicit fallback.
- Ensure material async actions have visible loading, success, failure, and recovery outcomes.
- Cross-check every `I-##` note against `F-##`, `S-##`, the state matrix, and any native reaction.
- Do not claim completion while a dead end, orphan state, contradictory transition, or unresolved core outcome remains.

## Safe revision

Before editing, inspect the current visual artifact and compare it with the requested semantic change. Mutate only affected screen, region, component, and interaction IDs. Preserve unrelated manual typography, spacing, color, copy, and composition changes. If a manual change conflicts with the semantic source, show the conflict before overwriting it.

## Validation evidence

Report these separately:

1. Semantic validation of `PROTOTYPE.md`
2. Structural validation of native nodes, components, variables, and interactions
3. Presentation validation for user-visible screen copy, tiled coverage, and external interaction notes
4. Visual validation for clipping, overlap, hierarchy, and readability

Do not call a preview image proof of native editability.
