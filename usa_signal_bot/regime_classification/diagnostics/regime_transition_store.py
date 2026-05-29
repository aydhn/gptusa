import json
import dataclasses
from pathlib import Path
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.exceptions import RegimeTransitionStoreError
from usa_signal_bot.regime_classification.diagnostics.phase129_models import (
    RegimeTransitionContext,
    RegimeTransitionFullReview,
    RegimeTransitionMatrix,
    RegimePersistenceProfile,
    RegimeDurationProfile,
    RegimeChurnDiagnostic,
    RegimeStabilityDiagnostic,
    RegimeDiagnosticsReadinessGate
)

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if hasattr(o, "value"): # Enum
            return o.value
        return super().default(o)

def write_json(path: Path, data: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, cls=EnhancedJSONEncoder, indent=2)
    return path

def write_jsonl(path: Path, items: List[Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(item, cls=EnhancedJSONEncoder) + "\n")
    return path

def regime_transition_store_dir(data_root: Path) -> Path:
    return data_root / "regime_classification" / "diagnostics"

def regime_transition_contexts_dir(data_root: Path) -> Path:
    return regime_transition_store_dir(data_root) / "contexts"

def regime_transition_reviews_dir(data_root: Path) -> Path:
    return regime_transition_store_dir(data_root) / "reviews"

def transition_matrices_dir(data_root: Path) -> Path:
    return regime_transition_store_dir(data_root) / "transition_matrices"

def persistence_profiles_dir(data_root: Path) -> Path:
    return regime_transition_store_dir(data_root) / "persistence_profiles"

def duration_profiles_dir(data_root: Path) -> Path:
    return regime_transition_store_dir(data_root) / "duration_profiles"

def churn_diagnostics_dir(data_root: Path) -> Path:
    return regime_transition_store_dir(data_root) / "churn"

def stability_diagnostics_dir(data_root: Path) -> Path:
    return regime_transition_store_dir(data_root) / "stability"

def readiness_gates_dir(data_root: Path) -> Path:
    return regime_transition_store_dir(data_root) / "gates"

def write_regime_transition_context_json(path: Path, item: RegimeTransitionContext) -> Path:
    return write_json(path, item)

def write_regime_transition_full_review_json(path: Path, item: RegimeTransitionFullReview) -> Path:
    return write_json(path, item)

def write_transition_matrices_jsonl(path: Path, items: List[RegimeTransitionMatrix]) -> Path:
    return write_jsonl(path, items)

def write_persistence_profiles_jsonl(path: Path, items: List[RegimePersistenceProfile]) -> Path:
    return write_jsonl(path, items)

def write_duration_profiles_jsonl(path: Path, items: List[RegimeDurationProfile]) -> Path:
    return write_jsonl(path, items)

def write_churn_diagnostics_jsonl(path: Path, items: List[RegimeChurnDiagnostic]) -> Path:
    return write_jsonl(path, items)

def write_stability_diagnostics_jsonl(path: Path, items: List[RegimeStabilityDiagnostic]) -> Path:
    return write_jsonl(path, items)

def write_regime_diagnostics_readiness_gate_json(path: Path, item: RegimeDiagnosticsReadinessGate) -> Path:
    return write_json(path, item)

def read_regime_transition_full_review_json(path: Path) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_regime_transition_reviews(data_root: Path) -> List[Path]:
    d = regime_transition_reviews_dir(data_root)
    if not d.exists():
        return []
    return sorted(list(d.glob("*.json")))

def get_latest_regime_transition_review(data_root: Path) -> Optional[Path]:
    revs = list_regime_transition_reviews(data_root)
    return revs[-1] if revs else None

def regime_transition_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "reviews": len(list_regime_transition_reviews(data_root))
    }
