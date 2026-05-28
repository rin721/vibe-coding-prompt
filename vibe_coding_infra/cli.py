from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .io import project_root
from .knowledge_base import answer, import_knowledge, search
from .state import next_summary
from .validator import check_repository


def _print_json(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_check(args: argparse.Namespace) -> int:
    root = project_root(Path(args.cwd) if args.cwd else None)
    findings = check_repository(root)
    if args.json:
        _print_json({"ok": not findings, "findings": [finding.render(root) for finding in findings]})
    elif findings:
        for finding in findings:
            print(finding.render(root))
    else:
        print("ok")
    return 1 if findings else 0


def cmd_next(args: argparse.Namespace) -> int:
    root = project_root(Path(args.cwd) if args.cwd else None)
    result = next_summary(root)
    if args.json:
        _print_json(result)
    else:
        print(result["message"])
        item = result.get("item")
        if item:
            print(f"id: {item.get('id')}")
            print(f"status: {item.get('status')}")
            print(f"next_condition: {item.get('next_condition')}")
    return 0


def cmd_knowledge_import(args: argparse.Namespace) -> int:
    root = project_root(Path(args.cwd) if args.cwd else None)
    entries = import_knowledge(root)
    if args.json:
        _print_json({"entries": len(entries)})
    else:
        print(f"imported {len(entries)} entries")
    return 0


def cmd_knowledge_search(args: argparse.Namespace) -> int:
    root = project_root(Path(args.cwd) if args.cwd else None)
    results = search(root, args.query, limit=args.limit)
    if args.json:
        _print_json({"results": results})
    else:
        for result in results:
            print(f"{result['score']} {result['source_path']} :: {result['title']}")
            print(f"  {result['snippet']}")
    return 0


def cmd_knowledge_answer(args: argparse.Namespace) -> int:
    root = project_root(Path(args.cwd) if args.cwd else None)
    result = answer(root, args.question, limit=args.limit)
    if args.json:
        _print_json(result)
    else:
        print(result["answer"])
        for citation in result["citations"]:
            print(f"- {citation['source_path']} ({citation['trust_level']}, score={citation['score']})")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="vibe-infra")
    parser.add_argument("--cwd", help="Repository root or child path")
    subparsers = parser.add_subparsers(dest="command", required=True)

    check = subparsers.add_parser("check", help="Validate repository infrastructure")
    check.add_argument("--json", action="store_true")
    check.set_defaults(func=cmd_check)

    next_cmd = subparsers.add_parser("next", help="Diagnose the next legal status item")
    next_cmd.add_argument("--json", action="store_true")
    next_cmd.set_defaults(func=cmd_next)

    kb_import = subparsers.add_parser("knowledge-import", help="Build the local knowledge index")
    kb_import.add_argument("--json", action="store_true")
    kb_import.set_defaults(func=cmd_knowledge_import)

    kb_search = subparsers.add_parser("knowledge-search", help="Search the local knowledge index")
    kb_search.add_argument("query")
    kb_search.add_argument("--limit", type=int, default=5)
    kb_search.add_argument("--json", action="store_true")
    kb_search.set_defaults(func=cmd_knowledge_search)

    kb_answer = subparsers.add_parser("knowledge-answer", help="Answer with indexed evidence")
    kb_answer.add_argument("question")
    kb_answer.add_argument("--limit", type=int, default=3)
    kb_answer.add_argument("--json", action="store_true")
    kb_answer.set_defaults(func=cmd_knowledge_answer)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))
