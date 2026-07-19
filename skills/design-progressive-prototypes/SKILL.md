---
name: design-progressive-prototypes
description: Turn a product idea, PRD, requirements note, or existing prototype feedback into a structurally complete, progressively detailed product prototype in Markdown, editable Figma, or Pencil .pen format. Use when defining, reviewing, generating, or revising product scope, user flows, screen inventories, interface states, low- or mid-fidelity wireframes, tiled annotated canvases, design-system-based Figma screens, Pencil files, or prototype change impact—especially when ordinary AI prototypes are too vague, too detailed, logically incomplete, polluted with internal explanatory copy, flattened, or difficult to edit locally.
---

# Design Progressive Prototypes

Create one product model at several levels of detail: complete at the structural level, detailed only where a decision requires it. Produce native, locally editable layers on a fully tiled review canvas. Keep internal explanations outside user-facing screens and do not hand off a prototype with unresolved logic gaps.

## Load the relevant contracts

Always read [references/prototype-contract.md](references/prototype-contract.md). Use [assets/PROTOTYPE.template.md](assets/PROTOTYPE.template.md) as the semantic artifact skeleton.

For visual output, also read [references/visual-output-contract.md](references/visual-output-contract.md), then read exactly one target workflow:

- [references/figma-output.md](references/figma-output.md) for Figma
- [references/pencil-output.md](references/pencil-output.md) for Pencil

## Route the request

- **Document:** Create or revise `PROTOTYPE.md` only.
- **Figma:** Create or revise `PROTOTYPE.md`, then create or update an editable Figma design file.
- **Pencil:** Create or revise `PROTOTYPE.md`, then create or update an editable `.pen` file and preview.
- **Review only:** Diagnose structural gaps, excessive detail, flattening, contradictions, and missing states without writing unless the user asks for changes.

Use the target explicitly named by the user. If the user requests a visual prototype without naming a target, prefer Figma when its tools are connected; otherwise offer Pencil, then document-only output. Never silently substitute a target.

Follow the user's output language. Keep IDs, file names, layer names, shared-data keys, and Mermaid syntax in ASCII.

## Create a new prototype

### 1. Frame the product in conversation

Extract the primary user, problem, desired outcome, must-have scope, non-goals, constraints, and assumptions from available material. Discover facts from supplied files before asking the user.

Ask only questions that change scope, a core flow, platform, or a major constraint. Ask no more than three questions in one checkpoint. If the user explicitly asks to skip checkpoints, record reasonable assumptions and continue.

Do not create artifacts during this step.

### 2. Present the minimum complete skeleton

Show a concise preview containing:

1. Product goal and primary user
2. In-scope and out-of-scope boundaries
3. Core and supporting flows with stable `F-##` IDs
4. Complete screen inventory with stable `S-##` IDs
5. Relevant loading, empty, error, permission, and recovery states
6. Explicit branch outcomes, recovery destinations, and uncertain assumptions

Do not include visual styling, final copy, or detailed wireframes in the skeleton.

### 3. Recommend detail targets

Score candidate screens by decision value, usage frequency, and design risk. Recommend two or three screens for detailed treatment and state why each matters. Wait for confirmation before expanding them unless the user explicitly waived checkpoints.

### 4. Write the semantic artifact

After confirmation, create `PROTOTYPE.md` in the requested location or the current project root. Preserve the exact level-one and level-two headings from the template. Use Mermaid for flows, compact tables for inventories, editable text for wireframes, semantic behavior descriptions, and stable IDs. Put only copy that an end user should see inside each wireframe. Keep page purpose, design rationale, assumptions, business rules, state labels, and interaction explanations in the document outside the wireframe.

Do not add detailed screens beyond the confirmed set. Mark deliberately deferred detail instead of inventing it.

For a new artifact, validate with:

```bash
python3 <skill-directory>/scripts/validate_prototype.py --initial <path-to-PROTOTYPE.md>
```

### 5. Generate the selected visual target

Generate visual output only after the semantic artifact is valid. Create an outline frame for every inventoried screen, but raise only the confirmed two or three screens to mid fidelity. Tile every screen and material state on the canvas so reviewers can see the complete flow without clicking. Place interaction notes outside screen frames and record trigger, condition, destination, failure, and recovery. Native interactions may supplement the notes but must never be the only representation of logic.

After generation, add or update the `Visual outputs` row in `PROTOTYPE.md`, then validate it with:

```bash
python3 <skill-directory>/scripts/validate_prototype.py --visual-target <figma-or-pencil> <path-to-PROTOTYPE.md>
```

Show the resulting Figma URL or `.pen` path and a visual preview. Report structural validation separately from visual validation.

## Revise an existing prototype

Classify the request before editing:

- **Local:** Copy, label, ordering, styling, or behavior contained within one screen or component. Apply it directly, validate, and summarize affected IDs.
- **Structural:** Authentication, permissions, payment, navigation, data lifecycle, adding or removing screens, or changing a flow outcome. First show affected flows, screens, states, and decisions; wait for confirmation, then edit.

Treat `PROTOTYPE.md` as the product-semantics source. Inspect the existing visual file before every visual update. Preserve manual visual changes that do not conflict with the requested semantic change. Locate nodes through semantic IDs, mutate only affected nodes, and never regenerate an entire file for a local change.

For later revisions, omit `--initial` so explicitly confirmed detail can grow beyond the first three screens. Update the change-impact and Visual outputs tables after successful writes.

## Control detail and editability

- Ensure every core product goal maps to at least one flow.
- Give every flow a reachable start, successful end, exhaustive labeled branches, and applicable failure and recovery paths.
- Reference every screen from a flow and cover its applicable states.
- Give every non-terminal screen or state an exit. Reject unreachable screens, unexplained loops, and dead ends.
- Keep internal prototype text outside screens. Screen children may contain only copy, data, labels, feedback, and help that an end user should actually see.
- Tile all screens and states with visible gaps. Keep interaction notes as separate sibling annotations, never as children of a user-facing screen.
- Require the Logic audit and, for visual output, the Presentation audit to pass before handoff. If a core open decision prevents a complete path, stop and resolve or explicitly defer that flow instead of claiming it passes.
- Keep the initial detailed set to at most three screens.
- Prefer components, variables, styles, Auto Layout, reusable nodes, and editable text over duplicated primitives.
- Never deliver a whole screen as a screenshot, single vector, or indivisible group.
- Surface assumptions; do not disguise guesses as settled requirements.
- Stop expanding when more detail would not help the next product decision.

## Handle unavailable tools

If Figma is unavailable or not writable, explain the missing connection or permission and offer Pencil or document-only output. If Pencil is missing or unauthenticated, provide the required installation or login step and offer Figma or document-only output. Do not claim a visual file is structurally validated when only a preview image was inspected.
