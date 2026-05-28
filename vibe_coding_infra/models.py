from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


CONTRACT_NAME = "prompt" + ".md"
SOURCE_REQUIREMENTS_NAME = "origin_" + "prompt" + ".md"

REQUIRED_PATHS = (
    SOURCE_REQUIREMENTS_NAME,
    CONTRACT_NAME,
    "AGENTS.md",
    "README.md",
    "docs/PROJECT_OVERVIEW.md",
    "docs/ARCHITECTURE.md",
    "docs/DEVELOPMENT.md",
    "docs/TESTING.md",
    "docs/KNOWLEDGE_BASE.md",
    "docs/ai/requirements/REQUIREMENT_LEDGER.md",
    "docs/ai/requirements/requirement_ledger.json",
    "docs/ai/research/RESEARCH_NOTES.md",
    "docs/ai/research/research_notes.json",
    "docs/ai/decisions/decisions.json",
    "docs/ai/knowledge/README.md",
    "docs/ai/tasks/EXECUTION_SLICES.md",
    "docs/ai/tasks/execution_slices.json",
    "docs/ai/state/STATUS.md",
    "docs/ai/state/status.json",
    "docs/ai/reports/TEST_REPORT.md",
    "docs/ai/handoff/AGENT_HANDOFF.md",
    "schemas/requirement-ledger.schema.json",
    "schemas/execution-slices.schema.json",
    "schemas/knowledge-entry.schema.json",
    "schemas/status.schema.json",
)

REQUIRED_CONTRACT_TERMS = (
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

TRACE_MARKERS = (
    SOURCE_REQUIREMENTS_NAME,
    CONTRACT_NAME,
    "github.com/" + "tukuaiai/" + "vibe-coding-cn",
    "基于上述" + "参考",
    "本文件" + "由",
    "推导" + "生成",
)

GENERATED_SCAN_PATHS = (
    CONTRACT_NAME,
    "AGENTS.md",
    "README.md",
    "docs",
    "metadata",
    "schemas",
    "scripts",
    "skills",
    "tools",
    "vibe_coding_infra",
    "tests",
    ".github",
    "pyproject.toml",
    "Makefile",
    ".gitignore",
)

REQUIRED_REQUIREMENT_FIELDS = (
    "id",
    "source",
    "raw_text",
    "normalized_text",
    "type",
    "priority_or_version",
    "status",
    "decision",
    "related_slice",
    "conflicts",
    "evidence",
    "next_action",
    "updated_at",
)

REQUIRED_SLICE_FIELDS = (
    "id",
    "title",
    "parent_task",
    "phase",
    "module",
    "goal",
    "inputs",
    "outputs",
    "allowed_files",
    "forbidden_files",
    "allowed_tools",
    "approval_required_for",
    "risk_level",
    "agency_level",
    "verification",
    "acceptance",
    "rollback_plan",
    "max_iterations",
    "max_retries",
    "audit_evidence",
    "human_override",
    "status",
    "next_condition",
    "updated_at",
)

REQUIRED_STATUS_FIELDS = (
    "id",
    "title",
    "status",
    "phase",
    "module",
    "depends_on",
    "risk_level",
    "allowed_files",
    "forbidden_files",
    "verification",
    "evidence",
    "next_condition",
    "actor",
    "agent_or_model",
    "authorization_source",
    "tool_calls",
    "input_trust_level",
    "agency_level",
    "human_override",
    "audit_evidence",
    "updated_at",
)

REQUIRED_RESEARCH_FIELDS = (
    "id",
    "question",
    "trigger",
    "query_paths",
    "sources",
    "key_evidence",
    "conclusion",
    "confidence",
    "scope",
    "risks",
    "requires_developer_confirmation",
    "updated_at",
)

SLICE_PRIORITY = (
    "blocked",
    "decision_required",
    "pending_verification",
    "needs_rework",
    "in_progress",
    "not_started",
)


@dataclass(frozen=True)
class Finding:
    level: str
    path: Path
    message: str

    def render(self, root: Path) -> str:
        try:
            rel = self.path.relative_to(root)
        except ValueError:
            rel = self.path
        return f"[{self.level}] {rel}: {self.message}"
