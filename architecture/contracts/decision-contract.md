# Decision Contract (MVP)

## RiskAssessment

```json
{
  "invoice_id": "INV-1001",
  "risk_level": "high",
  "confidence": 0.91,
  "reasons": ["overdue_days>45", "late_payments_180d>=3"],
  "assessed_at": "2026-02-07T10:30:00Z"
}
```

## CollectionStrategy

```json
{
  "invoice_id": "INV-1001",
  "channel": "email",
  "tone": "firm",
  "next_action": "escalate_after_24h",
  "escalation": true,
  "generated_at": "2026-02-07T10:30:01Z"
}
```