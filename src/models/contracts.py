"""
Compatibility forwarding layer.

Runtime contract definitions are sourced from src/common/contracts.py.
This module re-exports those symbols to avoid contract drift.
"""

from src.common.contracts import (  # noqa: F401
    CHANNELS,
    RISK_LEVELS,
    TONES,
    AuditEvent,
    CollectionStrategy,
    InvoiceInput,
    RiskAssessment,
    build_event_id,
    utc_now_iso,
)

LANGUAGE_DEFAULT = "en-US"


def _strip_language(payload: dict) -> dict:
    data = dict(payload)
    data.pop("language", None)
    return data


def parse_risk_assessment(payload: dict) -> RiskAssessment:
    obj = RiskAssessment(**_strip_language(payload))
    obj.validate()
    return obj


def parse_collection_strategy(payload: dict) -> CollectionStrategy:
    obj = CollectionStrategy(**_strip_language(payload))
    obj.validate()
    return obj


def parse_audit_event(payload: dict) -> AuditEvent:
    return AuditEvent(**_strip_language(payload))

__all__ = [
    "CHANNELS",
    "RISK_LEVELS",
    "LANGUAGE_DEFAULT",
    "TONES",
    "AuditEvent",
    "CollectionStrategy",
    "InvoiceInput",
    "RiskAssessment",
    "build_event_id",
    "parse_audit_event",
    "parse_collection_strategy",
    "parse_risk_assessment",
    "utc_now_iso",
]
