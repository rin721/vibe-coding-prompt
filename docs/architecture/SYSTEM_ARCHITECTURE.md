# System Architecture

## Architecture Level

`ordinary_application`

This repository is a local-first infrastructure toolkit. It favors transparent files, standard library components and repeatable checks before introducing network services or managed dependencies.

## Modules

| Module | Responsibility | Boundaries |
| --- | --- | --- |
| `cli` | User-facing command dispatch | No hidden writes beyond requested command |
| `scaffold` | Directory and template creation | Does not overwrite unless `--force` is used |
| `knowledge` | Local ingestion, indexing, retrieval and answer assembly | Does not invent facts without retrieved evidence |
| `quality` | Workspace checks and schema validation | Reports findings but does not mutate files |
| `security` | Sensitive information detection | Uses conservative pattern matching |
| `models` | Shared data structures | Keeps serialization stable |

## Data Flow

1. Documents and process files are created in `docs/` and `docs/ai/`.
2. `vibe ingest` chunks text files and stores entries in SQLite.
3. Retrieval combines FTS results and hashed vector similarity.
4. `vibe ask` returns extractive answers with source paths.
5. `vibe check` scans artifacts and schemas before completion.

## Storage

- `.vibe/knowledge.sqlite3` stores local knowledge entries.
- Source documents remain the auditable records.
- Generated indexes can be rebuilt from source files.

## Risks

- Hashed local vectors are a lightweight approximation, not semantic parity with embedding services.
- FTS query quality depends on imported source quality.
- Sensitive information scanning is a guardrail, not a complete security audit.
