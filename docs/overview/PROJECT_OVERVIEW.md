# Project Overview

## Goal

Build a local, auditable infrastructure for Vibe Coding workflows: requirement capture, controlled execution, knowledge retrieval, quality gates and handoff records.

## Users

- Developers using AI coding agents.
- Teams that need traceable requirements, decisions and implementation evidence.
- Maintainers who need to recover project context without relying on chat history.

## First Version Scope

- Repository scaffold and documentation layers.
- CLI for initialization, knowledge ingestion, search, question answering and checks.
- Local knowledge base with full text retrieval and vector similarity.
- Sensitive information scan and schema validation.
- Tests for core behavior.

## Explicit Non Goals

- Hosted multi tenant service.
- Production deployment automation.
- External LLM provider integration.
- Web user interface.

## Acceptance

- The CLI runs locally.
- The knowledge base can ingest docs and return evidence.
- Tests pass locally.
- Generated artifacts avoid source-tracing meta explanations.
