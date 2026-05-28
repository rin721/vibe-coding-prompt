from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .security import Finding, scan_path, scan_terms
from .storage import iter_text_files


@dataclass(slots=True)
class CheckReport:
    scanned_files: int = 0
    findings: list[Finding] = field(default_factory=list)
    schema_errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.findings and not self.schema_errors

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "scanned_files": self.scanned_files,
            "findings": [finding.__dict__ for finding in self.findings],
            "schema_errors": self.schema_errors,
        }


def check_workspace(root: Path, paths: list[Path] | None = None, forbidden_terms: list[str] | None = None) -> CheckReport:
    report = CheckReport()
    target_paths = paths or [root / "README.md", root / "docs", root / "src", root / "schemas", root / "skills", root / "tests"]
    for file_path in iter_text_files(target_paths):
        report.scanned_files += 1
        report.findings.extend(scan_path(file_path))
        if forbidden_terms:
            text = file_path.read_text(encoding="utf-8")
            report.findings.extend(scan_terms(text, forbidden_terms, str(file_path)))
    report.schema_errors.extend(validate_schema_files(root / "schemas"))
    return report


def validate_schema_files(schema_dir: Path) -> list[str]:
    errors: list[str] = []
    if not schema_dir.exists():
        return ["schemas directory does not exist"]
    for path in schema_dir.glob("*.json"):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{path}: invalid json: {exc}")
            continue
        if payload.get("$schema") is None:
            errors.append(f"{path}: missing $schema")
        if payload.get("type") != "object":
            errors.append(f"{path}: root type must be object")
        if "properties" not in payload:
            errors.append(f"{path}: missing properties")
    return errors
