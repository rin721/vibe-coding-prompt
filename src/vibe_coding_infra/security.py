from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


SECRET_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9_\-./+=]{16,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9_\-./+=]{20,}"),
]


@dataclass(slots=True)
class Finding:
    path: str
    line: int
    kind: str
    preview: str


def scan_text(text: str, path: str = "<memory>") -> list[Finding]:
    findings: list[Finding] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for pattern in SECRET_PATTERNS:
            if pattern.search(line):
                findings.append(
                    Finding(
                        path=path,
                        line=line_number,
                        kind="possible_secret",
                        preview=_redact(line.strip()),
                    )
                )
    return findings


def scan_path(path: Path) -> list[Finding]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return []
    return scan_text(text, str(path))


def scan_terms(text: str, forbidden_terms: list[str], path: str = "<memory>") -> list[Finding]:
    findings: list[Finding] = []
    lowered_terms = [term.lower() for term in forbidden_terms]
    for line_number, line in enumerate(text.splitlines(), start=1):
        lowered_line = line.lower()
        for term in lowered_terms:
            if term and term in lowered_line:
                findings.append(
                    Finding(
                        path=path,
                        line=line_number,
                        kind="forbidden_term",
                        preview=_redact(line.strip()),
                    )
                )
    return findings


def _redact(value: str) -> str:
    if len(value) <= 24:
        return "***"
    return f"{value[:12]}...{value[-6:]}"
