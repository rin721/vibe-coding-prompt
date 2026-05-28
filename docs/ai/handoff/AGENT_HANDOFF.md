# Agent Handoff

## Current Summary

The repository is a Vibe Coding infrastructure package. The key authority files are `origin_prompt.md`, `prompt.md`, and `AGENTS.md`.

## Current Mode

`standard`

## Current Agency

`controlled_execution`

## Current Slice

No active slice. `SLICE-001`, `SLICE-002`, and `SLICE-003` are completed.

## Quality Gates

```powershell
python -m vibe_coding_infra check
python -m unittest discover -s tests
```

Latest result: both gates passed with the Codex bundled Python runtime.

## Forbidden Without Confirmation

- Editing `origin_prompt.md`
- Destructive git operations
- Installing dependencies
- Skipping failed quality gates
