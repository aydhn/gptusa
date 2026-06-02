import json
from pathlib import Path
from typing import Any
import dataclasses

from usa_signal_bot.ml_research.ml_governance_closure.phase145_models import (
    AdvancedMLClosureContext,
    AdvancedMLClosureFullReview,
    ExplainabilityInputReference,
    FeatureAttributionProxy,
    FactorContributionSummary,
    ModelBehaviorExplanation,
    ExplainabilityReport,
    AdvancedMLArtifactLineage,
    MLGovernanceClosureResult,
    AdvancedMLFinalAuditResult,
    NonActivationMLClosureBoundaryResult,
    FinalMLModelCardClosure,
    AdvancedMLAcceptanceGate
)
from usa_signal_bot.core.exceptions import MLGovernanceClosureStoreError

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)
        if hasattr(obj, "value"):
            return obj.value
        return super().default(obj)

def _write_json(path: Path, data: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, cls=CustomJSONEncoder, indent=2)
    return path

def _write_jsonl(path: Path, items: list[Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(item, cls=CustomJSONEncoder) + "\n")
    return path

def ml_governance_closure_store_dir(data_root: Path) -> Path:
    return data_root / "ml_research" / "ml_governance_closure"

def ml_governance_closure_contexts_dir(data_root: Path) -> Path:
    return ml_governance_closure_store_dir(data_root) / "contexts"

def ml_governance_closure_reviews_dir(data_root: Path) -> Path:
    return ml_governance_closure_store_dir(data_root) / "reviews"

def explainability_inputs_dir(data_root: Path) -> Path:
    return ml_governance_closure_store_dir(data_root) / "explainability_inputs"

def feature_attribution_dir(data_root: Path) -> Path:
    return ml_governance_closure_store_dir(data_root) / "feature_attribution"

def factor_contribution_dir(data_root: Path) -> Path:
    return ml_governance_closure_store_dir(data_root) / "factor_contribution"

def model_behavior_explanations_dir(data_root: Path) -> Path:
    return ml_governance_closure_store_dir(data_root) / "model_behavior"

def explainability_reports_dir(data_root: Path) -> Path:
    return ml_governance_closure_store_dir(data_root) / "explainability_reports"

def artifact_lineage_dir(data_root: Path) -> Path:
    return ml_governance_closure_store_dir(data_root) / "artifact_lineage"

def governance_closure_dir(data_root: Path) -> Path:
    return ml_governance_closure_store_dir(data_root) / "governance_closure"

def final_audit_dir(data_root: Path) -> Path:
    return ml_governance_closure_store_dir(data_root) / "final_audit"

def non_activation_boundaries_dir(data_root: Path) -> Path:
    return ml_governance_closure_store_dir(data_root) / "non_activation_boundaries"

def final_model_card_closures_dir(data_root: Path) -> Path:
    return ml_governance_closure_store_dir(data_root) / "final_model_cards"

def acceptance_gates_dir(data_root: Path) -> Path:
    return ml_governance_closure_store_dir(data_root) / "acceptance_gates"

def write_advanced_ml_closure_context_json(path: Path, item: AdvancedMLClosureContext) -> Path:
    return _write_json(path, item)

def write_advanced_ml_closure_full_review_json(path: Path, item: AdvancedMLClosureFullReview) -> Path:
    return _write_json(path, item)

def write_explainability_input_refs_jsonl(path: Path, items: list[ExplainabilityInputReference]) -> Path:
    return _write_jsonl(path, items)

def write_feature_attributions_jsonl(path: Path, items: list[FeatureAttributionProxy]) -> Path:
    return _write_jsonl(path, items)

def write_factor_contribution_summaries_jsonl(path: Path, items: list[FactorContributionSummary]) -> Path:
    return _write_jsonl(path, items)

def write_model_behavior_explanations_jsonl(path: Path, items: list[ModelBehaviorExplanation]) -> Path:
    return _write_jsonl(path, items)

def write_explainability_report_json(path: Path, item: ExplainabilityReport) -> Path:
    return _write_json(path, item)

def write_artifact_lineage_json(path: Path, item: AdvancedMLArtifactLineage) -> Path:
    return _write_json(path, item)

def write_ml_governance_closure_json(path: Path, item: MLGovernanceClosureResult) -> Path:
    return _write_json(path, item)

def write_advanced_ml_final_audit_json(path: Path, item: AdvancedMLFinalAuditResult) -> Path:
    return _write_json(path, item)

def write_non_activation_ml_closure_boundary_json(path: Path, item: NonActivationMLClosureBoundaryResult) -> Path:
    return _write_json(path, item)

def write_final_ml_model_card_closure_json(path: Path, item: FinalMLModelCardClosure) -> Path:
    return _write_json(path, item)

def write_advanced_ml_acceptance_gate_json(path: Path, item: AdvancedMLAcceptanceGate) -> Path:
    return _write_json(path, item)

def read_advanced_ml_closure_full_review_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise MLGovernanceClosureStoreError(f"File not found: {path}")
    with open(path, "r") as f:
        return json.load(f)

def list_advanced_ml_closure_reviews(data_root: Path) -> list[Path]:
    rev_dir = ml_governance_closure_reviews_dir(data_root)
    if not rev_dir.exists():
        return []
    return list(rev_dir.glob("*.json"))

def get_latest_advanced_ml_closure_review(data_root: Path) -> Path | None:
    files = list_advanced_ml_closure_reviews(data_root)
    if not files:
        return None
    return max(files, key=lambda p: p.stat().st_mtime)

def ml_governance_closure_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "store_dir": str(ml_governance_closure_store_dir(data_root)),
        "review_count": len(list_advanced_ml_closure_reviews(data_root))
    }
