#!/usr/bin/env python3
"""Validate the structural contract of a Progressive Prototype document."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


REQUIRED_HEADINGS = [
    "## 1. Product Snapshot",
    "## 2. Scope and Assumptions",
    "## 3. Experience Map",
    "## 4. User Flows",
    "## 5. Screen Inventory",
    "## 6. Detailed Screens",
    "## 7. State Coverage",
    "## 8. Decisions and Change Impact",
]
PLACEHOLDERS = ("[Product name]", "[language]", "[Core flow name]", "[Screen name]")
VISUAL_TARGETS = ("figma", "pencil")
EDGE_RE = re.compile(
    r"^\s*([A-Za-z][\w-]*)\b.*?(?:-->|==>|-\.->)\s*(?:\|([^|]+)\|\s*)?([A-Za-z][\w-]*)\b"
)
INTERNAL_SCREEN_COPY_RE = re.compile(
    r"\b(?:decision being tested|annotation|interaction rule|business rule|page purpose|"
    r"design note|deferred|prototype note)\b|\b(?:D|F|S)-\d{2,}\b|"
    r"页面说明|页面目的|交互规则|业务规则|设计说明|决策待定|原型备注|延后处理",
    flags=re.IGNORECASE,
)
PASS_VALUES = {"pass", "passed", "通过"}


@dataclass(frozen=True)
class ValidationResult:
    errors: tuple[str, ...]
    warnings: tuple[str, ...]

    @property
    def valid(self) -> bool:
        return not self.errors


def _section(text: str, heading: str) -> str:
    start = text.find(heading)
    if start < 0:
        return ""
    start += len(heading)
    match = re.search(r"^## \d+\. ", text[start:], flags=re.MULTILINE)
    end = start + match.start() if match else len(text)
    return text[start:end]


def _table_ids(section: str, prefix: str) -> list[str]:
    pattern = rf"^\|\s*({re.escape(prefix)}-\d{{2,}})\s*\|"
    return re.findall(pattern, section, flags=re.MULTILINE)


def _named_subsections(section: str, prefix: str) -> list[tuple[str, str]]:
    pattern = re.compile(rf"^###\s+({re.escape(prefix)}-\d{{2,}})\b[^\n]*$", flags=re.MULTILINE)
    matches = list(pattern.finditer(section))
    return [
        (
            match.group(1),
            section[match.end() : matches[index + 1].start() if index + 1 < len(matches) else len(section)],
        )
        for index, match in enumerate(matches)
    ]


def _third_level_section(section: str, heading: str) -> str:
    pattern = re.compile(rf"^###\s+{re.escape(heading)}\s*$", flags=re.MULTILINE | re.IGNORECASE)
    match = pattern.search(section)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"^###\s+", section[start:], flags=re.MULTILINE)
    return section[start : start + next_heading.start() if next_heading else len(section)]


def _table_rows(section: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in section.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells or all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        rows.append(cells)
    return rows


def _node_label_matches(block: str, node: str, terms: str) -> bool:
    for line in block.splitlines():
        match = re.search(rf"\b{re.escape(node)}\b\s*[\(\[{{]+([^\]\)}}\n]+)", line)
        if match and re.search(terms, match.group(1), flags=re.IGNORECASE):
            return True
    return False


def _validate_flow_graph(flow_id: str, subsection: str, errors: list[str]) -> None:
    mermaid_match = re.search(r"```mermaid\s*(.*?)```", subsection, flags=re.DOTALL | re.IGNORECASE)
    if not mermaid_match:
        errors.append(f"{flow_id} must contain a Mermaid diagram")
        return

    block = mermaid_match.group(1)
    edges: list[tuple[str, str, str]] = []
    for line in block.splitlines():
        match = EDGE_RE.search(line)
        if match:
            edges.append((match.group(1), (match.group(2) or "").strip(), match.group(3)))
    if not edges:
        errors.append(f"{flow_id} Mermaid diagram has no parseable transitions")
        return

    nodes = {node for source, _, target in edges for node in (source, target)}
    start_nodes = {node for node in nodes if _node_label_matches(block, node, r"\bStart\b|入口|开始")}
    terminal_nodes = {
        node for node in nodes if _node_label_matches(block, node, r"\bSuccess\b|\bEnd\b|成功|结束")
    }
    if not start_nodes:
        errors.append(f"{flow_id} must include an explicit Start node")
    if not terminal_nodes:
        errors.append(f"{flow_id} must include an explicit Success or End node")

    outgoing: dict[str, list[tuple[str, str]]] = {}
    adjacency: dict[str, set[str]] = {}
    for source, label, target in edges:
        outgoing.setdefault(source, []).append((label, target))
        adjacency.setdefault(source, set()).add(target)

    dead_ends = sorted(nodes - set(outgoing) - terminal_nodes)
    if dead_ends:
        errors.append(f"{flow_id} has non-terminal dead ends: " + ", ".join(dead_ends))

    terminal_with_exits = sorted(terminal_nodes & set(outgoing))
    if terminal_with_exits:
        errors.append(f"{flow_id} terminal nodes must not have outgoing transitions: " + ", ".join(terminal_with_exits))

    if start_nodes:
        reachable = set(start_nodes)
        frontier = list(start_nodes)
        while frontier:
            source = frontier.pop()
            for target in adjacency.get(source, set()):
                if target not in reachable:
                    reachable.add(target)
                    frontier.append(target)
        unreachable = sorted(nodes - reachable)
        if unreachable:
            errors.append(f"{flow_id} has unreachable nodes: " + ", ".join(unreachable))

    for source, transitions in outgoing.items():
        if len(transitions) < 2:
            continue
        labels = [label.strip().lower() for label, _ in transitions]
        if any(not label for label in labels):
            errors.append(f"{flow_id} branch {source} must label every outcome")
        duplicate_labels = sorted({label for label in labels if label and labels.count(label) > 1})
        if duplicate_labels:
            errors.append(f"{flow_id} branch {source} has duplicate outcome labels: " + ", ".join(duplicate_labels))


def validate_text(
    text: str,
    *,
    initial: bool = False,
    visual_target: str | None = None,
) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    missing = [heading for heading in REQUIRED_HEADINGS if heading not in text]
    if missing:
        errors.extend(f"Missing required heading: {heading}" for heading in missing)

    present_placeholders = [placeholder for placeholder in PLACEHOLDERS if placeholder in text]
    if present_placeholders:
        errors.append("Unresolved template placeholders: " + ", ".join(present_placeholders))

    experience = _section(text, "## 3. Experience Map")
    flows = _section(text, "## 4. User Flows")
    inventory = _section(text, "## 5. Screen Inventory")
    details = _section(text, "## 6. Detailed Screens")
    states = _section(text, "## 7. State Coverage")
    decisions = _section(text, "## 8. Decisions and Change Impact")

    flow_sections = _named_subsections(flows, "F")
    if not flow_sections:
        errors.append("User Flows must contain at least one F-## heading")
    flow_ids = [flow_id for flow_id, _ in flow_sections]
    duplicate_flow_ids = sorted({flow_id for flow_id in flow_ids if flow_ids.count(flow_id) > 1})
    if duplicate_flow_ids:
        errors.append("Duplicate User Flow IDs: " + ", ".join(duplicate_flow_ids))
    unmapped_flows = sorted(set(flow_ids) - set(re.findall(r"\bF-\d{2,}\b", experience)))
    if unmapped_flows:
        errors.append("Flows missing from Experience Map: " + ", ".join(unmapped_flows))
    for flow_id, subsection in flow_sections:
        _validate_flow_graph(flow_id, subsection, errors)

    inventory_ids = _table_ids(inventory, "S")
    if inventory and not inventory_ids:
        errors.append("Screen Inventory must contain at least one S-## row")
    duplicate_inventory_ids = sorted({item for item in inventory_ids if inventory_ids.count(item) > 1})
    if duplicate_inventory_ids:
        errors.append("Duplicate Screen Inventory IDs: " + ", ".join(duplicate_inventory_ids))

    flow_screen_ids = set(re.findall(r"\bS-\d{2,}\b", flows))
    unreferenced = sorted(set(inventory_ids) - flow_screen_ids)
    if unreferenced:
        errors.append("Screens not referenced by a user flow: " + ", ".join(unreferenced))
    unknown_flow_screens = sorted(flow_screen_ids - set(inventory_ids))
    if unknown_flow_screens:
        errors.append("User flows reference screens missing from inventory: " + ", ".join(unknown_flow_screens))

    detail_ids = re.findall(r"^###\s+(S-\d{2,})\b", details, flags=re.MULTILINE)
    if initial and len(detail_ids) > 3:
        errors.append(f"Initial artifact details {len(detail_ids)} screens; maximum is 3")
    unknown_details = sorted(set(detail_ids) - set(inventory_ids))
    if unknown_details:
        errors.append("Detailed screens missing from inventory: " + ", ".join(unknown_details))
    if not detail_ids:
        warnings.append("No screens are detailed; confirm that this is intentionally a skeleton")

    for wireframe in re.findall(r"```text\s*(.*?)```", details, flags=re.DOTALL | re.IGNORECASE):
        match = INTERNAL_SCREEN_COPY_RE.search(wireframe)
        if match:
            errors.append(
                "Screen wireframes may contain only user-visible copy; move internal text outside the screen: "
                + match.group(0)
            )

    state_ids = set(_table_ids(states, "S"))
    missing_states = sorted(set(inventory_ids) - state_ids)
    if missing_states:
        errors.append("Screens missing from State Coverage: " + ", ".join(missing_states))

    if "deferred" not in text.lower() and "延后" not in text and "暂缓" not in text:
        warnings.append("No deferred detail is recorded; verify that the artifact is not over-specified")

    logic_section = _third_level_section(decisions, "Logic audit")
    if not logic_section:
        errors.append("Decisions and Change Impact must contain a '### Logic audit' table")
    else:
        logic_rows = {
            row[0]: row
            for row in _table_rows(logic_section)
            if row and re.fullmatch(r"F-\d{2,}", row[0])
        }
        missing_logic = sorted({flow_id for flow_id, _ in flow_sections} - set(logic_rows))
        if missing_logic:
            errors.append("Flows missing from Logic audit: " + ", ".join(missing_logic))
        unknown_logic = sorted(set(logic_rows) - {flow_id for flow_id, _ in flow_sections})
        if unknown_logic:
            errors.append("Logic audit references unknown flows: " + ", ".join(unknown_logic))
        for flow_id, row in logic_rows.items():
            if len(row) < 7:
                errors.append(f"Logic audit row {flow_id} must contain all seven columns")
                continue
            unresolved = [cell for cell in row[1:6] if not cell or cell.strip().lower() in {"pending", "tbd", "todo"}]
            if unresolved:
                errors.append(f"Logic audit row {flow_id} contains unresolved checks")
            if row[6].strip().lower() not in PASS_VALUES:
                errors.append(f"Logic audit row {flow_id} must end with Pass/通过")

    if visual_target is not None:
        target = visual_target.lower()
        if target not in VISUAL_TARGETS:
            errors.append(f"Unsupported visual target: {visual_target}")
        if "### Visual outputs" not in decisions:
            errors.append("Visual output validation requires a '### Visual outputs' table")
        else:
            rows = re.findall(
                r"^\|\s*(Figma|Pencil)\s*\|\s*([^|]+)\|\s*([^|]+)\|",
                decisions,
                flags=re.MULTILINE | re.IGNORECASE,
            )
            matching = [row for row in rows if row[0].lower() == target]
            if not matching:
                errors.append(f"Visual outputs table has no {target.title()} row")
            elif any(row[1].strip() in {"", "-", "TBD"} for row in matching):
                errors.append(f"Visual outputs table has no usable {target.title()} location")

        presentation_section = _third_level_section(decisions, "Presentation audit")
        if not presentation_section:
            errors.append("Visual output validation requires a '### Presentation audit' table")
        else:
            audit_rows = [row for row in _table_rows(presentation_section) if len(row) >= 3]
            categories = {
                "copy": [row for row in audit_rows if re.search(r"user-visible copy|用户可见文案|屏内文案", row[0], re.I)],
                "tiled": [row for row in audit_rows if re.search(r"tiled|平铺", row[0], re.I)],
                "notes": [row for row in audit_rows if re.search(r"interaction notes|交互备注", row[0], re.I)],
            }
            for category, rows in categories.items():
                if not rows:
                    errors.append(f"Presentation audit is missing the {category} check")
                elif any(row[1].strip().lower() not in PASS_VALUES or not row[2].strip() for row in rows):
                    errors.append(f"Presentation audit {category} check must Pass and include evidence")

    return ValidationResult(tuple(errors), tuple(warnings))


def validate_file(
    path: Path,
    *,
    initial: bool = False,
    visual_target: str | None = None,
) -> ValidationResult:
    return validate_text(
        path.read_text(encoding="utf-8"),
        initial=initial,
        visual_target=visual_target,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prototype", type=Path, help="Path to PROTOTYPE.md")
    parser.add_argument(
        "--initial",
        action="store_true",
        help="Enforce the initial limit of no more than three detailed screens",
    )
    parser.add_argument(
        "--visual-target",
        choices=VISUAL_TARGETS,
        help="Require a usable row for the generated visual target",
    )
    args = parser.parse_args()

    if not args.prototype.is_file():
        print(f"ERROR: file not found: {args.prototype}")
        return 2

    result = validate_file(
        args.prototype,
        initial=args.initial,
        visual_target=args.visual_target,
    )
    for warning in result.warnings:
        print(f"WARNING: {warning}")
    for error in result.errors:
        print(f"ERROR: {error}")

    if result.valid:
        print(f"OK: {args.prototype} satisfies the Progressive Prototype contract")
        return 0
    print(f"FAILED: {len(result.errors)} error(s)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
