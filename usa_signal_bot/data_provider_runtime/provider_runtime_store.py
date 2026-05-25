import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from usa_signal_bot.data_provider_runtime.phase107_models import (
    ProviderRuntimeContext,
    ProviderRuntimeFullReview,
    ProviderRuntimeAdapterSpec,
    ProviderFetchDryRunPlan,
    ProviderFetchDryRunResult,
    ProviderContractTestReport,
    provider_runtime_context_to_dict,
    provider_runtime_full_review_to_dict,
    provider_runtime_adapter_spec_to_dict,
    provider_fetch_dry_run_plan_to_dict,
    provider_fetch_dry_run_result_to_dict,
    provider_contract_test_report_to_dict
)


def provider_runtime_store_dir(data_root: Path) -> Path:
    d = data_root / "data_provider_runtime"
    d.mkdir(parents=True, exist_ok=True)
    return d

def provider_runtime_contexts_dir(data_root: Path) -> Path:
    d = provider_runtime_store_dir(data_root) / "contexts"
    d.mkdir(parents=True, exist_ok=True)
    return d

def provider_runtime_reviews_dir(data_root: Path) -> Path:
    d = provider_runtime_store_dir(data_root) / "reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def provider_runtime_adapter_specs_dir(data_root: Path) -> Path:
    d = provider_runtime_store_dir(data_root) / "adapter_specs"
    d.mkdir(parents=True, exist_ok=True)
    return d

def provider_runtime_dry_run_plans_dir(data_root: Path) -> Path:
    d = provider_runtime_store_dir(data_root) / "dry_run_plans"
    d.mkdir(parents=True, exist_ok=True)
    return d

def provider_runtime_dry_run_results_dir(data_root: Path) -> Path:
    d = provider_runtime_store_dir(data_root) / "dry_run_results"
    d.mkdir(parents=True, exist_ok=True)
    return d

def provider_runtime_contract_tests_dir(data_root: Path) -> Path:
    d = provider_runtime_store_dir(data_root) / "contract_tests"
    d.mkdir(parents=True, exist_ok=True)
    return d


def write_provider_runtime_context_json(path: Path, item: ProviderRuntimeContext) -> Path:
    with open(path, "w") as f:
        json.dump(provider_runtime_context_to_dict(item), f, indent=2)
    return path

def write_provider_runtime_full_review_json(path: Path, item: ProviderRuntimeFullReview) -> Path:
    with open(path, "w") as f:
        json.dump(provider_runtime_full_review_to_dict(item), f, indent=2)
    return path

def write_provider_runtime_adapter_specs_jsonl(path: Path, items: List[ProviderRuntimeAdapterSpec]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(provider_runtime_adapter_spec_to_dict(item)) + "\n")
    return path

def write_provider_fetch_dry_run_plans_jsonl(path: Path, items: List[ProviderFetchDryRunPlan]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(provider_fetch_dry_run_plan_to_dict(item)) + "\n")
    return path

def write_provider_fetch_dry_run_results_jsonl(path: Path, items: List[ProviderFetchDryRunResult]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(provider_fetch_dry_run_result_to_dict(item)) + "\n")
    return path

def write_provider_contract_test_report_json(path: Path, item: ProviderContractTestReport) -> Path:
    with open(path, "w") as f:
        json.dump(provider_contract_test_report_to_dict(item), f, indent=2)
    return path

def read_provider_runtime_full_review_json(path: Path) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_provider_runtime_reviews(data_root: Path) -> List[Path]:
    return sorted(list(provider_runtime_reviews_dir(data_root).glob("*.json")))

def get_latest_provider_runtime_review(data_root: Path) -> Optional[Path]:
    files = list_provider_runtime_reviews(data_root)
    if not files:
        return None
    return files[-1]

def provider_runtime_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "reviews_count": len(list_provider_runtime_reviews(data_root)),
        "contexts_count": len(list(provider_runtime_contexts_dir(data_root).glob("*.json")))
    }
