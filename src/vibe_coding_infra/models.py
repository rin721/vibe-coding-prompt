from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


TrustLevel = Literal["official", "primary", "project", "community", "unverified"]
RequirementStatus = Literal[
    "confirmed",
    "pending_confirmation",
    "ai_inferred",
    "research_pending",
    "rejected",
    "deferred",
    "out_of_current_version",
    "backlog",
    "decision_required",
]
SliceStatus = Literal[
    "not_started",
    "in_progress",
    "needs_verification",
    "needs_acceptance",
    "blocked",
    "rework",
    "done",
    "skipped",
    "archived",
]


@dataclass(slots=True)
class Evidence:
    title: str
    locator: str
    trust_level: TrustLevel = "project"
    key_points: list[str] = field(default_factory=list)
    collected_at: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class Requirement:
    id: str
    source: str
    raw_text: str
    normalized_text: str
    type: str
    status: RequirementStatus
    priority_or_version: str = ""
    decision: str = ""
    related_slice: str = ""
    conflicts: list[str] = field(default_factory=list)
    evidence: list[Evidence] = field(default_factory=list)
    next_action: str = ""
    updated_at: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["evidence"] = [item.to_dict() for item in self.evidence]
        return data


@dataclass(slots=True)
class ExecutionSlice:
    id: str
    goal: str
    status: SliceStatus = "not_started"
    authorization_level: str = "suggestion"
    authorization_source: str = ""
    files: list[str] = field(default_factory=list)
    commands: list[str] = field(default_factory=list)
    non_goals: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    quality_gates: list[str] = field(default_factory=list)
    rollback: str = ""
    evidence: list[Evidence] = field(default_factory=list)
    next_action: str = ""
    updated_at: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["evidence"] = [item.to_dict() for item in self.evidence]
        data["authorization"] = {
            "level": data.pop("authorization_level"),
            "source": data.pop("authorization_source"),
        }
        data["scope"] = {
            "files": data.pop("files"),
            "commands": data.pop("commands"),
            "non_goals": data.pop("non_goals"),
        }
        return data


@dataclass(slots=True)
class KnowledgeEntry:
    id: str
    title: str
    body: str
    source_path: str
    source_kind: str = "document"
    trust_level: TrustLevel = "project"
    status: str = "stable"
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    updated_at: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class SearchResult:
    entry: KnowledgeEntry
    score: float
    highlights: list[str] = field(default_factory=list)


@dataclass(slots=True)
class Answer:
    question: str
    answer: str
    citations: list[SearchResult]

    def to_dict(self) -> dict[str, Any]:
        return {
            "question": self.question,
            "answer": self.answer,
            "citations": [
                {
                    "id": item.entry.id,
                    "title": item.entry.title,
                    "source_path": item.entry.source_path,
                    "score": round(item.score, 4),
                    "highlights": item.highlights,
                }
                for item in self.citations
            ],
        }
