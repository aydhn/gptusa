from pathlib import Path
from typing import Any
import json
from usa_signal_bot.provider_orchestration.phase110_models import (
    ProviderOrchestrationContext, ProviderOrchestrationFullReview,
    ProviderRoutePlan, ProviderRouteResult, SourceBlendResult,
    DataAvailabilityReport, RefreshPlanReport,
    provider_orchestration_context_to_dict, provider_orchestration_full_review_to_dict,
    provider_route_plan_to_dict, provider_route_result_to_dict,
    source_blend_result_to_dict, data_availability_report_to_dict,
    refresh_plan_report_to_dict
)

def provider_orchestration_store_dir(data_root: Path) -> Path:
    p = data_root / "provider_orchestration"
    p.mkdir(parents=True, exist_ok=True)
    return p

def provider_orchestration_contexts_dir(data_root: Path) -> Path:
    p = provider_orchestration_store_dir(data_root) / "contexts"
    p.mkdir(parents=True, exist_ok=True)
    return p

def provider_orchestration_reviews_dir(data_root: Path) -> Path:
    p = provider_orchestration_store_dir(data_root) / "reviews"
    p.mkdir(parents=True, exist_ok=True)
    return p

def provider_route_plans_dir(data_root: Path) -> Path:
    p = provider_orchestration_store_dir(data_root) / "route_plans"
    p.mkdir(parents=True, exist_ok=True)
    return p

def provider_route_results_dir(data_root: Path) -> Path:
    p = provider_orchestration_store_dir(data_root) / "route_results"
    p.mkdir(parents=True, exist_ok=True)
    return p

def source_blend_results_dir(data_root: Path) -> Path:
    p = provider_orchestration_store_dir(data_root) / "source_blends"
    p.mkdir(parents=True, exist_ok=True)
    return p

def availability_reports_dir(data_root: Path) -> Path:
    p = provider_orchestration_store_dir(data_root) / "availability_reports"
    p.mkdir(parents=True, exist_ok=True)
    return p

def refresh_reports_dir(data_root: Path) -> Path:
    p = provider_orchestration_store_dir(data_root) / "refresh_reports"
    p.mkdir(parents=True, exist_ok=True)
    return p

def _write_json(path: Path, data: dict[str, Any]) -> Path:
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    return path

def _write_jsonl(path: Path, items: list[dict[str, Any]]) -> Path:
    with open(path, "w") as f:
        for i in items:
            f.write(json.dumps(i) + "\n")
    return path

def write_provider_orchestration_context_json(path: Path, item: ProviderOrchestrationContext) -> Path:
    return _write_json(path, provider_orchestration_context_to_dict(item))

def write_provider_orchestration_full_review_json(path: Path, item: ProviderOrchestrationFullReview) -> Path:
    return _write_json(path, provider_orchestration_full_review_to_dict(item))

def write_provider_route_plans_jsonl(path: Path, items: list[ProviderRoutePlan]) -> Path:
    return _write_jsonl(path, [provider_route_plan_to_dict(i) for i in items])

def write_provider_route_results_jsonl(path: Path, items: list[ProviderRouteResult]) -> Path:
    return _write_jsonl(path, [provider_route_result_to_dict(i) for i in items])

def write_source_blend_results_jsonl(path: Path, items: list[SourceBlendResult]) -> Path:
    return _write_jsonl(path, [source_blend_result_to_dict(i) for i in items])

def write_data_availability_report_json(path: Path, item: DataAvailabilityReport) -> Path:
    return _write_json(path, data_availability_report_to_dict(item))

def write_refresh_plan_report_json(path: Path, item: RefreshPlanReport) -> Path:
    return _write_json(path, refresh_plan_report_to_dict(item))

def read_provider_orchestration_full_review_json(path: Path) -> dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_provider_orchestration_reviews(data_root: Path) -> list[Path]:
    d = provider_orchestration_reviews_dir(data_root)
    files = list(d.glob("*.json"))
    files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return files

def get_latest_provider_orchestration_review(data_root: Path) -> Path | None:
    files = list_provider_orchestration_reviews(data_root)
    return files[0] if files else None

def provider_orchestration_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "contexts": len(list(provider_orchestration_contexts_dir(data_root).glob("*.json"))),
        "reviews": len(list(provider_orchestration_reviews_dir(data_root).glob("*.json"))),
        "plans": len(list(provider_route_plans_dir(data_root).glob("*.jsonl")))
    }
