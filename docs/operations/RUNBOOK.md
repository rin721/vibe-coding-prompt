# Runbook

## Local Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

## Daily Workflow

1. Read current status and execution slice.
2. Check Git state.
3. Query the knowledge base for related facts.
4. Implement only within the authorized scope.
5. Run quality gates.
6. Update status and handoff notes.

## Recovery

1. Read `docs/ai/status/PROJECT_STATUS.md`.
2. Read `docs/ai/slices/EXECUTION_SLICES.md`.
3. Inspect Git status and recent diffs.
4. Run available tests.
5. Continue only when a legal execution slice is clear.
