import hashlib
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.enums import WalkForwardRiskFlag
from usa_signal_bot.backtesting.walk_forward.phase150_models import (
    WalkForwardFold,
    FoldReplayResult,
    FoldPerformanceMetric,
    FoldBenchmarkComparison,
    RobustnessSummary,
    WalkForwardValidationReport,
    create_walk_forward_validation_report_id,
    _now_utc
)

def compute_walk_forward_validation_report_hash(report: WalkForwardValidationReport) -> str:
    content = f"{report.report_id}:{report.robustness_summary.summary_hash}:{report.walk_forward_executed}:{report.stress_test_executed}"
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def build_walk_forward_validation_report(
    folds: List[WalkForwardFold],
    fold_replay_results: List[FoldReplayResult],
    fold_metrics: List[FoldPerformanceMetric],
    fold_benchmark_comparisons: List[FoldBenchmarkComparison],
    robustness_summary: RobustnessSummary
) -> WalkForwardValidationReport:
    report = WalkForwardValidationReport(
        report_id=create_walk_forward_validation_report_id(),
        created_at_utc=_now_utc(),
        folds=folds,
        fold_replay_results=fold_replay_results,
        fold_metrics=fold_metrics,
        fold_benchmark_comparisons=fold_benchmark_comparisons,
        robustness_summary=robustness_summary,
        report_hash=None,
        report_valid=True,
        walk_forward_executed=True,
        stress_test_executed=False,
        monte_carlo_executed=False,
        portfolio_optimization_enabled=False,
        strategy_activation_allowed=False,
        investment_advice=False,
        research_data_only=True,
        offline_backtest_research_only=True
    )

    errors = validate_walk_forward_validation_report(report)
    if errors:
        report.report_valid = False
        report.errors = errors
        report.risk_flags.append(WalkForwardRiskFlag.WALK_FORWARD_REPORT_INVALID)

    report.report_hash = compute_walk_forward_validation_report_hash(report)
    return report

def validate_walk_forward_validation_report(report: WalkForwardValidationReport) -> List[str]:
    errors = []
    if not report.walk_forward_executed:
        errors.append("walk_forward_executed must be true for Phase 150 report")
    if report.stress_test_executed:
        errors.append("stress_test_executed must be false in Phase 150")
    if report.monte_carlo_executed:
        errors.append("monte_carlo_executed must be false in Phase 150")
    if report.strategy_activation_allowed:
        errors.append("strategy_activation_allowed must be false")
    if report.investment_advice:
        errors.append("investment_advice must be false")
    if not report.robustness_summary.summary_valid:
        errors.append("robustness_summary is invalid")
    return errors

def walk_forward_validation_report_summary(report: WalkForwardValidationReport) -> Dict[str, Any]:
    return {
        "valid": report.report_valid,
        "fold_count": len(report.folds),
        "robustness_score": report.robustness_summary.oos_metrics.robustness_score
    }

def walk_forward_validation_report_to_text(report: WalkForwardValidationReport, limit: int = 300) -> str:
    summary = walk_forward_validation_report_summary(report)
    lines = [
        f"Walk Forward Validation Report:",
        f"  Valid: {summary['valid']}",
        f"  Folds: {summary['fold_count']}",
        f"  Score: {summary['robustness_score']}"
    ]
    return "\n".join(lines)[:limit]
