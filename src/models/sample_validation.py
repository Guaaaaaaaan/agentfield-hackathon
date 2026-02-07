from __future__ import annotations

import json
from pathlib import Path

from src.common.contracts import CHANNELS, InvoiceInput
from src.models.entities import (
    AuditEventRecord,
    CollectionStrategyRecord,
    Customer,
    Invoice,
    PaymentBehaviorSnapshot,
    RiskAssessmentRecord,
)


PIPELINE_FIELDS = {
    "invoice_id",
    "overdue_days",
    "amount",
    "customer_id",
    "late_payments_180d",
    "preferred_channel",
}
PIPELINE_ALLOWED_FIELDS = PIPELINE_FIELDS | {"language"}
RECORD_MODELS = {
    "customer_records.json": Customer,
    "invoice_records.json": Invoice,
    "payment_behavior_snapshot_records.json": PaymentBehaviorSnapshot,
    "risk_assessment_records.json": RiskAssessmentRecord,
    "collection_strategy_records.json": CollectionStrategyRecord,
    "audit_event_records.json": AuditEventRecord,
}


def _load_json_array(path: Path) -> list[dict]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, list):
        raise ValueError(f"Expected a JSON array in {path}")
    for index, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"Expected object at index {index} in {path}")
    return data


def validate_pipeline_inputs(path: Path) -> None:
    rows = _load_json_array(path)
    if len(rows) != 6:
        raise ValueError(f"pipeline_inputs.json must contain 6 rows, got {len(rows)}")

    for index, row in enumerate(rows):
        keys = set(row)
        missing = PIPELINE_FIELDS - keys
        extra = keys - PIPELINE_ALLOWED_FIELDS
        if missing:
            raise ValueError(f"Missing fields at pipeline_inputs[{index}]: {sorted(missing)}")
        if extra:
            raise ValueError(f"Unexpected fields at pipeline_inputs[{index}]: {sorted(extra)}")
        if row.get("language") != "en-US":
            raise ValueError(f"language must be 'en-US' at pipeline_inputs[{index}]")
        if row["preferred_channel"] not in CHANNELS:
            raise ValueError(
                f"invalid preferred_channel at pipeline_inputs[{index}]: {row['preferred_channel']}"
            )
        InvoiceInput(**{field: row[field] for field in PIPELINE_FIELDS})


def validate_record_samples(base_dir: Path) -> None:
    for filename, model in RECORD_MODELS.items():
        rows = _load_json_array(base_dir / filename)
        for index, row in enumerate(rows):
            if "language" in row and row["language"] != "en-US":
                raise ValueError(f"language must be 'en-US' at {filename}[{index}]")
            try:
                model.model_validate(row)
            except Exception as exc:  # pragma: no cover
                raise ValueError(f"{filename}[{index}] failed model validation: {exc}") from exc


def main() -> int:
    base_dir = Path("data/samples")
    validate_pipeline_inputs(base_dir / "pipeline_inputs.json")
    validate_record_samples(base_dir)
    print("Sample validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
