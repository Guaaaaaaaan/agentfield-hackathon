# OUTPUT_LANGUAGE_POLICY.md

## Goal
Ensure that all runtime outputs shown during the demo are English-only.

## Scope
Applies to:
- Risk reasoning output
- Strategy reasoning output
- Execution result output
- Audit event output shown on screen

## Enforcement Rules
1. System output language must be English (`en-US`) in demo mode.
2. Any non-English token in visible output is treated as a demo failure.
3. If non-English output appears, rerun with strict language prompt.

## Prompt Guardrail (Suggested)
Use this instruction in all AI calls during demo:

`You are in DEMO_ENGLISH_ONLY mode. Output English only. Never output Chinese. Keep output structured and concise.`

## Output Contract Add-on
Each output object should include:
- `language`: `"en-US"`

Example:
```json
{
  "risk_level": "high",
  "confidence": 0.91,
  "reasons": ["invoice is overdue for 46 days", "history shows repeated late payments"],
  "next_action": "escalate_after_24h",
  "language": "en-US"
}
```

## Pre-Demo Checks
- Run one full demo path and verify all visible text is English.
- Verify logs shown in terminal are English.
- Verify fallback/error messages are also English.

## Emergency Recovery
If Chinese appears during demo:
1. Stop output screen sharing momentarily.
2. Re-run with the strict English guardrail prompt.
3. Continue from the same sample case with English-only output.
