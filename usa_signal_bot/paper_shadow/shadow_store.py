import json
from pathlib import Path
from typing import Any
from usa_signal_bot.paper_shadow.shadow_models import (
    ShadowSimulationContext,
    ShadowPortfolioState,
    ShadowRehearsalSession,
    ShadowLedgerEvent,
    ShadowPnLSnapshot,
    ShadowRehearsalReview,
    shadow_simulation_context_to_dict,
    shadow_portfolio_state_to_dict,
    shadow_rehearsal_session_to_dict,
    shadow_ledger_event_to_dict,
    shadow_pnl_snapshot_to_dict,
    shadow_rehearsal_review_to_dict
)

def shadow_store_dir(data_root: Path) -> Path:
    d = data_root / "paper_shadow"
    d.mkdir(parents=True, exist_ok=True)
    return d

def shadow_contexts_dir(data_root: Path) -> Path:
    d = shadow_store_dir(data_root) / "contexts"
    d.mkdir(parents=True, exist_ok=True)
    return d

def shadow_portfolios_dir(data_root: Path) -> Path:
    d = shadow_store_dir(data_root) / "portfolios"
    d.mkdir(parents=True, exist_ok=True)
    return d

def shadow_sessions_dir(data_root: Path) -> Path:
    d = shadow_store_dir(data_root) / "sessions"
    d.mkdir(parents=True, exist_ok=True)
    return d

def shadow_ledgers_dir(data_root: Path) -> Path:
    d = shadow_store_dir(data_root) / "ledgers"
    d.mkdir(parents=True, exist_ok=True)
    return d

def shadow_pnl_dir(data_root: Path) -> Path:
    d = shadow_store_dir(data_root) / "pnl"
    d.mkdir(parents=True, exist_ok=True)
    return d

def shadow_reviews_dir(data_root: Path) -> Path:
    d = shadow_store_dir(data_root) / "reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_shadow_context_json(path: Path, item: ShadowSimulationContext) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(shadow_simulation_context_to_dict(item), f, indent=2)
    return path

def write_shadow_portfolio_json(path: Path, item: ShadowPortfolioState) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(shadow_portfolio_state_to_dict(item), f, indent=2)
    return path

def write_shadow_session_json(path: Path, item: ShadowRehearsalSession) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(shadow_rehearsal_session_to_dict(item), f, indent=2)
    return path

def write_shadow_ledger_jsonl(path: Path, items: list[ShadowLedgerEvent]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(shadow_ledger_event_to_dict(item)) + "\n")
    return path

def write_shadow_pnl_jsonl(path: Path, items: list[ShadowPnLSnapshot]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(shadow_pnl_snapshot_to_dict(item)) + "\n")
    return path

def write_shadow_rehearsal_review_json(path: Path, item: ShadowRehearsalReview) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(shadow_rehearsal_review_to_dict(item), f, indent=2)
    return path

def read_shadow_rehearsal_review_json(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def list_shadow_rehearsal_reviews(data_root: Path) -> list[Path]:
    return sorted(shadow_reviews_dir(data_root).glob("*.json"))

def get_latest_shadow_rehearsal_review(data_root: Path) -> Path | None:
    reviews = list_shadow_rehearsal_reviews(data_root)
    return reviews[-1] if reviews else None

def shadow_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "contexts_count": len(list(shadow_contexts_dir(data_root).glob("*.json"))),
        "portfolios_count": len(list(shadow_portfolios_dir(data_root).glob("*.json"))),
        "sessions_count": len(list(shadow_sessions_dir(data_root).glob("*.json"))),
        "ledgers_count": len(list(shadow_ledgers_dir(data_root).glob("*.jsonl"))),
        "pnl_count": len(list(shadow_pnl_dir(data_root).glob("*.jsonl"))),
        "reviews_count": len(list_shadow_rehearsal_reviews(data_root))
    }
