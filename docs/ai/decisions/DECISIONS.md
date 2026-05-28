# Decisions

| id | decision | status | evidence | updated_at |
|---|---|---|---|---|
| `DEC-0001` | Use Python standard library for baseline CLI and knowledge tooling. | `accepted` | `pyproject.toml`, `vibe_coding_infra/` | `2026-05-28` |
| `DEC-0002` | Keep Markdown for humans and JSON for machine validation. | `accepted` | `docs/ai/*/*.json`, `schemas/` | `2026-05-28` |
| `DEC-0003` | Use execution slices as the central unit for controlled agent work. | `accepted` | `docs/ai/tasks/execution_slices.json` | `2026-05-28` |
| `DEC-0004` | Implement a local knowledge base/RAG core before external services. | `accepted` | `vibe_coding_infra/knowledge_base.py` | `2026-05-28` |
