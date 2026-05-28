from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .io import read_json, read_text
from .models import (
    Finding,
    REQUIRED_PATHS,
    REQUIRED_REQUIREMENT_FIELDS,
    REQUIRED_RESEARCH_FIELDS,
    REQUIRED_SLICE_FIELDS,
    REQUIRED_STATUS_FIELDS,
)


def _missing_fields(item: dict, required: Iterable[str]) -> list[str]:
    return [field for field in required if field not in item]


def _check_collection(
    root: Path,
    path: str,
    collection_key: str,
    required_fields: Iterable[str],
) -> list[Finding]:
    full_path = root / path
    findings: list[Finding] = []
    try:
        data = read_json(full_path)
    except Exception as exc:  # noqa: BLE001 - CLI should report parse errors cleanly.
        return [Finding("error", full_path, f"cannot read JSON: {exc}")]

    items = data.get(collection_key)
    if not isinstance(items, list):
        return [Finding("error", full_path, f"missing list field `{collection_key}`")]

    seen: set[str] = set()
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            findings.append(Finding("error", full_path, f"{collection_key}[{index}] is not an object"))
            continue
        missing = _missing_fields(item, required_fields)
        if missing:
            item_id = item.get("id", f"#{index}")
            findings.append(Finding("error", full_path, f"{item_id} missing fields: {', '.join(missing)}"))
        item_id = item.get("id")
        if isinstance(item_id, str):
            if item_id in seen:
                findings.append(Finding("error", full_path, f"duplicate id: {item_id}"))
            seen.add(item_id)
    return findings


def check_repository(root: Path) -> list[Finding]:
    findings: list[Finding] = []

    for relative in REQUIRED_PATHS:
        path = root / relative
        if not path.exists():
            findings.append(Finding("error", path, "required file is missing"))
        elif path.is_file() and path.stat().st_size == 0:
            findings.append(Finding("error", path, "required file is empty"))

    prompt = root / "prompt.md"
    if prompt.exists():
        text = read_text(prompt)
        required_terms = (
            "代理行动权",
            "执行切片",
            "需求台账",
            "搜索研究",
            "质量门禁",
            "专属编程知识库",
            "可检索增强",
            "Single Source of Truth",
            "向量数据库",
            "全文索引",
            "检索 API",
            "智能问答入口",
            "知识条目导入流水线",
        )
        for term in required_terms:
            if term not in text:
                findings.append(Finding("error", prompt, f"missing required prompt term `{term}`"))

    findings.extend(
        _check_collection(
            root,
            "docs/ai/requirements/requirement_ledger.json",
            "requirements",
            REQUIRED_REQUIREMENT_FIELDS,
        )
    )
    findings.extend(
        _check_collection(
            root,
            "docs/ai/research/research_notes.json",
            "research_notes",
            REQUIRED_RESEARCH_FIELDS,
        )
    )
    findings.extend(
        _check_collection(
            root,
            "docs/ai/tasks/execution_slices.json",
            "slices",
            REQUIRED_SLICE_FIELDS,
        )
    )
    findings.extend(
        _check_collection(
            root,
            "docs/ai/state/status.json",
            "status_items",
            REQUIRED_STATUS_FIELDS,
        )
    )
    return findings
