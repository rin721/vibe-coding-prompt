# Testing

## Baseline Gates

```powershell
python -m vibe_coding_infra check
python -m unittest discover -s tests
```

## Knowledge Smoke Checks

```powershell
python -m vibe_coding_infra knowledge-import
python -m vibe_coding_infra knowledge-search "质量门禁" --limit 3
python -m vibe_coding_infra knowledge-answer "下一步之前要读取什么？" --limit 3
```

## Completion Rule

Work is not complete until required gates pass or an explicit substitute verification is recorded with remaining risk.

## Test Evidence

Test results should be recorded in `docs/ai/reports/TEST_REPORT.md` with command, result, date, and known limitations.
