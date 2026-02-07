from datetime import datetime

from pydantic import BaseModel, Field

from .enums import (
    ActionStatus,
    EventType,
    InvoiceStatus,
    PreferredChannel,
    RiskLevel,
)


class Customer(BaseModel):
    customer_id: str = Field(min_length=1)
    segment: str = Field(min_length=1)
    preferred_channel: PreferredChannel
    language: str = Field(default="en-US", min_length=2)
    delinquency_count_90d: int = Field(ge=0)
    disputes_count_180d: int = Field(ge=0)
    created_at: datetime


class Invoice(BaseModel):
    invoice_id: str = Field(min_length=1)
    customer_id: str = Field(min_length=1)
    amount_due: float = Field(gt=0)
    currency: str = Field(min_length=3, max_length=3)
    overdue_days: int = Field(ge=0)
    due_date: datetime
    invoice_status: InvoiceStatus
    created_at: datetime


class PaymentBehaviorSnapshot(BaseModel):
    snapshot_id: str = Field(min_length=1)
    customer_id: str = Field(min_length=1)
    avg_days_to_pay: float = Field(ge=0)
    late_payments_180d: int = Field(ge=0)
    collected_ratio_180d: float = Field(ge=0, le=1)
    snapshot_time: datetime


class RiskAssessmentRecord(BaseModel):
    risk_id: str = Field(min_length=1)
    invoice_id: str = Field(min_length=1)
    risk_level: RiskLevel
    confidence: float = Field(ge=0, le=1)
    reasons_json: list[str]
    language: str = Field(default="en-US", min_length=2)
    assessed_at: datetime


class CollectionStrategyRecord(BaseModel):
    strategy_id: str = Field(min_length=1)
    risk_id: str = Field(min_length=1)
    channel: PreferredChannel
    tone: str = Field(min_length=1)
    next_action: str = Field(min_length=1)
    escalation: bool
    language: str = Field(default="en-US", min_length=2)
    generated_at: datetime


class ExecutionAction(BaseModel):
    action_id: str = Field(min_length=1)
    strategy_id: str = Field(min_length=1)
    provider: str = Field(min_length=1)
    action_type: str = Field(min_length=1)
    action_status: ActionStatus
    executed_at: datetime


class AuditEventRecord(BaseModel):
    event_id: str = Field(min_length=1)
    action_id: str = Field(min_length=1)
    trace_id: str = Field(min_length=1)
    event_type: EventType
    payload_json: dict[str, object]
    language: str = Field(default="en-US", min_length=2)
    event_time: datetime
