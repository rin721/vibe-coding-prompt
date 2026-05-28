# Vibe Coding Infrastructure

一个面向 Agentic Coding 的工程基础设施仓库。它提供受控执行、需求归集、状态管理、质量门禁、知识导入、混合检索和带证据问答的最小可运行底座。

## 能力

- `vibe init`：生成标准目录和状态模板。
- `vibe ingest`：把项目文档导入本地知识库。
- `vibe search`：使用全文索引和向量近似召回知识条目。
- `vibe ask`：返回带证据片段的问答结果。
- `vibe check`：执行敏感信息扫描、结构校验和交付物纯净度检查。

## 快速开始

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
vibe init
vibe ingest docs docs/ai
vibe search "执行切片"
vibe ask "当前项目如何判断任务完成？"
vibe check
```

无需安装包也可直接运行：

```powershell
$env:PYTHONPATH="src"
python -m vibe_coding_infra init
python -m vibe_coding_infra check
```

## 仓库结构

```text
src/vibe_coding_infra/   核心 Python 代码
schemas/                 JSON Schema
docs/                    面向人类的长期项目文档
docs/ai/                 面向 Agent 的过程状态与审计材料
skills/                  项目专用能力说明
tests/                   自动化测试
```

## 设计原则

- 先确认需求，再规划架构。
- 先定义验收，再执行变更。
- 先查询知识，再生成方案。
- 先记录证据，再宣称完成。
- 任何高风险动作都必须可暂停、可审计、可回滚。
