import json
from pathlib import Path
from typing import Any, Dict, List

from usa_signal_bot.ml_research.ensemble_evaluation.phase143_models import (
    EnsemblePrototypeContext,
    EnsemblePrototypeFullReview,
    EnsemblePrototypeInputReference,
    EnsemblePrototypeSpec,
    OfflineEnsemblePredictionArtifact,
    BlendContributionDiagnostic,
    CandidateAgreementDiagnostic,
    EnsembleCandidateComparisonResult,
    OfflineEnsembleEvaluationReport,
    NonActivationEnsembleRegistry,
    EnsembleModelCardUpdate,
    EnsemblePrototypeBoundaryResult,
    EnsemblePrototypeReadinessGate
)
from usa_signal_bot.ml_research.ensemble_evaluation.phase143_models import (
    EnsemblePrototypeStatus, EnsemblePrototypeDecision, EnsemblePrototypeKind, OfflineEnsemblePredictionKind, BlendDiagnosticKind, CandidateAgreementKind, EnsembleCandidateComparisonKind, OfflineEnsembleEvaluationMetricKind, OfflineEnsembleEvaluationStatus, NonActivationEnsembleRegistryStatus, EnsembleRegistryEntryStatus, EnsemblePrototypeBoundaryRuleKind, EnsemblePrototypeReadinessStatus, EnsemblePrototypeReadinessRuleKind, EnsemblePrototypeQuality, EnsemblePrototypeRiskFlag, EnsemblePrototypeReportType
)

def _to_dict_recursive(obj):
    if hasattr(obj, "__dataclass_fields__"):
        res = {}
        for k in obj.__dataclass_fields__:
            val = getattr(obj, k)
            if hasattr(val, "value"): # Enum
                res[k] = val.value
            elif isinstance(val, list):
                res[k] = [_to_dict_recursive(i) for i in val]
            elif hasattr(val, "__dataclass_fields__"):
                res[k] = _to_dict_recursive(val)
            else:
                res[k] = val
        return res
    return obj

def ensemble_prototype_store_dir(data_root: Path) -> Path: return data_root / "ml_research" / "ensemble_evaluation"
def ensemble_prototype_contexts_dir(data_root: Path) -> Path: return ensemble_prototype_store_dir(data_root) / "contexts"
def ensemble_prototype_reviews_dir(data_root: Path) -> Path: return ensemble_prototype_store_dir(data_root) / "reviews"
def ensemble_prototype_inputs_dir(data_root: Path) -> Path: return ensemble_prototype_store_dir(data_root) / "inputs"
def ensemble_prototype_specs_dir(data_root: Path) -> Path: return ensemble_prototype_store_dir(data_root) / "prototype_specs"
def offline_ensemble_predictions_dir(data_root: Path) -> Path: return ensemble_prototype_store_dir(data_root) / "offline_predictions"
def blend_diagnostics_dir(data_root: Path) -> Path: return ensemble_prototype_store_dir(data_root) / "blend_diagnostics"
def candidate_agreement_dir(data_root: Path) -> Path: return ensemble_prototype_store_dir(data_root) / "candidate_agreement"
def ensemble_candidate_comparisons_dir(data_root: Path) -> Path: return ensemble_prototype_store_dir(data_root) / "candidate_comparisons"
def offline_ensemble_evaluation_reports_dir(data_root: Path) -> Path: return ensemble_prototype_store_dir(data_root) / "evaluation_reports"
def non_activation_ensemble_registries_dir(data_root: Path) -> Path: return ensemble_prototype_store_dir(data_root) / "registries"
def ensemble_model_card_updates_dir(data_root: Path) -> Path: return ensemble_prototype_store_dir(data_root) / "model_card_updates"
def ensemble_prototype_boundaries_dir(data_root: Path) -> Path: return ensemble_prototype_store_dir(data_root) / "boundaries"
def ensemble_prototype_gates_dir(data_root: Path) -> Path: return ensemble_prototype_store_dir(data_root) / "readiness_gates"

def _write_json(path: Path, item: Any):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(_to_dict_recursive(item), f, indent=2)
    return path

def _write_jsonl(path: Path, items: List[Any]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for i in items:
            f.write(json.dumps(_to_dict_recursive(i)) + "\n")
    return path

def write_ensemble_prototype_context_json(path: Path, item: EnsemblePrototypeContext) -> Path: return _write_json(path, item)
def write_ensemble_prototype_full_review_json(path: Path, item: EnsemblePrototypeFullReview) -> Path: return _write_json(path, item)
def write_ensemble_prototype_input_refs_jsonl(path: Path, items: List[EnsemblePrototypeInputReference]) -> Path: return _write_jsonl(path, items)
def write_ensemble_prototype_specs_jsonl(path: Path, items: List[EnsemblePrototypeSpec]) -> Path: return _write_jsonl(path, items)
def write_offline_ensemble_prediction_artifacts_jsonl(path: Path, items: List[OfflineEnsemblePredictionArtifact]) -> Path: return _write_jsonl(path, items)
def write_blend_diagnostics_jsonl(path: Path, items: List[BlendContributionDiagnostic]) -> Path: return _write_jsonl(path, items)
def write_candidate_agreement_diagnostics_jsonl(path: Path, items: List[CandidateAgreementDiagnostic]) -> Path: return _write_jsonl(path, items)
def write_ensemble_candidate_comparisons_jsonl(path: Path, items: List[EnsembleCandidateComparisonResult]) -> Path: return _write_jsonl(path, items)
def write_offline_ensemble_evaluation_reports_jsonl(path: Path, items: List[OfflineEnsembleEvaluationReport]) -> Path: return _write_jsonl(path, items)
def write_non_activation_ensemble_registry_json(path: Path, item: NonActivationEnsembleRegistry) -> Path: return _write_json(path, item)
def write_ensemble_model_card_updates_jsonl(path: Path, items: List[EnsembleModelCardUpdate]) -> Path: return _write_jsonl(path, items)
def write_ensemble_prototype_boundary_json(path: Path, item: EnsemblePrototypeBoundaryResult) -> Path: return _write_json(path, item)
def write_ensemble_prototype_readiness_gate_json(path: Path, item: EnsemblePrototypeReadinessGate) -> Path: return _write_json(path, item)

def read_ensemble_prototype_full_review_json(path: Path) -> Dict[str, Any]:
    if not path.exists(): return {}
    with open(path, "r") as f:
        return json.load(f)

def list_ensemble_prototype_reviews(data_root: Path) -> List[Path]:
    d = ensemble_prototype_reviews_dir(data_root)
    if not d.exists(): return []
    return list(d.glob("*.json"))

def get_latest_ensemble_prototype_review(data_root: Path) -> Path | None:
    l = list_ensemble_prototype_reviews(data_root)
    if not l: return None
    return sorted(l, key=lambda p: p.stat().st_mtime)[-1]

def ensemble_prototype_store_summary(data_root: Path) -> Dict[str, Any]:
    return {"review_count": len(list_ensemble_prototype_reviews(data_root))}
