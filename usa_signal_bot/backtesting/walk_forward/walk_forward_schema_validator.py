from typing import Any, Dict, List

from usa_signal_bot.backtesting.walk_forward.phase150_models import (
    WalkForwardInputReference,
    WalkForwardWindowPolicy,
    WalkForwardFold,
    FoldReplayResult,
    FoldPerformanceMetric,
    OOSRobustnessMetrics,
    TemporalStabilityMetric,
    WalkForwardValidationReport,
    WalkForwardContext
)

FORBIDDEN_COLUMNS = [
    "broker_order", "paper_order", "live_order", "sent_to_broker",
    "strategy_active", "deployment_enabled", "portfolio_weight",
    "target_weight", "allocation", "real_order", "live_signal",
    "recommended_weight", "production_patch"
]

def validate_walk_forward_column_names(columns: List[str]) -> List[str]:
    return [col for col in columns if col in FORBIDDEN_COLUMNS]

def validate_no_forbidden_walk_forward_columns(columns: List[str]) -> List[str]:
    forbidden = validate_walk_forward_column_names(columns)
    if forbidden:
        return [f"Forbidden columns found: {forbidden}"]
    return []

def validate_walk_forward_input_reference_schema(item: WalkForwardInputReference) -> List[str]:
    if not item.input_ref_id:
        return ["input_ref_id missing"]
    return []

def validate_walk_forward_window_policy_schema(item: WalkForwardWindowPolicy) -> List[str]:
    if not item.policy_id:
        return ["policy_id missing"]
    return []

def validate_walk_forward_fold_schema(item: WalkForwardFold) -> List[str]:
    if not item.fold_id:
        return ["fold_id missing"]
    return []

def validate_fold_replay_result_schema(item: FoldReplayResult) -> List[str]:
    if not item.result_id:
        return ["result_id missing"]
    return []

def validate_fold_performance_metrics_schema(items: List[FoldPerformanceMetric]) -> List[str]:
    return []

def validate_oos_robustness_metrics_schema(item: OOSRobustnessMetrics) -> List[str]:
    return []

def validate_temporal_stability_metrics_schema(items: List[TemporalStabilityMetric]) -> List[str]:
    return []

def validate_walk_forward_validation_report_schema(report: WalkForwardValidationReport) -> List[str]:
    if not report.report_id:
        return ["report_id missing"]
    return []

def validate_walk_forward_context_schema(context: WalkForwardContext) -> List[str]:
    if not context.context_id:
        return ["context_id missing"]
    return []

def walk_forward_schema_summary(errors: List[str]) -> Dict[str, Any]:
    return {
        "valid": len(errors) == 0,
        "error_count": len(errors)
    }

def walk_forward_schema_to_text(errors: List[str]) -> str:
    return "Schema Valid" if not errors else f"Schema Invalid ({len(errors)} errors)"
