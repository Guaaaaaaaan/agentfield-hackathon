from __future__ import annotations

from src.common.contracts import CollectionStrategy, RiskAssessment


def fallback_risk(invoice_id: str, reason: str = "risk_reasoner_failed") -> RiskAssessment:
    return RiskAssessment(
        invoice_id=invoice_id,
        risk_level="medium",
        confidence=0.50,
        reasons=[f"fallback:{reason}"],
    )


def fallback_strategy(invoice_id: str) -> CollectionStrategy:
    return CollectionStrategy(
        invoice_id=invoice_id,
        channel="email",
        tone="firm",
        next_action="manual_review_24h",
        escalation=False,
    )
