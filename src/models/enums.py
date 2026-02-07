from enum import Enum


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class InvoiceStatus(str, Enum):
    OPEN = "open"
    PAID = "paid"
    OVERDUE = "overdue"
    DISPUTED = "disputed"


class PreferredChannel(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    CALL_QUEUE = "call_queue"


class ActionStatus(str, Enum):
    QUEUED = "queued"
    SENT = "sent"
    FAILED = "failed"
    SKIPPED = "skipped"


class EventType(str, Enum):
    DECISION = "decision"
    EXECUTION = "execution"
    FALLBACK = "fallback"
    ERROR = "error"
