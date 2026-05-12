import json
from pathlib import Path
from typing import Any

from usa_signal_bot.providers.provider_models import (
    ProviderResponse, ProviderHealthResult, ProviderQualityScore, ProviderRoutingResult, ProviderReviewResult,
    provider_response_to_dict, provider_health_result_to_dict, provider_quality_score_to_dict,
    provider_routing_result_to_dict, provider_review_result_to_dict
)

def provider_store_dir(data_root: Path) -> Path:
    d = data_root / "providers"
    d.mkdir(parents=True, exist_ok=True)
    return d

def provider_health_dir(data_root: Path) -> Path:
    d = provider_store_dir(data_root) / "health"
    d.mkdir(exist_ok=True)
    return d

def provider_quality_dir(data_root: Path) -> Path:
    d = provider_store_dir(data_root) / "quality"
    d.mkdir(exist_ok=True)
    return d

def provider_routing_dir(data_root: Path) -> Path:
    d = provider_store_dir(data_root) / "routing"
    d.mkdir(exist_ok=True)
    return d

def provider_reviews_dir(data_root: Path) -> Path:
    d = provider_store_dir(data_root) / "reviews"
    d.mkdir(exist_ok=True)
    return d

def write_provider_response_json(path: Path, response: ProviderResponse) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(provider_response_to_dict(response), f, indent=2)
    return path

def write_provider_health_results_json(path: Path, results: list[ProviderHealthResult]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump([provider_health_result_to_dict(r) for r in results], f, indent=2)
    return path

def write_provider_quality_scores_jsonl(path: Path, scores: list[ProviderQualityScore]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for s in scores:
            f.write(json.dumps(provider_quality_score_to_dict(s)) + "\n")
    return path

def write_provider_routing_result_json(path: Path, result: ProviderRoutingResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(provider_routing_result_to_dict(result), f, indent=2)
    return path

def write_provider_review_result_json(path: Path, result: ProviderReviewResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(provider_review_result_to_dict(result), f, indent=2)
    return path

def read_provider_routing_result_json(path: Path) -> dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_provider_reviews(data_root: Path) -> list[Path]:
    d = provider_reviews_dir(data_root)
    return sorted(list(d.glob("*.json")))

def get_latest_provider_review(data_root: Path) -> Path | None:
    files = list_provider_reviews(data_root)
    return files[-1] if files else None

def provider_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "health_files": len(list(provider_health_dir(data_root).glob("*.json"))),
        "quality_files": len(list(provider_quality_dir(data_root).glob("*.jsonl"))),
        "routing_files": len(list(provider_routing_dir(data_root).glob("*.json"))),
        "review_files": len(list(provider_reviews_dir(data_root).glob("*.json")))
    }
