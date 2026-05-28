import json
from pathlib import Path
from typing import Any, List
from usa_signal_bot.regime_classification.foundation.phase126_models import (
    RegimeFoundationContext,
    RegimeFoundationFullReview,
    RegimeResearchInputBundle,
    MarketStateDatasetContract,
    MarketStateDatasetSkeleton,
    RegimeLabelTaxonomy,
    RegimeNonActivationBoundaryResult,
    regime_foundation_context_to_dict,
    regime_foundation_full_review_to_dict,
    regime_research_input_bundle_to_dict,
    market_state_dataset_contract_to_dict,
    market_state_dataset_skeleton_to_dict,
    regime_label_taxonomy_to_dict,
    regime_non_activation_boundary_result_to_dict
)

def regime_foundation_store_dir(data_root: Path) -> Path:
    d = data_root / "regime_classification" / "foundation"
    d.mkdir(parents=True, exist_ok=True)
    return d

def regime_foundation_contexts_dir(data_root: Path) -> Path:
    d = regime_foundation_store_dir(data_root) / "contexts"
    d.mkdir(parents=True, exist_ok=True)
    return d

def regime_foundation_reviews_dir(data_root: Path) -> Path:
    d = regime_foundation_store_dir(data_root) / "reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def regime_input_contracts_dir(data_root: Path) -> Path:
    d = regime_foundation_store_dir(data_root) / "input_contracts"
    d.mkdir(parents=True, exist_ok=True)
    return d

def market_state_contracts_dir(data_root: Path) -> Path:
    d = regime_foundation_store_dir(data_root) / "market_state_contracts"
    d.mkdir(parents=True, exist_ok=True)
    return d

def market_state_skeletons_dir(data_root: Path) -> Path:
    d = regime_foundation_store_dir(data_root) / "market_state_skeletons"
    d.mkdir(parents=True, exist_ok=True)
    return d

def regime_taxonomies_dir(data_root: Path) -> Path:
    d = regime_foundation_store_dir(data_root) / "taxonomies"
    d.mkdir(parents=True, exist_ok=True)
    return d

def regime_boundaries_dir(data_root: Path) -> Path:
    d = regime_foundation_store_dir(data_root) / "boundaries"
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_regime_foundation_context_json(path: Path, item: RegimeFoundationContext) -> Path:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(regime_foundation_context_to_dict(item), f, indent=2, ensure_ascii=False)
    return path

def write_regime_foundation_full_review_json(path: Path, item: RegimeFoundationFullReview) -> Path:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(regime_foundation_full_review_to_dict(item), f, indent=2, ensure_ascii=False)
    return path

def write_regime_input_bundle_json(path: Path, item: RegimeResearchInputBundle) -> Path:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(regime_research_input_bundle_to_dict(item), f, indent=2, ensure_ascii=False)
    return path

def write_market_state_dataset_contract_json(path: Path, item: MarketStateDatasetContract) -> Path:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(market_state_dataset_contract_to_dict(item), f, indent=2, ensure_ascii=False)
    return path

def write_market_state_dataset_skeleton_json(path: Path, item: MarketStateDatasetSkeleton) -> Path:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(market_state_dataset_skeleton_to_dict(item), f, indent=2, ensure_ascii=False)
    return path

def write_regime_label_taxonomy_json(path: Path, item: RegimeLabelTaxonomy) -> Path:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(regime_label_taxonomy_to_dict(item), f, indent=2, ensure_ascii=False)
    return path

def write_regime_non_activation_boundary_json(path: Path, item: RegimeNonActivationBoundaryResult) -> Path:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(regime_non_activation_boundary_result_to_dict(item), f, indent=2, ensure_ascii=False)
    return path

def read_regime_foundation_full_review_json(path: Path) -> dict[str, Any]:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def list_regime_foundation_reviews(data_root: Path) -> List[Path]:
    d = regime_foundation_reviews_dir(data_root)
    if not d.exists():
        return []
    return sorted(d.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)

def get_latest_regime_foundation_review(data_root: Path) -> Path | None:
    reviews = list_regime_foundation_reviews(data_root)
    return reviews[0] if reviews else None

def regime_foundation_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "context_count": len(list(regime_foundation_contexts_dir(data_root).glob("*.json"))),
        "review_count": len(list_regime_foundation_reviews(data_root)),
        "input_contract_count": len(list(regime_input_contracts_dir(data_root).glob("*.json"))),
        "dataset_contract_count": len(list(market_state_contracts_dir(data_root).glob("*.json"))),
        "skeleton_count": len(list(market_state_skeletons_dir(data_root).glob("*.json"))),
        "taxonomy_count": len(list(regime_taxonomies_dir(data_root).glob("*.json"))),
        "boundary_count": len(list(regime_boundaries_dir(data_root).glob("*.json"))),
    }
