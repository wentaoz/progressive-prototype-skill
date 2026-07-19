#!/usr/bin/env python3
"""Vendored Codex skill frontmatter validator used by CI."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml


MAX_SKILL_NAME_LENGTH = 64


def validate_skill(skill_path: str) -> tuple[bool, str]:
    skill_md = Path(skill_path) / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid YAML frontmatter format"

    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return False, f"Invalid YAML in frontmatter: {exc}"
    if not isinstance(frontmatter, dict):
        return False, "Frontmatter must be a YAML dictionary"

    if set(frontmatter) != {"name", "description"}:
        return False, "Frontmatter must contain only name and description"
    name = frontmatter["name"]
    description = frontmatter["description"]
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        return False, "Skill name must use lowercase hyphen-case"
    if len(name) > MAX_SKILL_NAME_LENGTH:
        return False, f"Skill name exceeds {MAX_SKILL_NAME_LENGTH} characters"
    if not isinstance(description, str) or not description.strip() or len(description) > 1024:
        return False, "Description must be a non-empty string of at most 1024 characters"
    if "<" in description or ">" in description:
        return False, "Description cannot contain angle brackets"
    return True, "Skill is valid!"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)
    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
