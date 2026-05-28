# Decisions

| id | decision | status | evidence | updated_at |
|---|---|---|---|---|
| `DEC-0001` | 使用 Python 标准库实现基础设施 CLI，避免引入不必要依赖。 | `accepted` | `pyproject.toml`, `vibe_coding_infra/` | `2026-05-28` |
| `DEC-0002` | Markdown 给人读，JSON 给工具校验，二者并存。 | `accepted` | `docs/ai/*/*.json` | `2026-05-28` |
| `DEC-0003` | 默认状态流以执行切片为中心。 | `accepted` | `docs/ai/tasks/execution_slices.json` | `2026-05-28` |
| `DEC-0004` | 将专属 Vibe Coding 编程知识库作为独立产品级基建写入 `origin_prompt.md`，并约束其事实来源身份不得绕过安全、确认和证据规则。 | `accepted` | `origin_prompt.md`, `REQ-0005` | `2026-05-28` |
| `DEC-0005` | 使用 Python 标准库实现本地知识条目导入、全文检索、轻量向量表示和带证据问答入口，作为后续外接向量数据库或搜索服务前的可验证核心骨架。 | `accepted` | `REQ-0006`, `vibe_coding_infra/knowledge_base.py`, `tests/test_knowledge_base.py` | `2026-05-28` |
