import json
from pathlib import Path
from typing import Any
from usa_signal_bot.regime_classification.validation.phase132_models import (
    RegimeContextValidationContext,
    RegimeContextValidationFullReview,
    CompatibilityValidationResult,
    ConditionalDiagnosticResult,
    ConditionalDiagnosticsProfile,
    RegimeAwareAcceptanceGate,
    regime_context_validation_context_to_dict,
    regime_context_validation_full_review_to_dict,
    compatibility_validation_result_to_dict,
    conditional_diagnostic_result_to_dict,
    conditional_diagnostics_profile_to_dict,
    regime_aware_acceptance_gate_to_dict
)

def regime_context_validation_store_dir(data_root: Path) -> Path:
    return data_root / "regime_classification" / "validation"

def regime_context_validation_contexts_dir(data_root: Path) -> Path:
    return regime_context_validation_store_dir(data_root) / "contexts"

def regime_context_validation_reviews_dir(data_root: Path) -> Path:
    return regime_context_validation_store_dir(data_root) / "reviews"

def compatibility_validation_results_dir(data_root: Path) -> Path:
    return regime_context_validation_store_dir(data_root) / "compatibility_validation"

def conditional_diagnostics_dir(data_root: Path) -> Path:
    return regime_context_validation_store_dir(data_root) / "conditional_diagnostics"

def conditional_diagnostics_profiles_dir(data_root: Path) -> Path:
    return regime_context_validation_store_dir(data_root) / "diagnostic_profiles"

def acceptance_gates_dir(data_root: Path) -> Path:
    return regime_context_validation_store_dir(data_root) / "acceptance_gates"

def write_regime_context_validation_context_json(path: Path, item: RegimeContextValidationContext) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(regime_context_validation_context_to_dict(item), f, indent=2)
    return path

def write_regime_context_validation_full_review_json(path: Path, item: RegimeContextValidationFullReview) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(regime_context_validation_full_review_to_dict(item), f, indent=2)
    return path

def write_compatibility_validation_result_json(path: Path, item: CompatibilityValidationResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(compatibility_validation_result_to_dict(item), f, indent=2)
    return path

def write_conditional_diagnostics_jsonl(path: Path, items: list[ConditionalDiagnosticResult]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(conditional_diagnostic_result_to_dict(item)) + "\n")
    return path

def write_conditional_diagnostics_profiles_jsonl(path: Path, items: list[ConditionalDiagnosticsProfile]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(conditional_diagnostics_profile_to_dict(item)) + "\n")
    return path

def write_regime_aware_acceptance_gate_json(path: Path, item: RegimeAwareAcceptanceGate) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(regime_aware_acceptance_gate_to_dict(item), f, indent=2)
    return path

def read_regime_context_validation_full_review_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, "r") as f:
        return json.load(f)

def list_regime_context_validation_reviews(data_root: Path) -> list[Path]:
    rev_dir = regime_context_validation_reviews_dir(data_root)
    if not rev_dir.exists():
        return []
    return sorted(list(rev_dir.glob("*.json")))

def get_latest_regime_context_validation_review(data_root: Path) -> Path | None:
    files = list_regime_context_validation_reviews(data_root)
    if not files:
        return None
    return max(files, key=lambda f: f.stat().st_mtime)

def regime_context_validation_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "reviews": len(list_regime_context_validation_reviews(data_root))
    }
