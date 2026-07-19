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


def validate_text(text: str, *, initial: bool = False) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    missing = [heading for heading in REQUIRED_HEADINGS if heading not in text]
    if missing:
        errors.extend(f"Missing required heading: {heading}" for heading in missing)

    present_placeholders = [placeholder for placeholder in PLACEHOLDERS if placeholder in text]
    if present_placeholders:
        errors.append("Unresolved template placeholders: " + ", ".join(present_placeholders))

    flows = _section(text, "## 4. User Flows")
    inventory = _section(text, "## 5. Screen Inventory")
    details = _section(text, "## 6. Detailed Screens")
    states = _section(text, "## 7. State Coverage")

    if flows and "```mermaid" not in flows:
        errors.append("User Flows must contain at least one Mermaid diagram")
    if flows and not re.search(r"\bStart\b|入口|开始", flows, flags=re.IGNORECASE):
        errors.append("User Flows must include an explicit Start node")
    if flows and not re.search(r"\bSuccess\b|\bEnd\b|成功|结束", flows, flags=re.IGNORECASE):
        errors.append("User Flows must include an explicit Success or End node")

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

    detail_ids = re.findall(r"^###\s+(S-\d{2,})\b", details, flags=re.MULTILINE)
    if initial and len(detail_ids) > 3:
        errors.append(f"Initial artifact details {len(detail_ids)} screens; maximum is 3")
    unknown_details = sorted(set(detail_ids) - set(inventory_ids))
    if unknown_details:
        errors.append("Detailed screens missing from inventory: " + ", ".join(unknown_details))
    if not detail_ids:
        warnings.append("No screens are detailed; confirm that this is intentionally a skeleton")

    state_ids = set(_table_ids(states, "S"))
    missing_states = sorted(set(inventory_ids) - state_ids)
    if missing_states:
        errors.append("Screens missing from State Coverage: " + ", ".join(missing_states))

    if not re.search(r"^###\s+F-\d{2,}\b", flows, flags=re.MULTILINE):
        errors.append("User Flows must contain at least one F-## heading")
    if "deferred" not in text.lower() and "延后" not in text and "暂缓" not in text:
        warnings.append("No deferred detail is recorded; verify that the artifact is not over-specified")

    return ValidationResult(tuple(errors), tuple(warnings))


def validate_file(path: Path, *, initial: bool = False) -> ValidationResult:
    return validate_text(path.read_text(encoding="utf-8"), initial=initial)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prototype", type=Path, help="Path to PROTOTYPE.md")
    parser.add_argument(
        "--initial",
        action="store_true",
        help="Enforce the initial limit of no more than three detailed screens",
    )
    args = parser.parse_args()

    if not args.prototype.is_file():
        print(f"ERROR: file not found: {args.prototype}")
        return 2

    result = validate_file(args.prototype, initial=args.initial)
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
