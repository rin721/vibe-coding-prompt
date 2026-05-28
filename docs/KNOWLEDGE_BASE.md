# Knowledge Base / RAG Architecture

The dedicated Vibe Coding programming knowledge base is a product-grade knowledge layer, not a synonym for `docs/` and not a chat memory.

## Role

- Make stable project facts searchable.
- Return evidence-backed answers with source citations.
- Provide retrieval-augmented context for agents, CLI tools, IDEs, and automation.
- Preserve source-of-truth links back to `docs/`, `docs/ai/*`, Git history, tests, decisions, research notes, and developer confirmations.

## Local Core

The current repository ships a standard-library local core in `vibe_coding_infra/knowledge_base.py`:

- Markdown import pipeline.
- Knowledge entry schema.
- Full-text index.
- Lightweight term-vector store.
- Retrieval helpers.
- Evidence-grounded answer payload.

This local core is intentionally dependency-free. A future implementation can replace storage with a production vector database and search service while keeping the same governance boundaries.

## Commands

```powershell
python -m vibe_coding_infra knowledge-build --output docs/ai/knowledge/knowledge_index.json
python -m vibe_coding_infra knowledge-search "执行切片"
python -m vibe_coding_infra knowledge-answer "下一步之前要读取什么？" --json
```

## Safety

External material remains untrusted until reviewed. The import pipeline must preserve source path, trust level, status, evidence, and update time. Knowledge base answers never override P0 safety rules, developer confirmation, or the current legal execution slice.
