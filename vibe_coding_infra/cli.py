from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .io import ensure_repo_root
from .knowledge_base import answer_question, build_repository_entries, search_entries, write_index
from .state import choose_next_slice
from .validator import check_repository


def _print_json(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_check(args: argparse.Namespace) -> int:
    root = ensure_repo_root(Path(args.root) if args.root else None)
    findings = check_repository(root)
    payload = {
        "root": str(root),
        "ok": not any(item.level == "error" for item in findings),
        "findings": [item.render(root) for item in findings],
    }
    if args.json:
        _print_json(payload)
    else:
        if payload["ok"]:
            print("Vibe Coding infrastructure check passed.")
        else:
            print("Vibe Coding infrastructure check failed.")
            for finding in findings:
                print(finding.render(root))
    return 0 if payload["ok"] else 1


def cmd_next(args: argparse.Namespace) -> int:
    root = ensure_repo_root(Path(args.root) if args.root else None)
    result = choose_next_slice(root)
    if args.json:
        _print_json(result)
    else:
        print(f"status: {result['status']}")
        print(f"reason: {result['reason']}")
        next_slice = result.get("next_slice")
        if next_slice:
            print(f"next_slice: {next_slice.get('id')} - {next_slice.get('title')}")
            print(f"goal: {next_slice.get('goal')}")
    return 0 if result["status"] in {"ready", "complete"} else 2


def cmd_knowledge_build(args: argparse.Namespace) -> int:
    root = ensure_repo_root(Path(args.root) if args.root else None)
    entries = build_repository_entries(root)
    output = Path(args.output)
    if not output.is_absolute():
        output = root / output
    write_index(output, entries)
    payload = {
        "root": str(root),
        "output": str(output),
        "entries": len(entries),
    }
    if args.json:
        _print_json(payload)
    else:
        print(f"Knowledge index written: {output}")
        print(f"entries: {len(entries)}")
    return 0


def cmd_knowledge_search(args: argparse.Namespace) -> int:
    root = ensure_repo_root(Path(args.root) if args.root else None)
    entries = build_repository_entries(root)
    payload = {
        "query": args.query,
        "results": search_entries(entries, args.query, limit=args.limit),
    }
    if args.json:
        _print_json(payload)
    else:
        for item in payload["results"]:
            entry = item["entry"]
            print(f"{entry['id']} score={item['score']} source={entry['source_path']}")
            print(f"title: {entry['title']}")
            print(f"matched_terms: {', '.join(item['matched_terms'])}")
    return 0


def cmd_knowledge_answer(args: argparse.Namespace) -> int:
    root = ensure_repo_root(Path(args.root) if args.root else None)
    entries = build_repository_entries(root)
    payload = answer_question(entries, args.question, limit=args.limit)
    if args.json:
        _print_json(payload)
    else:
        print(payload["answer"])
        for citation in payload["citations"]:
            print(f"- {citation['entry_id']} {citation['source_path']} score={citation['score']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="vibe-infra")
    parser.add_argument("--root", help="Repository root. Defaults to current directory.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_parser = subparsers.add_parser("check", help="Validate required files and machine-readable state.")
    check_parser.add_argument("--json", action="store_true", help="Print JSON output.")
    check_parser.set_defaults(func=cmd_check)

    next_parser = subparsers.add_parser("next", help="Diagnose the next legal execution slice.")
    next_parser.add_argument("--json", action="store_true", help="Print JSON output.")
    next_parser.set_defaults(func=cmd_next)

    kb_build_parser = subparsers.add_parser("knowledge-build", help="Build a local knowledge index from repository Markdown files.")
    kb_build_parser.add_argument("--output", default="docs/ai/knowledge/knowledge_index.json", help="Output JSON index path.")
    kb_build_parser.add_argument("--json", action="store_true", help="Print JSON output.")
    kb_build_parser.set_defaults(func=cmd_knowledge_build)

    kb_search_parser = subparsers.add_parser("knowledge-search", help="Search local repository knowledge.")
    kb_search_parser.add_argument("query", help="Search query.")
    kb_search_parser.add_argument("--limit", type=int, default=5, help="Maximum result count.")
    kb_search_parser.add_argument("--json", action="store_true", help="Print JSON output.")
    kb_search_parser.set_defaults(func=cmd_knowledge_search)

    kb_answer_parser = subparsers.add_parser("knowledge-answer", help="Return an evidence-grounded answer payload.")
    kb_answer_parser.add_argument("question", help="Question to answer from local knowledge.")
    kb_answer_parser.add_argument("--limit", type=int, default=3, help="Maximum citation count.")
    kb_answer_parser.add_argument("--json", action="store_true", help="Print JSON output.")
    kb_answer_parser.set_defaults(func=cmd_knowledge_answer)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)
