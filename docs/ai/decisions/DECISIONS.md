# Decisions

| id | decision | status | evidence | updated_at |
|---|---|---|---|---|
| `DEC-0001` | 使用 Python 标准库实现基础设施 CLI，避免引入不必要依赖。 | `accepted` | `pyproject.toml`, `vibe_coding_infra/` | `2026-05-28` |
| `DEC-0002` | Markdown 给人读，JSON 给工具校验，二者并存。 | `accepted` | `docs/ai/*/*.json` | `2026-05-28` |
| `DEC-0003` | 默认状态流以执行切片为中心。 | `accepted` | `docs/ai/tasks/execution_slices.json` | `2026-05-28` |
| `DEC-0004` | 将专属 Vibe Coding 编程知识库作为独立产品级基建写入 `origin_prompt.md`，并约束其事实来源身份不得绕过安全、确认和证据规则。 | `accepted` | `origin_prompt.md`, `REQ-0005` | `2026-05-28` |
