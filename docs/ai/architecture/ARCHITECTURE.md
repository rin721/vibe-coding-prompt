# AI Architecture Notes

## Current Mode

`standard`

## Agency Level

`controlled_execution` for documented low-risk repository generation and validation.

## Modules

- `prompt`: authoritative Agent prompt.
- `docs`: human and Agent documentation.
- `schemas`: machine-readable field contracts.
- `knowledge_base`: dedicated Knowledge Base/RAG layer for import, search, retrieval, and evidence-grounded answer payloads.
- `vibe_coding_infra`: local CLI for quality gates, next-step diagnosis, and knowledge base primitives.
- `skills`: reusable project skill templates.

## Quality Gates

- `python -m vibe_coding_infra check`
- `python -m vibe_coding_infra knowledge-search "执行切片"`
- `python -m unittest discover -s tests`
