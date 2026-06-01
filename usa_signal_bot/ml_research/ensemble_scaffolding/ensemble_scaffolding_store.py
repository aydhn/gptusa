from typing import Any, Dict, List, Optional
from pathlib import Path
import json
from .phase142_models import *

def ensemble_scaffolding_store_dir(data_root: Path) -> Path: return data_root / "ml_research" / "ensemble_scaffolding"
def ensemble_scaffolding_contexts_dir(data_root: Path) -> Path: return ensemble_scaffolding_store_dir(data_root) / "contexts"
def ensemble_scaffolding_reviews_dir(data_root: Path) -> Path: return ensemble_scaffolding_store_dir(data_root) / "reviews"
def ensemble_candidates_dir(data_root: Path) -> Path: return ensemble_scaffolding_store_dir(data_root) / "candidates"
def ensemble_family_specs_dir(data_root: Path) -> Path: return ensemble_scaffolding_store_dir(data_root) / "family_specs"
def candidate_groups_dir(data_root: Path) -> Path: return ensemble_scaffolding_store_dir(data_root) / "candidate_groups"
def blend_policies_dir(data_root: Path) -> Path: return ensemble_scaffolding_store_dir(data_root) / "blend_policies"
def blend_plans_dir(data_root: Path) -> Path: return ensemble_scaffolding_store_dir(data_root) / "blend_plans"
def prediction_correlations_dir(data_root: Path) -> Path: return ensemble_scaffolding_store_dir(data_root) / "prediction_correlations"
def diversity_profiles_dir(data_root: Path) -> Path: return ensemble_scaffolding_store_dir(data_root) / "diversity_profiles"
def complementarity_profiles_dir(data_root: Path) -> Path: return ensemble_scaffolding_store_dir(data_root) / "complementarity_profiles"
def calibration_aware_eligibility_dir(data_root: Path) -> Path: return ensemble_scaffolding_store_dir(data_root) / "calibration_aware_eligibility"
def ensemble_preparation_reports_dir(data_root: Path) -> Path: return ensemble_scaffolding_store_dir(data_root) / "preparation_reports"
def ensemble_governance_dir(data_root: Path) -> Path: return ensemble_scaffolding_store_dir(data_root) / "governance"
def non_activation_boundaries_dir(data_root: Path) -> Path: return ensemble_scaffolding_store_dir(data_root) / "non_activation_boundaries"
def model_card_ensemble_updates_dir(data_root: Path) -> Path: return ensemble_scaffolding_store_dir(data_root) / "model_card_updates"
def ensemble_readiness_gates_dir(data_root: Path) -> Path: return ensemble_scaffolding_store_dir(data_root) / "readiness_gates"

def _write_json(p: Path, obj: Any):
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w") as f:
        json.dump(obj, f, indent=2)

def _write_jsonl(p: Path, items: List[Any]):
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w") as f:
        for i in items:
            f.write(json.dumps(i) + "\n")

def write_ensemble_scaffolding_context_json(path: Path, item: EnsembleScaffoldingContext) -> Path:
    _write_json(path, ensemble_scaffolding_context_to_dict(item))
    return path

def write_ensemble_scaffolding_full_review_json(path: Path, item: EnsembleScaffoldingFullReview) -> Path:
    _write_json(path, ensemble_scaffolding_full_review_to_dict(item))
    return path

def write_ensemble_candidates_jsonl(path: Path, items: List[EnsembleCandidateReference]) -> Path:
    _write_jsonl(path, [ensemble_candidate_reference_to_dict(i) for i in items])
    return path

def write_ensemble_family_specs_jsonl(path: Path, items: List[EnsembleFamilySpec]) -> Path:
    _write_jsonl(path, [ensemble_family_spec_to_dict(i) for i in items])
    return path

def write_candidate_groups_jsonl(path: Path, items: List[CandidateGroupSpec]) -> Path:
    _write_jsonl(path, [candidate_group_spec_to_dict(i) for i in items])
    return path

def write_blend_policies_jsonl(path: Path, items: List[BlendPolicySpec]) -> Path:
    _write_jsonl(path, [blend_policy_spec_to_dict(i) for i in items])
    return path

def write_blend_plans_jsonl(path: Path, items: List[BlendCoefficientPlan]) -> Path:
    _write_jsonl(path, [blend_coefficient_plan_to_dict(i) for i in items])
    return path

def write_prediction_correlations_jsonl(path: Path, items: List[PredictionCorrelationDiagnostic]) -> Path:
    _write_jsonl(path, [prediction_correlation_diagnostic_to_dict(i) for i in items])
    return path

def write_diversity_profiles_jsonl(path: Path, items: List[CandidateDiversityProfile]) -> Path:
    _write_jsonl(path, [candidate_diversity_profile_to_dict(i) for i in items])
    return path

def write_complementarity_profiles_jsonl(path: Path, items: List[ComplementarityProfile]) -> Path:
    _write_jsonl(path, [complementarity_profile_to_dict(i) for i in items])
    return path

def write_calibration_aware_eligibility_jsonl(path: Path, items: List[CalibrationAwareEligibilityProfile]) -> Path:
    _write_jsonl(path, [calibration_aware_eligibility_profile_to_dict(i) for i in items])
    return path

def write_ensemble_preparation_reports_jsonl(path: Path, items: List[EnsemblePreparationReport]) -> Path:
    _write_jsonl(path, [ensemble_preparation_report_to_dict(i) for i in items])
    return path

def write_ensemble_governance_json(path: Path, item: EnsembleGovernanceResult) -> Path:
    _write_json(path, ensemble_governance_result_to_dict(item))
    return path

def write_non_activation_ensemble_boundary_json(path: Path, item: NonActivationEnsembleBoundaryResult) -> Path:
    _write_json(path, non_activation_ensemble_boundary_result_to_dict(item))
    return path

def write_model_card_ensemble_updates_jsonl(path: Path, items: List[ModelCardEnsembleUpdate]) -> Path:
    _write_jsonl(path, [model_card_ensemble_update_to_dict(i) for i in items])
    return path

def write_ensemble_readiness_gate_json(path: Path, item: EnsembleReadinessGate) -> Path:
    _write_json(path, ensemble_readiness_gate_to_dict(item))
    return path

def read_ensemble_scaffolding_full_review_json(path: Path) -> Dict[str, Any]:
    if not path.exists(): return {}
    with open(path, "r") as f:
        return json.load(f)

def list_ensemble_scaffolding_reviews(data_root: Path) -> List[Path]:
    d = ensemble_scaffolding_reviews_dir(data_root)
    if not d.exists(): return []
    return list(d.glob("*.json"))

def get_latest_ensemble_scaffolding_review(data_root: Path) -> Optional[Path]:
    lst = list_ensemble_scaffolding_reviews(data_root)
    if not lst: return None
    return sorted(lst)[-1]

def ensemble_scaffolding_store_summary(data_root: Path) -> Dict[str, Any]:
    return {"reviews": len(list_ensemble_scaffolding_reviews(data_root))}
