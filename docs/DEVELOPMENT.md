# Development

## Requirements

- Python `3.9+`
- No runtime third-party dependencies

## Commands

```powershell
python -m vibe_coding_infra check
python -m vibe_coding_infra next
python -m unittest discover -s tests
```

## Change Rules

- 修改 `origin_prompt.md` 需要开发者明确授权。
- 修改 `prompt.md` 后必须运行基础设施检查。
- 修改 `vibe_coding_infra/` 后必须运行单元测试。
- 修改 `docs/ai/*` 后必须保持 JSON 与 Markdown 摘要一致。
