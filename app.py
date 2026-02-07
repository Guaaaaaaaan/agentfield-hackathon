from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
load_dotenv()

from src.agents.collection_strategy_reasoner import collection_strategy_reasoner
from src.agents.execute_and_audit_skill import execute_and_audit_skill
from src.agents.invoice_risk_reasoner import invoice_risk_reasoner
from src.common.audit import AuditLogger
from src.common.contracts import CollectionStrategy, InvoiceInput, RiskAssessment
from src.orchestration.pipeline import Executor, RiskReasoner, StrategyReasoner, run_pipeline


def _mock_invoice_risk_reasoner(invoice: InvoiceInput) -> RiskAssessment:
    if invoice.overdue_days > 45:
        return RiskAssessment(invoice.invoice_id, "high", 0.91, ["overdue_days>45"])
    return RiskAssessment(invoice.invoice_id, "low", 0.62, ["payment_pattern_stable"])


def _mock_collection_strategy_reasoner(invoice: InvoiceInput, risk: RiskAssessment) -> CollectionStrategy:
    if risk.risk_level == "high":
        return CollectionStrategy(invoice.invoice_id, "email", "urgent", "escalate_after_24h", True)
    return CollectionStrategy(invoice.invoice_id, "email", "gentle", "friendly_reminder_72h", False)


def _mock_execute_and_audit_skill(_: CollectionStrategy) -> str:
    return "sent"


def _resolve_runtime(use_mock: bool) -> tuple[RiskReasoner, StrategyReasoner, Executor]:
    if use_mock:
        return (
            _mock_invoice_risk_reasoner,
            _mock_collection_strategy_reasoner,
            _mock_execute_and_audit_skill,
        )
    return invoice_risk_reasoner, collection_strategy_reasoner, execute_and_audit_skill


def _to_invoice_input(item: dict[str, Any]) -> InvoiceInput:
    return InvoiceInput(
        invoice_id=str(item["invoice_id"]),
        overdue_days=int(item["overdue_days"]),
        amount=float(item["amount"]),
        customer_id=str(item["customer_id"]),
        late_payments_180d=int(item["late_payments_180d"]),
        preferred_channel=str(item.get("preferred_channel", "email")),
    )


def _load_inputs(input_path: str) -> list[InvoiceInput]:
    payload = json.loads(Path(input_path).read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        return [_to_invoice_input(payload)]
    if isinstance(payload, list):
        if not payload:
            raise ValueError("input payload list must not be empty")
        return [_to_invoice_input(item) for item in payload]
    raise ValueError("input payload must be a JSON object or list of objects")


def _print_demo_output(outputs: list[dict[str, Any]]) -> None:
    print("=== Intelligent Billing Operations Engine (MVP Demo) ===")
    print()

    success = 0
    failed = 0
    fallback = 0
    total = len(outputs)

    for idx, item in enumerate(outputs, start=1):
        invoice_id = str(item.get("invoice_id", "N/A"))
        risk_level = str(item.get("risk_level", "unknown"))
        confidence = float(item.get("confidence", 0.0))
        reasons_list = item.get("reasons", [])
        reasons = "; ".join(str(reason) for reason in reasons_list) if reasons_list else "none"
        channel = str(item.get("channel", "N/A"))
        tone = str(item.get("tone", "N/A"))
        escalation = bool(item.get("escalation", False))
        next_action = str(item.get("next_action", "N/A"))
        audit_event = item.get("audit_event") if isinstance(item.get("audit_event"), dict) else {}
        status = str(audit_event.get("status", "unknown"))
        trace_id = str(item.get("trace_id", "N/A"))
        is_fallback = bool(item.get("fallback", False))
        org_name = str(item.get("org_name", "org"))
        email_address = str(item.get("email_address", "-"))
        phone_number = str(item.get("phone_number", "-"))
        scheduled_contact_date = str(item.get("scheduled_contact_date", "-"))

        if status in {"sent", "queued"}:
            success += 1
        elif status == "failed":
            failed += 1
        if is_fallback:
            fallback += 1

        print(f"[{idx}/{total}] Invoice: {invoice_id}")
        print(f"  Organization: {org_name}")
        print(f"  Email:    {email_address}")
        print(f"  Phone:    {phone_number}")
        print(f"  Risk:     {risk_level} (confidence: {confidence:.2f})")
        print(f"  Reasons:  {reasons}")
        print(f"  Strategy: channel={channel}, tone={tone}, escalation={str(escalation).lower()}")
        print(f"  Action:   {next_action}")
        print(f"  Status:   {status}")
        print(f"  Trace:    {trace_id}")
        print(f"  Scheduled: {scheduled_contact_date}")
        print()

    print("=== Summary ===")
    print(f"Total: {total} | Success: {success} | Failed: {failed} | Fallback: {fallback}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run billing orchestration demo flow.")
    parser.add_argument("--use-mock", action="store_true", help="Use local mock adapters for debug only.")
    parser.add_argument("--json", action="store_true", help="Output raw JSON payload.")
    parser.add_argument(
        "--input",
        default="data/samples/pipeline_inputs_runtime.json",
        help="Path to JSON input file (single object or list of objects).",
    )
    args = parser.parse_args()

    risk_fn, strategy_fn, exec_fn = _resolve_runtime(args.use_mock)
    raw_items = json.loads(Path(args.input).read_text(encoding="utf-8"))
    if isinstance(raw_items, dict):
        raw_items = [raw_items]
    if not isinstance(raw_items, list):
        raise ValueError("input payload must be a JSON object or list of objects")
    if not raw_items:
        raise ValueError("input payload list must not be empty")

    inputs = [_to_invoice_input(item) for item in raw_items]
    logger = AuditLogger()

    results: list[dict[str, Any]] = []
    for idx, (invoice, raw) in enumerate(zip(inputs, raw_items), start=1):
        output = run_pipeline(
            invoice=invoice,
            risk_reasoner=risk_fn,
            strategy_reasoner=strategy_fn,
            executor=exec_fn,
            audit_logger=logger,
            trace_id=f"TRACE-RUN-{idx:03d}-{invoice.invoice_id}",
        )
        for key in ("org_name", "email_address", "phone_number", "scheduled_contact_date"):
            if key in raw:
                output[key] = raw[key]
        results.append(output)
    outputs = results
    if args.json:
        output: dict[str, Any] | list[dict[str, Any]] = outputs[0] if len(outputs) == 1 else outputs
        print(json.dumps(output, ensure_ascii=True, indent=2))
    else:
        _print_demo_output(outputs)


if __name__ == "__main__":
    main()
