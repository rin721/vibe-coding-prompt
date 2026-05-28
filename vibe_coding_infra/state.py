from __future__ import annotations

from pathlib import Path
from typing import Any

from .io import read_json
from .models import SLICE_PRIORITY


def load_slices(root: Path) -> list[dict[str, Any]]:
    data = read_json(root / "docs/ai/tasks/execution_slices.json")
    slices = data.get("slices", [])
    return [item for item in slices if isinstance(item, dict)]


def load_status_items(root: Path) -> list[dict[str, Any]]:
    data = read_json(root / "docs/ai/state/status.json")
    items = data.get("status_items", [])
    return [item for item in items if isinstance(item, dict)]


def choose_next_slice(root: Path) -> dict[str, Any]:
    slices = load_slices(root)
    if not slices:
        return {
            "status": "blocked",
            "reason": "No execution slices are defined.",
            "next_slice": None,
        }

    candidates_by_status: dict[str, list[dict[str, Any]]] = {
        status: [item for item in slices if item.get("status") == status]
        for status in SLICE_PRIORITY
    }

    for status in SLICE_PRIORITY:
        candidates = sorted(candidates_by_status[status], key=lambda item: item.get("id", ""))
        if len(candidates) == 1:
            return {
                "status": "ready",
                "reason": f"Selected the only `{status}` slice by priority.",
                "next_slice": candidates[0],
            }
        if len(candidates) > 1:
            return {
                "status": "diagnosis_required",
                "reason": f"Multiple `{status}` slices exist; a human or Agent must resolve uniqueness.",
                "next_slice": None,
                "candidates": [item.get("id") for item in candidates],
            }

    completed = [item for item in slices if item.get("status") in {"completed", "archived", "skipped"}]
    if len(completed) == len(slices):
        return {
            "status": "complete",
            "reason": "All execution slices are completed, archived, or skipped.",
            "next_slice": None,
        }

    return {
        "status": "diagnosis_required",
        "reason": "No uniquely actionable slice matched the standard priority order.",
        "next_slice": None,
    }
