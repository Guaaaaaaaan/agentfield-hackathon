from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Callable

from src.common.audit import AuditLogger, build_flow_output, normalize_execution_result
from src.common.contracts import (
    AuditEvent,
    CollectionStrategy,
    InvoiceInput,
    RiskAssessment,
    build_event_id,
    utc_now_iso,
)
from src.common.fallback import fallback_risk, fallback_strategy

RiskReasoner = Callable[[InvoiceInput], RiskAssessment]
StrategyReasoner = Callable[[InvoiceInput, RiskAssessment], CollectionStrategy]
Executor = Callable[[CollectionStrategy], Any]


def _trace_id() -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"TRACE-{ts}"


def _write_fallback_event(
    audit_logger: AuditLogger,
    trace: str,
    seq: int,
    invoice_id: str,
    risk_level: str | None,
    next_action: str | None,
    detail: str,
    event_time: str,
) -> None:
    audit_logger.write(
        AuditEvent(
            event_id=build_event_id(trace, seq),
            trace_id=trace,
            event_type="fallback",
            invoice_id=invoice_id,
            risk_level=risk_level,
            next_action=next_action,
            status="fallback_applied",
            fallback=True,
            detail=detail,
            event_time=event_time,
        )
    )


def run_pipeline(
    invoice: InvoiceInput,
    risk_reasoner: RiskReasoner,
    strategy_reasoner: StrategyReasoner,
    executor: Executor,
    audit_logger: AuditLogger,
    trace_id: str | None = None,
) -> dict[str, Any]:
    trace = trace_id or _trace_id()
    seq = 1
    used_fallback = False

    try:
        risk = risk_reasoner(invoice)
        risk.validate()
    except Exception as exc:
        used_fallback = True
        risk = fallback_risk(invoice.invoice_id, "risk_reasoner_failed")
        _write_fallback_event(
            audit_logger=audit_logger,
            trace=trace,
            seq=seq,
            invoice_id=invoice.invoice_id,
            risk_level=risk.risk_level,
            next_action=None,
            detail=f"risk fallback: {exc}",
            event_time=risk.assessed_at,
        )
        seq += 1

    try:
        strategy = strategy_reasoner(invoice, risk)
        strategy.validate()
    except Exception as exc:
        used_fallback = True
        strategy = fallback_strategy(invoice.invoice_id)
        _write_fallback_event(
            audit_logger=audit_logger,
            trace=trace,
            seq=seq,
            invoice_id=invoice.invoice_id,
            risk_level=risk.risk_level,
            next_action=strategy.next_action,
            detail=f"strategy fallback: {exc}",
            event_time=strategy.generated_at,
        )
        seq += 1

    execution_event_type = "execution"
    execution_detail: str | dict | None = None
    try:
        raw_exec_result = executor(strategy)
        exec_status, exec_payload = normalize_execution_result(raw_exec_result)
        if exec_status == "failed":
            used_fallback = True
            execution_event_type = "execution_error"
        if exec_payload:
            execution_detail = exec_payload
    except Exception as exc:
        used_fallback = True
        execution_event_type = "execution_error"
        exec_status = "failed"
        execution_detail = f"execution exception: {exc}"

    execution_event = AuditEvent(
        event_id=build_event_id(trace, seq),
        trace_id=trace,
        event_type=execution_event_type,
        invoice_id=invoice.invoice_id,
        risk_level=risk.risk_level,
        next_action=strategy.next_action,
        status=exec_status,
        fallback=used_fallback,
        detail=execution_detail,
        event_time=utc_now_iso(),
    )
    audit_logger.write(execution_event)

    return build_flow_output(
        trace_id=trace,
        risk=risk,
        strategy=strategy,
        audit_event=execution_event,
        fallback=used_fallback,
    )
