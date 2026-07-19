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

## Interaction depth

Connect the core success flow and material failure or recovery branches. Do not wire every secondary control. Keep interaction destinations aligned with `F-##` and `S-##` IDs.

## Safe revision

Before editing, inspect the current visual artifact and compare it with the requested semantic change. Mutate only affected screen, region, component, and interaction IDs. Preserve unrelated manual typography, spacing, color, copy, and composition changes. If a manual change conflicts with the semantic source, show the conflict before overwriting it.

## Validation evidence

Report these separately:

1. Semantic validation of `PROTOTYPE.md`
2. Structural validation of native nodes, components, variables, and interactions
3. Visual validation for clipping, overlap, hierarchy, and readability

Do not call a preview image proof of native editability.
