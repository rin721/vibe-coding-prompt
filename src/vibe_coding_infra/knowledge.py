from __future__ import annotations

import json
import sqlite3
from contextlib import closing
from pathlib import Path
from typing import Iterable

from .models import Answer, KnowledgeEntry, SearchResult
from .storage import iter_text_files
from .text import chunk_text, cosine_similarity, hashed_vector, make_snippet, stable_id, tokenize


class KnowledgeBase:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def init(self) -> None:
        with closing(self.connect()) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS entries (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    body TEXT NOT NULL,
                    source_path TEXT NOT NULL,
                    source_kind TEXT NOT NULL,
                    trust_level TEXT NOT NULL,
                    status TEXT NOT NULL,
                    tags_json TEXT NOT NULL,
                    metadata_json TEXT NOT NULL,
                    vector_json TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            connection.execute(
                """
                CREATE VIRTUAL TABLE IF NOT EXISTS entries_fts
                USING fts5(id UNINDEXED, title, body, source_path)
                """
            )
            connection.commit()

    def upsert(self, entry: KnowledgeEntry) -> None:
        vector = hashed_vector(f"{entry.title}\n{entry.body}")
        with closing(self.connect()) as connection:
            connection.execute(
                """
                INSERT INTO entries (
                    id, title, body, source_path, source_kind, trust_level, status,
                    tags_json, metadata_json, vector_json, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    title=excluded.title,
                    body=excluded.body,
                    source_path=excluded.source_path,
                    source_kind=excluded.source_kind,
                    trust_level=excluded.trust_level,
                    status=excluded.status,
                    tags_json=excluded.tags_json,
                    metadata_json=excluded.metadata_json,
                    vector_json=excluded.vector_json,
                    updated_at=excluded.updated_at
                """,
                (
                    entry.id,
                    entry.title,
                    entry.body,
                    entry.source_path,
                    entry.source_kind,
                    entry.trust_level,
                    entry.status,
                    json.dumps(entry.tags, ensure_ascii=False),
                    json.dumps(entry.metadata, ensure_ascii=False, sort_keys=True),
                    json.dumps(vector),
                    entry.updated_at,
                ),
            )
            connection.execute("DELETE FROM entries_fts WHERE id = ?", (entry.id,))
            connection.execute(
                "INSERT INTO entries_fts(id, title, body, source_path) VALUES (?, ?, ?, ?)",
                (entry.id, entry.title, entry.body, entry.source_path),
            )
            connection.commit()

    def ingest_paths(self, paths: Iterable[Path], root: Path | None = None) -> int:
        self.init()
        count = 0
        root = root or Path.cwd()
        for path in iter_text_files(paths):
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            relative = _safe_relative(path, root).as_posix()
            for index, chunk in enumerate(chunk_text(text)):
                title = _title_for(path, chunk, index)
                entry = KnowledgeEntry(
                    id=stable_id(str(relative), str(index), chunk[:80]),
                    title=title,
                    body=chunk,
                    source_path=relative,
                    source_kind="document" if path.suffix.lower() in {".md", ".txt", ".rst"} else "code",
                    trust_level="project",
                    tags=[path.suffix.lower().lstrip(".") or "text"],
                    metadata={"chunk_index": index, "path": relative},
                )
                self.upsert(entry)
                count += 1
        return count

    def search(self, query: str, limit: int = 5) -> list[SearchResult]:
        self.init()
        query_vector = hashed_vector(query)
        candidates: dict[str, float] = {}
        with closing(self.connect()) as connection:
            for row in self._fts_rows(connection, query, limit * 4):
                candidates[row["id"]] = candidates.get(row["id"], 0.0) + 1.0
            for row in connection.execute("SELECT * FROM entries"):
                vector = json.loads(row["vector_json"])
                score = cosine_similarity(query_vector, vector)
                if score > 0:
                    candidates[row["id"]] = candidates.get(row["id"], 0.0) + score
            if not candidates:
                return []
            placeholders = ",".join("?" for _ in candidates)
            rows = connection.execute(f"SELECT * FROM entries WHERE id IN ({placeholders})", tuple(candidates)).fetchall()

        results: list[SearchResult] = []
        for row in rows:
            entry = _entry_from_row(row)
            score = candidates[entry.id]
            results.append(SearchResult(entry=entry, score=score, highlights=[make_snippet(entry.body, query)]))
        results.sort(key=lambda item: item.score, reverse=True)
        return results[:limit]

    def ask(self, question: str, limit: int = 4) -> Answer:
        results = self.search(question, limit=limit)
        if not results:
            return Answer(
                question=question,
                answer="没有找到足够证据。请先导入相关文档，或补充更具体的问题。",
                citations=[],
            )
        lines = ["基于当前可检索证据，可以这样回答："]
        for index, result in enumerate(results, start=1):
            snippet = result.highlights[0] if result.highlights else make_snippet(result.entry.body, question)
            lines.append(f"{index}. {snippet} [{result.entry.source_path}]")
        return Answer(question=question, answer="\n".join(lines), citations=results)

    def _fts_rows(self, connection: sqlite3.Connection, query: str, limit: int) -> list[sqlite3.Row]:
        terms = tokenize(query)
        if not terms:
            return []
        fts_query = " OR ".join(terms[:8])
        try:
            return connection.execute(
                "SELECT id FROM entries_fts WHERE entries_fts MATCH ? LIMIT ?",
                (fts_query, limit),
            ).fetchall()
        except sqlite3.OperationalError:
            return []


def _entry_from_row(row: sqlite3.Row) -> KnowledgeEntry:
    return KnowledgeEntry(
        id=row["id"],
        title=row["title"],
        body=row["body"],
        source_path=row["source_path"],
        source_kind=row["source_kind"],
        trust_level=row["trust_level"],
        status=row["status"],
        tags=json.loads(row["tags_json"]),
        metadata=json.loads(row["metadata_json"]),
        updated_at=row["updated_at"],
    )


def _title_for(path: Path, chunk: str, index: int) -> str:
    for line in chunk.splitlines():
        cleaned = line.strip().lstrip("#").strip()
        if cleaned:
            return cleaned[:120]
    return f"{path.name} chunk {index + 1}"


def _safe_relative(path: Path, root: Path) -> Path:
    try:
        return path.resolve().relative_to(root.resolve())
    except ValueError:
        return path.resolve()
