from __future__ import annotations

from dataclasses import dataclass

from src.common.contracts import CollectionStrategy, InvoiceInput, RiskAssessment

_VALID_CHANNELS = {"email", "sms", "call_queue"}


@dataclass(slots=True)
class StrategyReasoningError(Exception):
    """Raised when strategy reasoning cannot produce a valid contract output."""

    code: str
    detail: str

    def __str__(self) -> str:
        return f"{self.code}: {self.detail}"


def _normalize_channel(preferred_channel: str) -> str:
    channel = (preferred_channel or "").strip().lower()
    return channel if channel in _VALID_CHANNELS else "email"


def collection_strategy_reasoner(invoice: InvoiceInput, risk: RiskAssessment) -> CollectionStrategy:
    """Generate collection strategy from risk signal and customer contact preference."""
    if not invoice.invoice_id:
        raise StrategyReasoningError("INVALID_INVOICE", "invoice_id is required")

    if risk.risk_level == "high":
        channel = _normalize_channel(invoice.preferred_channel)
        strategy = CollectionStrategy(
            invoice_id=invoice.invoice_id,
            channel="call_queue" if invoice.overdue_days >= 45 else channel,
            tone="urgent",
            next_action="escalate_after_24h",
            escalation=True,
        )
    elif risk.risk_level == "medium":
        channel = _normalize_channel(invoice.preferred_channel)
        if channel == "call_queue":
            channel = "sms"
        strategy = CollectionStrategy(
            invoice_id=invoice.invoice_id,
            channel=channel,
            tone="firm",
            next_action="follow_up_48h",
            escalation=False,
        )
    elif risk.risk_level == "low":
        strategy = CollectionStrategy(
            invoice_id=invoice.invoice_id,
            channel="email",
            tone="gentle",
            next_action="friendly_reminder_72h",
            escalation=False,
        )
    else:
        raise StrategyReasoningError("INVALID_RISK", f"unsupported risk_level: {risk.risk_level}")

    strategy.validate()
    return strategy
