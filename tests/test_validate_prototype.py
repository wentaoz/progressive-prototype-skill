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


if __name__ == "__main__":
    unittest.main()
