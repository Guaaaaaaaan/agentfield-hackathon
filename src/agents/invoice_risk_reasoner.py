from __future__ import annotations

from dataclasses import dataclass

from src.common.contracts import InvoiceInput, RiskAssessment


@dataclass(slots=True)
class RiskReasoningError(Exception):
    """Raised when risk reasoning cannot produce a valid contract output."""

    code: str
    detail: str

    def __str__(self) -> str:
        return f"{self.code}: {self.detail}"


def _validate_invoice(invoice: InvoiceInput) -> None:
    if not invoice.invoice_id:
        raise RiskReasoningError("INVALID_INVOICE", "invoice_id is required")
    if invoice.overdue_days < 0:
        raise RiskReasoningError("INVALID_INVOICE", "overdue_days must be >= 0")
    if invoice.amount <= 0:
        raise RiskReasoningError("INVALID_INVOICE", "amount must be > 0")
    if invoice.late_payments_180d < 0:
        raise RiskReasoningError("INVALID_INVOICE", "late_payments_180d must be >= 0")


def invoice_risk_reasoner(invoice: InvoiceInput) -> RiskAssessment:
    """Infer invoice risk using deterministic rules and contract-safe output."""
    _validate_invoice(invoice)

    risk_points = 0
    reasons: list[str] = []

    if invoice.overdue_days >= 60:
        risk_points += 3
        reasons.append("invoice overdue for 60+ days")
    elif invoice.overdue_days >= 31:
        risk_points += 2
        reasons.append("invoice overdue for more than 30 days")
    elif invoice.overdue_days >= 8:
        risk_points += 1
        reasons.append("invoice recently overdue")

    if invoice.late_payments_180d >= 5:
        risk_points += 3
        reasons.append("customer has 5+ late payments in 180 days")
    elif invoice.late_payments_180d >= 3:
        risk_points += 2
        reasons.append("customer has repeated late payments")
    elif invoice.late_payments_180d >= 1:
        risk_points += 1
        reasons.append("customer has at least one recent late payment")

    if invoice.amount >= 5000:
        risk_points += 2
        reasons.append("invoice amount is materially high")
    elif invoice.amount >= 1000:
        risk_points += 1
        reasons.append("invoice amount is above normal threshold")

    if risk_points >= 6:
        risk_level = "high"
        confidence = 0.90
    elif risk_points >= 3:
        risk_level = "medium"
        confidence = 0.78
    else:
        risk_level = "low"
        confidence = 0.66

    if not reasons:
        reasons.append("payment behavior appears stable")

    out = RiskAssessment(
        invoice_id=invoice.invoice_id,
        risk_level=risk_level,
        confidence=confidence,
        reasons=reasons,
    )
    out.validate()
    return out
