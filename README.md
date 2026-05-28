# Vibe Coding / Agentic Coding 工程级 Prompt 使用教程

这个仓库提供一份可直接交给 AI 编程 Agent 使用的工程级提示词：

- `prompt.md`：给 AI Agent 使用的权威 prompt / skill 协议。
- `README.md`：给人类使用者看的食用说明。
- `origin_prompt.md`：原始需求描述，保留用于追溯。

它不是普通“怎么写代码”的教程，而是一份让 Agent 自己知道如何从模糊项目想法开始，逐步完成需求澄清、架构规划、任务拆分、执行切片、测试验收、状态管理、文档沉淀和交接恢复的工程协作协议。

## 适合谁

适合这些场景：

- 你只有一个项目想法，但还说不清需求。
- 你希望 AI Agent 不只是写代码，而是能帮你收敛需求、拆任务、做验证和维护状态。
- 你会频繁对 Agent 说“下一步”，希望它能自己从项目文件中恢复上下文。
- 你需要 Codex、Claude Code、Kiro、Cursor、Antigravity 等不同工具都能读懂同一套项目规则。
- 你希望 Agent 的行动权可审计、可暂停、可回滚，而不是无限自动发挥。

不建议把它完整套到极小的一次性任务上。小修小改可以让 Agent 使用 `prompt.md` 中的轻量模式。

## 快速食用

1. 打开 `prompt.md`。
2. 将全文复制到目标 AI 编程工具的系统提示词、项目规则、自定义指令或 Agent rule 中。
3. 在你的项目仓库里对 Agent 说：

```text
请使用这份 prompt 的协议，从我的项目想法开始引导我完成需求确认和工程落地。
我的想法是：……
```

4. Agent 应先判断项目类型、推荐轻量/标准/严格模式，并提出少量关键问题。
5. 需求确认前，不要让 Agent 直接开始写代码。
6. 后续你可以主要发送：

```text
下一步
```

Agent 应读取项目状态文件，找到当前唯一合法执行切片，然后推进、验证、记录和汇报。

## 不同工具怎么用

### Codex

把 `prompt.md` 放入项目规则、系统提示或直接作为本轮任务上下文。若 Codex 支持项目 skill，可把核心规程映射到 skill。

建议第一句话：

```text
请读取 prompt.md，并按其中的工程级 Agent 协议启动这个项目。先不要写代码，先做项目类型判断、模式建议和需求澄清。
```

### Claude Code

将 `prompt.md` 作为 project instructions 或长期规则。让 Claude Code 在项目中维护 `docs/ai/*` 状态文件。

### Cursor

将 `prompt.md` 摘要或全文放入 Cursor Rules。若规则长度受限，可让根目录规则文件指向 `docs/ai/rules/AGENT_RULES.md`，再由 Agent 建立完整文档体系。

### Kiro

把 `prompt.md` 作为 spec/workflow 的上层协议。Kiro 的需求、设计和任务可以映射到 `docs/ai/requirements/`、`docs/ai/architecture/` 和 `docs/ai/tasks/`。

### Google Antigravity / Antigravity CLI

让 Antigravity 读取 `prompt.md` 和项目中的 `docs/ai/*` 文件。每次执行前要求它先确认当前唯一合法执行切片和代理授权。

## 推荐工作流

### 新项目

1. 给 Agent 一个普通语言想法。
2. Agent 判断项目类型。
3. Agent 推荐轻量、标准或严格模式。
4. Agent 引导你回答少量关键问题。
5. 你确认第一版范围和定稿需求。
6. Agent 生成架构、任务树、执行切片和状态文件。
7. 你发送“下一步”，Agent 按切片推进。

### 已有项目接手

1. 让 Agent 先只读扫描仓库。
2. Agent 总结现有结构、规则、测试、CI、依赖和未提交改动。
3. Agent 补齐 `docs/ai/*` 状态与计划。
4. 若现有规则与 prompt 冲突，Agent 先给差异说明，不直接覆盖。
5. 你确认迁移或增量改造方案。

### 单次 bug 修复

可以使用轻量模式。至少保留：

- 问题描述。
- 复现方式。
- 修改范围。
- 验证结果。
- 变更记录。
- 完成判定。

不要强行生成完整 skills 体系。

## 三种模式怎么选

