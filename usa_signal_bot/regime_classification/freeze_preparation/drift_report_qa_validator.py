from typing import Optional
from typing import Any, Dict, List
from usa_signal_bot.core.enums import DriftReportQaStatus, DriftReportLanguageRiskKind
from usa_signal_bot.regime_classification.freeze_preparation.phase134_models import (
    DriftReportDocument,
    DriftReportQaRuleResult,
    create_drift_report_qa_result_id,
    _now_utc_str
)

def qa_rule_no_investment_advice(text: str) -> DriftReportQaRuleResult:
    terms = ["investment advice", "garanti kâr", "risksiz kazanç"]
    matched = [t for t in terms if t in text.lower()]
    passed = len(matched) == 0
    return DriftReportQaRuleResult(
        qa_result_id=create_drift_report_qa_result_id(),
        created_at_utc=_now_utc_str(),
        rule_name="No Investment Advice",
        status=DriftReportQaStatus.PASS if passed else DriftReportQaStatus.FAIL,
        passed=passed,
        language_risk=DriftReportLanguageRiskKind.INVESTMENT_ADVICE_LANGUAGE if not passed else None,
        matched_terms=matched,
        message="Failed investment advice check" if not passed else "Passed"
    )

def qa_rule_no_trade_signal_language(text: str) -> DriftReportQaRuleResult:
    terms = ["kesin al", "kesin sat", "güçlü al", "güçlü sat", "buy signal", "sell signal", "strong buy", "strong sell"]
    matched = [t for t in terms if t in text.lower()]
    passed = len(matched) == 0
    return DriftReportQaRuleResult(
        qa_result_id=create_drift_report_qa_result_id(),
        created_at_utc=_now_utc_str(),
        rule_name="No Trade Signal Language",
        status=DriftReportQaStatus.PASS if passed else DriftReportQaStatus.FAIL,
        passed=passed,
        language_risk=DriftReportLanguageRiskKind.TRADE_SIGNAL_LANGUAGE if not passed else None,
        matched_terms=matched,
        message="Failed trade signal check" if not passed else "Passed"
    )

def qa_rule_no_order_decision_language(text: str) -> DriftReportQaRuleResult:
    terms = ["order decision", "broker order", "paper order", "entry", "exit"]
    matched = [t for t in terms if t in text.lower()]
    passed = len(matched) == 0
    return DriftReportQaRuleResult(
        qa_result_id=create_drift_report_qa_result_id(),
        created_at_utc=_now_utc_str(),
        rule_name="No Order Decision Language",
        status=DriftReportQaStatus.PASS if passed else DriftReportQaStatus.FAIL,
        passed=passed,
        language_risk=DriftReportLanguageRiskKind.ORDER_DECISION_LANGUAGE if not passed else None,
        matched_terms=matched,
        message="Failed order decision check" if not passed else "Passed"
    )

def qa_rule_no_portfolio_allocation_language(text: str) -> DriftReportQaRuleResult:
    terms = ["portfolio weight", "target weight", "allocation"]
    matched = [t for t in terms if t in text.lower()]
    passed = len(matched) == 0
    return DriftReportQaRuleResult(
        qa_result_id=create_drift_report_qa_result_id(),
        created_at_utc=_now_utc_str(),
        rule_name="No Portfolio Allocation Language",
        status=DriftReportQaStatus.PASS if passed else DriftReportQaStatus.FAIL,
        passed=passed,
        language_risk=DriftReportLanguageRiskKind.PORTFOLIO_ALLOCATION_LANGUAGE if not passed else None,
        matched_terms=matched,
        message="Failed portfolio allocation check" if not passed else "Passed"
    )

def qa_rule_no_guarantee_language(text: str) -> DriftReportQaRuleResult:
    terms = ["guarantee", "sure thing", "kesin"]
    matched = [t for t in terms if t in text.lower()]
    passed = len(matched) == 0
    return DriftReportQaRuleResult(
        qa_result_id=create_drift_report_qa_result_id(),
        created_at_utc=_now_utc_str(),
        rule_name="No Guarantee Language",
        status=DriftReportQaStatus.PASS if passed else DriftReportQaStatus.FAIL,
        passed=passed,
        language_risk=DriftReportLanguageRiskKind.GUARANTEE_LANGUAGE if not passed else None,
        matched_terms=matched,
        message="Failed guarantee language check" if not passed else "Passed"
    )

