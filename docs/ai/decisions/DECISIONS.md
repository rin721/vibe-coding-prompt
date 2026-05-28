# Decisions

| id | decision | status | evidence | updated_at |
|---|---|---|---|---|
| `DEC-0001` | 使用 Python 标准库实现基础设施 CLI，避免引入不必要依赖。 | `accepted` | `pyproject.toml`, `vibe_coding_infra/` | `2026-05-28` |
| `DEC-0002` | Markdown 给人读，JSON 给工具校验，二者并存。 | `accepted` | `docs/ai/*/*.json` | `2026-05-28` |
| `DEC-0003` | 默认状态流以执行切片为中心。 | `accepted` | `docs/ai/tasks/execution_slices.json` | `2026-05-28` |
