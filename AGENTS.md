# Agent Operating Rules

This repository is governed by `prompt.md`. Any AI coding agent must read `prompt.md` before changing files.

Minimum rules:

1. Do not modify `origin_prompt.md` unless the developer explicitly asks.
2. Treat `prompt.md` as the authoritative Agent behavior contract.
3. Read `docs/ai/state/STATUS.md`, `docs/ai/tasks/EXECUTION_SLICES.md`, and `docs/ai/requirements/REQUIREMENT_LEDGER.md` before executing "next step" work.
4. Act only within the current legal execution slice.
5. Record evidence in `docs/ai/*`; do not rely only on chat history.
6. Run `python -m vibe_coding_infra check` after infrastructure changes.
7. Run `python -m unittest discover -s tests` after code changes.
8. Pause and request confirmation for destructive actions, production changes, secrets, data migrations, payments, permissions, sensitive data, or expanded agency.

Default agency level for this repository is `controlled_execution` inside documented slices and `advisory` outside them.
