from __future__ import annotations

import hashlib
import math
import re
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from .io import read_json, read_text, write_json
from .models import CONTRACT_NAME


INDEX_PATH = Path("docs/ai/knowledge/knowledge_index.json")
TOKEN_RE = re.compile(r"[A-Za-z0-9_./:-]+|[\u4e00-\u9fff]{1,4}")
SENSITIVE_RE = re.compile(
    r"(api[_-]?key|secret|token|password|private[_-]?key)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{8,}",
    re.IGNORECASE,
)
INJECTION_RE = re.compile(
    r"(ignore\s+previous|override\s+instructions|system\s+prompt|忽略.*之前.*指令|忽略.*以上.*指令|覆盖.*系统.*指令)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class KnowledgeEntry:
    id: str
    source_path: str
    title: str
    body: str
    trust_level: str
    tags: list[str]
    checksum: str
    updated_at: str
    deprecated: bool = False


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text)]


def vectorize(text: str) -> Counter[str]:
    return Counter(tokenize(text))


def cosine(a: Counter[str], b: Counter[str]) -> float:
    if not a or not b:
        return 0.0
    common = set(a) & set(b)
    numerator = sum(a[token] * b[token] for token in common)
    a_norm = math.sqrt(sum(value * value for value in a.values()))
    b_norm = math.sqrt(sum(value * value for value in b.values()))
    if not a_norm or not b_norm:
        return 0.0
    return numerator / (a_norm * b_norm)


def checksum(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def default_source_paths(root: Path) -> list[Path]:
    paths: list[Path] = []
    for pattern in ("README.md", "AGENTS.md", CONTRACT_NAME, "docs/**/*.md", "skills/**/*.md"):
        paths.extend(path for path in root.glob(pattern) if path.is_file())
    return sorted(set(paths))


def _title_for(path: Path, body: str) -> str:
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip() or path.stem
    return path.stem


def _tags_for(path: Path) -> list[str]:
    parts = set(path.parts)
    tags: list[str] = []
    if "requirements" in parts:
        tags.append("requirements")
    if "research" in parts:
        tags.append("research")
    if "tasks" in parts:
        tags.append("execution")
    if "state" in parts:
        tags.append("state")
    if "knowledge" in parts:
        tags.append("knowledge")
    if "skills" in parts:
        tags.append("skill")
    if path.name == CONTRACT_NAME:
        tags.append("contract")
    return tags or ["documentation"]


def _source_label(root: Path, path: Path) -> str:
    rel = path.relative_to(root).as_posix()
    if path.name == CONTRACT_NAME:
        return "root_agent_contract"
    return rel


def _trust_for(path: Path, body: str) -> str:
    if SENSITIVE_RE.search(body) or INJECTION_RE.search(body):
        return "needs_review"
    if "docs" in path.parts or path.name in {"README.md", "AGENTS.md", CONTRACT_NAME}:
        return "high"
    return "medium"


def build_entries(root: Path, paths: Iterable[Path] | None = None) -> list[KnowledgeEntry]:
    entries: list[KnowledgeEntry] = []
    for path in paths or default_source_paths(root):
        try:
            body = read_text(path)
        except UnicodeDecodeError:
            continue
        rel = _source_label(root, path)
        digest = checksum(rel + "\n" + body)
        entries.append(
            KnowledgeEntry(
                id=f"KB-{digest[:12]}",
                source_path=rel,
                title=_title_for(path, body),
                body=body,
                trust_level=_trust_for(path, body),
                tags=_tags_for(path),
                checksum=digest,
                updated_at="2026-05-28",
            )
        )
    return entries


def save_index(root: Path, entries: list[KnowledgeEntry]) -> Path:
    path = root / INDEX_PATH
    payload = {"version": 1, "entries": [asdict(entry) for entry in entries]}
    write_json(path, payload)
    return path


def load_entries(root: Path) -> list[KnowledgeEntry]:
    path = root / INDEX_PATH
    if not path.exists():
        return []
    data = read_json(path)
    raw_entries = data.get("entries", [])
    entries: list[KnowledgeEntry] = []
    for item in raw_entries:
        if isinstance(item, dict):
            entries.append(
                KnowledgeEntry(
                    id=str(item.get("id", "")),
                    source_path=str(item.get("source_path", "")),
                    title=str(item.get("title", "")),
                    body=str(item.get("body", "")),
                    trust_level=str(item.get("trust_level", "unverified")),
                    tags=list(item.get("tags", [])),
                    checksum=str(item.get("checksum", "")),
                    updated_at=str(item.get("updated_at", "")),
                    deprecated=bool(item.get("deprecated", False)),
                )
            )
    return entries


def import_knowledge(root: Path) -> list[KnowledgeEntry]:
    entries = build_entries(root)
    save_index(root, entries)
    return entries


def search(root: Path, query: str, limit: int = 5) -> list[dict[str, object]]:
    entries = load_entries(root)
    if not entries:
        entries = import_knowledge(root)
    query_tokens = set(tokenize(query))
    query_vector = vectorize(query)
    results: list[dict[str, object]] = []
    for entry in entries:
        if entry.deprecated:
            continue
        body_tokens = set(tokenize(entry.title + "\n" + entry.body))
        keyword_score = len(query_tokens & body_tokens)
        vector_score = cosine(query_vector, vectorize(entry.title + "\n" + entry.body))
        score = keyword_score + vector_score
        if score <= 0:
            continue
        snippet = _snippet(entry.body, query_tokens)
        results.append(
            {
                "id": entry.id,
                "source_path": entry.source_path,
                "title": entry.title,
                "trust_level": entry.trust_level,
                "tags": entry.tags,
                "score": round(score, 4),
                "snippet": snippet,
            }
        )
    results.sort(key=lambda item: (-float(item["score"]), str(item["source_path"])))
    return results[:limit]


def _snippet(body: str, query_tokens: set[str]) -> str:
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    for line in lines:
        lowered = line.lower()
        if any(token in lowered for token in query_tokens):
            return line[:240]
    return (lines[0] if lines else "")[:240]


def answer(root: Path, question: str, limit: int = 3) -> dict[str, object]:
    hits = search(root, question, limit=limit)
    if not hits:
        return {
            "answer": "No indexed evidence was found. Rebuild the knowledge index or inspect source files directly.",
            "citations": [],
            "confidence": "low",
        }
    citations = [
        {
            "source_path": hit["source_path"],
            "title": hit["title"],
            "trust_level": hit["trust_level"],
            "score": hit["score"],
            "snippet": hit["snippet"],
        }
        for hit in hits
    ]
    answer_text = "The indexed evidence points to: " + " ".join(str(hit["snippet"]) for hit in hits[:2])
    return {"answer": answer_text, "citations": citations, "confidence": "medium"}
