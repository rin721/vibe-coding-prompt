# Agent Handoff

## Current Summary

The repository is a Vibe Coding infrastructure package. The key authority files are `origin_prompt.md`, `prompt.md`, and `AGENTS.md`. `prompt.md` has been resynced with the optimized Knowledge Base/RAG requirements, and the repository now includes a local dedicated knowledge base core.

## Current Mode

`standard`

## Current Agency

`controlled_execution`

## Current Slice

No active slice. `SLICE-001` through `SLICE-005` are completed.

## Quality Gates

```powershell
python -m vibe_coding_infra check
python -m vibe_coding_infra knowledge-search "执行切片"
python -m unittest discover -s tests
```

Latest result: infrastructure check, knowledge search smoke check, knowledge answer smoke check, and `5` unit tests passed with the Codex bundled Python runtime.

## Forbidden Without Confirmation

- Editing `origin_prompt.md`
- Destructive git operations
- Installing dependencies
- Skipping failed quality gates
