from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.common.contracts import AuditEvent, CollectionStrategy, RiskAssessment

DEFAULT_LANGUAGE = "en-US"
ALLOWED_EXECUTION_STATUS = {"queued", "sent", "failed", "skipped"}


class AuditLogger:
    def __init__(self, audit_path: str = "data/samples/audit.log") -> None:
        self._audit_path = Path(audit_path)
        self.events: list[AuditEvent] = []

    def write(self, event: AuditEvent) -> None:
        self.events.append(event)
        self._audit_path.parent.mkdir(parents=True, exist_ok=True)
        with self._audit_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event.to_dict(), ensure_ascii=True) + "\n")


def normalize_execution_result(result: Any) -> tuple[str, dict[str, Any] | None]:
    if isinstance(result, str):
        status = result.strip().lower()
        return (status if status in ALLOWED_EXECUTION_STATUS else "failed", None)

    if hasattr(result, "status"):
        status = str(getattr(result, "status", "")).strip().lower()
        detail: dict[str, Any] | None = None
        if hasattr(result, "to_dict"):
            payload = result.to_dict()
            if isinstance(payload, dict):
                detail = payload
        elif isinstance(result, dict):
            detail = result
        return (status if status in ALLOWED_EXECUTION_STATUS else "failed", detail)

    if isinstance(result, dict):
        status = str(result.get("status", "")).strip().lower()
        return (status if status in ALLOWED_EXECUTION_STATUS else "failed", result)

    return "failed", {"raw_type": type(result).__name__}


def build_flow_output(
    trace_id: str,
    risk: RiskAssessment,
    strategy: CollectionStrategy,
    audit_event: AuditEvent,
    fallback: bool,
    language: str = DEFAULT_LANGUAGE,
) -> dict[str, Any]:
    return {
        "trace_id": trace_id,
        "invoice_id": risk.invoice_id,
        "risk_level": risk.risk_level,
        "confidence": risk.confidence,
        "reasons": list(risk.reasons),
        "next_action": strategy.next_action,
        "audit_event": audit_event.to_dict(),
        "language": language,
        "fallback": fallback,
        "channel": strategy.channel,
        "tone": strategy.tone,
        "escalation": strategy.escalation,
    }
