from __future__ import annotations

import unittest

from vibe_coding_infra.text import chunk_text, cosine_similarity, hashed_vector, stable_id, tokenize


class TextTests(unittest.TestCase):
    def test_tokenize_supports_chinese_and_ascii(self) -> None:
        tokens = tokenize("Vibe Coding 工程闭环")
        self.assertIn("vibe", tokens)
        self.assertIn("工程闭环", tokens)
        self.assertIn("工程", tokens)

    def test_chunk_text_splits_large_blocks(self) -> None:
        chunks = chunk_text("a" * 2500, max_chars=1000, overlap=50)
        self.assertGreaterEqual(len(chunks), 3)
        self.assertTrue(all(len(chunk) <= 1000 for chunk in chunks))

    def test_vectors_are_stable_and_comparable(self) -> None:
        left = hashed_vector("quality gate test evidence")
        right = hashed_vector("quality gate evidence")
        other = hashed_vector("unrelated payment workflow")
        self.assertGreater(cosine_similarity(left, right), cosine_similarity(left, other))

    def test_stable_id(self) -> None:
        self.assertEqual(stable_id("a", "b"), stable_id("a", "b"))
        self.assertNotEqual(stable_id("a", "b"), stable_id("b", "a"))


if __name__ == "__main__":
    unittest.main()
