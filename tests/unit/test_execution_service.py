from __future__ import annotations

from dataclasses import dataclass

from src.common.contracts import CollectionStrategy
from src.services.execution_service import (
    ALLOWED_EXECUTION_STATUS,
    DEFAULT_LANGUAGE,
    ExecutionResult,
    execute_collection_action,
)
from src.skills.execute_and_audit_skill import execute_and_audit_skill


def _assert_contract(result: ExecutionResult) -> None:
    assert isinstance(result, ExecutionResult)
    assert result.language == DEFAULT_LANGUAGE
    assert result.next_action
    assert result.status in ALLOWED_EXECUTION_STATUS


def test_execute_collection_action_success_for_all_supported_channels() -> None:
    cases = [
        ("email", "mock_email_gateway", "send_email", "sent"),
        ("sms", "mock_sms_gateway", "send_sms", "sent"),
        ("call_queue", "internal_call_queue", "queue_call", "queued"),
    ]

    for channel, provider, action_type, status in cases:
        strategy = CollectionStrategy(
            invoice_id="INV-S1",
            channel=channel,
            tone="firm",
            next_action="follow_up_48h",
            escalation=False,
        )
        result = execute_collection_action(strategy)

        _assert_contract(result)
        assert result.invoice_id == "INV-S1"
        assert result.channel == channel
        assert result.provider == provider
        assert result.action_type == action_type
        assert result.status == status


@dataclass(slots=True)
class _UnsafeStrategy:
    invoice_id: str
    channel: str
    next_action: str

    def validate(self) -> None:
        # Intentional no-op to pass validation stage and hit channel mapping.
        return None


def test_execute_collection_action_invalid_channel_returns_structured_failed() -> None:
    strategy = _UnsafeStrategy(
        invoice_id="INV-F1",
        channel="fax",
        next_action="manual_review_24h",
    )

    result = execute_collection_action(strategy)  # type: ignore[arg-type]

    _assert_contract(result)
    assert result.status == "failed"
    assert result.provider == "none"
    assert result.action_type == "no_op"
    assert result.detail.startswith("unsupported channel for execution:")


def test_execute_collection_action_strategy_validation_failure_returns_failed() -> None:
    strategy = CollectionStrategy(
        invoice_id="INV-F2",
        channel="email",
        tone="bad_tone",
        next_action="manual_review_24h",
        escalation=False,
    )

    result = execute_collection_action(strategy)

    _assert_contract(result)
    assert result.status == "failed"
    assert result.provider == "none"
    assert result.action_type == "no_op"
    assert result.detail.startswith("strategy validation failed:")


def test_execute_and_audit_skill_returns_execution_result() -> None:
    strategy = CollectionStrategy(
        invoice_id="INV-S2",
        channel="email",
        tone="firm",
        next_action="follow_up_48h",
        escalation=False,
    )

    result = execute_and_audit_skill(strategy)

    _assert_contract(result)
    assert isinstance(result, ExecutionResult)
