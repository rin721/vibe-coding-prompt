from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from vibe_coding_infra.knowledge import KnowledgeBase


class KnowledgeBaseTests(unittest.TestCase):
    def test_ingest_search_and_ask(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            docs.mkdir()
            (docs / "note.md").write_text(
                "# Quality Gates\n\nTasks are complete only after tests and evidence agree.",
                encoding="utf-8",
            )
            kb = KnowledgeBase(root / ".vibe" / "knowledge.sqlite3")
            count = kb.ingest_paths([docs], root=root)
            self.assertEqual(count, 1)

            results = kb.search("quality evidence", limit=3)
            self.assertTrue(results)
            self.assertEqual(results[0].entry.source_path, "docs/note.md")

            answer = kb.ask("How is a task complete?")
            self.assertIn("docs/note.md", answer.answer)
            self.assertTrue(answer.citations)


if __name__ == "__main__":
    unittest.main()
