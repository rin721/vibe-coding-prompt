from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Iterable


DEFAULT_DIRS = [
    "docs/overview",
    "docs/architecture",
    "docs/development",
    "docs/operations",
    "docs/knowledge",
    "docs/ai/requirements",
    "docs/ai/research",
    "docs/ai/decisions",
    "docs/ai/tasks",
    "docs/ai/slices",
    "docs/ai/status",
    "docs/ai/reports",
    "docs/ai/handoff",
    "docs/ai/learning",
    "docs/ai/rules",
    "docs/ai/security",
    "skills/project",
    "schemas",
    ".vibe",
]


def ensure_dirs(root: Path, dirs: Iterable[str] = DEFAULT_DIRS) -> None:
    for directory in dirs:
        (root / directory).mkdir(parents=True, exist_ok=True)


def write_text_if_missing(path: Path, text: str, force: bool = False) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        return False
    path.write_text(text, encoding="utf-8", newline="\n")
    return True


def append_jsonl(path: Path, item: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = asdict(item) if is_dataclass(item) else item
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        handle.write("\n")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def iter_text_files(paths: Iterable[Path]) -> Iterable[Path]:
    allowed_suffixes = {".md", ".txt", ".rst", ".py", ".toml", ".json", ".yaml", ".yml"}
    for path in paths:
        if path.is_file() and path.suffix.lower() in allowed_suffixes:
            yield path
        elif path.is_dir():
            for child in path.rglob("*"):
                if child.is_file() and child.suffix.lower() in allowed_suffixes:
                    if any(part.startswith(".") for part in child.parts):
                        continue
                    yield child
