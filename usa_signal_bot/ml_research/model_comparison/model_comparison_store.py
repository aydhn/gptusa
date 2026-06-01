from pathlib import Path
import json
from typing import Any, List

from usa_signal_bot.ml_research.model_comparison.phase140_models import (
    BaselineModelComparisonContext,
    BaselineModelComparisonFullReview,
    ModelComparisonInputReference,
    MetricNormalizationResult,
    ModelComparisonScore,
    SplitAwareComparisonResult,
    RegimeAwareComparisonResult,
    ModelRankingTable,
    CandidateShortlist,
    CalibrationReadinessProfile,
    SelectionGovernanceResult,
    ModelCardComparisonUpdate,
    ModelComparisonReadinessGate,
    baseline_model_comparison_context_to_dict,
    baseline_model_comparison_full_review_to_dict,
    model_comparison_input_reference_to_dict,
    metric_normalization_result_to_dict,
    model_comparison_score_to_dict,
    split_aware_comparison_result_to_dict,
    regime_aware_comparison_result_to_dict,
    model_ranking_table_to_dict,
    candidate_shortlist_to_dict,
    calibration_readiness_profile_to_dict,
    selection_governance_result_to_dict,
    model_card_comparison_update_to_dict,
    model_comparison_readiness_gate_to_dict
)

def model_comparison_store_dir(data_root: Path) -> Path: return data_root / "ml_research" / "model_comparison"
def model_comparison_contexts_dir(data_root: Path) -> Path: return model_comparison_store_dir(data_root) / "contexts"
def model_comparison_reviews_dir(data_root: Path) -> Path: return model_comparison_store_dir(data_root) / "reviews"
def model_comparison_inputs_dir(data_root: Path) -> Path: return model_comparison_store_dir(data_root) / "inputs"
def metric_normalization_dir(data_root: Path) -> Path: return model_comparison_store_dir(data_root) / "metric_normalization"
def model_scores_dir(data_root: Path) -> Path: return model_comparison_store_dir(data_root) / "model_scores"
def split_comparisons_dir(data_root: Path) -> Path: return model_comparison_store_dir(data_root) / "split_comparisons"
def regime_comparisons_dir(data_root: Path) -> Path: return model_comparison_store_dir(data_root) / "regime_comparisons"
def rankings_dir(data_root: Path) -> Path: return model_comparison_store_dir(data_root) / "rankings"
def candidate_shortlists_dir(data_root: Path) -> Path: return model_comparison_store_dir(data_root) / "candidate_shortlists"
def calibration_preparation_dir(data_root: Path) -> Path: return model_comparison_store_dir(data_root) / "calibration_preparation"
def selection_governance_dir(data_root: Path) -> Path: return model_comparison_store_dir(data_root) / "selection_governance"
def model_card_comparison_updates_dir(data_root: Path) -> Path: return model_comparison_store_dir(data_root) / "model_card_updates"
def model_comparison_gates_dir(data_root: Path) -> Path: return model_comparison_store_dir(data_root) / "readiness_gates"

def _ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def write_model_comparison_context_json(path: Path, item: BaselineModelComparisonContext) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(baseline_model_comparison_context_to_dict(item), f, indent=2)
    return path

def write_model_comparison_full_review_json(path: Path, item: BaselineModelComparisonFullReview) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(baseline_model_comparison_full_review_to_dict(item), f, indent=2)
    return path

def write_model_comparison_input_refs_jsonl(path: Path, items: list[ModelComparisonInputReference]) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(model_comparison_input_reference_to_dict(it)) + "\n")
    return path

def write_metric_normalization_results_jsonl(path: Path, items: list[MetricNormalizationResult]) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(metric_normalization_result_to_dict(it)) + "\n")
    return path

def write_model_comparison_scores_jsonl(path: Path, items: list[ModelComparisonScore]) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(model_comparison_score_to_dict(it)) + "\n")
    return path

def write_split_aware_comparisons_jsonl(path: Path, items: list[SplitAwareComparisonResult]) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(split_aware_comparison_result_to_dict(it)) + "\n")
    return path

def write_regime_aware_comparisons_jsonl(path: Path, items: list[RegimeAwareComparisonResult]) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(regime_aware_comparison_result_to_dict(it)) + "\n")
    return path

def write_model_ranking_table_json(path: Path, item: ModelRankingTable) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(model_ranking_table_to_dict(item), f, indent=2)
    return path

def write_candidate_shortlist_json(path: Path, item: CandidateShortlist) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(candidate_shortlist_to_dict(item), f, indent=2)
    return path

def write_calibration_readiness_profiles_jsonl(path: Path, items: list[CalibrationReadinessProfile]) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(calibration_readiness_profile_to_dict(it)) + "\n")
    return path

def write_selection_governance_json(path: Path, item: SelectionGovernanceResult) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(selection_governance_result_to_dict(item), f, indent=2)
    return path

def write_model_card_comparison_updates_jsonl(path: Path, items: list[ModelCardComparisonUpdate]) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(model_card_comparison_update_to_dict(it)) + "\n")
    return path

def write_model_comparison_readiness_gate_json(path: Path, item: ModelComparisonReadinessGate) -> Path:
    _ensure_dir(path.parent)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(model_comparison_readiness_gate_to_dict(item), f, indent=2)
    return path

def read_model_comparison_full_review_json(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def list_model_comparison_reviews(data_root: Path) -> list[Path]:
    d = model_comparison_reviews_dir(data_root)
    if not d.exists():
        return []
    return sorted(d.glob("*.json"))

def get_latest_model_comparison_review(data_root: Path) -> Path | None:
    ls = list_model_comparison_reviews(data_root)
    return ls[-1] if ls else None

def model_comparison_store_summary(data_root: Path) -> dict[str, Any]:
    return {"reviews_count": len(list_model_comparison_reviews(data_root))}
