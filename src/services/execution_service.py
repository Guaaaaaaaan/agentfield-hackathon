from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from src.common.contracts import CollectionStrategy, utc_now_iso

ALLOWED_EXECUTION_STATUS = {"queued", "sent", "failed", "skipped"}
DEFAULT_LANGUAGE = "en-US"

_DETAIL_VALIDATION_FAILED = "strategy validation failed"
_DETAIL_UNSUPPORTED_CHANNEL = "unsupported channel for execution"
_DETAIL_INTERNAL_ERROR = "internal execution error"
_DETAIL_ACCEPTED = "execution accepted by provider"


@dataclass(slots=True)
class ExecutionError(Exception):
    """Raised when execution result cannot satisfy the execution contract."""

    code: str
    detail: str

    def __str__(self) -> str:
        return f"{self.code}: {self.detail}"


@dataclass(slots=True)
class ExecutionResult:
    invoice_id: str
    channel: str
    provider: str
    action_type: str
    status: str
    detail: str
    next_action: str
    language: str = DEFAULT_LANGUAGE
    executed_at: str = field(default_factory=utc_now_iso)

    def validate(self) -> None:
        if self.status not in ALLOWED_EXECUTION_STATUS:
            raise ExecutionError("INVALID_STATUS", f"unsupported status: {self.status}")
        if not self.invoice_id:
            raise ExecutionError("INVALID_RESULT", "invoice_id is required")
        if not self.provider:
            raise ExecutionError("INVALID_RESULT", "provider is required")
        if not self.action_type:
            raise ExecutionError("INVALID_RESULT", "action_type is required")
        if not self.detail:
            raise ExecutionError("INVALID_RESULT", "detail is required")
        if not self.next_action:
            raise ExecutionError("INVALID_RESULT", "next_action is required")
        if self.language != DEFAULT_LANGUAGE:
            raise ExecutionError("INVALID_LANGUAGE", f"language must be {DEFAULT_LANGUAGE}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


_CHANNEL_ACTION_MAP: dict[str, tuple[str, str, str]] = {
    "email": ("mock_email_gateway", "send_email", "sent"),
    "sms": ("mock_sms_gateway", "send_sms", "sent"),
    "call_queue": ("internal_call_queue", "queue_call", "queued"),
}


def _safe_attr(obj: Any, name: str, default: str) -> str:
    value = getattr(obj, name, default)
    if value is None:
        return default
    text = str(value).strip()
    return text or default


def _failed_result(strategy: Any, detail: str) -> ExecutionResult:
    result = ExecutionResult(
        invoice_id=_safe_attr(strategy, "invoice_id", "UNKNOWN"),
        channel=_safe_attr(strategy, "channel", "unknown"),
        provider="none",
        action_type="no_op",
        status="failed",
        detail=detail,
        next_action=_safe_attr(strategy, "next_action", "manual_review_24h"),
    )
    result.validate()
    return result


def execute_collection_action(strategy: CollectionStrategy) -> ExecutionResult:
    """Return a contract-stable execution result and never leak unhandled exceptions."""
    try:
        try:
            strategy.validate()
        except Exception as exc:
            return _failed_result(strategy, f"{_DETAIL_VALIDATION_FAILED}: {exc}")

        mapping = _CHANNEL_ACTION_MAP.get(strategy.channel)
        if mapping is None:
            return _failed_result(strategy, f"{_DETAIL_UNSUPPORTED_CHANNEL}: {strategy.channel}")

        provider, action_type, success_status = mapping
        result = ExecutionResult(
            invoice_id=strategy.invoice_id,
            channel=strategy.channel,
            provider=provider,
            action_type=action_type,
            status=success_status,
            detail=_DETAIL_ACCEPTED,
            next_action=strategy.next_action,
        )
        result.validate()
        return result
    except Exception as exc:
        return _failed_result(strategy, f"{_DETAIL_INTERNAL_ERROR}: {exc}")
