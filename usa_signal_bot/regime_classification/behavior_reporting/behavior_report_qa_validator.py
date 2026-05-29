from typing import Any
from usa_signal_bot.core.enums import BehaviorReportQaStatus, BehaviorReportLanguageRiskKind
from usa_signal_bot.regime_classification.behavior_reporting.phase130_models import (
    BehaviorReportDocument, BehaviorReportQaRuleResult
)

def _build_qa_result(name: str, passed: bool, risk: BehaviorReportLanguageRiskKind | None = None, msg: str = "") -> BehaviorReportQaRuleResult:
    res = BehaviorReportQaRuleResult()
    res.rule_name = name
    res.passed = passed
    res.status = BehaviorReportQaStatus.PASS if passed else BehaviorReportQaStatus.FAIL
    res.language_risk = risk
    res.message = msg
    return res

def qa_rule_no_investment_advice(text: str) -> BehaviorReportQaRuleResult:
    bad = ["kesin al", "kesin sat", "güçlü al", "güçlü sat", "garanti kâr", "risksiz kazanç"]
    found = [b for b in bad if b in text.lower()]
    return _build_qa_result("no_investment_advice", len(found) == 0,
                            BehaviorReportLanguageRiskKind.INVESTMENT_ADVICE_LANGUAGE if found else None,
                            f"Found: {found}" if found else "OK")

def qa_rule_no_trade_signal_language(text: str) -> BehaviorReportQaRuleResult:
    bad = ["buy signal", "sell signal", "strong buy", "strong sell"]
    found = [b for b in bad if b in text.lower()]
    return _build_qa_result("no_trade_signal_language", len(found) == 0,
                            BehaviorReportLanguageRiskKind.TRADE_SIGNAL_LANGUAGE if found else None,
                            f"Found: {found}" if found else "OK")

def qa_rule_no_order_decision_language(text: str) -> BehaviorReportQaRuleResult:
    bad = ["entry", "exit", "order", "broker order", "paper order"]
    found = [b for b in bad if b in text.lower()]
    return _build_qa_result("no_order_decision_language", len(found) == 0,
                            BehaviorReportLanguageRiskKind.ORDER_DECISION_LANGUAGE if found else None,
                            f"Found: {found}" if found else "OK")

def qa_rule_no_portfolio_allocation_language(text: str) -> BehaviorReportQaRuleResult:
    bad = ["portfolio weight", "target weight", "allocation"]
    found = [b for b in bad if b in text.lower()]
    return _build_qa_result("no_portfolio_allocation_language", len(found) == 0,
                            BehaviorReportLanguageRiskKind.PORTFOLIO_ALLOCATION_LANGUAGE if found else None,
                            f"Found: {found}" if found else "OK")

def qa_rule_no_guarantee_language(text: str) -> BehaviorReportQaRuleResult:
    bad = ["guaranteed", "no risk"]
    found = [b for b in bad if b in text.lower()]
    return _build_qa_result("no_guarantee_language", len(found) == 0,
                            BehaviorReportLanguageRiskKind.GUARANTEE_LANGUAGE if found else None,
                            f"Found: {found}" if found else "OK")

def qa_rule_no_broker_execution_language(text: str) -> BehaviorReportQaRuleResult:
    bad = ["sent_to_broker", "sent to broker", "executed"]
    found = [b for b in bad if b in text.lower()]
    return _build_qa_result("no_broker_execution_language", len(found) == 0,
                            BehaviorReportLanguageRiskKind.BROKER_EXECUTION_LANGUAGE if found else None,
                            f"Found: {found}" if found else "OK")

def qa_rule_no_deployment_language(text: str) -> BehaviorReportQaRuleResult:
    bad = ["deploy", "production", "production_patch"]
    found = [b for b in bad if b in text.lower()]
    return _build_qa_result("no_deployment_language", len(found) == 0,
                            BehaviorReportLanguageRiskKind.DEPLOYMENT_LANGUAGE if found else None,
                            f"Found: {found}" if found else "OK")

def qa_rule_no_sensitive_secret_language(text: str) -> BehaviorReportQaRuleResult:
    bad = ["api_key", "token", "password", "secret"]
    found = [b for b in bad if b in text.lower()]
    return _build_qa_result("no_sensitive_secret_language", len(found) == 0,
                            BehaviorReportLanguageRiskKind.SENSITIVE_SECRET_LANGUAGE if found else None,
                            f"Found: {found}" if found else "OK")

def run_behavior_report_qa(document: BehaviorReportDocument, rendered_text: str | None = None) -> list[BehaviorReportQaRuleResult]:
    if rendered_text is None:
        rendered_text = str(document.to_dict())

    return [
        qa_rule_no_investment_advice(rendered_text),
        qa_rule_no_trade_signal_language(rendered_text),
        qa_rule_no_order_decision_language(rendered_text),
        qa_rule_no_portfolio_allocation_language(rendered_text),
        qa_rule_no_guarantee_language(rendered_text),
        qa_rule_no_broker_execution_language(rendered_text),
        qa_rule_no_deployment_language(rendered_text),
        qa_rule_no_sensitive_secret_language(rendered_text)
    ]

def behavior_report_qa_passed(results: list[BehaviorReportQaRuleResult]) -> bool:
    return all(r.passed for r in results)

def behavior_report_qa_summary(results: list[BehaviorReportQaRuleResult]) -> dict[str, Any]:
    return {"passed": behavior_report_qa_passed(results), "count": len(results)}

def behavior_report_qa_to_text(results: list[BehaviorReportQaRuleResult], limit: int = 200) -> str:
    lines = [f"QA passed: {behavior_report_qa_passed(results)}"]
    for r in results:
        lines.append(f"- {r.rule_name}: {r.status.value}")
    return "\n".join(lines)[:limit]
