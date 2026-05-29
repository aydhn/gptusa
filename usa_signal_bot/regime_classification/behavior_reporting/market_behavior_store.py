import json
from pathlib import Path
from typing import Any

from usa_signal_bot.regime_classification.behavior_reporting.phase130_models import (
    MarketBehaviorContext, MarketBehaviorFullReview, MarketBehaviorProfile,
    RegimeBehaviorSummary, RegimeDiagnosticsInterpretation, BehaviorReportDocument,
    BehaviorReportQaRuleResult, MarketBehaviorReadinessGate
)

def market_behavior_store_dir(data_root: Path) -> Path:
    d = data_root / "regime_classification" / "behavior_reporting"
    d.mkdir(parents=True, exist_ok=True)
    return d

def market_behavior_contexts_dir(data_root: Path) -> Path:
    d = market_behavior_store_dir(data_root) / "contexts"
    d.mkdir(exist_ok=True)
    return d

def market_behavior_reviews_dir(data_root: Path) -> Path:
    d = market_behavior_store_dir(data_root) / "reviews"
    d.mkdir(exist_ok=True)
    return d

def market_behavior_profiles_dir(data_root: Path) -> Path:
    d = market_behavior_store_dir(data_root) / "profiles"
    d.mkdir(exist_ok=True)
    return d

def regime_behavior_summaries_dir(data_root: Path) -> Path:
    d = market_behavior_store_dir(data_root) / "summaries"
    d.mkdir(exist_ok=True)
    return d

def diagnostics_interpretations_dir(data_root: Path) -> Path:
    d = market_behavior_store_dir(data_root) / "interpretations"
    d.mkdir(exist_ok=True)
    return d

def behavior_reports_dir(data_root: Path) -> Path:
    d = market_behavior_store_dir(data_root) / "reports"
    d.mkdir(exist_ok=True)
    return d

def behavior_report_qa_dir(data_root: Path) -> Path:
    d = market_behavior_store_dir(data_root) / "report_qa"
    d.mkdir(exist_ok=True)
    return d

def behavior_readiness_gates_dir(data_root: Path) -> Path:
    d = market_behavior_store_dir(data_root) / "gates"
    d.mkdir(exist_ok=True)
    return d

def write_market_behavior_context_json(path: Path, item: MarketBehaviorContext) -> Path:
    with open(path, "w") as f:
        json.dump(item.to_dict(), f, indent=2)
    return path

def write_market_behavior_full_review_json(path: Path, item: MarketBehaviorFullReview) -> Path:
    with open(path, "w") as f:
        json.dump(item.to_dict(), f, indent=2)
    return path

def write_market_behavior_profiles_jsonl(path: Path, items: list[MarketBehaviorProfile]) -> Path:
    with open(path, "w") as f:
        for i in items:
            f.write(json.dumps(i.to_dict()) + "\n")
    return path

def write_regime_behavior_summaries_jsonl(path: Path, items: list[RegimeBehaviorSummary]) -> Path:
    with open(path, "w") as f:
        for i in items:
            f.write(json.dumps(i.to_dict()) + "\n")
    return path

def write_diagnostics_interpretations_jsonl(path: Path, items: list[RegimeDiagnosticsInterpretation]) -> Path:
    with open(path, "w") as f:
        for i in items:
            f.write(json.dumps(i.to_dict()) + "\n")
    return path

def write_behavior_report_document_json(path: Path, item: BehaviorReportDocument) -> Path:
    with open(path, "w") as f:
        json.dump(item.to_dict(), f, indent=2)
    return path

def write_behavior_report_qa_results_jsonl(path: Path, items: list[BehaviorReportQaRuleResult]) -> Path:
    with open(path, "w") as f:
        for i in items:
            f.write(json.dumps(i.to_dict()) + "\n")
    return path

def write_market_behavior_readiness_gate_json(path: Path, item: MarketBehaviorReadinessGate) -> Path:
    with open(path, "w") as f:
        json.dump(item.to_dict(), f, indent=2)
    return path

def read_market_behavior_full_review_json(path: Path) -> dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_market_behavior_reviews(data_root: Path) -> list[Path]:
    d = market_behavior_reviews_dir(data_root)
    return list(d.glob("*.json"))

def get_latest_market_behavior_review(data_root: Path) -> Path | None:
    files = list_market_behavior_reviews(data_root)
    if not files: return None
    files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return files[0]

def market_behavior_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "reviews": len(list_market_behavior_reviews(data_root))
    }
