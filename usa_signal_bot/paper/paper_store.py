from pathlib import Path
import json
from typing import Any, Dict, List, Optional
import shutil
import os

from usa_signal_bot.paper.paper_models import (
    VirtualAccount, PaperOrder, PaperOrderIntent, PaperFill, PaperPosition,
    CashLedgerEntry, PaperEquitySnapshot, PaperTrade, PaperEngineRunResult,
    virtual_account_to_dict, paper_order_to_dict, paper_order_intent_to_dict,
    paper_fill_to_dict, paper_position_to_dict, cash_ledger_entry_to_dict,
    paper_equity_snapshot_to_dict, paper_trade_to_dict, paper_engine_run_result_to_dict
)

def paper_store_dir(data_root: Path) -> Path:
    d = data_root / "paper"
    d.mkdir(parents=True, exist_ok=True)
    return d

def build_paper_account_dir(data_root: Path, account_id: str) -> Path:
    safe_id = Path(account_id).name
    d = paper_store_dir(data_root) / "accounts" / safe_id
    d.mkdir(parents=True, exist_ok=True)
    return d

def build_paper_run_dir(data_root: Path, run_id: str) -> Path:
    safe_id = Path(run_id).name
    d = paper_store_dir(data_root) / "runs" / safe_id
    d.mkdir(parents=True, exist_ok=True)
    return d

def _atomic_write_json(path: Path, data: Any) -> Path:
    temp_path = path.with_suffix('.tmp')
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(temp_path, path)
    return path

def _atomic_write_jsonl(path: Path, data_list: List[dict]) -> Path:
    temp_path = path.with_suffix('.tmp')
    with open(temp_path, "w", encoding="utf-8") as f:
        for item in data_list:
            f.write(json.dumps(item) + "\n")
    os.replace(temp_path, path)
    return path

def write_virtual_account_json(path: Path, account: VirtualAccount) -> Path:
    return _atomic_write_json(path, virtual_account_to_dict(account))

def write_paper_orders_jsonl(path: Path, orders: List[PaperOrder]) -> Path:
    return _atomic_write_jsonl(path, [paper_order_to_dict(o) for o in orders])

def write_paper_order_intents_jsonl(path: Path, intents: List[PaperOrderIntent]) -> Path:
    return _atomic_write_jsonl(path, [paper_order_intent_to_dict(i) for i in intents])

def write_paper_fills_jsonl(path: Path, fills: List[PaperFill]) -> Path:
    return _atomic_write_jsonl(path, [paper_fill_to_dict(f) for f in fills])

def write_paper_positions_jsonl(path: Path, positions: List[PaperPosition]) -> Path:
    return _atomic_write_jsonl(path, [paper_position_to_dict(p) for p in positions])

def write_cash_ledger_jsonl(path: Path, entries: List[CashLedgerEntry]) -> Path:
    return _atomic_write_jsonl(path, [cash_ledger_entry_to_dict(e) for e in entries])

def write_paper_equity_snapshots_jsonl(path: Path, snapshots: List[PaperEquitySnapshot]) -> Path:
    return _atomic_write_jsonl(path, [paper_equity_snapshot_to_dict(s) for s in snapshots])

def write_paper_trades_jsonl(path: Path, trades: List[PaperTrade]) -> Path:
    return _atomic_write_jsonl(path, [paper_trade_to_dict(t) for t in trades])

def write_paper_engine_run_result_json(path: Path, result: PaperEngineRunResult) -> Path:
    return _atomic_write_json(path, paper_engine_run_result_to_dict(result))

def read_virtual_account_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def _read_jsonl(path: Path) -> List[Dict[str, Any]]:
    res = []
    if not path.exists():
        return res
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    res.append(json.loads(line))
                except Exception:
                    pass
    return res

def read_paper_orders_jsonl(path: Path) -> List[Dict[str, Any]]:
    return _read_jsonl(path)

def read_paper_fills_jsonl(path: Path) -> List[Dict[str, Any]]:
    return _read_jsonl(path)

def read_paper_engine_run_result_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def list_paper_runs(data_root: Path) -> List[Path]:
    runs_dir = paper_store_dir(data_root) / "runs"
    if not runs_dir.exists():
        return []

    runs = []
    for d in runs_dir.iterdir():
        if d.is_dir():
            runs.append(d)

    return sorted(runs, key=lambda p: p.stat().st_ctime, reverse=True)

def get_latest_paper_run_dir(data_root: Path) -> Optional[Path]:
    runs = list_paper_runs(data_root)
    return runs[0] if runs else None

def paper_store_summary(data_root: Path) -> Dict[str, Any]:
    runs = list_paper_runs(data_root)

    accounts_dir = paper_store_dir(data_root) / "accounts"
    account_count = 0
    if accounts_dir.exists():
        account_count = len([d for d in accounts_dir.iterdir() if d.is_dir()])

    return {
        "total_runs": len(runs),
        "total_accounts": account_count,
        "latest_run": runs[0].name if runs else None
    }
