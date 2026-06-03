from typing import Any, Dict, List

from usa_signal_bot.backtesting.walk_forward.phase150_models import (
    BenchmarkComparisonIngestionResult,
    WalkForwardInputReference,
    WalkForwardWindowPolicy,
    WalkForwardFold,
    FoldReplayResult,
    FoldPerformanceMetric,
    FoldBenchmarkComparison,
    OOSRobustnessMetrics,
    TemporalStabilityMetric,
    DegradationDiagnostic,
    RobustnessSummary,
    WalkForwardValidationReport,
    TemporalStabilityAuditReport,
    WalkForwardSafetyBoundaryResult,
    Phase151ReadinessGate,
    WalkForwardContext,
    WalkForwardFullReview
)

from usa_signal_bot.backtesting.walk_forward.benchmark_comparison_ingestion import benchmark_comparison_ingestion_to_text
from usa_signal_bot.backtesting.walk_forward.walk_forward_window_policy import walk_forward_window_policy_to_text
from usa_signal_bot.backtesting.walk_forward.anchored_split_builder import anchored_folds_to_text
from usa_signal_bot.backtesting.walk_forward.rolling_split_builder import rolling_folds_to_text
from usa_signal_bot.backtesting.walk_forward.fold_replay_runner import fold_replay_results_to_text
from usa_signal_bot.backtesting.walk_forward.fold_performance_metrics import fold_performance_metrics_to_text
from usa_signal_bot.backtesting.walk_forward.fold_benchmark_comparison import fold_benchmark_comparisons_to_text
from usa_signal_bot.backtesting.walk_forward.oos_robustness_metrics import oos_robustness_metrics_to_text
from usa_signal_bot.backtesting.walk_forward.temporal_stability_analyzer import temporal_stability_to_text
from usa_signal_bot.backtesting.walk_forward.degradation_diagnostics import degradation_diagnostics_to_text
from usa_signal_bot.backtesting.walk_forward.robustness_summary import robustness_summary_to_text
from usa_signal_bot.backtesting.walk_forward.walk_forward_validation_report import walk_forward_validation_report_to_text
from usa_signal_bot.backtesting.walk_forward.temporal_stability_audit import temporal_stability_audit_to_text
from usa_signal_bot.backtesting.walk_forward.walk_forward_safety_boundary import walk_forward_safety_boundary_to_text
from usa_signal_bot.backtesting.walk_forward.phase151_readiness_gate import phase151_readiness_gate_to_text
from usa_signal_bot.backtesting.walk_forward.walk_forward_report import walk_forward_full_review_to_text, walk_forward_limitations_text

def benchmark_comparison_ingestion_result_to_text(item: BenchmarkComparisonIngestionResult) -> str:
    return benchmark_comparison_ingestion_to_text(item)

def walk_forward_input_reference_to_text(item: WalkForwardInputReference) -> str:
    return f"WalkForwardInputReference: {item.input_kind.value} (Available: {item.available})"

def walk_forward_fold_to_text(item: WalkForwardFold, limit: int = 300) -> str:
    return f"Fold {item.fold_index} [{item.fold_kind.value}]"

def fold_replay_result_to_text(item: FoldReplayResult, limit: int = 300) -> str:
    return f"FoldReplayResult {item.fold_index} [{item.replay_status.value}]"

def walk_forward_context_to_text(item: WalkForwardContext, limit: int = 300) -> str:
    return f"WalkForwardContext: {item.status.value}, Ready: {item.ready_for_phase151}"

def walk_forward_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"Store Summary: {summary['reviews']} reviews, {summary['contexts']} contexts"
