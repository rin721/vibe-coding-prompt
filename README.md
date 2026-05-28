# Vibe Coding 基础设施仓库

这个仓库提供一套可直接交给 AI 编程 Agent 使用的 Vibe Coding 工程基础设施。

它包含：

- `origin_prompt.md`：上游原始需求，用于追溯。
- `prompt.md`：标准版工程级 Agent prompt，是 Agent 行为规范的权威来源。
- `AGENTS.md`：仓库内 Agent 操作规则摘要。
- `docs/`：人类长期项目文档。
- `docs/ai/`：AI Agent 运行状态、需求台账、研究记录、执行切片、测试证据和交接材料。
- `schemas/`：机器可读状态文件的 JSON Schema。
- `vibe_coding_infra/`：基础设施校验与下一步诊断 CLI。
- `skills/`：可复用项目专用 skill 示例。
- `scripts/`：跨工具入口脚本。

核心原则：

```text
需求要确认，行动要授权，任务要切片，结果要验证，状态要落盘，风险要暂停。
```

## 快速开始

检查仓库基础设施：

```powershell
python -m vibe_coding_infra check
```

查看下一步诊断：

```powershell
python -m vibe_coding_infra next
```

运行测试：

```powershell
python -m unittest discover -s tests
```

## 给 Agent 的启动语

```text
请读取 prompt.md 和 AGENTS.md，按 Vibe Coding 工程协议启动。
先恢复 docs/ai/* 状态，确认当前唯一合法执行切片，再决定下一步。
```

## 文档分层

人类长期文档放在 `docs/`，用于理解项目、二次开发、维护和交接。

AI 过程产物放在 `docs/ai/`，用于记录需求、状态、证据、失败、研究、执行切片和代理行动权。

## 模式

| 模式 | 适用场景 | 最小要求 |
|---|---|---|
| 轻量模式 | 小工具、一次性修复、低风险原型 | 目标、边界、状态、验证、变更记录 |
| 标准模式 | 普通工程项目、可维护应用、已有项目接手 | 需求、研究、架构、任务、执行切片、状态、测试 |
| 严格模式 | 生产、安全、隐私、权限、资金、多人协作、长期维护 | 完整确认、审计、风险、回滚、交接和质量门禁 |

## 参考来源

本仓库的上游原始需求来自 `origin_prompt.md`，并吸收 Vibe Coding 基础设施参考仓库的工程语境：`https://github.com/tukuaiai/vibe-coding-cn`。
