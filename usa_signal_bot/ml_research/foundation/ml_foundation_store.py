from typing import Any, Dict, List, Optional
from pathlib import Path
import json
import dataclasses
from .phase136_models import (
    MLFoundationContext, MLFoundationFullReview, MLSourceRegistry,
    MLFeatureContract, MLTargetContract, MLLabelContract, MLDatasetContract,
    MLLeakageGuardResult, MLNonActivationBoundaryResult, MLResearchGovernanceResult,
    MLFoundationReadinessGate
)
from ...core.exceptions import MLFoundationStoreError

# Custom JSON encoder to handle dataclasses and enums
class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        elif hasattr(o, "value"):
            return o.value
        return super().default(o)

def ml_foundation_store_dir(data_root: Path) -> Path:
    p = data_root / "ml_research" / "foundation"
    p.mkdir(parents=True, exist_ok=True)
    return p

def ml_foundation_contexts_dir(data_root: Path) -> Path:
    p = ml_foundation_store_dir(data_root) / "contexts"
    p.mkdir(exist_ok=True)
    return p

def ml_foundation_reviews_dir(data_root: Path) -> Path:
    p = ml_foundation_store_dir(data_root) / "reviews"
    p.mkdir(exist_ok=True)
    return p

def ml_source_registries_dir(data_root: Path) -> Path:
    p = ml_foundation_store_dir(data_root) / "source_registries"
    p.mkdir(exist_ok=True)
    return p

def ml_feature_contracts_dir(data_root: Path) -> Path:
    p = ml_foundation_store_dir(data_root) / "feature_contracts"
    p.mkdir(exist_ok=True)
    return p

def ml_target_contracts_dir(data_root: Path) -> Path:
    p = ml_foundation_store_dir(data_root) / "target_contracts"
    p.mkdir(exist_ok=True)
    return p

def ml_label_contracts_dir(data_root: Path) -> Path:
    p = ml_foundation_store_dir(data_root) / "label_contracts"
    p.mkdir(exist_ok=True)
    return p

def ml_dataset_contracts_dir(data_root: Path) -> Path:
    p = ml_foundation_store_dir(data_root) / "dataset_contracts"
    p.mkdir(exist_ok=True)
    return p

def ml_leakage_guards_dir(data_root: Path) -> Path:
    p = ml_foundation_store_dir(data_root) / "leakage_guards"
    p.mkdir(exist_ok=True)
    return p

def ml_non_activation_boundaries_dir(data_root: Path) -> Path:
    p = ml_foundation_store_dir(data_root) / "non_activation_boundaries"
    p.mkdir(exist_ok=True)
    return p

def ml_governance_dir(data_root: Path) -> Path:
    p = ml_foundation_store_dir(data_root) / "governance"
    p.mkdir(exist_ok=True)
    return p

def ml_readiness_gates_dir(data_root: Path) -> Path:
    p = ml_foundation_store_dir(data_root) / "readiness_gates"
    p.mkdir(exist_ok=True)
    return p

def _write_json(path: Path, obj: Any) -> Path:
    with open(path, "w") as f:
        json.dump(obj, f, cls=EnhancedJSONEncoder, indent=2)
    return path

def write_ml_foundation_context_json(path: Path, item: MLFoundationContext) -> Path:
    return _write_json(path, item)

def write_ml_foundation_full_review_json(path: Path, item: MLFoundationFullReview) -> Path:
    return _write_json(path, item)

def write_ml_source_registry_json(path: Path, item: MLSourceRegistry) -> Path:
    return _write_json(path, item)

def write_ml_feature_contracts_jsonl(path: Path, items: List[MLFeatureContract]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(item, cls=EnhancedJSONEncoder) + "\n")
    return path

def write_ml_target_contracts_jsonl(path: Path, items: List[MLTargetContract]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(item, cls=EnhancedJSONEncoder) + "\n")
    return path

def write_ml_label_contracts_jsonl(path: Path, items: List[MLLabelContract]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(item, cls=EnhancedJSONEncoder) + "\n")
    return path

def write_ml_dataset_contract_json(path: Path, item: MLDatasetContract) -> Path:
    return _write_json(path, item)

def write_ml_leakage_guard_json(path: Path, item: MLLeakageGuardResult) -> Path:
    return _write_json(path, item)

def write_ml_non_activation_boundary_json(path: Path, item: MLNonActivationBoundaryResult) -> Path:
    return _write_json(path, item)

def write_ml_research_governance_json(path: Path, item: MLResearchGovernanceResult) -> Path:
    return _write_json(path, item)

def write_ml_foundation_readiness_gate_json(path: Path, item: MLFoundationReadinessGate) -> Path:
    return _write_json(path, item)

def read_ml_foundation_full_review_json(path: Path) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_ml_foundation_reviews(data_root: Path) -> List[Path]:
    d = ml_foundation_reviews_dir(data_root)
    return sorted(list(d.glob("*.json")))

def get_latest_ml_foundation_review(data_root: Path) -> Optional[Path]:
    reviews = list_ml_foundation_reviews(data_root)
    if reviews:
        return reviews[-1]
    return None

def ml_foundation_store_summary(data_root: Path) -> Dict[str, Any]:
    return {"reviews_count": len(list_ml_foundation_reviews(data_root))}
