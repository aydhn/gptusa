"""Report QA Acceptance Gate."""
from typing import Any
from datetime import datetime, timezone
import re

from .phase124_models import (
    ReportQaAcceptanceGate,
    ReportQaAcceptanceRule,
    ReportQaAcceptanceStatus,
    FreezePreparationRiskFlag,
    create_report_qa_acceptance_gate_id,
    create_report_qa_acceptance_rule_id
)

def build_report_qa_acceptance_gate(report_payload: dict[str, Any] | None = None, qa_payload: list[dict[str, Any]] | None = None) -> ReportQaAcceptanceGate:
    now = datetime.now(timezone.utc).isoformat()
    report_text = report_payload.get("text", "") if report_payload else ""

    rules = build_report_qa_acceptance_rules(report_text, qa_payload)

    accepted = all(r.passed for r in rules if r.required)
    status = ReportQaAcceptanceStatus.ACCEPTED if accepted else ReportQaAcceptanceStatus.REJECTED

    unsafe_count = sum(len(r.matched_terms) for r in rules)

    gate = ReportQaAcceptanceGate(
        gate_id=create_report_qa_acceptance_gate_id(),
        created_at_utc=now,
        status=status,
        rules=rules,
        qa_results_ref=None,
        research_report_ref=None,
        accepted=accepted,
        unsafe_language_count=unsafe_count,
        investment_advice_detected=any(r.passed == False and r.name == "No Investment Advice" for r in rules),
        trade_signal_language_detected=any(r.passed == False and r.name == "No Trade Signal Language" for r in rules),
        order_language_detected=any(r.passed == False and r.name == "No Order Language" for r in rules),
        portfolio_language_detected=any(r.passed == False and r.name == "No Portfolio Language" for r in rules),
        guarantee_language_detected=any(r.passed == False and r.name == "No Guarantee Language" for r in rules),
        broker_execution_language_detected=any(r.passed == False and r.name == "No Broker Execution Language" for r in rules),
        secret_language_detected=any(r.passed == False and r.name == "No Secret Language" for r in rules)
    )

    errors = validate_report_qa_acceptance_gate(gate)
    gate.errors.extend(errors)
    if errors:
        gate.status = ReportQaAcceptanceStatus.BLOCKED
        gate.accepted = False
        gate.risk_flags.append(FreezePreparationRiskFlag.REPORT_QA_NOT_ACCEPTED)

    return gate

def build_report_qa_acceptance_rules(report_text: str, qa_payload: list[dict[str, Any]] | None = None) -> list[ReportQaAcceptanceRule]:
    return [
        qa_acceptance_rule_no_investment_advice(report_text),
        qa_acceptance_rule_no_trade_signal_language(report_text),
        qa_acceptance_rule_no_order_language(report_text),
        qa_acceptance_rule_no_portfolio_language(report_text),
        qa_acceptance_rule_no_guarantee_language(report_text),
        qa_acceptance_rule_no_broker_execution_language(report_text),
        qa_acceptance_rule_no_secret_language(report_text)
    ]

def _check_terms(text: str, terms: list[str], name: str) -> ReportQaAcceptanceRule:
    text_lower = text.lower()
    matched = [t for t in terms if t in text_lower]
    passed = len(matched) == 0
    return ReportQaAcceptanceRule(
        rule_id=create_report_qa_acceptance_rule_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        name=name,
        required=True,
        status=ReportQaAcceptanceStatus.ACCEPTED if passed else ReportQaAcceptanceStatus.REJECTED,
        passed=passed,
        matched_terms=matched,
        message="Passed" if passed else f"Found forbidden terms: {', '.join(matched)}"
    )

def qa_acceptance_rule_no_investment_advice(report_text: str) -> ReportQaAcceptanceRule:
    terms = ["investment advice", "financial advice", "buy now", "sell now"]
    return _check_terms(report_text, terms, "No Investment Advice")

def qa_acceptance_rule_no_trade_signal_language(report_text: str) -> ReportQaAcceptanceRule:
    terms = ["buy signal", "sell signal", "strong buy", "strong sell"]
    return _check_terms(report_text, terms, "No Trade Signal Language")

def qa_acceptance_rule_no_order_language(report_text: str) -> ReportQaAcceptanceRule:
    terms = ["kesin al", "kesin sat", "güçlü al", "güçlü sat", "emir gönder", "aktif trading", "paper'a al", "canlıya al"]
    return _check_terms(report_text, terms, "No Order Language")

def qa_acceptance_rule_no_portfolio_language(report_text: str) -> ReportQaAcceptanceRule:
    terms = ["portfolio weight", "target weight", "allocation"]
    return _check_terms(report_text, terms, "No Portfolio Language")

def qa_acceptance_rule_no_guarantee_language(report_text: str) -> ReportQaAcceptanceRule:
    terms = ["garanti kâr", "risksiz kazanç", "guaranteed profit", "sure bet"]
    return _check_terms(report_text, terms, "No Guarantee Language")

def qa_acceptance_rule_no_broker_execution_language(report_text: str) -> ReportQaAcceptanceRule:
    terms = ["sent to broker", "broker order id", "live order id"]
    return _check_terms(report_text, terms, "No Broker Execution Language")

def qa_acceptance_rule_no_secret_language(report_text: str) -> ReportQaAcceptanceRule:
    terms = ["api key", "password", "secret token"]
    return _check_terms(report_text, terms, "No Secret Language")

def validate_report_qa_acceptance_gate(gate: ReportQaAcceptanceGate) -> list[str]:
    errors = []
    if not gate.accepted:
        errors.append("Report QA not accepted due to rule failures.")
    return errors

def report_qa_acceptance_summary(gate: ReportQaAcceptanceGate) -> dict[str, Any]:
    return {"accepted": gate.accepted, "unsafe_count": gate.unsafe_language_count}

def report_qa_acceptance_to_text(gate: ReportQaAcceptanceGate, limit: int = 300) -> str:
    return f"Report QA Gate {gate.gate_id} - Accepted: {gate.accepted}"
