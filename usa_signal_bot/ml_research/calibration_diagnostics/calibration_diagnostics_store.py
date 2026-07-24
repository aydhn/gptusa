import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from usa_signal_bot.ml_research.calibration_diagnostics.phase141_models import (
    CalibrationDiagnosticsContext,
    CalibrationDiagnosticsFullReview,
    CalibrationCandidateReference,
    CalibrationInputProfile,
    ReliabilityBinResult,
    CalibrationMetricResult,
    BrierDecompositionResult,
    ScoreDistributionDiagnostic,
    ClassBalanceDiagnostic,
    CalibrationDiagnosticsReport,
    PostTrainingValidationResult,
    CalibrationGovernanceResult,
    ModelCardCalibrationUpdate,
    CalibrationReadinessGate,
    calibration_diagnostics_context_to_dict,
    calibration_diagnostics_full_review_to_dict,
    calibration_candidate_reference_to_dict,
    calibration_input_profile_to_dict,
    reliability_bin_result_to_dict,
    calibration_metric_result_to_dict,
    brier_decomposition_result_to_dict,
    score_distribution_diagnostic_to_dict,
    class_balance_diagnostic_to_dict,
    calibration_diagnostics_report_to_dict,
    post_training_validation_result_to_dict,
    calibration_governance_result_to_dict,
    model_card_calibration_update_to_dict,
    calibration_readiness_gate_to_dict
)

def calibration_diagnostics_store_dir(data_root: Path) -> Path: return data_root / "ml_research" / "calibration_diagnostics"
def calibration_diagnostics_contexts_dir(data_root: Path) -> Path: return calibration_diagnostics_store_dir(data_root) / "contexts"
def calibration_diagnostics_reviews_dir(data_root: Path) -> Path: return calibration_diagnostics_store_dir(data_root) / "reviews"
def calibration_candidates_dir(data_root: Path) -> Path: return calibration_diagnostics_store_dir(data_root) / "candidates"
def calibration_input_profiles_dir(data_root: Path) -> Path: return calibration_diagnostics_store_dir(data_root) / "input_profiles"
def reliability_bins_dir(data_root: Path) -> Path: return calibration_diagnostics_store_dir(data_root) / "reliability_bins"
def calibration_metrics_dir(data_root: Path) -> Path: return calibration_diagnostics_store_dir(data_root) / "calibration_metrics"
def brier_decomposition_dir(data_root: Path) -> Path: return calibration_diagnostics_store_dir(data_root) / "brier_decomposition"
def score_distribution_dir(data_root: Path) -> Path: return calibration_diagnostics_store_dir(data_root) / "score_distribution"
def class_balance_dir(data_root: Path) -> Path: return calibration_diagnostics_store_dir(data_root) / "class_balance"
def diagnostics_reports_dir(data_root: Path) -> Path: return calibration_diagnostics_store_dir(data_root) / "reports"
def post_training_validations_dir(data_root: Path) -> Path: return calibration_diagnostics_store_dir(data_root) / "post_training_validation"
def calibration_governance_dir(data_root: Path) -> Path: return calibration_diagnostics_store_dir(data_root) / "governance"
def model_card_calibration_updates_dir(data_root: Path) -> Path: return calibration_diagnostics_store_dir(data_root) / "model_card_updates"
def calibration_readiness_gates_dir(data_root: Path) -> Path: return calibration_diagnostics_store_dir(data_root) / "readiness_gates"

def _ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)


def _write_jsonl_chunked(f, items, to_dict_func, chunk_size=1000):
    chunk = []
    for it in items:
        chunk.append(json.dumps(to_dict_func(it)))
        if len(chunk) >= chunk_size:
            f.write('\n'.join(chunk) + '\n')
            chunk.clear()
    if chunk:
        f.write('\n'.join(chunk) + '\n')

def write_calibration_diagnostics_context_json(path: Path, item: CalibrationDiagnosticsContext) -> Path:
    _ensure_dir(path.parent)
    with open(path, 'w') as f: json.dump(calibration_diagnostics_context_to_dict(item), f, indent=2)
    return path

