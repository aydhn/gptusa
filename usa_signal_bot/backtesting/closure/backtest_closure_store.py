import json
from pathlib import Path
from typing import Any
from usa_signal_bot.backtesting.closure.phase152_models import *

def backtest_closure_store_dir(data_root: Path) -> Path:
    return data_root / "backtesting" / "closure"

def backtest_closure_reviews_dir(data_root: Path) -> Path:
    return backtest_closure_store_dir(data_root) / "reviews"

def write_backtest_closure_full_review_json(path: Path, item: BacktestClosureFullReview) -> Path:
    import dataclasses

    def dc_default(o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        elif hasattr(o, "name"): # Enum
            return o.name
        return str(o)

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(dataclasses.asdict(item), f, default=dc_default, indent=2)
    return path

def backtest_closure_store_summary(data_root: Path) -> dict[str, Any]:
    return {"dir": str(backtest_closure_store_dir(data_root))}
