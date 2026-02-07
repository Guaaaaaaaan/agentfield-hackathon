from __future__ import annotations

from dataclasses import dataclass
import json
import os

from src.common.contracts import CollectionStrategy, InvoiceInput, RiskAssessment

_VALID_CHANNELS = {"email", "sms", "call_queue"}
_VALID_TONES = {"gentle", "firm", "urgent"}


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


def _parse_json_response(text: str) -> dict[str, object]:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        lines = [line for line in lines if not line.strip().startswith("```")]
        cleaned = "\n".join(lines).strip()
    return json.loads(cleaned)


def _to_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes"}
    return bool(value)


def _apply_channel_override(invoice: InvoiceInput, risk: RiskAssessment, channel: str) -> str:
    normalized = _normalize_channel(channel)
    if risk.risk_level == "low":
        return "email"
    if risk.risk_level == "medium":
        return "sms" if normalized == "call_queue" else normalized
    if risk.risk_level == "high" and invoice.overdue_days >= 45:
        return "call_queue"
    return normalized


def _ai_strategy_decide(invoice: InvoiceInput, risk: RiskAssessment) -> CollectionStrategy:
    try:
        from google import genai
    except Exception as exc:  # pragma: no cover
        raise StrategyReasoningError("AI_IMPORT_FAILED", str(exc)) from exc

    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise StrategyReasoningError("AI_CONFIG_ERROR", "GEMINI_API_KEY is missing")

    model_name = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")

    client = genai.Client(api_key=api_key)

    system_prompt = (
        "You are a billing collection strategy engine. Given risk assessment and invoice data,\n"
        "decide the best collection strategy. You MUST respond with ONLY a valid JSON object,\n"
        "no markdown, no explanation. Format:\n"
        '{"channel": "email|sms|call_queue", "tone": "gentle|firm|urgent", "next_action": "action_description", "escalation": true|false}\n\n'
        "Rules:\n"
        "- channel must be exactly one of: email, sms, call_queue\n"
        "- tone must be exactly one of: gentle, firm, urgent\n"
        '- next_action must be a non-empty English string (e.g. "escalate_after_24h", "follow_up_48h", "friendly_reminder_72h")\n'
        "- escalation must be boolean\n"
        "- For high risk: prefer call_queue, urgent tone, escalation=true\n"
        "- For medium risk: prefer email or sms, firm tone, escalation=false\n"
        "- For low risk: prefer email, gentle tone, escalation=false"
    )
    user_prompt = (
        f"Invoice ID: {invoice.invoice_id}\n"
        f"Risk Level: {risk.risk_level}\n"
        f"Confidence: {risk.confidence}\n"
        f"Reasons: {risk.reasons}\n"
        f"Overdue Days: {invoice.overdue_days}\n"
        f"Amount: {invoice.amount}\n"
        f"Customer Preferred Channel: {invoice.preferred_channel}"
    )

    response = client.models.generate_content(
        model=model_name,
        contents=f"{system_prompt}\n\n{user_prompt}",
    )
    raw_text = response.text or ""
    if not raw_text:
        raise StrategyReasoningError("AI_EMPTY_RESPONSE", "empty response text from model")

    payload = _parse_json_response(raw_text)
    tone = str(payload.get("tone", "")).strip().lower()
    if tone not in _VALID_TONES:
        raise StrategyReasoningError("AI_INVALID_RESPONSE", f"invalid tone: {tone}")

    strategy = CollectionStrategy(
        invoice_id=invoice.invoice_id,
        channel=_apply_channel_override(invoice, risk, str(payload.get("channel", "email"))),
        tone=tone,
        next_action=str(payload.get("next_action", "")).strip(),
        escalation=_to_bool(payload.get("escalation")),
    )
    strategy.validate()
    return strategy


def _rule_based_strategy(invoice: InvoiceInput, risk: RiskAssessment) -> CollectionStrategy:
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


def collection_strategy_reasoner(invoice: InvoiceInput, risk: RiskAssessment) -> CollectionStrategy:
    """Generate collection strategy with AI-first reasoning and deterministic fallback."""
    if not invoice.invoice_id:
        raise StrategyReasoningError("INVALID_INVOICE", "invoice_id is required")

    try:
        result = _ai_strategy_decide(invoice, risk)
        result.validate()
        print(f"[STRATEGY] AI success for {invoice.invoice_id}")
        return result
    except Exception as exc:
        print(f"[STRATEGY] AI failed, using fallback: {exc}")
        return _rule_based_strategy(invoice, risk)
