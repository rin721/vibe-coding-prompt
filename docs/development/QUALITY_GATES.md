# Quality Gates

## Default Gates

- Unit tests.
- Schema validation.
- Sensitive information scan.
- Generated artifact purity scan.
- Knowledge ingestion smoke test.

## Local Commands

```powershell
$env:PYTHONPATH="src"
python -m unittest discover -s tests
python -m vibe_coding_infra check
python -m vibe_coding_infra ingest docs docs/ai
python -m vibe_coding_infra search "quality gates"
```

## Completion Rule / 任务完成判定

A task is complete only when implementation, verification evidence, state update and handoff notes agree.

任务完成必须同时满足实现结果、验证证据、状态记录和交接说明一致；缺少任一证据时只能标记为待验证或待验收。
