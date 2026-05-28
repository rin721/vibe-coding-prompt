# Execution Slices

| id | title | status | allowed files | verification |
|---|---|---|---|---|
| `SLICE-001` | Standard prompt finalization | `completed` | `prompt.md` | UTF-8 check, prompt term check |
| `SLICE-002` | Infrastructure repository generation | `completed` | `README.md`, `AGENTS.md`, `docs/`, `schemas/`, `vibe_coding_infra/`, `scripts/`, `skills/`, `.github/` | infrastructure check |
| `SLICE-003` | Quality gate verification | `completed` | `docs/ai/reports/TEST_REPORT.md`, status files | `python -m vibe_coding_infra check`, `python -m unittest discover -s tests` |
| `SLICE-004` | Origin prompt Knowledge Base/RAG optimization | `completed` | `origin_prompt.md`, `docs/ai/requirements/`, `docs/ai/decisions/`, `docs/ai/tasks/`, `docs/ai/state/`, `docs/ai/reports/` | UTF-8 check, required KB/RAG term check, infrastructure check |
