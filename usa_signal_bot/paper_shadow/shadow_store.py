import json
import dataclasses
from pathlib import Path
from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_shadow.shadow_models import (
    ShadowSimulationContext, ShadowPortfolioState, ShadowRehearsalSession,
    ShadowLedgerEvent, ShadowPnLSnapshot, ShadowRehearsalReview
)
from usa_signal_bot.core.serialization import serialize_value
from usa_signal_bot.paper_common.io import ensure_dir, read_json, list_files, count_files

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return serialize_value(obj)
        except TypeError:
            return super().default(obj)

def shadow_store_dir(data_root: Path) -> Path:
    return ensure_dir(data_root / "paper_shadow")

def shadow_contexts_dir(data_root: Path) -> Path:
    return ensure_dir(shadow_store_dir(data_root) / "contexts")

def shadow_portfolios_dir(data_root: Path) -> Path:
    return ensure_dir(shadow_store_dir(data_root) / "portfolios")

def shadow_sessions_dir(data_root: Path) -> Path:
    return ensure_dir(shadow_store_dir(data_root) / "sessions")

def shadow_ledgers_dir(data_root: Path) -> Path:
    return ensure_dir(shadow_store_dir(data_root) / "ledgers")

def shadow_pnl_dir(data_root: Path) -> Path:
    return ensure_dir(shadow_store_dir(data_root) / "pnl")

def shadow_reviews_dir(data_root: Path) -> Path:
    return ensure_dir(shadow_store_dir(data_root) / "reviews")

def _write_json(path: Path, item: Any) -> Path:
    data = serialize_value(item)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, cls=JSONEncoder)
    return path

def _write_jsonl(path: Path, items: List[Any]) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        for item in items:
            data = serialize_value(item)
            f.write(json.dumps(data, cls=JSONEncoder) + "\n")
    return path

def write_shadow_context_json(path: Path, item: ShadowSimulationContext) -> Path:
    return _write_json(path, item)

def write_shadow_portfolio_json(path: Path, item: ShadowPortfolioState) -> Path:
    return _write_json(path, item)

def write_shadow_session_json(path: Path, item: ShadowRehearsalSession) -> Path:
    return _write_json(path, item)

def write_shadow_ledger_jsonl(path: Path, items: List[ShadowLedgerEvent]) -> Path:
    return _write_jsonl(path, items)

def write_shadow_pnl_jsonl(path: Path, items: List[ShadowPnLSnapshot]) -> Path:
    return _write_jsonl(path, items)

def write_shadow_rehearsal_review_json(path: Path, item: ShadowRehearsalReview) -> Path:
    return _write_json(path, item)

def read_shadow_rehearsal_review_json(path: Path) -> Dict[str, Any]:
    return read_json(path)

def list_shadow_rehearsal_reviews(data_root: Path) -> List[Path]:
    d = shadow_reviews_dir(data_root)
    return list_files(d, "*.json", sort=True, reverse=True)

def get_latest_shadow_rehearsal_review(data_root: Path) -> Optional[Path]:
    files = list_shadow_rehearsal_reviews(data_root)
    return files[0] if files else None

def shadow_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "reviews_count": len(list_shadow_rehearsal_reviews(data_root)),
        "sessions_count": count_files(shadow_sessions_dir(data_root), "*.json")
    }
