import json
from pathlib import Path
from typing import Any
from usa_signal_bot.feature_engine.phase116_models import (
    FeatureFoundationContext, FeatureFoundationFullReview, FeatureRegistry,
    FeatureInputContract, FeatureOutputSchema,
    feature_foundation_context_to_dict, feature_foundation_full_review_to_dict,
    feature_registry_to_dict, feature_input_contract_to_dict, feature_output_schema_to_dict
)

def feature_foundation_store_dir(data_root: Path) -> Path:
    p = data_root / "feature_engine" / "foundation"
    p.mkdir(parents=True, exist_ok=True)
    return p

def feature_foundation_contexts_dir(data_root: Path) -> Path:
    p = feature_foundation_store_dir(data_root) / "contexts"
    p.mkdir(parents=True, exist_ok=True)
    return p

def feature_foundation_reviews_dir(data_root: Path) -> Path:
    p = feature_foundation_store_dir(data_root) / "reviews"
    p.mkdir(parents=True, exist_ok=True)
    return p

def indicator_registries_dir(data_root: Path) -> Path:
    p = feature_foundation_store_dir(data_root) / "indicator_registries"
    p.mkdir(parents=True, exist_ok=True)
    return p

def feature_registries_dir(data_root: Path) -> Path:
    p = feature_foundation_store_dir(data_root) / "feature_registries"
    p.mkdir(parents=True, exist_ok=True)
    return p

def factor_registries_dir(data_root: Path) -> Path:
    p = feature_foundation_store_dir(data_root) / "factor_registries"
    p.mkdir(parents=True, exist_ok=True)
    return p

def feature_contracts_dir(data_root: Path) -> Path:
    p = feature_foundation_store_dir(data_root) / "contracts"
    p.mkdir(parents=True, exist_ok=True)
    return p

def feature_schemas_dir(data_root: Path) -> Path:
    p = feature_foundation_store_dir(data_root) / "schemas"
    p.mkdir(parents=True, exist_ok=True)
    return p

def write_feature_foundation_context_json(path: Path, item: FeatureFoundationContext) -> Path:
    with open(path, "w") as f:
        json.dump(feature_foundation_context_to_dict(item), f, indent=2)
    return path

def write_feature_foundation_full_review_json(path: Path, item: FeatureFoundationFullReview) -> Path:
    with open(path, "w") as f:
        json.dump(feature_foundation_full_review_to_dict(item), f, indent=2)
    return path

def write_feature_registry_json(path: Path, item: FeatureRegistry) -> Path:
    with open(path, "w") as f:
        json.dump(feature_registry_to_dict(item), f, indent=2)
    return path

def write_feature_input_contract_json(path: Path, item: FeatureInputContract) -> Path:
    with open(path, "w") as f:
        json.dump(feature_input_contract_to_dict(item), f, indent=2)
    return path

def write_feature_output_schema_json(path: Path, item: FeatureOutputSchema) -> Path:
    with open(path, "w") as f:
        json.dump(feature_output_schema_to_dict(item), f, indent=2)
    return path

def read_feature_foundation_full_review_json(path: Path) -> dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_feature_foundation_reviews(data_root: Path) -> list[Path]:
    d = feature_foundation_reviews_dir(data_root)
    return sorted(list(d.glob("*.json")))

def get_latest_feature_foundation_review(data_root: Path) -> Path | None:
    files = list_feature_foundation_reviews(data_root)
    return files[-1] if files else None

def feature_foundation_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "contexts": len(list(feature_foundation_contexts_dir(data_root).glob("*.json"))),
        "reviews": len(list(feature_foundation_reviews_dir(data_root).glob("*.json")))
    }
