# Testing

## Quality Gates

- `python -m vibe_coding_infra check`
- `python -m unittest discover -s tests`

## Evidence

测试结果写入 `docs/ai/reports/TEST_REPORT.md`。

## Completion Rule

只有当基础设施检查和代码测试通过，且状态文件已同步，相关执行切片才可以标记为 `completed`。