def qa_rule_no_broker_execution_language(text: str) -> DriftReportQaRuleResult:
    terms = ["sent_to_broker", "broker execution"]
    matched = [t for t in terms if t in text.lower()]
    passed = len(matched) == 0
    return DriftReportQaRuleResult(
        qa_result_id=create_drift_report_qa_result_id(),
        created_at_utc=_now_utc_str(),
        rule_name="No Broker Execution Language",
        status=DriftReportQaStatus.PASS if passed else DriftReportQaStatus.FAIL,
        passed=passed,
        language_risk=DriftReportLanguageRiskKind.BROKER_EXECUTION_LANGUAGE if not passed else None,
        matched_terms=matched,
        message="Failed broker execution check" if not passed else "Passed"
    )

def qa_rule_no_deployment_language(text: str) -> DriftReportQaRuleResult:
    terms = ["deploy", "production", "production_patch"]
    matched = [t for t in terms if t in text.lower()]
    passed = len(matched) == 0
    return DriftReportQaRuleResult(
        qa_result_id=create_drift_report_qa_result_id(),
        created_at_utc=_now_utc_str(),
        rule_name="No Deployment Language",
        status=DriftReportQaStatus.PASS if passed else DriftReportQaStatus.FAIL,
        passed=passed,
        language_risk=DriftReportLanguageRiskKind.DEPLOYMENT_LANGUAGE if not passed else None,
        matched_terms=matched,
        message="Failed deployment check" if not passed else "Passed"
    )

def qa_rule_no_live_monitoring_language(text: str) -> DriftReportQaRuleResult:
    terms = ["live monitoring", "daemon started", "scheduler enabled"]
    matched = [t for t in terms if t in text.lower()]
    passed = len(matched) == 0
    return DriftReportQaRuleResult(
        qa_result_id=create_drift_report_qa_result_id(),
        created_at_utc=_now_utc_str(),
        rule_name="No Live Monitoring Language",
        status=DriftReportQaStatus.PASS if passed else DriftReportQaStatus.FAIL,
        passed=passed,
        language_risk=DriftReportLanguageRiskKind.LIVE_MONITORING_LANGUAGE if not passed else None,
        matched_terms=matched,
        message="Failed live monitoring check" if not passed else "Passed"
    )

def qa_rule_no_sensitive_secret_language(text: str) -> DriftReportQaRuleResult:
    terms = ["api_key", "token", "secret", "password"]
    matched = [t for t in terms if t in text.lower()]
    passed = len(matched) == 0
    return DriftReportQaRuleResult(
        qa_result_id=create_drift_report_qa_result_id(),
        created_at_utc=_now_utc_str(),
        rule_name="No Sensitive Secret Language",
        status=DriftReportQaStatus.PASS if passed else DriftReportQaStatus.FAIL,
        passed=passed,
        language_risk=DriftReportLanguageRiskKind.SECRET_LANGUAGE if not passed else None,
        matched_terms=matched,
        message="Failed sensitive secret check" if not passed else "Passed"
    )

def run_drift_report_qa(document: DriftReportDocument, rendered_text: Optional[str] = None) -> List[DriftReportQaRuleResult]:
    text = rendered_text or document.rendered_text or ""
    results = [
        qa_rule_no_investment_advice(text),
        qa_rule_no_trade_signal_language(text),
        qa_rule_no_order_decision_language(text),
        qa_rule_no_portfolio_allocation_language(text),
        qa_rule_no_guarantee_language(text),
        qa_rule_no_broker_execution_language(text),
        qa_rule_no_deployment_language(text),
        qa_rule_no_live_monitoring_language(text),
        qa_rule_no_sensitive_secret_language(text)
    ]
    return results

def drift_report_qa_passed(results: List[DriftReportQaRuleResult]) -> bool:
    return all(r.passed for r in results)

def drift_report_qa_summary(results: List[DriftReportQaRuleResult]) -> Dict[str, Any]:
    return {
        "passed": drift_report_qa_passed(results),
        "failed_rules": sum(1 for r in results if not r.passed)
    }

def drift_report_qa_to_text(results: List[DriftReportQaRuleResult], limit: int = 200) -> str:
    passed = drift_report_qa_passed(results)
    return f"QA Passed: {passed}"[:limit]
