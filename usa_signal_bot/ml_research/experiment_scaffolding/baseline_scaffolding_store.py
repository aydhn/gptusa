import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from usa_signal_bot.ml_research.experiment_scaffolding.phase138_models import (
    BaselineMLScaffoldingContext,
    BaselineMLScaffoldingFullReview,
    BaselineExperimentSpec,
    BaselineModelFamilySpec,
    EvaluationMetricSpec,
    EvaluationHarnessContract,
    PredictionOutputBoundary,
    ModelCardDraft,
    BaselineExperimentRegistry,
    NonActivationEvaluationBoundaryResult,
    BaselineExperimentReadinessGate
)

def baseline_scaffolding_store_dir(data_root: Path) -> Path:
    p = data_root / "ml_research" / "experiment_scaffolding"
    p.mkdir(parents=True, exist_ok=True)
    return p

def _make_subdir(data_root: Path, name: str) -> Path:
    p = baseline_scaffolding_store_dir(data_root) / name
    p.mkdir(parents=True, exist_ok=True)
    return p

def baseline_scaffolding_contexts_dir(data_root: Path) -> Path: return _make_subdir(data_root, "contexts")
def baseline_scaffolding_reviews_dir(data_root: Path) -> Path: return _make_subdir(data_root, "reviews")
def baseline_experiment_specs_dir(data_root: Path) -> Path: return _make_subdir(data_root, "experiment_specs")
def baseline_model_family_specs_dir(data_root: Path) -> Path: return _make_subdir(data_root, "model_family_specs")
def evaluation_metric_specs_dir(data_root: Path) -> Path: return _make_subdir(data_root, "metric_specs")
def evaluation_harness_contracts_dir(data_root: Path) -> Path: return _make_subdir(data_root, "evaluation_harness")
def prediction_output_boundaries_dir(data_root: Path) -> Path: return _make_subdir(data_root, "prediction_boundaries")
def model_card_drafts_dir(data_root: Path) -> Path: return _make_subdir(data_root, "model_cards")
def experiment_registries_dir(data_root: Path) -> Path: return _make_subdir(data_root, "experiment_registries")
def non_activation_boundaries_dir(data_root: Path) -> Path: return _make_subdir(data_root, "non_activation_boundaries")
def baseline_readiness_gates_dir(data_root: Path) -> Path: return _make_subdir(data_root, "readiness_gates")

def write_baseline_scaffolding_context_json(path: Path, item: BaselineMLScaffoldingContext) -> Path:
    path.write_text(json.dumps(item.to_dict(), indent=2))
    return path

def write_baseline_scaffolding_full_review_json(path: Path, item: BaselineMLScaffoldingFullReview) -> Path:
    path.write_text(json.dumps(item.to_dict(), indent=2))
    return path

def write_baseline_experiment_specs_jsonl(path: Path, items: List[BaselineExperimentSpec]) -> Path:
    lines = [json.dumps(i.to_dict()) for i in items]
    path.write_text("\n".join(lines))
    return path

def write_baseline_model_family_specs_jsonl(path: Path, items: List[BaselineModelFamilySpec]) -> Path:
    lines = [json.dumps(i.to_dict()) for i in items]
    path.write_text("\n".join(lines))
    return path

def write_evaluation_metric_specs_jsonl(path: Path, items: List[EvaluationMetricSpec]) -> Path:
    lines = [json.dumps(i.to_dict()) for i in items]
    path.write_text("\n".join(lines))
    return path

def write_evaluation_harness_contract_json(path: Path, item: EvaluationHarnessContract) -> Path:
    path.write_text(json.dumps(item.to_dict(), indent=2))
    return path

def write_prediction_output_boundary_json(path: Path, item: PredictionOutputBoundary) -> Path:
    path.write_text(json.dumps(item.to_dict(), indent=2))
    return path

def write_model_card_drafts_jsonl(path: Path, items: List[ModelCardDraft]) -> Path:
    lines = [json.dumps(i.to_dict()) for i in items]
    path.write_text("\n".join(lines))
    return path

def write_model_card_markdown(path: Path, item: ModelCardDraft, overwrite: bool = False) -> Path:
    if not overwrite and path.exists():
        return path
    path.write_text(item.rendered_markdown or "")
    return path

def write_experiment_registry_json(path: Path, item: BaselineExperimentRegistry) -> Path:
    path.write_text(json.dumps(item.to_dict(), indent=2))
    return path

def write_non_activation_evaluation_boundary_json(path: Path, item: NonActivationEvaluationBoundaryResult) -> Path:
    path.write_text(json.dumps(item.to_dict(), indent=2))
    return path

def write_baseline_experiment_readiness_gate_json(path: Path, item: BaselineExperimentReadinessGate) -> Path:
    path.write_text(json.dumps(item.to_dict(), indent=2))
    return path

def read_baseline_scaffolding_full_review_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}

def list_baseline_scaffolding_reviews(data_root: Path) -> List[Path]:
    d = baseline_scaffolding_reviews_dir(data_root)
    return list(d.glob("*.json"))

def get_latest_baseline_scaffolding_review(data_root: Path) -> Optional[Path]:
    paths = list_baseline_scaffolding_reviews(data_root)
    if not paths:
        return None
    paths.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return paths[0]

def baseline_scaffolding_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "reviews_count": len(list_baseline_scaffolding_reviews(data_root))
    }
