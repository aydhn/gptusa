# Stub for paper_store.py

# Phase 90 integration stub

# Phase 90 integration


# --- Phase 92 ---
# Phase 92

# --- Definitions recovered from git history (deleted by an accidental overwrite) ---
from pathlib import Path
import json
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
import os
from usa_signal_bot.paper.paper_models import VirtualAccount
from usa_signal_bot.paper.paper_models import PaperOrder
from usa_signal_bot.paper.paper_models import PaperOrderIntent
from usa_signal_bot.paper.paper_models import PaperFill
from usa_signal_bot.paper.paper_models import PaperPosition
from usa_signal_bot.paper.paper_models import CashLedgerEntry
from usa_signal_bot.paper.paper_models import PaperEquitySnapshot
from usa_signal_bot.paper.paper_models import PaperTrade
from usa_signal_bot.paper.paper_models import PaperEngineRunResult
from usa_signal_bot.paper.paper_models import virtual_account_to_dict
from usa_signal_bot.paper.paper_models import paper_order_to_dict
from usa_signal_bot.paper.paper_models import paper_order_intent_to_dict
from usa_signal_bot.paper.paper_models import paper_fill_to_dict
from usa_signal_bot.paper.paper_models import paper_position_to_dict
from usa_signal_bot.paper.paper_models import cash_ledger_entry_to_dict
from usa_signal_bot.paper.paper_models import paper_equity_snapshot_to_dict
from usa_signal_bot.paper.paper_models import paper_trade_to_dict
from usa_signal_bot.paper.paper_models import paper_engine_run_result_to_dict


def paper_store_dir(data_root: 'Path') -> 'Path':
    d = data_root / 'paper'
    d.mkdir(parents=True, exist_ok=True)
    return d


def build_paper_account_dir(data_root: 'Path', account_id: 'str') -> 'Path':
    safe_id = Path(account_id).name
    d = paper_store_dir(data_root) / 'accounts' / safe_id
    d.mkdir(parents=True, exist_ok=True)
    return d


def build_paper_run_dir(data_root: 'Path', run_id: 'str') -> 'Path':
    safe_id = Path(run_id).name
    d = paper_store_dir(data_root) / 'runs' / safe_id
    d.mkdir(parents=True, exist_ok=True)
    return d


def _atomic_write_json(path: 'Path', data: 'Any') -> 'Path':
    temp_path = path.with_suffix('.tmp')
    with open(temp_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    os.replace(temp_path, path)
    return path


def _atomic_write_jsonl(path: 'Path', data_list: 'List[dict]') -> 'Path':
    temp_path = path.with_suffix('.tmp')
    with open(temp_path, 'w', encoding='utf-8') as f:
        for item in data_list:
            f.write(json.dumps(item) + '\n')
    os.replace(temp_path, path)
    return path


def write_virtual_account_json(path: 'Path', account: 'VirtualAccount') -> 'Path':
    return _atomic_write_json(path, virtual_account_to_dict(account))


def write_paper_orders_jsonl(path: 'Path', orders: 'List[PaperOrder]') -> 'Path':
    return _atomic_write_jsonl(path, [paper_order_to_dict(o) for o in orders])


def write_paper_fills_jsonl(path: 'Path', fills: 'List[PaperFill]') -> 'Path':
    return _atomic_write_jsonl(path, [paper_fill_to_dict(f) for f in fills])


def write_paper_positions_jsonl(path: 'Path', positions: 'List[PaperPosition]') -> 'Path':
    return _atomic_write_jsonl(path, [paper_position_to_dict(p) for p in positions])


def write_cash_ledger_jsonl(path: 'Path', entries: 'List[CashLedgerEntry]') -> 'Path':
    return _atomic_write_jsonl(path, [cash_ledger_entry_to_dict(e) for e in entries])


def write_paper_equity_snapshots_jsonl(path: 'Path', snapshots: 'List[PaperEquitySnapshot]') -> 'Path':
    return _atomic_write_jsonl(path, [paper_equity_snapshot_to_dict(s) for s in snapshots])


def write_paper_trades_jsonl(path: 'Path', trades: 'List[PaperTrade]') -> 'Path':
    return _atomic_write_jsonl(path, [paper_trade_to_dict(t) for t in trades])


def write_paper_engine_run_result_json(path: 'Path', result: 'PaperEngineRunResult') -> 'Path':
    return _atomic_write_json(path, paper_engine_run_result_to_dict(result))


def read_virtual_account_json(path: 'Path') -> 'Dict[str, Any]':
    if not path.exists():
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def read_paper_engine_run_result_json(path: 'Path') -> 'Dict[str, Any]':
    if not path.exists():
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def list_paper_runs(data_root: 'Path') -> 'List[Path]':
    runs_dir = paper_store_dir(data_root) / 'runs'
    if not runs_dir.exists():
        return []
    runs = []
    for d in runs_dir.iterdir():
        if d.is_dir():
            runs.append(d)
    return sorted(runs, key=lambda p: p.stat().st_ctime, reverse=True)


def paper_store_summary(data_root: 'Path') -> 'Dict[str, Any]':
    runs = list_paper_runs(data_root)
    accounts_dir = paper_store_dir(data_root) / 'accounts'
    account_count = 0
    if accounts_dir.exists():
        account_count = len([d for d in accounts_dir.iterdir() if d.is_dir()])
    return {'total_runs': len(runs), 'total_accounts': account_count, 'latest_run': runs[0].name if runs else None}
