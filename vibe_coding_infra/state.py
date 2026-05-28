from __future__ import annotations

from pathlib import Path
from typing import Any

from .io import read_json
from .models import SLICE_PRIORITY


def load_status(root: Path) -> list[dict[str, Any]]:
    data = read_json(root / "docs/ai/state/status.json")
    items = data.get("status_items", [])
    if not isinstance(items, list):
        raise ValueError("status_items must be a list")
    return [item for item in items if isinstance(item, dict)]


def choose_next_status(root: Path) -> dict[str, Any] | None:
    items = load_status(root)
    by_status: dict[str, list[dict[str, Any]]] = {status: [] for status in SLICE_PRIORITY}
    for item in items:
        status = item.get("status")
        if status in by_status:
            by_status[status].append(item)
    for status in SLICE_PRIORITY:
        candidates = sorted(by_status[status], key=lambda item: str(item.get("id", "")))
        if candidates:
            return candidates[0]
    return None


def next_summary(root: Path) -> dict[str, Any]:
    selected = choose_next_status(root)
    if selected is None:
        return {
            "status": "complete",
            "message": "No active, blocked, pending, rework, or not-started status item was found.",
            "item": None,
        }
    state = selected.get("status", "unknown")
    if state in {"blocked", "decision_required"}:
        message = "Current work is blocked or requires a decision before execution."
    elif state == "pending_verification":
        message = "Run verification for the selected status item before moving on."
    elif state == "needs_rework":
        message = "Rework the selected status item inside its allowed scope."
    elif state == "in_progress":
        message = "Continue the current in-progress execution slice."
    else:
        message = "Start the selected not-started execution slice if its dependencies are satisfied."
    return {"status": state, "message": message, "item": selected}
