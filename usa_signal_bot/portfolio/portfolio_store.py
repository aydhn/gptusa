import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import os

from usa_signal_bot.portfolio.portfolio_models import (
    PortfolioConstructionResult,
    PortfolioBasket,
    AllocationResult,
    PortfolioCandidate,
    portfolio_construction_result_to_dict,
    portfolio_basket_to_dict,
    allocation_result_to_dict,
    portfolio_candidate_to_dict
)
from usa_signal_bot.portfolio.risk_budgeting import RiskBudgetReport, risk_budget_report_to_dict
from usa_signal_bot.portfolio.concentration_guards import ConcentrationReport, concentration_report_to_dict
from usa_signal_bot.portfolio.portfolio_validation import PortfolioValidationReport

def portfolio_store_dir(data_root: Path) -> Path:
    from usa_signal_bot.core.exceptions import PortfolioStorageError
    try:
        p = data_root / "portfolio"
        p.mkdir(parents=True, exist_ok=True)
        return p
    except Exception as e:
        raise PortfolioStorageError(f"Failed to create portfolio store dir: {e}")

def build_portfolio_run_dir(data_root: Path, run_id: str) -> Path:
    from usa_signal_bot.core.exceptions import PortfolioStorageError
    if ".." in run_id or "/" in run_id or "\\" in run_id:
        raise PortfolioStorageError(f"Invalid run_id for path: {run_id}")

    run_dir = portfolio_store_dir(data_root) / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir

def _atomic_write_json(path: Path, data: dict) -> Path:
    temp_path = path.with_suffix(".tmp.json")
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(temp_path, path)
    return path

def _atomic_write_jsonl(path: Path, data: List[dict]) -> Path:
    temp_path = path.with_suffix(".tmp.jsonl")
    with open(temp_path, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item) + "\n")
    os.replace(temp_path, path)
    return path

def write_portfolio_construction_result_json(path: Path, result: PortfolioConstructionResult) -> Path:
    data = portfolio_construction_result_to_dict(result)
    return _atomic_write_json(path, data)

def write_portfolio_basket_json(path: Path, basket: PortfolioBasket) -> Path:
    data = portfolio_basket_to_dict(basket)
    return _atomic_write_json(path, data)

def write_allocations_jsonl(path: Path, allocations: List[AllocationResult]) -> Path:
    data = [allocation_result_to_dict(a) for a in allocations]
    return _atomic_write_jsonl(path, data)

def write_portfolio_candidates_jsonl(path: Path, candidates: List[PortfolioCandidate]) -> Path:
    data = [portfolio_candidate_to_dict(c) for c in candidates]
    return _atomic_write_jsonl(path, data)

def write_risk_budget_report_json(path: Path, report: RiskBudgetReport) -> Path:
    data = risk_budget_report_to_dict(report)
    return _atomic_write_json(path, data)

def write_concentration_report_json(path: Path, report: ConcentrationReport) -> Path:
    data = concentration_report_to_dict(report)
    return _atomic_write_json(path, data)

def write_portfolio_validation_report_json(path: Path, report: PortfolioValidationReport) -> Path:
    from dataclasses import asdict
    data = asdict(report)
    return _atomic_write_json(path, data)

def read_portfolio_construction_result_json(path: Path) -> dict:
    from usa_signal_bot.core.exceptions import PortfolioStorageError
    if not path.exists():
        raise PortfolioStorageError(f"Result file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def read_allocations_jsonl(path: Path) -> List[dict]:
    from usa_signal_bot.core.exceptions import PortfolioStorageError
    if not path.exists():
        raise PortfolioStorageError(f"Allocations file not found: {path}")
    data = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(json.loads(line))
    return data

def list_portfolio_runs(data_root: Path) -> List[Path]:
    store_dir = portfolio_store_dir(data_root)
    runs = []
    for item in store_dir.iterdir():
        if item.is_dir() and (item / "result.json").exists():
            runs.append(item)
    return sorted(runs, key=lambda p: p.stat().st_mtime, reverse=True)

def get_latest_portfolio_run_dir(data_root: Path) -> Optional[Path]:
    runs = list_portfolio_runs(data_root)
    if not runs:
        return None
    return runs[0]

def portfolio_store_summary(data_root: Path) -> dict:
    runs = list_portfolio_runs(data_root)
    return {
        "run_count": len(runs),
        "latest_run": runs[0].name if runs else None,
        "store_path": str(portfolio_store_dir(data_root))
    }
