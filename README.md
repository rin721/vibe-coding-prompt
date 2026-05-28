# Vibe Coding Infrastructure

This repository provides a Vibe Coding foundation for AI-assisted software delivery. It combines an agent contract, project state files, executable quality gates, local knowledge retrieval, and handoff records so future agents can recover context and continue work safely.

## What It Contains

- Root agent contract for engineering behavior and safety rules.
- `AGENTS.md` with local operating rules.
- `docs/` for long-lived human documentation.
- `docs/ai/` for requirements, research, decisions, execution slices, status, test evidence, risks, and handoff.
- `schemas/` for machine-readable validation.
- `vibe_coding_infra/` for local checks, next-step diagnosis, knowledge import, full-text search, lightweight vector scoring, and evidence-backed answers.
- `skills/` for reusable project-specific workflows.
- `tests/` for infrastructure behavior.

## Quick Start

```powershell
python -m vibe_coding_infra check
python -m vibe_coding_infra next
python -m vibe_coding_infra knowledge-import
python -m vibe_coding_infra knowledge-search "执行切片"
python -m vibe_coding_infra knowledge-answer "下一步之前要读取什么？"
python -m unittest discover -s tests
```

## Workflow

1. Confirm requirements, mode, architecture level, and agency level.
2. Record stable decisions and current state under `docs/ai/`.
3. Split work into tasks and execution slices.
4. Execute only the current legal slice.
5. Run quality gates and record evidence.
6. Import stable knowledge into the local knowledge index.
7. Update handoff before ending a work session.

## Quality Gates

The baseline gates are:

```powershell
python -m vibe_coding_infra check
python -m unittest discover -s tests
```

The knowledge smoke checks are:

```powershell
python -m vibe_coding_infra knowledge-import
python -m vibe_coding_infra knowledge-search "质量门禁" --limit 3
python -m vibe_coding_infra knowledge-answer "当前仓库如何判断下一步？" --limit 3
```
