---
name: design-progressive-prototypes
description: Turn a product idea, PRD, requirements note, or existing prototype feedback into a structurally complete, progressively detailed product prototype. Use when defining, reviewing, or revising product scope, user flows, screen inventories, interface states, low-fidelity wireframes, or prototype change impact—especially when ordinary AI prototypes are either too vague to evaluate or too detailed to understand and edit.
---

# Design Progressive Prototypes

Create one product model at several levels of detail: complete at the structural level, detailed only where a decision requires it. Keep the user's attention on product decisions instead of decorative output.

## Load the contract

Read [references/prototype-contract.md](references/prototype-contract.md) before drafting or changing a prototype. Use [assets/PROTOTYPE.template.md](assets/PROTOTYPE.template.md) as the output skeleton.

## Choose the workflow

- **New prototype:** Accept a short idea or existing product material, then run the framing and skeleton checkpoints before writing a file.
- **Revise a prototype:** Read the existing `PROTOTYPE.md`, classify the requested change, trace affected flow and screen IDs, and update only affected sections.
- **Review only:** Diagnose gaps, excessive detail, contradictions, and missing states without writing unless the user also asks for changes.

Follow the user's output language. Keep IDs, file names, and Mermaid syntax in ASCII.

## Create a new prototype

### 1. Frame the product in conversation

Extract the primary user, problem, desired outcome, must-have scope, non-goals, constraints, and assumptions from available material. Discover facts from supplied files before asking the user.

Ask only questions that change scope, a core flow, or a major constraint. Ask no more than three questions in one checkpoint. If the user explicitly asks to skip checkpoints, record reasonable assumptions and continue.

Do not create `PROTOTYPE.md` during this step.

### 2. Present the minimum complete skeleton

Show a concise preview containing:

1. Product goal and primary user
2. In-scope and out-of-scope boundaries
3. Core and supporting flows with stable `F-##` IDs
4. Complete screen inventory with stable `S-##` IDs
5. Relevant loading, empty, error, permission, and recovery states
6. Uncertain assumptions and contradictions

Do not include visual styling, final copy, or detailed wireframes in the skeleton.

### 3. Recommend detail targets

Score candidate screens by decision value, usage frequency, and design risk. Recommend two or three screens for detailed treatment and state why each matters. Wait for confirmation before expanding them unless the user explicitly waived checkpoints.

### 4. Write the artifact

After confirmation, create `PROTOTYPE.md` in the requested location or the current project root. Preserve the exact level-one and level-two headings from the template. Use:

- Mermaid for flows
- Compact tables for inventories and state coverage
- Editable monospace text for low-fidelity wireframes
- Semantic descriptions for behavior and constraints
- Stable IDs for flows, screens, states, and decisions

Do not add detailed screens beyond the confirmed set. Mark deliberately deferred detail instead of inventing it.

### 5. Validate

For a new prototype, run:

```bash
python3 <skill-directory>/scripts/validate_prototype.py --initial <path-to-PROTOTYPE.md>
```

For a later revision, omit `--initial` so explicitly confirmed detail can grow beyond the first three screens.

Fix validation errors before handing off. Report warnings as explicit limitations rather than silently expanding scope.

## Revise an existing prototype

Classify the request before editing:

- **Local:** Copy, label, ordering, or behavior contained within one screen. Apply it directly, validate, and summarize the affected IDs.
- **Structural:** Authentication, permissions, payment, navigation, data lifecycle, adding or removing screens, or changing a flow outcome. First show the affected flows, screens, states, and decisions; wait for confirmation, then edit.

Keep unrelated sections byte-stable when practical. Update the change-impact table with the date, request, affected IDs, and resolved conflicts. Never regenerate the entire document merely to make a local change.

## Control detail

- Ensure every core product goal maps to at least one flow.
- Give every flow a start, successful end, and applicable alternate or failure path.
- Reference every screen from a flow and cover its applicable states.
- Keep the initial detailed set to at most three screens.
- Prefer annotations and constraints over polished copy or visual decoration.
- Surface assumptions; do not disguise guesses as settled requirements.
- Stop expanding when more detail would not help the next product decision.
