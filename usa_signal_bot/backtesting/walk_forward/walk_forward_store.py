import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from usa_signal_bot.backtesting.walk_forward.phase150_models import (
    WalkForwardContext,
    WalkForwardFullReview,
    WalkForwardInputReference,
    WalkForwardWindowPolicy,
    WalkForwardFold,
    FoldReplayConfig,
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
    walk_forward_context_to_dict,
    walk_forward_full_review_to_dict,
    walk_forward_input_reference_to_dict,
    walk_forward_window_policy_to_dict,
    walk_forward_fold_to_dict,
    fold_replay_config_to_dict,
    fold_replay_result_to_dict,
    fold_performance_metric_to_dict,
    fold_benchmark_comparison_to_dict,
    oos_robustness_metrics_to_dict,
    temporal_stability_metric_to_dict,
    degradation_diagnostic_to_dict,
    robustness_summary_to_dict,
    walk_forward_validation_report_to_dict,
    temporal_stability_audit_report_to_dict,
    walk_forward_safety_boundary_result_to_dict,
    phase151_readiness_gate_to_dict
)

def walk_forward_store_dir(data_root: Path) -> Path:
    return data_root / "backtesting" / "walk_forward"

def walk_forward_contexts_dir(data_root: Path) -> Path:
    return walk_forward_store_dir(data_root) / "contexts"

def walk_forward_reviews_dir(data_root: Path) -> Path:
    return walk_forward_store_dir(data_root) / "reviews"

def walk_forward_inputs_dir(data_root: Path) -> Path:
    return walk_forward_store_dir(data_root) / "inputs"

def window_policies_dir(data_root: Path) -> Path:
    return walk_forward_store_dir(data_root) / "window_policies"

def folds_dir(data_root: Path) -> Path:
    return walk_forward_store_dir(data_root) / "folds"

def fold_replay_configs_dir(data_root: Path) -> Path:
    return walk_forward_store_dir(data_root) / "fold_replay_configs"

def fold_replay_results_dir(data_root: Path) -> Path:
    return walk_forward_store_dir(data_root) / "fold_replay_results"

def fold_metrics_dir(data_root: Path) -> Path:
    return walk_forward_store_dir(data_root) / "fold_metrics"

def fold_benchmark_comparisons_dir(data_root: Path) -> Path:
    return walk_forward_store_dir(data_root) / "fold_benchmark_comparisons"

def oos_metrics_dir(data_root: Path) -> Path:
    return walk_forward_store_dir(data_root) / "oos_metrics"

def temporal_stability_dir(data_root: Path) -> Path:
    return walk_forward_store_dir(data_root) / "temporal_stability"

def degradation_diagnostics_dir(data_root: Path) -> Path:
    return walk_forward_store_dir(data_root) / "degradation_diagnostics"

def robustness_summaries_dir(data_root: Path) -> Path:
    return walk_forward_store_dir(data_root) / "robustness_summaries"

def validation_reports_dir(data_root: Path) -> Path:
    return walk_forward_store_dir(data_root) / "validation_reports"

def temporal_audits_dir(data_root: Path) -> Path:
    return walk_forward_store_dir(data_root) / "temporal_audits"

def safety_boundaries_dir(data_root: Path) -> Path:
    return walk_forward_store_dir(data_root) / "safety_boundaries"

def phase151_gates_dir(data_root: Path) -> Path:
    return walk_forward_store_dir(data_root) / "phase151_gates"

def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

def write_walk_forward_context_json(path: Path, item: WalkForwardContext) -> Path:
    _ensure_dir(path.parent)
    with open(path, 'w') as f:
        json.dump(walk_forward_context_to_dict(item), f, indent=2)
    return path

def write_walk_forward_full_review_json(path: Path, item: WalkForwardFullReview) -> Path:
    _ensure_dir(path.parent)
    with open(path, 'w') as f:
        json.dump(walk_forward_full_review_to_dict(item), f, indent=2)
    return path

def write_walk_forward_input_refs_jsonl(path: Path, items: List[WalkForwardInputReference]) -> Path:
    _ensure_dir(path.parent)
    with open(path, 'w') as f:
        for it in items:
            f.write(json.dumps(walk_forward_input_reference_to_dict(it)) + '\n')
    return path

def write_window_policy_json(path: Path, item: WalkForwardWindowPolicy) -> Path:
    _ensure_dir(path.parent)
    with open(path, 'w') as f:
        json.dump(walk_forward_window_policy_to_dict(item), f, indent=2)
    return path

