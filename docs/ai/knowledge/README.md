# Knowledge Index

This directory stores the local knowledge index generated from stable repository sources.

The index is a baseline fact-access layer:

- Markdown and JSON files remain auditable sources.
- Imported entries carry source paths, trust level, tags, and checksums.
- Search combines keyword overlap and token-vector scoring.
- Answers include citations and do not replace source review.

Run:

```powershell
python -m vibe_coding_infra knowledge-import
python -m vibe_coding_infra knowledge-search "质量门禁"
python -m vibe_coding_infra knowledge-answer "当前下一步是什么？"
```
