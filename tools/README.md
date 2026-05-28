# Tools

Tooling is intentionally minimal.

- `vibe_coding_infra check` validates required files and machine-readable state fields.
- `vibe_coding_infra next` diagnoses the next legal execution slice.
- `scripts/check.ps1` and `scripts/next.ps1` are PowerShell wrappers.

Do not add new dependencies unless a decision record explains why the standard library is insufficient.
