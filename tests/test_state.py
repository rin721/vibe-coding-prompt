from __future__ import annotations

import unittest
from pathlib import Path

from vibe_coding_infra.state import next_summary


class StateTests(unittest.TestCase):
    def test_complete_when_no_active_status_remains(self) -> None:
        root = Path(__file__).resolve().parents[1]
        result = next_summary(root)
        self.assertEqual("complete", result["status"])
        self.assertIsNone(result["item"])


if __name__ == "__main__":
    unittest.main()
