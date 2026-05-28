# 工程级 AI Agent 项目驱动 Prompt 食用教程

这个仓库收纳的是一份面向 AI 编程 Agent 的工程级项目驱动 prompt。它不是普通的“帮我写代码”提示词，而是让 Codex、Claude Code、Kiro、Cursor、Google Antigravity / Antigravity CLI 等 Agent 从一个模糊想法开始，按工程项目的方式逐步推进：

```text
项目类型判断 -> 模式选择 -> 需求澄清 -> 定稿确认 -> 架构规划
-> Agent 基础设施 -> 任务拆分 -> 时间切片 -> 实现 -> 验证
-> 修复 -> 状态记录 -> 交接
```

## 文件说明

- `prompt.md`：最终可直接使用的完整工程级 prompt 正文。
- `origin_prompt.md`：原始需求描述，用来追溯 `prompt.md` 的生成目标。
- `README.md`：当前这份食用教程。

## 适合什么场景

适合你想让 AI Agent 主动驱动一个工程项目，而不是每一步都由你手动说清需求、架构、任务和验收标准。

典型场景：

- 从一个模糊想法启动新项目。
- 让 Agent 先帮你判断项目类型、风险和流程强度。
- 让 Agent 引导不懂代码的普通想法者补全需求。
- 在写代码前建立需求、架构、任务、时间切片、状态、测试和交接机制。
- 后续只发送“下一步”，让 Agent 根据仓库状态文件继续推进。
- 在切换 Agent、切换工具、上下文丢失后仍能恢复项目状态。

不适合直接重型套用到所有小任务。如果只是一次性改一个小文档、修一个明确 bug 或写一个低风险脚本，可以让 Agent 按 `轻量模式` 执行。

## 快速使用

1. 打开 `prompt.md`。
2. 将它放入目标 AI 编程工具的项目规则、系统提示词、长期上下文或 Agent rules 中。
3. 在真实项目仓库里启动 Agent。
4. 先给 Agent 一段普通话描述你的项目想法，不需要一开始就写成专业需求。
5. 明确要求 Agent 先按 `prompt.md` 做项目启动，不要直接写代码。
6. 根据 Agent 生成的选项、问题和模板，补充、修正并确认第一版需求。
7. 等需求、架构、任务和时间切片确认后，再进入实现阶段。

示例项目想法：

```text
我想做一个面向个人开发者的 API Key 管理工具，可以本地运行，
后续也可能扩展成团队 SaaS。现在我只知道大概想解决密钥太乱、
复制粘贴容易出错的问题，请先帮我判断项目类型和第一版范围。
```

## 推荐启动口令

你可以这样开始：

```text
请按照 prompt.md 的规则启动项目。先不要写代码。

请先根据我的想法判断项目类型、风险等级和推荐工作模式，
然后用普通人能理解的语言生成项目启动模板、需求澄清问题、
技术方案选项、第一版范围建议、验收方式和风险确认项。

项目想法：
<在这里写你的项目想法>
```

如果是已有项目接手，可以这样开始：

```text
请按照 prompt.md 的规则接手当前已有项目。先不要重构，也不要直接写代码。

请先扫描仓库结构、README、测试、CI、依赖、现有文档和未提交改动，
再判断项目类型、当前风险、已有规则与 prompt.md 规则的差异，
然后提出最小可行的 docs/ai 状态补齐方案。
```

## 后续怎么发“下一步”

当 Agent 已经建立好项目文档和状态体系后，你可以只发送：

```text
下一步
```

Agent 应该先读取项目里的状态文件，而不是凭聊天记忆行动。通常会读取：

- `docs/ai/state/STATUS.md`
- `docs/ai/tasks/TASKS.md`
- `docs/ai/tasks/TIME_SLICES.md`
- `docs/ai/requirements/REQUIREMENTS.md`
- `docs/ai/architecture/ARCHITECTURE.md`
- `docs/ai/acceptance/ACCEPTANCE.md`
- `docs/ai/reports/TEST_REPORT.md`
- `docs/ai/changes/CHANGELOG.md`
- `docs/ai/handoff/AGENT_HANDOFF.md`

