# Development

## Requirements

- Python `3.9+`
- No runtime third-party dependencies

## Commands

```powershell
python -m vibe_coding_infra check
python -m vibe_coding_infra next
python -m vibe_coding_infra knowledge-import
python -m vibe_coding_infra knowledge-search "执行切片"
python -m vibe_coding_infra knowledge-answer "下一步之前要读取什么？"
python -m unittest discover -s tests
```

## Change Rules

- Read current state and execution slices before editing.
- Keep Markdown summaries and JSON state aligned.
- Update test evidence after running checks.
- Update the knowledge index after stable documentation changes.
- Do not add dependencies unless the current slice permits it and the risk is recorded.
- Pause for destructive operations, secrets, sensitive data, production actions, permissions, payments, or database migrations.

## Coding Style

- Prefer simple standard-library Python.
- Keep CLI output deterministic and easy to parse.
- Use JSON for machine-readable state and Markdown for human-readable context.
- Keep validation errors precise and actionable.
