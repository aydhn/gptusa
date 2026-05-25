import os
from pathlib import Path
import json
from typing import Any
from usa_signal_bot.provider_cache.phase108_models import (
    ProviderCacheContext,
    ProviderCacheFullReview,
    ProviderCacheIndex,
    FallbackDryRunResult,
    SourceComparisonResult,
    provider_cache_context_to_dict,
    provider_cache_full_review_to_dict,
    provider_cache_index_to_dict,
    fallback_dry_run_result_to_dict,
    source_comparison_result_to_dict
)

def provider_cache_review_store_dir(data_root: Path) -> Path:
    return data_root / "provider_cache"

def provider_cache_contexts_dir(data_root: Path) -> Path:
    return provider_cache_review_store_dir(data_root) / "contexts"

def provider_cache_reviews_dir(data_root: Path) -> Path:
    return provider_cache_review_store_dir(data_root) / "reviews"

def provider_cache_indexes_dir(data_root: Path) -> Path:
    return provider_cache_review_store_dir(data_root) / "indexes"

def fallback_dry_run_results_dir(data_root: Path) -> Path:
    return provider_cache_review_store_dir(data_root) / "fallback_results"

def source_comparison_results_dir(data_root: Path) -> Path:
    return provider_cache_review_store_dir(data_root) / "source_comparisons"

def write_provider_cache_context_json(path: Path, item: ProviderCacheContext) -> Path:
    os.makedirs(path.parent, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(provider_cache_context_to_dict(item), f, indent=2)
    return path

def write_provider_cache_full_review_json(path: Path, item: ProviderCacheFullReview) -> Path:
    os.makedirs(path.parent, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(provider_cache_full_review_to_dict(item), f, indent=2)
    return path

def write_provider_cache_index_json(path: Path, item: ProviderCacheIndex) -> Path:
    os.makedirs(path.parent, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(provider_cache_index_to_dict(item), f, indent=2)
    return path

def write_fallback_dry_run_results_jsonl(path: Path, items: list[FallbackDryRunResult]) -> Path:
    os.makedirs(path.parent, exist_ok=True)
    with open(path, 'w') as f:
        for i in items:
            f.write(json.dumps(fallback_dry_run_result_to_dict(i)) + "\n")
    return path

def write_source_comparison_results_jsonl(path: Path, items: list[SourceComparisonResult]) -> Path:
    os.makedirs(path.parent, exist_ok=True)
    with open(path, 'w') as f:
        for i in items:
            f.write(json.dumps(source_comparison_result_to_dict(i)) + "\n")
    return path

def read_provider_cache_full_review_json(path: Path) -> dict[str, Any]:
    if not path.exists(): return {}
    with open(path, 'r') as f:
        return json.load(f)

def list_provider_cache_reviews(data_root: Path) -> list[Path]:
    d = provider_cache_reviews_dir(data_root)
    if not d.exists(): return []
    return list(d.glob("provider_cache_review_*.json"))

def get_latest_provider_cache_review(data_root: Path) -> Path | None:
    reviews = list_provider_cache_reviews(data_root)
    if not reviews: return None
    return max(reviews, key=lambda p: p.stat().st_mtime)

def provider_cache_store_summary(data_root: Path) -> dict[str, Any]:
    return {"reviews": len(list_provider_cache_reviews(data_root))}
