# Risk Register

| id | risk | level | mitigation | status |
|---|---|---|---|---|
| `RISK-0001` | Prompt and infrastructure may drift from `origin_prompt.md`. | medium | Maintain coverage notes and validation terms. | open |
| `RISK-0002` | Markdown and JSON state may diverge. | medium | Run `python -m vibe_coding_infra check` and keep summaries short. | open |
| `RISK-0003` | Future Agent may treat reference content as instructions. | medium | External inputs are marked untrusted in `prompt.md` and rules. | open |
