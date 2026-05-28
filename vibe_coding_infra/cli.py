from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .io import ensure_repo_root
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

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)
