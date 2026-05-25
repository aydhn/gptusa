import json
from pathlib import Path
from typing import List, Dict, Any, Optional


from usa_signal_bot.provider_quality.phase109_models import (
    ProviderQualityContext,
    ProviderQualityFullReview,
    ProviderDataQualityScore,
    SourceTrustProfile,
    ProviderSelectionScore,
    ProviderRanking,
    provider_quality_context_to_dict,
    provider_quality_full_review_to_dict,
    provider_data_quality_score_to_dict,
    source_trust_profile_to_dict,
    provider_selection_score_to_dict,
    provider_ranking_to_dict
)

def provider_quality_store_dir(data_root: Path) -> Path:
    d = data_root / "provider_quality"
    d.mkdir(parents=True, exist_ok=True)
    return d

def provider_quality_contexts_dir(data_root: Path) -> Path:
    d = provider_quality_store_dir(data_root) / "contexts"
    d.mkdir(parents=True, exist_ok=True)
    return d

def provider_quality_reviews_dir(data_root: Path) -> Path:
    d = provider_quality_store_dir(data_root) / "reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def data_quality_scores_dir(data_root: Path) -> Path:
    d = provider_quality_store_dir(data_root) / "data_quality_scores"
    d.mkdir(parents=True, exist_ok=True)
    return d

def source_trust_profiles_dir(data_root: Path) -> Path:
    d = provider_quality_store_dir(data_root) / "source_trust_profiles"
    d.mkdir(parents=True, exist_ok=True)
    return d

def provider_selection_scores_dir(data_root: Path) -> Path:
    d = provider_quality_store_dir(data_root) / "provider_selection_scores"
    d.mkdir(parents=True, exist_ok=True)
    return d

def provider_rankings_dir(data_root: Path) -> Path:
    d = provider_quality_store_dir(data_root) / "provider_rankings"
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_provider_quality_context_json(path: Path, item: ProviderQualityContext) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(provider_quality_context_to_dict(item), f, indent=2, default=str)
    return path

def write_provider_quality_full_review_json(path: Path, item: ProviderQualityFullReview) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(provider_quality_full_review_to_dict(item), f, indent=2, default=str)
    return path

def write_data_quality_scores_jsonl(path: Path, items: List[ProviderDataQualityScore]) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(provider_data_quality_score_to_dict(it), default=str) + "\n")
    return path

def write_source_trust_profiles_jsonl(path: Path, items: List[SourceTrustProfile]) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(source_trust_profile_to_dict(it), default=str) + "\n")
    return path

def write_provider_selection_scores_jsonl(path: Path, items: List[ProviderSelectionScore]) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(provider_selection_score_to_dict(it), default=str) + "\n")
    return path

def write_provider_rankings_jsonl(path: Path, items: List[ProviderRanking]) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(provider_ranking_to_dict(it), default=str) + "\n")
    return path

def read_provider_quality_full_review_json(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def list_provider_quality_reviews(data_root: Path) -> List[Path]:
    rev_dir = provider_quality_reviews_dir(data_root)
    return sorted(list(rev_dir.glob("*.json")), reverse=True)

def get_latest_provider_quality_review(data_root: Path) -> Optional[Path]:
    files = list_provider_quality_reviews(data_root)
    return files[0] if files else None

def provider_quality_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "contexts_count": len(list(provider_quality_contexts_dir(data_root).glob("*.json"))),
        "reviews_count": len(list_provider_quality_reviews(data_root)),
        "data_quality_scores_count": len(list(data_quality_scores_dir(data_root).glob("*.jsonl"))),
        "source_trust_profiles_count": len(list(source_trust_profiles_dir(data_root).glob("*.jsonl"))),
        "provider_selection_scores_count": len(list(provider_selection_scores_dir(data_root).glob("*.jsonl"))),
        "provider_rankings_count": len(list(provider_rankings_dir(data_root).glob("*.jsonl")))
    }
