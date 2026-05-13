import json
from pathlib import Path
from typing import Any, List, Optional
import datetime

from usa_signal_bot.execution.liquidity_models import (
    LiquidityProfile,
    TradabilityGuardResult,
    BorrowabilityProxyResult,
    ExecutionRealismReview,
    liquidity_profile_to_dict,
    tradability_guard_result_to_dict,
    borrowability_proxy_result_to_dict,
    execution_realism_review_to_dict
)

def execution_store_dir(data_root: Path) -> Path:
    d = data_root / "execution"
    d.mkdir(parents=True, exist_ok=True)
    return d

def liquidity_profiles_dir(data_root: Path) -> Path:
    d = execution_store_dir(data_root) / "liquidity_profiles"
    d.mkdir(parents=True, exist_ok=True)
    return d

def tradability_results_dir(data_root: Path) -> Path:
    d = execution_store_dir(data_root) / "tradability"
    d.mkdir(parents=True, exist_ok=True)
    return d

def borrowability_results_dir(data_root: Path) -> Path:
    d = execution_store_dir(data_root) / "borrowability"
    d.mkdir(parents=True, exist_ok=True)
    return d

def execution_reviews_dir(data_root: Path) -> Path:
    d = execution_store_dir(data_root) / "reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_liquidity_profile_json(path: Path, profile: LiquidityProfile) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(liquidity_profile_to_dict(profile), f, indent=2)
    return path

def write_liquidity_profiles_jsonl(path: Path, profiles: list[LiquidityProfile]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for p in profiles:
            f.write(json.dumps(liquidity_profile_to_dict(p)) + "\n")
    return path

def write_tradability_guard_result_json(path: Path, result: TradabilityGuardResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tradability_guard_result_to_dict(result), f, indent=2)
    return path

def write_borrowability_proxy_result_json(path: Path, result: BorrowabilityProxyResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(borrowability_proxy_result_to_dict(result), f, indent=2)
    return path

def write_execution_realism_review_json(path: Path, review: ExecutionRealismReview) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(execution_realism_review_to_dict(review), f, indent=2)
    return path

def read_execution_realism_review_json(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def list_execution_realism_reviews(data_root: Path) -> list[Path]:
    d = execution_reviews_dir(data_root)
    return sorted([p for p in d.glob("*.json") if p.is_file()])

def get_latest_execution_realism_review(data_root: Path) -> Path | None:
    files = list_execution_realism_reviews(data_root)
    if not files:
        return None
    return files[-1]

def execution_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "liquidity_profiles_count": len(list(liquidity_profiles_dir(data_root).glob("*.json"))),
        "tradability_results_count": len(list(tradability_results_dir(data_root).glob("*.json"))),
        "borrowability_results_count": len(list(borrowability_results_dir(data_root).glob("*.json"))),
        "execution_reviews_count": len(list_execution_realism_reviews(data_root)),
        "latest_review_path": str(get_latest_execution_realism_review(data_root)) if get_latest_execution_realism_review(data_root) else None
    }