如果状态不清楚，Agent 不应该编造任务，而应该先生成状态诊断报告。

## 三种使用强度

| 模式 | 适合场景 | 文档和流程强度 |
|---|---|---|
| 轻量模式 | 一次性、低风险、小范围任务 | 只保留最小需求、任务边界、状态、验证和变更记录 |
| 标准模式 | 普通工程项目，默认推荐 | 维护需求、架构、任务、时间切片、状态、测试、变更和交接 |
| 严格模式 | 生产、多用户、安全、隐私、权限、资金、长期维护 | 完整文档体系、风险登记、决策记录、测试报告、skills 和交接机制 |

如果项目涉及生产环境、数据损失、密钥、权限、支付、账单、数据库迁移或不可逆操作，应升级到严格模式，或至少进入严格确认流程。

## 建议的项目文档位置

`prompt.md` 要求区分人类长期文档和 AI 过程产物：

```text
docs/                         # 面向开发者、二次开发者和维护者的长期文档
docs/ai/                      # AI Agent 运行产物和状态文件
docs/ai/requirements/         # 需求
docs/ai/architecture/         # 架构
docs/ai/planning/             # 路线图
docs/ai/tasks/                # 任务和时间切片
docs/ai/state/                # 当前状态
docs/ai/reports/              # 测试和验证报告
docs/ai/changes/              # 变更记录
docs/ai/issues/               # 问题记录
docs/ai/risks/                # 风险登记
docs/ai/decisions/            # 决策记录
docs/ai/handoff/              # Agent 交接说明
docs/ai/skills/               # 项目专用 skills
docs/ai/rules/                # Agent 规则入口
docs/ai/learning/             # 可追溯学习记录
```

根目录应尽量保持干净。如果某个工具必须读取根目录规则文件，可以让根目录入口文件指向 `docs/ai/rules/` 中的权威规则。

## 适配不同 Agent

- Codex：可放入项目级规则或 `AGENTS.md`，并让它以 `docs/ai/*` 为项目状态来源。
- Claude Code：可放入 `CLAUDE.md` 或长期项目说明中，再指向 `docs/ai/rules/AGENT_RULES.md`。
- Cursor：可拆入 `.cursor/rules/`，但要保留 `prompt.md` 或 `docs/ai/rules/` 作为权威来源。
- Kiro：可结合 `.kiro/steering/` 和 `.kiro/specs/`，但仓库内 `docs/ai/*` 仍应作为跨工具状态记录。
- Google Antigravity / Antigravity CLI：放入其支持读取的 rules、context 或 skills 目录，并要求先读状态文件再行动。

核心原则不变：每次工作前先读项目文档，每次工作后更新项目文档。

## 最重要的使用原则

- 先确认需求，再写代码。
- 先做项目类型判断，再选流程强度。
- 先拆任务和时间切片，再执行。
- 先验证，再标记完成。
- 代码写完不等于任务完成。
- 不依赖聊天上下文，项目事实必须写入仓库文件。
- 不盲从不合理修正，Agent 必须指出风险并给替代方案。
- 不绕过安全、隐私、权限、资金、生产环境和不可逆操作边界。
- 不陷入无限重构、无限优化、无限修复。

## 不建议这样用

- 不要让 Agent 跳过需求确认直接写完整项目。
- 不要只把 `prompt.md` 当成一次性聊天提示词。
- 不要在没有状态文件时反复发送“下一步”。
- 不要让 Agent 在测试没跑、文档没更新、状态没记录时宣称完成。
- 不要把临时新想法直接插入当前实现范围；非关键想法应进入 backlog。
- 不要把轻量任务强行做成完整重型工程流程。

## 一句话理解

这份 prompt 的目标，是让 AI Agent 从“会写代码的助手”升级为“能按工程流程稳定推进项目、记录证据、保护边界并可交接恢复的协作 Agent”。
