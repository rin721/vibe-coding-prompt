# AI Architecture Notes

## Current Structure

- Human-facing architecture lives in `docs/ARCHITECTURE.md`.
- Agent-facing state is split across requirements, decisions, tasks, status, reports, risks, knowledge, and handoff.
- The local CLI validates required files and machine-readable fields.
- The knowledge layer imports stable documentation and process state into a searchable evidence index.

## Boundaries

- Source files remain the audit record.
- Knowledge answers must cite evidence.
- Current execution slice boundaries control file edits and tool use.
- High-risk operations require explicit confirmation.
