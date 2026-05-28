# Project Overview

This project is a Vibe Coding infrastructure package for agentic software delivery. It turns requirements, decisions, state, verification evidence, and reusable knowledge into files and checks that future agents can read without relying on chat memory.

## Goals

- Help non-specialist developers move from vague ideas to confirmed engineering scope.
- Keep agency controlled, auditable, pausable, reversible, and recoverable.
- Preserve requirements, research, decisions, tasks, execution slices, state, evidence, and handoff in repository files.
- Provide local CLI checks so agents can validate the infrastructure before claiming completion.
- Provide a dedicated programming knowledge base/RAG core with import, search, lightweight vector scoring, and evidence-backed answers.

## Non Goals

- It does not replace human decisions about product value, risk, or budget.
- It does not grant agents unlimited autonomy.
- It does not require every small task to use a heavy governance process.

## Primary Surfaces

- Agent contract and local operating rules.
- Human-facing documentation under `docs/`.
- Agent-facing state and evidence under `docs/ai/`.
- Local validation and knowledge tooling under `vibe_coding_infra/`.
- Project-specific skills under `skills/`.
