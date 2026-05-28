from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from vibe_coding_infra.knowledge_base import (
    answer_question,
    build_full_text_index,
    import_markdown_paths,
    search_entries,
)


class KnowledgeBaseTests(unittest.TestCase):
    def test_markdown_import_search_and_answer_include_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            docs = root / "docs"
            docs.mkdir()
            source = docs / "ARCHITECTURE.md"
            source.write_text("# Architecture\n\n执行切片 must include verification evidence.\n", encoding="utf-8")

            entries = import_markdown_paths([source], root)
            self.assertEqual(entries[0].source_path, "docs/ARCHITECTURE.md")
            self.assertEqual(entries[0].evidence, ["docs/ARCHITECTURE.md"])

            results = search_entries(entries, "执行切片 verification")
            self.assertEqual(results[0]["entry"]["id"], "KB-0001")
            self.assertIn("verification", results[0]["matched_terms"])

            answer = answer_question(entries, "执行切片 requires what evidence?")
            self.assertEqual(answer["citations"][0]["source_path"], "docs/ARCHITECTURE.md")

    def test_full_text_index_maps_terms_to_entry_ids(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            readme = root / "README.md"
            readme.write_text("# Project\n\nKnowledge retrieval API.\n", encoding="utf-8")

            entries = import_markdown_paths([readme], root)
            index = build_full_text_index(entries)

            self.assertIn("knowledge", index)
            self.assertEqual(index["knowledge"], ["KB-0001"])


if __name__ == "__main__":
    unittest.main()
