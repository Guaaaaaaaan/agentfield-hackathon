# CODEX_GUIDELINES.md

## Context
- Date: 2026-02-07 (SGT)
- Goal: deliver MVP core flow before 15:30 SGT
- Core flow: `Overdue Invoice -> Risk -> Strategy -> Execute + Audit`

## Global Guide Line (All Codex)
- Keep all visible runtime output in English only (`language = "en-US"`).
- Every final flow output must include: `risk_level`, `confidence`, `reasons`, `next_action`, `audit_event`.
- Any module failure must trigger fallback; never break the full pipeline.
- Fallback path must emit audit evidence with `fallback=true`.
- Do not edit files outside your lane boundary.
- Work in short rounds (20-40 minutes) and report after each round.

### Standard Report Template (Every Round)
1. Changed files
2. Key changes (max 3 lines)
3. Commands executed
4. Result
5. Blockers
6. Next step

## Codex-A Guide Line (Foundation Lane)

### File Boundary
- `requirements.txt`
- `.gitignore`
- `src/models/*`
- `data/samples/*`

### Responsibilities
- Prepare dependencies and base project config files.
- Implement Pydantic models based on `docs/ERD.md` and contracts.
- Create 6-10 sample JSON records covering low/medium/high risk.
- Ensure sample payloads can be parsed directly into models.

### Definition of Done
- Models import successfully and validate schema constraints.
- Sample data deserializes into model objects without errors.
- Contract-required fields are complete and aligned.

### Not In Scope
- No agent business logic.
- No orchestration entry (`app.py`) and no test harness edits.

## Codex-B Guide Line (Agent Logic Lane)

### File Boundary
- `src/agents/*`
- `src/services/*`
- `src/skills/*`

### Responsibilities
- Implement `invoice_risk_reasoner`.
- Implement `collection_strategy_reasoner`.
- Implement `execute_and_audit_skill`.
- Keep reasons non-empty and outputs contract-stable.
- Keep output wording English-only by default.
- Expose clear error signals for orchestration fallback.

### Definition of Done
- Three modules run independently with typed inputs/outputs.
- Normal path returns full contract fields.
- Failure path returns standardized failure object or typed exception.

### Not In Scope
- No sample data generation.
- No orchestration entrypoint and no test framework ownership.

## Codex-C Guide Line (Orchestration & Quality Lane)

### File Boundary
- `src/orchestration/*`
- `src/common/*`
- `app.py`
- `tests/*`
- README run section

### Responsibilities
- Wire A/B outputs into one end-to-end flow.
- Implement fallback controls (timeout/error/default strategy).
- Build CLI entrypoint and demo-safe output format.
- Add minimum unit + integration tests for happy path and fallback.

### Definition of Done
- End-to-end flow runs successfully 3 consecutive times.
- Fallback path does not interrupt flow and writes audit event.
- Tests run and cover at least core flow + fallback behavior.

### Not In Scope
- Do not change core business rules in A/B files unless explicitly approved.

## Merge Gate (Must Pass Before Final Submission)
- Core flow is runnable.
- English-only visible output verified.
- Fallback behavior verified.
- Audit fields complete and traceable.
- README steps reproduce the demo locally.
