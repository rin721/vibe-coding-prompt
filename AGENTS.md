# Agent Operating Rules

This repository is governed by the root agent contract and the state files under `docs/ai/`.

Minimum rules:

1. Read the root contract, this file, current state, execution slices, and requirement ledger before making changes.
2. Act only inside the current legal execution slice.
3. Record evidence under `docs/ai/*`; do not rely only on chat history.
4. Run `python -m vibe_coding_infra check` after infrastructure changes.
5. Run `python -m unittest discover -s tests` after code changes.
6. Pause and request confirmation for destructive actions, production changes, secrets, data migrations, payments, permissions, sensitive data, dependency installation, or expanded agency.

Default agency level for this repository is `controlled_execution` inside documented slices and `advisory` outside them.