def write_folds_jsonl(path: Path, items: List[WalkForwardFold]) -> Path:
    _ensure_dir(path.parent)
    with open(path, 'w') as f:
        for it in items:
            f.write(json.dumps(walk_forward_fold_to_dict(it)) + '\n')
    return path

def write_fold_replay_configs_jsonl(path: Path, items: List[FoldReplayConfig]) -> Path:
    _ensure_dir(path.parent)
    with open(path, 'w') as f:
        for it in items:
            f.write(json.dumps(fold_replay_config_to_dict(it)) + '\n')
    return path

def write_fold_replay_results_jsonl(path: Path, items: List[FoldReplayResult]) -> Path:
    _ensure_dir(path.parent)
    with open(path, 'w') as f:
        for it in items:
            f.write(json.dumps(fold_replay_result_to_dict(it)) + '\n')
    return path

def write_fold_metrics_jsonl(path: Path, items: List[FoldPerformanceMetric]) -> Path:
    _ensure_dir(path.parent)
    with open(path, 'w') as f:
        for it in items:
            f.write(json.dumps(fold_performance_metric_to_dict(it)) + '\n')
    return path

def write_fold_benchmark_comparisons_jsonl(path: Path, items: List[FoldBenchmarkComparison]) -> Path:
    _ensure_dir(path.parent)
    with open(path, 'w') as f:
        for it in items:
            f.write(json.dumps(fold_benchmark_comparison_to_dict(it)) + '\n')
    return path

def write_oos_robustness_metrics_json(path: Path, item: OOSRobustnessMetrics) -> Path:
    _ensure_dir(path.parent)
    with open(path, 'w') as f:
        json.dump(oos_robustness_metrics_to_dict(item), f, indent=2)
    return path

def write_temporal_stability_metrics_jsonl(path: Path, items: List[TemporalStabilityMetric]) -> Path:
    _ensure_dir(path.parent)
    with open(path, 'w') as f:
        for it in items:
            f.write(json.dumps(temporal_stability_metric_to_dict(it)) + '\n')
    return path

def write_degradation_diagnostics_jsonl(path: Path, items: List[DegradationDiagnostic]) -> Path:
    _ensure_dir(path.parent)
    with open(path, 'w') as f:
        for it in items:
            f.write(json.dumps(degradation_diagnostic_to_dict(it)) + '\n')
    return path

def write_robustness_summary_json(path: Path, item: RobustnessSummary) -> Path:
    _ensure_dir(path.parent)
    with open(path, 'w') as f:
        json.dump(robustness_summary_to_dict(item), f, indent=2)
    return path

def write_walk_forward_validation_report_json(path: Path, item: WalkForwardValidationReport) -> Path:
    _ensure_dir(path.parent)
    with open(path, 'w') as f:
        json.dump(walk_forward_validation_report_to_dict(item), f, indent=2)
    return path

def write_temporal_stability_audit_json(path: Path, item: TemporalStabilityAuditReport) -> Path:
    _ensure_dir(path.parent)
    with open(path, 'w') as f:
        json.dump(temporal_stability_audit_report_to_dict(item), f, indent=2)
    return path

def write_walk_forward_safety_boundary_json(path: Path, item: WalkForwardSafetyBoundaryResult) -> Path:
    _ensure_dir(path.parent)
    with open(path, 'w') as f:
        json.dump(walk_forward_safety_boundary_result_to_dict(item), f, indent=2)
    return path

def write_phase151_readiness_gate_json(path: Path, item: Phase151ReadinessGate) -> Path:
    _ensure_dir(path.parent)
    with open(path, 'w') as f:
        json.dump(phase151_readiness_gate_to_dict(item), f, indent=2)
    return path

def read_walk_forward_full_review_json(path: Path) -> Dict[str, Any]:
    with open(path, 'r') as f:
        return json.load(f)

def list_walk_forward_reviews(data_root: Path) -> List[Path]:
    rev_dir = walk_forward_reviews_dir(data_root)
    if not rev_dir.exists():
        return []
    return list(rev_dir.glob("*.json"))

def get_latest_walk_forward_review(data_root: Path) -> Optional[Path]:
    files = list_walk_forward_reviews(data_root)
    if not files:
        return None
    return max(files, key=lambda f: f.stat().st_mtime)

def walk_forward_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "reviews": len(list_walk_forward_reviews(data_root)),
        "contexts": len(list(walk_forward_contexts_dir(data_root).glob("*.json"))) if walk_forward_contexts_dir(data_root).exists() else 0
    }
