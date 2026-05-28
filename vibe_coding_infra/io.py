from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def ensure_repo_root(path: Path | None = None) -> Path:
    root = (path or Path.cwd()).resolve()
    if (root / "prompt.md").exists() and (root / "origin_prompt.md").exists():
        return root
    raise FileNotFoundError("not a Vibe Coding infrastructure repository root")
