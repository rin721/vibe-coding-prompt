# Knowledge Base And RAG

The dedicated programming knowledge base is a product-level infrastructure layer for Vibe Coding. It is not a plain documentation folder and not chat memory. It makes verified project facts discoverable, answerable, retrieval-augmented, and traceable.

## Capabilities

- **Full-text index** for exact terms, paths, command names, identifiers, and errors.
- **Vector-style scoring** for related concepts and similar experience recall.
- **Retrieval API** through local Python functions and CLI commands.
- **Answer entry** that returns evidence-backed responses with citations.
- **Import pipeline** that reads stable documentation and agent state files.

## Entry Lifecycle

1. Source collection.
2. Trust-level labeling.
3. Sensitive information scan.
4. Prompt-injection risk scan.
5. Metadata normalization.
6. Chunking and tokenization.
7. Full-text indexing.
8. Lightweight vector scoring.
9. Evidence answer generation.
10. Feedback and deprecation handling.

## Trust Rules

External content is untrusted until verified. Knowledge entries cannot override safety boundaries, developer confirmation, source files, or the current legal execution slice.
