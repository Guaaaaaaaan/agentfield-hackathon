from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any


RISK_LEVELS = {"low", "medium", "high"}
CHANNELS = {"email", "sms", "call_queue"}
TONES = {"gentle", "firm", "urgent"}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


@dataclass(slots=True)
class InvoiceInput:
    invoice_id: str
    overdue_days: int
    amount: float
    customer_id: str
    late_payments_180d: int
    preferred_channel: str = "email"


@dataclass(slots=True)
class RiskAssessment:
    invoice_id: str
    risk_level: str
    confidence: float
    reasons: list[str]
    assessed_at: str = field(default_factory=utc_now_iso)

    def validate(self) -> None:
        if self.risk_level not in RISK_LEVELS:
            raise ValueError(f"invalid risk_level: {self.risk_level}")
        if not 0.0 <= float(self.confidence) <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if not self.reasons:
            raise ValueError("reasons must be non-empty")


@dataclass(slots=True)
class CollectionStrategy:
    invoice_id: str
    channel: str
    tone: str
    next_action: str
    escalation: bool
    generated_at: str = field(default_factory=utc_now_iso)

    def validate(self) -> None:
        if self.channel not in CHANNELS:
            raise ValueError(f"invalid channel: {self.channel}")
        if self.tone not in TONES:
            raise ValueError(f"invalid tone: {self.tone}")
        if not self.next_action:
            raise ValueError("next_action must be non-empty")


@dataclass(slots=True)
class AuditEvent:
    event_id: str
    trace_id: str
    event_type: str
    invoice_id: str
    status: str
    event_time: str
    risk_level: str | None = None
    next_action: str | None = None
    fallback: bool = False
    detail: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_event_id(trace_id: str, seq: int) -> str:
    return f"{trace_id}-AUD-{seq:03d}"
