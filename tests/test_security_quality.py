from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from vibe_coding_infra.quality import check_workspace
from vibe_coding_infra.security import scan_terms, scan_text


class SecurityQualityTests(unittest.TestCase):
    def test_secret_scan_detects_token_like_values(self) -> None:
        key_name = "api" + "_key"
        value = "abcdefghijklmnopqrstuvwxyz" + "123456"
        findings = scan_text(f"{key_name} = '{value}'")
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].kind, "possible_secret")

    def test_scan_terms_detects_forbidden_terms(self) -> None:
        findings = scan_terms("clean line\nforbidden value", ["forbidden"])
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].line, 2)

    def test_workspace_check_validates_schema_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "schemas").mkdir()
            (root / "schemas" / "ok.json").write_text(
                '{"$schema":"x","type":"object","properties":{}}',
                encoding="utf-8",
            )
            (root / "README.md").write_text("hello", encoding="utf-8")
            report = check_workspace(root, paths=[root / "README.md"])
            self.assertTrue(report.ok)


if __name__ == "__main__":
    unittest.main()
