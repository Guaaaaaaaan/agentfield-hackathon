from __future__ import annotations

from src.common.audit import AuditLogger
from src.common.contracts import CollectionStrategy, InvoiceInput, RiskAssessment
from src.orchestration.pipeline import run_pipeline


def _good_risk(invoice: InvoiceInput) -> RiskAssessment:
    return RiskAssessment(invoice.invoice_id, "medium", 0.75, ["payment_delay_pattern"])


def _good_strategy(invoice: InvoiceInput, _: RiskAssessment) -> CollectionStrategy:
    return CollectionStrategy(invoice.invoice_id, "email", "firm", "follow_up_48h", False)


def test_risk_fallback_and_required_fields() -> None:
    invoice = InvoiceInput("INV-U1", 60, 300.0, "C1", 4, "email")
    logger = AuditLogger(audit_path="data/samples/test_audit.log")

    def bad_risk(_: InvoiceInput) -> RiskAssessment:
        raise RuntimeError("risk timeout")

    out = run_pipeline(
        invoice=invoice,
        risk_reasoner=bad_risk,
        strategy_reasoner=_good_strategy,
        executor=lambda _: "sent",
        audit_logger=logger,
        trace_id="TRACE-U1",
    )

    assert out["language"] == "en-US"
    assert out["fallback"] is True
    assert out["risk_level"] == "medium"
    assert out["confidence"] == 0.5
    assert out["reasons"]
    assert out["next_action"]
    assert out["audit_event"]["fallback"] is True


def test_strategy_fallback_and_required_fields() -> None:
    invoice = InvoiceInput("INV-U2", 25, 200.0, "C2", 0, "email")
    logger = AuditLogger(audit_path="data/samples/test_audit.log")

    def bad_strategy(_: InvoiceInput, __: RiskAssessment) -> CollectionStrategy:
        raise RuntimeError("strategy failed")

    out = run_pipeline(
        invoice=invoice,
        risk_reasoner=_good_risk,
        strategy_reasoner=bad_strategy,
        executor=lambda _: "sent",
        audit_logger=logger,
        trace_id="TRACE-U2",
    )

    assert out["language"] == "en-US"
    assert out["fallback"] is True
    assert out["next_action"] == "manual_review_24h"
    assert out["risk_level"]
    assert out["confidence"] >= 0
    assert out["reasons"]
    assert out["audit_event"]["status"] == "sent"


def test_executor_failure_is_audited_without_crash() -> None:
    invoice = InvoiceInput("INV-U3", 20, 150.0, "C3", 1, "email")
    logger = AuditLogger(audit_path="data/samples/test_audit.log")

    def broken_executor(_: CollectionStrategy) -> str:
        raise RuntimeError("provider unavailable")

    out = run_pipeline(
        invoice=invoice,
        risk_reasoner=_good_risk,
        strategy_reasoner=_good_strategy,
        executor=broken_executor,
        audit_logger=logger,
        trace_id="TRACE-U3",
    )

    assert out["language"] == "en-US"
    assert out["fallback"] is True
    assert out["audit_event"]["status"] == "failed"
    assert out["audit_event"]["event_type"] == "execution_error"
    assert out["risk_level"]
    assert out["confidence"] >= 0
    assert out["reasons"]
    assert out["next_action"]


def test_executor_dict_result_branch_is_supported() -> None:
    invoice = InvoiceInput("INV-U4", 12, 500.0, "C4", 1, "email")
    logger = AuditLogger(audit_path="data/samples/test_audit.log")

    def dict_executor(_: CollectionStrategy) -> dict[str, str]:
        return {"status": "queued", "provider": "mock_queue"}

    out = run_pipeline(
        invoice=invoice,
        risk_reasoner=_good_risk,
        strategy_reasoner=_good_strategy,
        executor=dict_executor,
        audit_logger=logger,
        trace_id="TRACE-U4",
    )

    assert out["language"] == "en-US"
    assert out["fallback"] is False
    assert out["audit_event"]["status"] == "queued"
    assert out["audit_event"]["event_type"] == "execution"
