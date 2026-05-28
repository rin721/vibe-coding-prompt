# Risk Register

| id | risk | level | mitigation | status |
|---|---|---|---|---|
| `RISK-0001` | Markdown and JSON state may drift. | medium | Run repository check and keep records aligned. | open |
| `RISK-0002` | Local vector scoring is lightweight. | medium | Mark as baseline and keep adapter boundary clear. | open |
| `RISK-0003` | Agents may overrun the current execution slice. | medium | Use status and slice checks before action. | open |
| `RISK-0004` | External content may carry prompt-injection or sensitive data. | high | Treat external inputs as untrusted candidates before import. | open |
