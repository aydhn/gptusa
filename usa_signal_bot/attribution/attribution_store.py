"""Storage operations for attribution data."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from usa_signal_bot.attribution.attribution_models import (
    AttributionTradeEvent, AttributionContribution, RiskAttributionContribution,
    SignalContribution, AttributionScorecard, AttributionReview,
    attribution_trade_event_to_dict, attribution_contribution_to_dict,
    risk_attribution_contribution_to_dict, signal_contribution_to_dict,
    attribution_scorecard_to_dict, attribution_review_to_dict
)

def attribution_store_dir(data_root: Path) -> Path:
    d = data_root / "attribution"
    d.mkdir(parents=True, exist_ok=True)
    return d

def attribution_events_dir(data_root: Path) -> Path:
    d = attribution_store_dir(data_root) / "events"
    d.mkdir(parents=True, exist_ok=True)
    return d

def performance_contributions_dir(data_root: Path) -> Path:
    d = attribution_store_dir(data_root) / "performance_contributions"
    d.mkdir(parents=True, exist_ok=True)
    return d

def risk_contributions_dir(data_root: Path) -> Path:
    d = attribution_store_dir(data_root) / "risk_contributions"
    d.mkdir(parents=True, exist_ok=True)
    return d

def signal_contributions_dir(data_root: Path) -> Path:
    d = attribution_store_dir(data_root) / "signal_contributions"
    d.mkdir(parents=True, exist_ok=True)
    return d

def attribution_scorecards_dir(data_root: Path) -> Path:
    d = attribution_store_dir(data_root) / "scorecards"
    d.mkdir(parents=True, exist_ok=True)
    return d

def attribution_reviews_dir(data_root: Path) -> Path:
    d = attribution_store_dir(data_root) / "reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_jsonl(path: Path, items: List[Dict[str, Any]]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(item) + "\n")
    return path

def write_attribution_events_jsonl(path: Path, items: List[AttributionTradeEvent]) -> Path:
    return write_jsonl(path, [attribution_trade_event_to_dict(i) for i in items])

def write_performance_contributions_jsonl(path: Path, items: List[AttributionContribution]) -> Path:
    return write_jsonl(path, [attribution_contribution_to_dict(i) for i in items])

def write_risk_contributions_jsonl(path: Path, items: List[RiskAttributionContribution]) -> Path:
    return write_jsonl(path, [risk_attribution_contribution_to_dict(i) for i in items])

def write_signal_contributions_jsonl(path: Path, items: List[SignalContribution]) -> Path:
    return write_jsonl(path, [signal_contribution_to_dict(i) for i in items])

def write_attribution_scorecard_json(path: Path, item: AttributionScorecard) -> Path:
    with open(path, "w") as f:
        json.dump(attribution_scorecard_to_dict(item), f, indent=2)
    return path

def write_attribution_review_json(path: Path, item: AttributionReview) -> Path:
    with open(path, "w") as f:
        json.dump(attribution_review_to_dict(item), f, indent=2)
    return path

def read_attribution_review_json(path: Path) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_attribution_reviews(data_root: Path) -> List[Path]:
    d = attribution_reviews_dir(data_root)
    return sorted(list(d.glob("*.json")), key=lambda p: p.stat().st_mtime, reverse=True)

def get_latest_attribution_review(data_root: Path) -> Optional[Path]:
    reviews = list_attribution_reviews(data_root)
    return reviews[0] if reviews else None

def attribution_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "reviews_count": len(list_attribution_reviews(data_root)),
        "latest_review": str(get_latest_attribution_review(data_root)) if get_latest_attribution_review(data_root) else None
    }
