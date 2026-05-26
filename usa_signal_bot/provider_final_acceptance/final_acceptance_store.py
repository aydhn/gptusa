import json
from pathlib import Path
from typing import Any
from usa_signal_bot.provider_final_acceptance.phase115_models import (
    ProviderFinalAcceptanceContext,
    ProviderFinalAcceptanceFullReview,
    DataProviderFinalAcceptanceReport,
    ProviderLayerClosureBundle,
    FeatureFactorDataContract,
    FeatureFactorEngineKickoffGate,
    provider_final_acceptance_context_to_dict,
    provider_final_acceptance_full_review_to_dict,
    data_provider_final_acceptance_report_to_dict,
    provider_layer_closure_bundle_to_dict,
    feature_factor_data_contract_to_dict,
    feature_factor_engine_kickoff_gate_to_dict
)

def final_acceptance_store_dir(data_root: Path) -> Path:
    d = data_root / "provider_final_acceptance"
    d.mkdir(parents=True, exist_ok=True)
    return d

def final_acceptance_contexts_dir(data_root: Path) -> Path:
    d = final_acceptance_store_dir(data_root) / "contexts"
    d.mkdir(parents=True, exist_ok=True)
    return d

def final_acceptance_reviews_dir(data_root: Path) -> Path:
    d = final_acceptance_store_dir(data_root) / "reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def final_acceptance_reports_dir(data_root: Path) -> Path:
    d = final_acceptance_store_dir(data_root) / "acceptance_reports"
    d.mkdir(parents=True, exist_ok=True)
    return d

def provider_layer_closures_dir(data_root: Path) -> Path:
    d = final_acceptance_store_dir(data_root) / "provider_layer_closures"
    d.mkdir(parents=True, exist_ok=True)
    return d

def feature_factor_contracts_dir(data_root: Path) -> Path:
    d = final_acceptance_store_dir(data_root) / "feature_factor_contracts"
    d.mkdir(parents=True, exist_ok=True)
    return d

def feature_factor_kickoff_gates_dir(data_root: Path) -> Path:
    d = final_acceptance_store_dir(data_root) / "feature_factor_kickoff_gates"
    d.mkdir(parents=True, exist_ok=True)
    return d

def _write_json(path: Path, data: dict) -> Path:
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    return path

def write_provider_final_acceptance_context_json(path: Path, item: ProviderFinalAcceptanceContext) -> Path:
    return _write_json(path, provider_final_acceptance_context_to_dict(item))

def write_provider_final_acceptance_full_review_json(path: Path, item: ProviderFinalAcceptanceFullReview) -> Path:
    return _write_json(path, provider_final_acceptance_full_review_to_dict(item))

def write_data_provider_final_acceptance_report_json(path: Path, item: DataProviderFinalAcceptanceReport) -> Path:
    return _write_json(path, data_provider_final_acceptance_report_to_dict(item))

def write_provider_layer_closure_bundle_json(path: Path, item: ProviderLayerClosureBundle) -> Path:
    return _write_json(path, provider_layer_closure_bundle_to_dict(item))

def write_feature_factor_data_contract_json(path: Path, item: FeatureFactorDataContract) -> Path:
    return _write_json(path, feature_factor_data_contract_to_dict(item))

def write_feature_factor_kickoff_gate_json(path: Path, item: FeatureFactorEngineKickoffGate) -> Path:
    return _write_json(path, feature_factor_engine_kickoff_gate_to_dict(item))

def read_provider_final_acceptance_full_review_json(path: Path) -> dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_provider_final_acceptance_reviews(data_root: Path) -> list[Path]:
    return list(final_acceptance_reviews_dir(data_root).glob("*.json"))

def get_latest_provider_final_acceptance_review(data_root: Path) -> Path | None:
    files = list_provider_final_acceptance_reviews(data_root)
    if not files:
        return None
    return max(files, key=lambda p: p.stat().st_mtime)

def final_acceptance_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "reviews_count": len(list_provider_final_acceptance_reviews(data_root))
    }
