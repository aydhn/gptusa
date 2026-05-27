import datetime
from typing import Any

from usa_signal_bot.core.enums import ReportQaStatus, ReportLanguageRiskKind
from usa_signal_bot.feature_engine.factor_explainability.phase123_models import (
    ResearchReportDocument,
    ReportQaRuleResult,
    create_report_qa_rule_result_id
)

def _build_qa_result(rule_name: str, passed: bool, risk: ReportLanguageRiskKind | None, matched: list[str]) -> ReportQaRuleResult:
    return ReportQaRuleResult(
        qa_result_id=create_report_qa_rule_result_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        rule_name=rule_name,
        status=ReportQaStatus.PASS if passed else ReportQaStatus.FAIL,
        passed=passed,
        language_risk=risk,
        matched_terms=matched,
        field=None,
        message=f"{rule_name} {'passed' if passed else 'failed'}",
        warnings=[],
        errors=[],
        metadata={}
    )

def qa_rule_no_investment_advice(text: str) -> ReportQaRuleResult:
    terms = ["kesin al", "kesin sat", "güçlü al", "güçlü sat"]
    matched = [t for t in terms if t in text.lower()]
    return _build_qa_result("qa_rule_no_investment_advice", not bool(matched), ReportLanguageRiskKind.INVESTMENT_ADVICE_LANGUAGE if matched else None, matched)

def qa_rule_no_trade_signal_language(text: str) -> ReportQaRuleResult:
    terms = ["buy signal", "sell signal", "strong buy", "strong sell"]
    matched = [t for t in terms if t in text.lower()]
    return _build_qa_result("qa_rule_no_trade_signal_language", not bool(matched), ReportLanguageRiskKind.TRADE_SIGNAL_LANGUAGE if matched else None, matched)

def qa_rule_no_order_decision_language(text: str) -> ReportQaRuleResult:
    terms = ["entry", "exit", "order", "paper order"]
    matched = [t for t in terms if t in text.lower()]
    return _build_qa_result("qa_rule_no_order_decision_language", not bool(matched), ReportLanguageRiskKind.ORDER_DECISION_LANGUAGE if matched else None, matched)

def qa_rule_no_portfolio_allocation_language(text: str) -> ReportQaRuleResult:
    terms = ["portfolio weight", "target weight", "allocation"]
    matched = [t for t in terms if t in text.lower()]
    return _build_qa_result("qa_rule_no_portfolio_allocation_language", not bool(matched), ReportLanguageRiskKind.PORTFOLIO_ALLOCATION_LANGUAGE if matched else None, matched)

def qa_rule_no_guarantee_language(text: str) -> ReportQaRuleResult:
    terms = ["garanti kâr", "risksiz kazanç"]
    matched = [t for t in terms if t in text.lower()]
    return _build_qa_result("qa_rule_no_guarantee_language", not bool(matched), ReportLanguageRiskKind.GUARANTEE_LANGUAGE if matched else None, matched)

def qa_rule_no_broker_execution_language(text: str) -> ReportQaRuleResult:
    terms = ["sent_to_broker", "broker order"]
    matched = [t for t in terms if t in text.lower()]
    return _build_qa_result("qa_rule_no_broker_execution_language", not bool(matched), ReportLanguageRiskKind.BROKER_EXECUTION_LANGUAGE if matched else None, matched)

def qa_rule_no_sensitive_secret_language(text: str) -> ReportQaRuleResult:
    terms = ["api_key", "token", "secret", "password"]
    matched = [t for t in terms if t in text.lower()]
    return _build_qa_result("qa_rule_no_sensitive_secret_language", not bool(matched), ReportLanguageRiskKind.SENSITIVE_SECRET_LANGUAGE if matched else None, matched)

def run_report_qa(document: ResearchReportDocument, rendered_text: str | None = None) -> list[ReportQaRuleResult]:
    text = rendered_text or " ".join([s.body for s in document.sections])

    results = [
        qa_rule_no_investment_advice(text),
        qa_rule_no_trade_signal_language(text),
        qa_rule_no_order_decision_language(text),
        qa_rule_no_portfolio_allocation_language(text),
        qa_rule_no_guarantee_language(text),
        qa_rule_no_broker_execution_language(text),
        qa_rule_no_sensitive_secret_language(text)
    ]
    return results

def report_qa_passed(results: list[ReportQaRuleResult]) -> bool:
    return all(r.passed for r in results)

def report_qa_summary(results: list[ReportQaRuleResult]) -> dict[str, Any]:
    return {"passed": report_qa_passed(results), "count": len(results)}

def report_qa_to_text(results: list[ReportQaRuleResult], limit: int = 200) -> str:
    return f"QA Passed: {report_qa_passed(results)} ({len(results)} rules checked)"
