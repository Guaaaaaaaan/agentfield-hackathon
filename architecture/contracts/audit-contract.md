# Audit Event Contract (MVP)

```json
{
  "event_id": "AUD-001",
  "trace_id": "TRACE-20260207-001",
  "event_type": "execution",
  "invoice_id": "INV-1001",
  "risk_level": "high",
  "next_action": "escalate_after_24h",
  "status": "sent",
  "event_time": "2026-02-07T10:30:02Z"
}
```

最小必填字段：
- `trace_id`
- `invoice_id`
- `event_type`
- `status`
- `event_time`