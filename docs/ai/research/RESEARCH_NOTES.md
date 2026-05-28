# Research Notes

## RES-0001

Question: What is the minimum local knowledge base/RAG core needed for this infrastructure?

Trigger: The infrastructure must support search, question answering, retrieval augmentation, and traceability without requiring external services for the baseline.

Query paths:

- Local contract semantics.
- Repository documentation requirements.
- Standard-library implementation constraints.

Conclusion: A local index can provide a verifiable baseline by importing Markdown and JSON sources, scanning sensitive patterns, tokenizing text, storing entries, scoring keyword overlap, scoring token-vector similarity, and producing evidence-backed answers. It can later be replaced or extended by a true vector database and external search service.

Confidence: `medium`

Risks:

- Token-vector scoring is lightweight and not a substitute for production embeddings.
- Chinese segmentation is simple.
- External content still needs verification before stable import.

Updated at: `2026-05-28`
