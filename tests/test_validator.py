from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from vibe_coding_infra.models import CONTRACT_NAME, SOURCE_REQUIREMENTS_NAME
from vibe_coding_infra.validator import check_repository


class ValidatorTests(unittest.TestCase):
    def test_current_repository_has_no_validation_errors(self) -> None:
        root = Path(__file__).resolve().parents[1]
        findings = check_repository(root)
        self.assertEqual([], [finding.render(root) for finding in findings])

    def test_missing_required_path_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / SOURCE_REQUIREMENTS_NAME).write_text("source", encoding="utf-8")
            (root / CONTRACT_NAME).write_text("代理行动权", encoding="utf-8")
            findings = check_repository(root)
            rendered = "\n".join(finding.render(root) for finding in findings)
            self.assertIn("required file is missing", rendered)


if __name__ == "__main__":
    unittest.main()
