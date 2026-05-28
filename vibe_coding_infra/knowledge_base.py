from __future__ import annotations

import json
import math
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Iterable

from .io import read_text


TOKEN_RE = re.compile(r"[\w.-]+", re.UNICODE)


@dataclass(frozen=True)
class KnowledgeEntry:
    id: str
    title: str
    body: str
    source_path: str
    source_type: str
    trust_level: str
    status: str
    tags: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    updated_at: str = field(default_factory=lambda: date.today().isoformat())
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: dict[str, Any]) -> "KnowledgeEntry":
        return cls(
            id=str(data["id"]),
            title=str(data["title"]),
            body=str(data["body"]),
            source_path=str(data["source_path"]),
            source_type=str(data["source_type"]),
            trust_level=str(data["trust_level"]),
            status=str(data["status"]),
            tags=[str(item) for item in data.get("tags", [])],
            evidence=[str(item) for item in data.get("evidence", [])],
            updated_at=str(data.get("updated_at") or date.today().isoformat()),
            metadata=dict(data.get("metadata", {})),
        )

    def to_mapping(self) -> dict[str, Any]:
        return asdict(self)


def tokenize(text: str) -> list[str]:
    return [match.group(0).lower() for match in TOKEN_RE.finditer(text)]


def entry_vector(entry: KnowledgeEntry) -> Counter[str]:
    vector: Counter[str] = Counter()
    vector.update(tokenize(entry.body))
    vector.update({token: count * 3 for token, count in Counter(tokenize(entry.title)).items()})
    vector.update({token: count * 2 for token, count in Counter(tokenize(" ".join(entry.tags))).items()})
    vector.update(tokenize(entry.source_path))
    return vector


def _cosine_score(query: Counter[str], document: Counter[str]) -> float:
    shared = set(query) & set(document)
    if not shared:
        return 0.0
    numerator = sum(query[token] * document[token] for token in shared)
    query_norm = math.sqrt(sum(value * value for value in query.values()))
    document_norm = math.sqrt(sum(value * value for value in document.values()))
    if query_norm == 0 or document_norm == 0:
        return 0.0
    return numerator / (query_norm * document_norm)


def build_full_text_index(entries: Iterable[KnowledgeEntry]) -> dict[str, list[str]]:
    postings: dict[str, set[str]] = defaultdict(set)
    for entry in entries:
        for token in entry_vector(entry):
            postings[token].add(entry.id)
    return {token: sorted(ids) for token, ids in sorted(postings.items())}


def search_entries(entries: Iterable[KnowledgeEntry], query: str, limit: int = 5) -> list[dict[str, Any]]:
    query_vector = Counter(tokenize(query))
    ranked: list[dict[str, Any]] = []
    for entry in entries:
        vector = entry_vector(entry)
        score = _cosine_score(query_vector, vector)
        if score <= 0:
            continue
        ranked.append(
            {
                "entry": entry.to_mapping(),
                "score": round(score, 6),
                "matched_terms": sorted(set(query_vector) & set(vector)),
            }
        )
    ranked.sort(key=lambda item: (-item["score"], item["entry"]["id"]))
    return ranked[:limit]


def answer_question(entries: Iterable[KnowledgeEntry], question: str, limit: int = 3) -> dict[str, Any]:
    results = search_entries(entries, question, limit=limit)
    citations = [
        {
            "entry_id": item["entry"]["id"],
            "title": item["entry"]["title"],
            "source_path": item["entry"]["source_path"],
            "evidence": item["entry"]["evidence"],
            "score": item["score"],
        }
        for item in results
    ]
    if citations:
        answer = "Found evidence-backed knowledge entries. Review citations before treating the answer as stable fact."
    else:
        answer = "No sufficient evidence found in the local knowledge base. Fall back to source files and record the gap."
    return {
        "question": question,
        "answer": answer,
        "citations": citations,
        "results": results,
    }


def import_markdown_paths(paths: Iterable[Path], root: Path) -> list[KnowledgeEntry]:
    entries: list[KnowledgeEntry] = []
    for index, path in enumerate(sorted({item.resolve() for item in paths if item.exists() and item.is_file()}), start=1):
        text = read_text(path)
        title = _first_heading(text) or path.stem
        relative = str(path.relative_to(root.resolve())).replace("\\", "/")
        entries.append(
            KnowledgeEntry(
                id=f"KB-{index:04d}",
                title=title,
                body=text,
                source_path=relative,
                source_type="markdown",
                trust_level="primary_local_file",
                status="candidate",
                tags=_tags_for_path(relative),
                evidence=[relative],
                metadata={"import_pipeline": "markdown_local_files"},
            )
        )
    return entries


def build_repository_entries(root: Path) -> list[KnowledgeEntry]:
    candidates: list[Path] = []
    for pattern in ("README.md", "AGENTS.md", "prompt.md", "docs/**/*.md", "skills/**/*.md"):
        candidates.extend(root.glob(pattern))
    return import_markdown_paths(candidates, root)


def build_index_payload(entries: Iterable[KnowledgeEntry]) -> dict[str, Any]:
    entry_list = list(entries)
    return {
        "version": 1,
        "generated_at": date.today().isoformat(),
        "entries": [entry.to_mapping() for entry in entry_list],
        "full_text_index": build_full_text_index(entry_list),
        "vector_store": [
            {
                "entry_id": entry.id,
                "weights": dict(entry_vector(entry)),
            }
            for entry in entry_list
        ],
    }


def load_entries(path: Path) -> list[KnowledgeEntry]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    raw_entries = data.get("entries")
    if not isinstance(raw_entries, list):
        raise ValueError("knowledge index missing list field `entries`")
    return [KnowledgeEntry.from_mapping(item) for item in raw_entries if isinstance(item, dict)]


def write_index(path: Path, entries: Iterable[KnowledgeEntry]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = build_index_payload(entries)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _first_heading(text: str) -> str | None:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip() or None
    return None


def _tags_for_path(relative_path: str) -> list[str]:
    parts = [part for part in Path(relative_path).parts if part not in {".", ""}]
    tags = [part.removesuffix(".md").lower() for part in parts[:3]]
    if relative_path.startswith("docs/ai/"):
        tags.append("agent-state")
    if relative_path == "prompt.md":
        tags.append("prompt")
    return sorted(set(tags))
