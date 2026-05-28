from __future__ import annotations

import unittest
from pathlib import Path

from vibe_coding_infra.knowledge_base import answer, import_knowledge, search


class KnowledgeBaseTests(unittest.TestCase):
    def test_import_and_search(self) -> None:
        root = Path(__file__).resolve().parents[1]
        entries = import_knowledge(root)
        self.assertGreater(len(entries), 5)
        results = search(root, "执行切片", limit=3)
        self.assertTrue(results)
        self.assertIn("source_path", results[0])

    def test_answer_returns_citations(self) -> None:
        root = Path(__file__).resolve().parents[1]
        import_knowledge(root)
        result = answer(root, "下一步之前要读取什么？", limit=3)
        self.assertIn("answer", result)
        self.assertTrue(result["citations"])


if __name__ == "__main__":
    unittest.main()
