# Execution Slices / 执行切片

执行切片是 Agent 单次推进的最小安全闭环，必须包含目标、授权、文件范围、风险、质量门禁、证据和下一步。

| ID | Goal | Status | Authorization | Files | Gates | Next Action |
| --- | --- | --- | --- | --- | --- | --- |
| SLICE-001 | Generate repository baseline | done | developer request | `README.md`, `src/`, `docs/`, `schemas/`, `tests/` | tests, check, scan | maintain |
| SLICE-002 | Evaluate retrieval quality | backlog | project roadmap | `.vibe/`, `docs/knowledge/` | search examples | create evaluation set |
