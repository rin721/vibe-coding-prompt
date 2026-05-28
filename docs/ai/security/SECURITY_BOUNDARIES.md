# Security Boundaries

## Stop Conditions

- Secrets or private data may be exposed.
- Production systems may be changed.
- Data may be deleted or migrated.
- Permission, billing, payment or authentication behavior may change.
- A command is destructive or difficult to roll back.

## Guardrails

- Prefer read-only inspection before mutation.
- Keep rollback instructions close to risky changes.
- Do not import sensitive material into the knowledge base.
- Scan artifacts before completion.
