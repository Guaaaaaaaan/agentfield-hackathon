from __future__ import annotations

import json
from pathlib import Path

from src.agents.collection_strategy_reasoner import collection_strategy_reasoner
from src.agents.execute_and_audit_skill import execute_and_audit_skill
from src.agents.invoice_risk_reasoner import invoice_risk_reasoner
from src.common.audit import AuditLogger
from src.common.contracts import InvoiceInput
from src.orchestration.pipeline import run_pipeline


def _load_runtime_inputs() -> list[InvoiceInput]:
    raw = json.loads(Path("data/samples/pipeline_inputs_runtime.json").read_text(encoding="utf-8"))
    return [
        InvoiceInput(
            invoice_id=item["invoice_id"],
            overdue_days=item["overdue_days"],
            amount=item["amount"],
            customer_id=item["customer_id"],
            late_payments_180d=item["late_payments_180d"],
            preferred_channel=item.get("preferred_channel", "email"),
        )
        for item in raw
    ]


def test_pipeline_with_real_modules_and_three_consecutive_runs() -> None:
    logger = AuditLogger(audit_path="data/samples/test_audit.log")
    invoices = _load_runtime_inputs()[:3]

    for idx, invoice in enumerate(invoices, start=1):
        out = run_pipeline(
            invoice=invoice,
            risk_reasoner=invoice_risk_reasoner,
            strategy_reasoner=collection_strategy_reasoner,
            executor=execute_and_audit_skill,
            audit_logger=logger,
            trace_id=f"TRACE-I{idx}",
        )
        assert out["language"] == "en-US"
        assert out["risk_level"] in {"low", "medium", "high"}
        assert isinstance(out["confidence"], float)
        assert out["reasons"]
        assert out["next_action"]
        assert out["fallback"] in {True, False}
        assert "audit_event" in out
        assert out["audit_event"]["status"] in {"queued", "sent", "failed", "skipped"}
