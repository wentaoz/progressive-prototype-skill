from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/design-progressive-prototypes/scripts/validate_prototype.py"
EXAMPLE = ROOT / "examples/appointment-booking/PROTOTYPE.md"

spec = importlib.util.spec_from_file_location("validate_prototype", SCRIPT)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = validator
spec.loader.exec_module(validator)


class ValidatePrototypeTests(unittest.TestCase):
    def test_example_is_valid(self) -> None:
        result = validator.validate_file(EXAMPLE)
        self.assertEqual((), result.errors)

    def test_missing_heading_fails(self) -> None:
        text = EXAMPLE.read_text(encoding="utf-8").replace("## 7. State Coverage", "## State Coverage")
        result = validator.validate_text(text, initial=True)
        self.assertTrue(any("Missing required heading" in item for item in result.errors))

    def test_unreferenced_screen_fails(self) -> None:
        text = EXAMPLE.read_text(encoding="utf-8").replace(
            "| S-03 | Confirmation |",
            "| S-99 | Confirmation |",
        )
        result = validator.validate_text(text, initial=True)
        self.assertTrue(any("S-99" in item and "not referenced" in item for item in result.errors))

    def test_flow_screen_must_exist_in_inventory(self) -> None:
        text = EXAMPLE.read_text(encoding="utf-8").replace(
            "S03[S-03 Confirmation]",
            "S99[S-99 Confirmation]",
        ).replace(
            "S02 -->|Slot available| S03",
            "S02 -->|Slot available| S99",
        ).replace(
            "S03 --> SUCCESS([Success])",
            "S99 --> SUCCESS([Success])",
        )
        result = validator.validate_text(text)
        self.assertTrue(any("missing from inventory" in item and "S-99" in item for item in result.errors))

    def test_flow_must_appear_in_experience_map(self) -> None:
        text = EXAMPLE.read_text(encoding="utf-8")
        experience = validator._section(text, "## 3. Experience Map").replace("F-01", "F-99")
        text = text.replace(validator._section(text, "## 3. Experience Map"), experience)
        result = validator.validate_text(text)
        self.assertTrue(any("Experience Map" in item and "F-01" in item for item in result.errors))

    def test_more_than_three_detailed_screens_fails(self) -> None:
        text = EXAMPLE.read_text(encoding="utf-8").replace(
            "## 7. State Coverage",
            "### S-01 Duplicate detail\n\n### S-02 Duplicate detail\n\n## 7. State Coverage",
        )
        result = validator.validate_text(text, initial=True)
        self.assertTrue(any("maximum is 3" in item for item in result.errors))

    def test_later_revision_can_expand_confirmed_detail(self) -> None:
        text = EXAMPLE.read_text(encoding="utf-8").replace(
            "## 7. State Coverage",
            "### S-01 Additional confirmed view\n\n### S-02 Additional confirmed view\n\n## 7. State Coverage",
        )
        result = validator.validate_text(text)
        self.assertFalse(any("maximum is 3" in item for item in result.errors))

    def test_visual_target_requires_matching_output_row(self) -> None:
        text = EXAMPLE.read_text(encoding="utf-8")
        result = validator.validate_text(text, visual_target="figma")
        self.assertTrue(any("no Figma row" in item for item in result.errors))

    def test_visual_target_accepts_usable_location(self) -> None:
        text = EXAMPLE.read_text(encoding="utf-8").replace(
            "| Document | ./PROTOTYPE.md | v0.2.1 example | S-01, S-02 | 2026-07-19 |",
            "| Document | ./PROTOTYPE.md | v0.2.1 example | S-01, S-02 | 2026-07-19 |\n"
            "| Figma | https://figma.com/design/test | Current | S-01, S-02 | 2026-07-19 |",
        )
        result = validator.validate_text(text, visual_target="figma")
        self.assertEqual((), result.errors)

    def test_each_flow_requires_terminal_outcome(self) -> None:
        text = EXAMPLE.read_text(encoding="utf-8").replace(
            "S03 --> SUCCESS([Success])",
            "S03 --> REVIEW[S-03 Review]",
        )
        result = validator.validate_text(text)
        self.assertTrue(any("Success or End" in item for item in result.errors))

    def test_non_terminal_dead_end_fails(self) -> None:
        text = EXAMPLE.read_text(encoding="utf-8").replace(
            "S02 -->|Slot taken| S01",
            "S02 -->|Slot taken| S01\n    S02 -->|Needs help| HELP[Help]",
        )
        result = validator.validate_text(text)
        self.assertTrue(any("dead ends" in item and "HELP" in item for item in result.errors))

    def test_branch_requires_labeled_outcomes(self) -> None:
        text = EXAMPLE.read_text(encoding="utf-8").replace(
            "S02 -->|Slot taken| S01",
            "S02 --> S01",
        )
        result = validator.validate_text(text)
        self.assertTrue(any("must label every outcome" in item for item in result.errors))

    def test_unreachable_flow_node_fails(self) -> None:
        text = EXAMPLE.read_text(encoding="utf-8").replace(
            "S03 --> SUCCESS([Success])",
            "S03 --> SUCCESS([Success])\n    ORPHAN[S-99 Orphan] --> SUCCESS",
        )
        result = validator.validate_text(text)
        self.assertTrue(any("unreachable nodes" in item and "ORPHAN" in item for item in result.errors))

    def test_internal_explanation_inside_wireframe_fails(self) -> None:
        text = EXAMPLE.read_text(encoding="utf-8").replace(
            "| Selected: 10:30",
            "| Business rule: hold for five minutes             |\n| Selected: 10:30",
        )
        result = validator.validate_text(text)
        self.assertTrue(any("user-visible copy" in item and "Business rule" in item for item in result.errors))

    def test_logic_audit_is_required(self) -> None:
        text = EXAMPLE.read_text(encoding="utf-8").replace("### Logic audit", "### Flow review")
        result = validator.validate_text(text)
        self.assertTrue(any("Logic audit" in item for item in result.errors))

    def test_logic_audit_must_pass(self) -> None:
        text = EXAMPLE.read_text(encoding="utf-8").replace(
            "| F-01 | Covered from START",
            "| F-01 | Pending",
        )
        result = validator.validate_text(text)
        self.assertTrue(any("unresolved checks" in item for item in result.errors))

    def test_visual_target_requires_presentation_audit(self) -> None:
        text = EXAMPLE.read_text(encoding="utf-8").replace(
            "### Presentation audit",
            "### Visual review",
        ).replace(
            "| Document | ./PROTOTYPE.md | v0.2.1 example | S-01, S-02 | 2026-07-19 |",
            "| Figma | https://figma.com/design/test | Current | S-01, S-02 | 2026-07-19 |",
        )
        result = validator.validate_text(text, visual_target="figma")
        self.assertTrue(any("Presentation audit" in item for item in result.errors))


if __name__ == "__main__":
    unittest.main()
