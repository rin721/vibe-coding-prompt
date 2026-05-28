# Project Overview

本项目是一套 Vibe Coding 基础设施：它把 `origin_prompt.md` 推导成标准版 `prompt.md`，再用该 prompt 建立可被 AI Agent 持续读取、执行和验证的工程仓库。

## Goals

- 让普通想法者能从模糊想法进入工程化协作。
- 让 Agent 的代理行动权可校准、可审计、可暂停、可回滚、可收回。
- 让需求、研究、架构、任务、执行切片、状态、证据和交接都落盘。
- 提供最小 CLI 和 schema，帮助后续 Agent 检查仓库健康度并找到下一步。
- 提供专属 Vibe Coding 编程知识库/RAG 本地核心，让稳定事实可搜索、可问答、可检索增强并可回溯证据。

## Non Goals

- 不替代具体业务项目的需求确认。
- 不承诺某个 AI 工具拥有无限自治。
- 不机械复刻任何参考仓库目录。

## Primary Artifacts

- `prompt.md`：Agent 行为规范。
- `docs/ai/requirements/REQUIREMENT_LEDGER.md`：需求台账。
- `docs/ai/tasks/EXECUTION_SLICES.md`：执行切片。
- `docs/ai/state/STATUS.md`：当前状态。
- `docs/KNOWLEDGE_BASE.md`：知识库/RAG 架构说明。
- `schemas/knowledge-entry.schema.json`：知识条目 schema。
- `vibe_coding_infra/`：校验、下一步诊断和知识库/RAG 本地核心代码。
