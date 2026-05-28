# Knowledge Base

## Positioning

The knowledge base stores verified project facts, decisions, research conclusions, task state, test evidence and reusable engineering patterns.

It helps agents recover context, retrieve evidence and avoid relying on transient chat history.

## Retrieval Surfaces

- Full text search for exact terms, file paths, commands and identifiers.
- Local vector approximation for related wording and similar context.
- Evidence based question answering that cites source paths.
- Import and quality review pipeline for new facts.

## Entry Lifecycle

```text
candidate -> reviewed -> stable -> deprecated
```

## Import Rules

- Each entry must have a source path.
- Unverified external material remains candidate knowledge.
- Stable knowledge must be traceable to project files, decisions, tests or confirmed records.
- Sensitive information must not be imported.

## Evaluation

Retrieval quality should be reviewed with representative questions:

- Can the system find current execution state?
- Can it explain completion criteria?
- Can it retrieve decisions and evidence?
- Can it expose conflicting or stale knowledge?