def write_calibration_diagnostics_full_review_json(path: Path, item: CalibrationDiagnosticsFullReview) -> Path:
    _ensure_dir(path.parent)
    with open(path, 'w') as f: json.dump(calibration_diagnostics_full_review_to_dict(item), f, indent=2)
    return path

def write_calibration_candidates_jsonl(path: Path, items: List[CalibrationCandidateReference]) -> Path:
    _ensure_dir(path.parent)
    with open(path, 'w') as f:
        _write_jsonl_chunked(f, items, calibration_candidate_reference_to_dict)
    return path

def write_calibration_input_profiles_jsonl(path: Path, items: List[CalibrationInputProfile]) -> Path:
    _ensure_dir(path.parent)
    with open(path, 'w') as f:
        _write_jsonl_chunked(f, items, calibration_input_profile_to_dict)
    return path

def write_reliability_bins_jsonl(path: Path, items: List[ReliabilityBinResult]) -> Path:
    _ensure_dir(path.parent)
    with open(path, 'w') as f:
        _write_jsonl_chunked(f, items, reliability_bin_result_to_dict)
    return path

def write_calibration_metrics_jsonl(path: Path, items: List[CalibrationMetricResult]) -> Path:
    _ensure_dir(path.parent)
    with open(path, 'w') as f:
        _write_jsonl_chunked(f, items, calibration_metric_result_to_dict)
    return path

def write_brier_decomposition_json(path: Path, item: BrierDecompositionResult) -> Path:
    _ensure_dir(path.parent)
    with open(path, 'w') as f: json.dump(brier_decomposition_result_to_dict(item), f, indent=2)
    return path

def write_score_distribution_jsonl(path: Path, items: List[ScoreDistributionDiagnostic]) -> Path:
    _ensure_dir(path.parent)
    with open(path, 'w') as f:
        _write_jsonl_chunked(f, items, score_distribution_diagnostic_to_dict)
    return path

def write_class_balance_jsonl(path: Path, items: List[ClassBalanceDiagnostic]) -> Path:
    _ensure_dir(path.parent)
    with open(path, 'w') as f:
        _write_jsonl_chunked(f, items, class_balance_diagnostic_to_dict)
    return path

def write_calibration_diagnostics_reports_jsonl(path: Path, items: List[CalibrationDiagnosticsReport]) -> Path:
    _ensure_dir(path.parent)
    with open(path, 'w') as f:
        _write_jsonl_chunked(f, items, calibration_diagnostics_report_to_dict)
    return path

def write_post_training_validations_jsonl(path: Path, items: List[PostTrainingValidationResult]) -> Path:
    _ensure_dir(path.parent)
    with open(path, 'w') as f:
        _write_jsonl_chunked(f, items, post_training_validation_result_to_dict)
    return path

def write_calibration_governance_json(path: Path, item: CalibrationGovernanceResult) -> Path:
    _ensure_dir(path.parent)
    with open(path, 'w') as f: json.dump(calibration_governance_result_to_dict(item), f, indent=2)
    return path

def write_model_card_calibration_updates_jsonl(path: Path, items: List[ModelCardCalibrationUpdate]) -> Path:
    _ensure_dir(path.parent)
    with open(path, 'w') as f:
        _write_jsonl_chunked(f, items, model_card_calibration_update_to_dict)
    return path

def write_calibration_readiness_gate_json(path: Path, item: CalibrationReadinessGate) -> Path:
    _ensure_dir(path.parent)
    with open(path, 'w') as f: json.dump(calibration_readiness_gate_to_dict(item), f, indent=2)
    return path

def read_calibration_diagnostics_full_review_json(path: Path) -> Dict[str, Any]:
    with open(path, 'r') as f: return json.load(f)

def list_calibration_diagnostics_reviews(data_root: Path) -> List[Path]:
    rev_dir = calibration_diagnostics_reviews_dir(data_root)
    if not rev_dir.exists(): return []
    return sorted(list(rev_dir.glob("*.json")))

def get_latest_calibration_diagnostics_review(data_root: Path) -> Optional[Path]:
    revs = list_calibration_diagnostics_reviews(data_root)
    return revs[-1] if revs else None

def calibration_diagnostics_store_summary(data_root: Path) -> Dict[str, Any]:
    return {"reviews": len(list_calibration_diagnostics_reviews(data_root))}
