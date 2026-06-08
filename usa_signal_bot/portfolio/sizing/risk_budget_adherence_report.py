import json
import hashlib
from typing import Any
from usa_signal_bot.portfolio.sizing.phase154_models import RiskBudgetAdherenceReport, SizingPrototypeResult, SizingPolicy

def build_risk_budget_adherence_report(results: list[SizingPrototypeResult], policy: SizingPolicy) -> RiskBudgetAdherenceReport:
    report = RiskBudgetAdherenceReport()
    report.result_count = len(results)
    report.max_risk_budget_usage_fraction = calculate_max_risk_budget_usage(results)
    report.average_risk_budget_usage_fraction = calculate_average_risk_budget_usage(results)
    report.breach_count = count_risk_budget_breaches(results, policy)
    report.report_hash = compute_risk_budget_adherence_report_hash(report)
    report.report_valid = len(validate_risk_budget_adherence_report(report)) == 0
    return report

def calculate_max_risk_budget_usage(results: list[SizingPrototypeResult]) -> float | None:
    usages = [r.risk_budget_usage_fraction for r in results if r.risk_budget_usage_fraction is not None]
    if not usages:
        return None
    return max(usages)

def calculate_average_risk_budget_usage(results: list[SizingPrototypeResult]) -> float | None:
    usages = [r.risk_budget_usage_fraction for r in results if r.risk_budget_usage_fraction is not None]
    if not usages:
        return None
    return sum(usages) / len(usages)

def count_risk_budget_breaches(results: list[SizingPrototypeResult], policy: SizingPolicy) -> int:
    return sum(1 for r in results if r.risk_budget_usage_fraction is not None and r.risk_budget_usage_fraction > policy.max_risk_budget_usage_fraction)

def compute_risk_budget_adherence_report_hash(report: RiskBudgetAdherenceReport) -> str:
    data = {
        "result_count": report.result_count,
        "max_risk_budget_usage_fraction": report.max_risk_budget_usage_fraction,
        "average_risk_budget_usage_fraction": report.average_risk_budget_usage_fraction,
        "breach_count": report.breach_count
    }
    data_str = json.dumps(data, sort_keys=True)
    return hashlib.sha256(data_str.encode('utf-8')).hexdigest()

def validate_risk_budget_adherence_report(report: RiskBudgetAdherenceReport) -> list[str]:
    errors = []
    if report.actual_capital_allocation_detected:
        errors.append("Actual capital allocation detected.")
    if report.actual_position_size_detected:
        errors.append("Actual position size detected.")
    if report.target_weight_detected:
        errors.append("Target weight detected.")
    return errors

def risk_budget_adherence_report_summary(report: RiskBudgetAdherenceReport) -> dict[str, Any]:
    return {"breach_count": report.breach_count, "valid": report.report_valid}

def risk_budget_adherence_report_to_text(report: RiskBudgetAdherenceReport, limit: int = 300) -> str:
    return f"Risk Budget Adherence Report: {report.breach_count} breaches"[:limit]
