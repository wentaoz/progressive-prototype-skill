# Prototype artifact contract

Use this contract to keep prototypes complete without making every section equally detailed.

## 1. Product Snapshot

State the primary user, problem, intended outcome, and one observable success signal. Keep this section short enough to scan before reviewing a flow.

## 2. Scope and Assumptions

Separate must-have scope, explicit non-goals, constraints, and unsettled assumptions. Assign open decisions `D-##` IDs. Never turn an assumption into scope without noting the decision.

## 3. Experience Map

List the smallest set of user stages needed to understand the experience. Map each stage to a user intent and one or more flow IDs. This is navigation for the document, not a journey-map essay.

## 4. User Flows

Assign each flow an `F-##` ID. Mermaid nodes that represent screens must contain their `S-##` IDs. Include:

- an explicit `Start` node;
- an explicit `Success` or `End` node;
- decision branches where outcomes diverge;
- recovery or failure branches when material.

Supporting flows may be compact, but every inventoried screen must appear in at least one flow.

## 5. Screen Inventory

Assign each screen an `S-##` ID and record its purpose, entry points, primary action, relevant states, and fidelity: `outline`, `detailed`, or `deferred`. Inventory completeness is independent of visual detail.

## 6. Detailed Screens

Detail only confirmed screens. Start each screen with a `### S-##` heading and include:

- decision being tested;
- editable text wireframe;
- component or region annotations;
- actions and resulting screen or state IDs;
- rules and deliberately deferred detail.

Keep the first artifact to two or three detailed screens. Text wireframes express hierarchy, not pixel measurements.

## 7. State Coverage

For every screen, mark loading, empty, error, permission, recovery, and success as `required`, `not applicable`, or `deferred`, with a short rationale for deferred items. Do not create ceremonial variants with no product consequence.

## 8. Decisions and Change Impact

List open and resolved decisions separately. On revision, append a compact change-impact row containing the date, request, affected IDs, conflicts resolved, and any follow-up decision.

## Detail selection

Rate candidate screens qualitatively:

| Factor | High signal |
|---|---|
| Decision value | The layout or interaction changes product scope or user behavior |
| Usage frequency | Most users encounter it or repeat it often |
| Design risk | It contains branching, trust, permissions, money, or destructive actions |

Recommend the smallest set that exposes the largest unresolved decisions. A high score does not authorize detail without confirmation.

## Change classification

Treat a change as structural if it changes any flow edge, introduces or removes a screen, changes authentication or permissions, moves money, alters retained data, or changes a success outcome. Everything else is local unless its impact analysis reveals propagation.
