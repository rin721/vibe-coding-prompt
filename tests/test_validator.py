from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from vibe_coding_infra.state import choose_next_slice
from vibe_coding_infra.validator import check_repository


class RepositoryValidationTests(unittest.TestCase):
    def test_current_repository_has_no_validation_errors(self) -> None:
        root = Path(__file__).resolve().parents[1]
        findings = check_repository(root)
        errors = [finding.render(root) for finding in findings if finding.level == "error"]
        self.assertEqual(errors, [])

    def test_next_slice_reports_complete_when_all_slices_done(self) -> None:
        root = Path(__file__).resolve().parents[1]
        result = choose_next_slice(root)
        self.assertIn(result["status"], {"complete", "ready"})

    def test_missing_required_files_are_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "prompt.md").write_text(
                "代理行动权 执行切片 需求台账 搜索研究 质量门禁 专属编程知识库 "
                "可检索增强 Single Source of Truth 向量数据库 全文索引 检索 API "
                "智能问答入口 知识条目导入流水线",
                encoding="utf-8",
            )
            findings = check_repository(root)
            messages = [finding.message for finding in findings]
            self.assertIn("required file is missing", messages)


if __name__ == "__main__":
    unittest.main()