| 模式 | 什么时候用 | 特点 |
|---|---|---|
| 轻量模式 | 小工具、一次性修复、低风险原型 | 少文档，但仍要有需求、状态、验证和变更记录 |
| 标准模式 | 普通工程项目、可维护应用、已有项目接手 | 推荐默认模式，平衡工程质量和成本 |
| 严格模式 | 生产、安全、隐私、权限、资金、多人协作、长期维护 | 需要完整证据、风险登记、决策记录和更强确认 |

如果你不确定，先让 Agent 推荐。默认一般选标准模式。

## 你需要记住的几个词

- **代理行动权**：你委派给 Agent 的工程行动权。它不是无限自治，必须可暂停、可审计、可回滚。
- **定稿需求**：你确认过的第一版需求基线。Agent 后续不能随便改。
- **需求台账**：记录所有想法、修正、拒绝、暂缓和变更去向的文件。
- **任务树**：项目目标拆成阶段、模块和任务。
- **执行切片**：Agent 单次能推进的最小可验证闭环。
- **下一步协议**：你说“下一步”时，Agent 只能按当前唯一合法执行切片行动。

## Agent 应该创建的典型目录

标准或严格模式下，Agent 通常会在项目中维护：

```text
docs/
docs/ai/requirements/REQUIREMENTS.md
docs/ai/requirements/REQUIREMENT_LEDGER.md
docs/ai/architecture/ARCHITECTURE.md
docs/ai/planning/ROADMAP.md
docs/ai/tasks/TASKS.md
docs/ai/tasks/EXECUTION_SLICES.md
docs/ai/state/STATUS.md
docs/ai/reports/TEST_REPORT.md
docs/ai/decisions/DECISIONS.md
docs/ai/changes/CHANGELOG.md
docs/ai/issues/ISSUES.md
docs/ai/handoff/AGENT_HANDOFF.md
docs/ai/risks/RISK_REGISTER.md
docs/ai/skills/
docs/ai/rules/AGENT_RULES.md
```

人类长期文档放在 `docs/`。Agent 过程产物放在 `docs/ai/*`。

## 和 Agent 对话的建议

好的开场：

```text
我想做一个帮助个人管理学习计划的工具，但我不懂技术。请按 prompt.md 的协议先帮我判断项目类型、推荐模式，并用选择题引导我确认第一版范围。
```

好的“下一步”：

```text
下一步
```

好的变更请求：

```text
我想把第一版从本地工具改成网页应用。请先记录为待确认变更，分析影响，不要直接改代码。
```

好的安全提醒：

```text
这里可能涉及真实用户数据。请升级为严格确认流程，先给风险和回滚方案。
```

## 什么时候必须让 Agent 停下来

看到这些情况时，应该要求 Agent 暂停：

- 它还没确认需求就开始写代码。
- 它把你的模糊想法当成已确认事实。
- 它说“顺手”做了不在当前任务里的东西。
- 它要改生产配置、数据库、权限、支付、密钥或部署。
- 它要删除、重置、批量迁移或覆盖未知文件。
- 它测试没跑通却说完成。
- 它找不到当前执行切片还继续编任务。
- 它把轻量任务做成一堆空壳文档。

可以直接说：

```text
暂停。请按 prompt.md 重新说明当前授权来源、当前唯一合法执行切片、风险和下一步确认点。
```

## 如何更新这份 prompt

后续修改 `prompt.md` 时，建议保留版本记录和覆盖追溯，重点检查这些主题有没有丢：

- 普通想法者引导。
- 需求归集与定稿确认。
- 模式裁剪。
- 代理行动权。
- 任务树和执行切片。
- 状态管理。
- 下一步协议。
- 测试验收。
- 失败修复。
- 防死亡优化。
- 文档沉淀。
- 项目专用 skills。
- 自主学习。
- 多工具适配。
- 安全和外部输入防护。
- 已有项目接手。

凡是改变确认边界、完成判定、目录结构、安全规则、下一步协议或 Agent 默认行为的修改，都属于破坏性或代理权影响变更，需要格外谨慎。

## 最小使用原则

这份 prompt 的核心不是“文档越多越好”，而是：

```text
需求要确认，行动要授权，任务要切片，结果要验证，状态要落盘，风险要暂停。
```

如果 Agent 做到了这些，它就能更像一个可靠的工程协作者；如果做不到，就应该先降级为建议型或只读型。
