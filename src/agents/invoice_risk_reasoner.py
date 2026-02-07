from __future__ import annotations

from dataclasses import dataclass
import json
import os

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


def _parse_json_response(text: str) -> dict[str, object]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        lines = [line for line in lines if not line.strip().startswith("```")]
        cleaned = "\n".join(lines).strip()
    return json.loads(cleaned)


def _ai_risk_assess(invoice: InvoiceInput) -> RiskAssessment:
    try:
        import google.generativeai as genai
    except Exception as exc:  # pragma: no cover
        raise RiskReasoningError("AI_IMPORT_FAILED", str(exc)) from exc

    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RiskReasoningError("AI_CONFIG_ERROR", "GEMINI_API_KEY is missing")

    model_name = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
    timeout_sec = int(os.environ.get("REQUEST_TIMEOUT_SEC", "10"))

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)

    system_prompt = (
        "You are a billing risk assessment engine. Given invoice and customer data,\n"
        "assess the overdue risk. You MUST respond with ONLY a valid JSON object,\n"
        "no markdown, no explanation. Format:\n"
        '{"risk_level": "low|medium|high", "confidence": 0.0-1.0, "reasons": ["reason1", "reason2"]}\n\n'
        "Rules:\n"
        "- risk_level must be exactly one of: low, medium, high\n"
        "- confidence must be a float between 0.0 and 1.0\n"
        "- reasons must be a non-empty list of English strings\n"
        "- Consider: overdue_days, late_payments_180d, amount, customer behavior"
    )
    user_prompt = (
        f"Invoice ID: {invoice.invoice_id}\n"
        f"Overdue Days: {invoice.overdue_days}\n"
        f"Amount: {invoice.amount}\n"
        f"Customer ID: {invoice.customer_id}\n"
        f"Late Payments (180d): {invoice.late_payments_180d}\n"
        f"Preferred Channel: {invoice.preferred_channel}"
    )

    response = model.generate_content(
        f"{system_prompt}\n\n{user_prompt}",
        request_options={"timeout": timeout_sec},
    )
    raw_text = getattr(response, "text", "") or ""
    if not raw_text:
        raise RiskReasoningError("AI_EMPTY_RESPONSE", "empty response text from model")

    payload = _parse_json_response(raw_text)
    reasons_raw = payload.get("reasons")
    if not isinstance(reasons_raw, list):
        raise RiskReasoningError("AI_INVALID_RESPONSE", "reasons must be a list")

    result = RiskAssessment(
        invoice_id=invoice.invoice_id,
        risk_level=str(payload.get("risk_level", "")).strip().lower(),
        confidence=float(payload.get("confidence", 0)),
        reasons=[str(item).strip() for item in reasons_raw if str(item).strip()],
    )
    result.validate()
    return result


def _rule_based_risk_assess(invoice: InvoiceInput) -> RiskAssessment:
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


def invoice_risk_reasoner(invoice: InvoiceInput) -> RiskAssessment:
    """Infer invoice risk with AI-first reasoning and deterministic fallback."""
    _validate_invoice(invoice)
    try:
        result = _ai_risk_assess(invoice)
        result.validate()
        print(f"[RISK] AI success for {invoice.invoice_id}")
        return result
    except Exception as exc:
        print(f"[RISK] AI failed, using fallback: {exc}")
        return _rule_based_risk_assess(invoice)
