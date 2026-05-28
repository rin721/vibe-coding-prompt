# Vibe Coding Workflow Skill

## Trigger

Use this skill when a task requires governed Agentic Coding workflow: requirement clarification, execution slicing, evidence tracking, local knowledge retrieval or quality gate verification.

## Boundary

This skill does not grant extra authority. It follows the current execution slice, repository rules and security boundaries.

## Steps

1. Read current status, requirements, decisions and execution slices.
2. Query the local knowledge base when available.
3. Identify the current legal execution slice.
4. Implement only within scope.
5. Run quality gates.
6. Update evidence, status and handoff notes.

## Outputs

- Updated code or documentation.
- Verification evidence.
- Status and handoff updates.

## Failure Handling

Stop and report when authorization is unclear, state conflicts, sensitive data appears, tests fail repeatedly or the task exceeds scope.
