import hashlib
import json
from typing import Any, Dict, List
from usa_signal_bot.portfolio.optimization.phase156_models import ObjectiveComparisonReport, OptimizerSandboxResult, OptimizerObjectiveScore

def build_objective_comparison_report(results: List[OptimizerSandboxResult], scores: List[OptimizerObjectiveScore]) -> ObjectiveComparisonReport:
    r = ObjectiveComparisonReport(
        optimizer_results=results,
        objective_scores=scores,
        method_count=len({res.method_kind for res in results}),
        symbol_count=len({res.symbol for res in results}),
        best_method_by_objective=infer_best_method_by_objective(scores),
        report_valid=True,
        optimization_research_sandbox=True,
        not_investment_advice=True
    )
    r.report_hash = compute_objective_comparison_report_hash(r)
    return r

def infer_best_method_by_objective(scores: List[OptimizerObjectiveScore]) -> Dict[str, str]:
    best = {}
    for s in scores:
        k = s.objective_kind.value
        # Mock logic
        best[k] = s.method_kind.value
    return best

def compute_objective_comparison_report_hash(report: ObjectiveComparisonReport) -> str:
    s = f"{report.method_count}_{report.symbol_count}"
    return hashlib.sha256(s.encode()).hexdigest()

def validate_objective_comparison_report(report: ObjectiveComparisonReport) -> List[str]:
    errs = []
    if report.actual_target_weight_detected: errs.append("Actual target weight detected")
    if report.actual_portfolio_weight_detected: errs.append("Actual portfolio weight detected")
    if report.actual_allocation_detected: errs.append("Actual allocation detected")
    if report.actual_position_size_detected: errs.append("Actual position size detected")
    if report.order_size_detected: errs.append("Order size detected")
    if report.capital_allocation_detected: errs.append("Capital allocation detected")
    if report.investment_advice: errs.append("Investment advice detected")
    return errs

def objective_comparison_report_summary(report: ObjectiveComparisonReport) -> Dict[str, Any]:
    return {"methods": report.method_count, "symbols": report.symbol_count}

def objective_comparison_report_to_text(report: ObjectiveComparisonReport, limit: int = 300) -> str:
    return str(report.to_dict())[:limit]
