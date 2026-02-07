# Sample Data Guide

This folder contains two sample categories:

- Demo contract samples: for runtime flow demos and contract checks.
- ERD record samples: for entity-level persistence model validation.

## Contract Samples (Runtime-Oriented)

- `pipeline_inputs.json`
  - Source: `src/common/contracts.py::InvoiceInput` (+ `language` for demo gate checks).
  - Required fields per row:
    - `invoice_id`
    - `overdue_days`
    - `amount`
    - `customer_id`
    - `late_payments_180d`
    - `preferred_channel`
    - `language` (`"en-US"`)
  - Contains 6 rows covering low/medium/high scenarios.
  - Use case: demo validation payload with explicit language policy check.

- `pipeline_inputs_runtime.json`
  - Source: `src/common/contracts.py::InvoiceInput` (runtime-ready shape).
  - Required fields per row:
    - `invoice_id`
    - `overdue_days`
    - `amount`
    - `customer_id`
    - `late_payments_180d`
    - `preferred_channel`
  - Does not include `language`.
  - Use case: direct runtime loading by orchestration code.

- `risk_assessments.json`
- `collection_strategies.json`
- `audit_events.json`
  - Source: runtime output contract semantics used by demo flow.
  - `language` is included as `"en-US"` for visible output checks.

## ERD Record Samples (Storage-Oriented)

- `customer_records.json` -> `src/models/entities.py::Customer`
- `invoice_records.json` -> `src/models/entities.py::Invoice`
- `payment_behavior_snapshot_records.json` -> `src/models/entities.py::PaymentBehaviorSnapshot`
- `risk_assessment_records.json` -> `src/models/entities.py::RiskAssessmentRecord`
- `collection_strategy_records.json` -> `src/models/entities.py::CollectionStrategyRecord`
- `audit_event_records.json` -> `src/models/entities.py::AuditEventRecord`

These files are used to validate that record payloads can deserialize into entity models directly.

## Validation

Run:

```powershell
python -m src.models.sample_validation
```

Expected output:

```text
Sample validation passed.
```

## Channel and Language Rules

- Channel enum is unified to `email | sms | call_queue`.
- All included `language` fields are fixed to `"en-US"`.
