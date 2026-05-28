from __future__ import annotations

import argparse
import json
from pathlib import Path

from .knowledge import KnowledgeBase
from .quality import check_workspace
from .scaffold import scaffold


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="vibe", description="Governed Agentic Coding infrastructure tools.")
    parser.add_argument("--root", default=".", help="Workspace root.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create standard directories and state templates.")
    init_parser.add_argument("--force", action="store_true", help="Overwrite existing template files.")

    ingest_parser = subparsers.add_parser("ingest", help="Import text files into the local knowledge base.")
    ingest_parser.add_argument("paths", nargs="*", default=["docs", "docs/ai"], help="Files or directories to ingest.")
    ingest_parser.add_argument("--db", default=".vibe/knowledge.sqlite3", help="Knowledge database path.")

    search_parser = subparsers.add_parser("search", help="Search the local knowledge base.")
    search_parser.add_argument("query")
    search_parser.add_argument("--limit", type=int, default=5)
    search_parser.add_argument("--db", default=".vibe/knowledge.sqlite3")

    ask_parser = subparsers.add_parser("ask", help="Answer a question with retrieved evidence.")
    ask_parser.add_argument("question")
    ask_parser.add_argument("--limit", type=int, default=4)
    ask_parser.add_argument("--db", default=".vibe/knowledge.sqlite3")

    check_parser = subparsers.add_parser("check", help="Run local quality checks.")
    check_parser.add_argument("paths", nargs="*", help="Optional files or directories to scan.")
    check_parser.add_argument("--forbid", action="append", default=[], help="Term that must not appear in scanned files.")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()

    if args.command == "init":
        changed = scaffold(root, force=args.force)
        print(json.dumps({"created_or_updated": changed}, ensure_ascii=False, indent=2))
        return 0

    if args.command == "ingest":
        db = KnowledgeBase(root / args.db)
        paths = [root / item for item in args.paths]
        count = db.ingest_paths(paths, root=root)
        print(json.dumps({"ingested": count, "database": str(root / args.db)}, ensure_ascii=False, indent=2))
        return 0

    if args.command == "search":
        db = KnowledgeBase(root / args.db)
        results = db.search(args.query, limit=args.limit)
        payload = [
            {
                "id": result.entry.id,
                "title": result.entry.title,
                "source_path": result.entry.source_path,
                "score": round(result.score, 4),
                "highlights": result.highlights,
            }
            for result in results
        ]
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    if args.command == "ask":
        db = KnowledgeBase(root / args.db)
        answer = db.ask(args.question, limit=args.limit)
        print(json.dumps(answer.to_dict(), ensure_ascii=False, indent=2))
        return 0

    if args.command == "check":
        paths = [root / item for item in args.paths] if args.paths else None
        report = check_workspace(root, paths=paths, forbidden_terms=args.forbid)
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
        return 0 if report.ok else 1

    parser.error(f"Unknown command: {args.command}")
    return 2
