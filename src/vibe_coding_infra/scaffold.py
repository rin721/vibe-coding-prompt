from __future__ import annotations

from pathlib import Path

from .storage import ensure_dirs, write_text_if_missing


TEMPLATES: dict[str, str] = {
    "docs/overview/PROJECT_OVERVIEW.md": """# Project Overview

## Goal

Describe the product goal in plain language.

## Users

- Primary user:
- Secondary user:

## First Version Scope

### Must Have

- 

### Explicit Non Goals

- 

## Acceptance

- 
""",
    "docs/architecture/SYSTEM_ARCHITECTURE.md": """# System Architecture

## Architecture Level

`ordinary_application`

## Modules

| Module | Responsibility | Boundaries |
| --- | --- | --- |
|  |  |  |

## Data Flow

1. 

## Risks

- 
""",
    "docs/knowledge/KNOWLEDGE_BASE.md": """# Knowledge Base

## Positioning

The knowledge base stores verified project facts, decisions, research conclusions, task state, test evidence and reusable engineering patterns.

## Retrieval Surfaces

- Full text search
- Vector similarity search
- Evidence based question answering
- Import and quality review pipeline

## Entry Lifecycle

`candidate -> reviewed -> stable -> deprecated`
""",
    "docs/development/QUALITY_GATES.md": """# Quality Gates

## Default Gates

- Format or style check
- Unit tests
- Schema validation
- Sensitive information scan
- Documentation consistency check

## Completion Rule

A task is complete only when implementation, verification evidence, status update and handoff notes agree.
""",
    "docs/operations/RUNBOOK.md": """# Runbook

## Local Commands

```powershell
$env:PYTHONPATH="src"
python -m vibe_coding_infra check
python -m unittest discover -s tests
```

## Recovery

1. Read project status.
2. Inspect latest task and execution slice.
3. Check Git state.
4. Run available quality gates.
5. Continue only inside the authorized slice.
""",
    "docs/ai/requirements/REQUIREMENTS_LEDGER.md": """# Requirements Ledger

| ID | Source | Raw Text | Normalized Text | Type | Status | Decision | Evidence | Next Action | Updated At |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| REQ-001 | developer | Build Vibe Coding infrastructure | Provide governed workflow, knowledge base, CLI and quality gates | goal | confirmed | included | local files | maintain |  |
""",
    "docs/ai/research/RESEARCH_NOTES.md": """# Research Notes

| ID | Question | Trigger | Evidence | Conclusion | Confidence | Needs Confirmation |
| --- | --- | --- | --- | --- | --- | --- |
""",
    "docs/ai/decisions/DECISIONS.md": """# Decisions

| ID | Decision | Rationale | Status | Evidence | Updated At |
| --- | --- | --- | --- | --- | --- |
| DEC-001 | Use Python standard library for the first local implementation | Keeps setup small and auditable | accepted | code and tests |  |
""",
    "docs/ai/tasks/TASK_TREE.md": """# Task Tree

## Project Goal

Build a governed local infrastructure for Agentic Coding workflows.

## Phases

- Phase 1: Core protocol and repository scaffold
- Phase 2: Knowledge ingestion and retrieval
- Phase 3: Quality gates and workflow automation
- Phase 4: Evaluation and hardening
""",
    "docs/ai/slices/EXECUTION_SLICES.md": """# Execution Slices

| ID | Goal | Status | Authorization | Files | Gates | Next Action |
| --- | --- | --- | --- | --- | --- | --- |
| SLICE-001 | Generate repository baseline | done | developer request | repository scaffold | tests and scans | maintain |
""",
    "docs/ai/status/PROJECT_STATUS.md": """# Project Status

status: `active`
mode: `standard`
agency_level: `controlled_execution`
current_slice: `SLICE-001`

## Latest Evidence

- Repository scaffold exists.
- Local test suite is expected to run with `python -m unittest discover -s tests`.
""",
    "docs/ai/reports/TEST_REPORT.md": """# Test Report

| Run | Command | Result | Notes |
| --- | --- | --- | --- |
""",
    "docs/ai/handoff/HANDOFF.md": """# Handoff

## Current Goal

Maintain the Vibe Coding infrastructure baseline.

## Completed

- Protocol file
- Repository scaffold
- Local knowledge base implementation
- CLI entrypoints

## Next Action

Run quality gates after each change and keep status files synchronized.
""",
    "docs/ai/learning/LESSONS.md": """# Lessons

| ID | Lesson | Evidence | Scope | Risk | Changes Behavior |
| --- | --- | --- | --- | --- | --- |
""",
    "docs/ai/rules/AGENT_CHARTER.md": """# Agent Charter

## Core Rules

- Work only inside the authorized execution slice.
- Preserve user changes.
- Record evidence before marking work complete.
- Escalate high risk actions.
- Keep knowledge entries traceable to source files.
""",
    "docs/ai/security/SECURITY_BOUNDARIES.md": """# Security Boundaries

## Stop Conditions

- Secrets or private data may be exposed.
- Production systems may be changed.
- Data may be deleted or migrated.
- Permission, billing, payment or authentication behavior may change.
- A command is destructive or difficult to roll back.
""",
}


def scaffold(root: Path, force: bool = False) -> list[str]:
    ensure_dirs(root)
    changed: list[str] = []
    for relative, content in TEMPLATES.items():
        if write_text_if_missing(root / relative, content, force=force):
            changed.append(relative)
    return changed
