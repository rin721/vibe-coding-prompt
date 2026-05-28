# AI Architecture Notes

## Current Mode

`standard`

## Agency Level

`controlled_execution` for documented low-risk repository generation and validation.

## Modules

- `prompt`: authoritative Agent prompt.
- `docs`: human and Agent documentation.
- `schemas`: machine-readable field contracts.
- `vibe_coding_infra`: local CLI for quality gates and next-step diagnosis.
- `skills`: reusable project skill templates.

## Quality Gates

- `python -m vibe_coding_infra check`
- `python -m unittest discover -s tests`
