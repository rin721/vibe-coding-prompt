# 工程级 AI Agent 项目驱动 Prompt 食用教程

这个仓库收纳的是一份面向 AI 编程 Agent 的工程级项目驱动提示词。它不是普通的“帮我写代码”提示词，而是让 Codex、Claude Code、Cursor、Kiro、Google Antigravity 等 Agent 在真实项目里按“需求澄清 -> 文档沉淀 -> 架构规划 -> 任务拆分 -> 时间切片 -> 实现 -> 测试 -> 修复 -> 交接”的节奏推进工作。

## 文件说明

- `prompt.md`：最终可用的完整提示词正文。
- `origin_prompt.md`：原始需求描述，用来追溯这份提示词的生成目标。
- `README.md`：当前这份食用教程。

## 适合什么场景

适合你想让 AI Agent 主动驱动一个工程项目，而不是每一步都靠人手把需求、架构、任务和验收标准说清楚。

典型场景包括：

- 从一个模糊想法启动新项目。
- 让 Agent 先生成项目模板、需求澄清问题和可选技术方案。
- 让 Agent 在写代码前建立文档、状态、任务、测试和交接机制。
- 后续你只想不断发送“下一步”，由 Agent 根据项目状态文件继续推进。
- 希望项目在换 Agent、换工具、清空上下文后仍然能恢复开发。

## 快速使用

1. 打开 `prompt.md`。
2. 将它作为目标 AI 编程工具的系统提示词、项目规则、Agent 规则或长期上下文使用。
3. 在一个项目仓库中启动 Agent。
4. 用一句话描述你想做的项目，例如：

```text
我想做一个面向个人开发者的 API Key 管理工具，可以本地运行，也可以后续扩展成团队 SaaS。
```

5. 让 Agent 按提示词要求先做项目启动，不要直接写代码。
6. 你根据 Agent 生成的模板补充、确认或修正需求。
7. 等需求、架构、任务和时间切片建立完成后，再进入实现阶段。

## 推荐启动口令

可以这样开始：

```text
请按照 prompt.md 的规则启动项目。先不要写代码，先根据我的想法生成项目启动模板、需求澄清模板、技术方案选项、架构约束、验收标准和风险确认项。

项目想法：
<在这里写你的项目想法>
```

## 后续推进方式

当项目文档体系建立完成后，你可以只发送：

```text
下一步
```

Agent 应该根据仓库里的 `STATUS.md`、`TASKS.md`、`TIME_SLICES.md`、`REQUIREMENTS.md`、`ARCHITECTURE.md`、`ACCEPTANCE.md` 等文件判断当前唯一合法任务，然后执行当前时间切片允许范围内的最小工作。

如果状态不清楚，Agent 不应该编造任务，而应该先生成状态诊断报告。

## 最重要的使用原则

- 先文档，后代码。
- 先确认，后实现。
- 先拆分，后执行。
- 先验证，后完成。
- 不依赖聊天上下文，项目事实必须写入仓库文件。
- 不盲从不合理修正，Agent 需要指出风险并给出替代方案。
- 不把“代码写了”当成“任务完成”。
- 不陷入无限重构、无限优化、无限修复。

## 建议搭配的项目文件

正式项目中建议让 Agent 至少维护这些文件：

```text
AGENTS.md
PROJECT_BRIEF.md
REQUIREMENTS.md
ARCHITECTURE.md
ROADMAP.md
TASKS.md
TIME_SLICES.md
STATUS.md
ACCEPTANCE.md
DECISIONS.md
CHANGELOG.md
ISSUES.md
RISK_REGISTER.md
BACKLOG.md
TEST_REPORT.md
AGENT_HANDOFF.md
AGENT_RULES.md
SKILLS.md
```

这些文件的作用是把项目事实沉淀到仓库里，让不同 Agent、不同工具、不同会话都能接力。

## 适配不同 Agent

- Codex：可放入 `AGENTS.md` 或项目级规则。
- Claude Code：可放入 `CLAUDE.md`，也可以同时保留 `AGENTS.md`。
- Cursor：可拆入 `.cursor/rules/`。
- Kiro：可结合 `.kiro/steering/` 和 `.kiro/specs/` 使用。
- Google Antigravity / Antigravity CLI：可放入其支持读取的 rules、context 或 skills 目录。

无论使用哪个工具，核心要求都一样：每次工作前先读项目文档，每次工作后更新项目文档。

## 不建议这样用

- 不要直接让 Agent 跳过需求确认开始写完整项目。
- 不要只把提示词当作一次性聊天上下文。
- 不要在没有 `STATUS.md`、`TASKS.md`、`TIME_SLICES.md` 时反复发送“下一步”。
- 不要让 Agent 在测试没跑、文档没更新、状态没记录时宣称完成。
- 不要把临时想法直接插入当前实现范围；非关键优化应进入 `BACKLOG.md`。

## 一句话理解

这份提示词的目标是让 AI Agent 从“会写代码”升级为“能按工程流程稳定推进项目的协作者”。
