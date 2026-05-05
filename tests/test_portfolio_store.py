import pytest
from pathlib import Path
from usa_signal_bot.portfolio.portfolio_store import (
    portfolio_store_dir, build_portfolio_run_dir,
    write_portfolio_construction_result_json, read_portfolio_construction_result_json,
    write_allocations_jsonl, read_allocations_jsonl, portfolio_store_summary
)
from usa_signal_bot.portfolio.portfolio_models import PortfolioConstructionResult, AllocationRequest, AllocationResult
from usa_signal_bot.core.enums import PortfolioConstructionStatus, AllocationMethod, AllocationStatus

def test_store_creation(tmp_path):
    d = portfolio_store_dir(tmp_path)
    assert d.exists()
    assert d.is_dir()

    r = build_portfolio_run_dir(tmp_path, "run1")
    assert r.exists()
    assert r.is_dir()

def test_write_read_result(tmp_path):
    req = AllocationRequest("r1", [], 100, 100, AllocationMethod.EQUAL_WEIGHT, 0.8, "utc")
    res = PortfolioConstructionResult("run", "utc", PortfolioConstructionStatus.COMPLETED, req, {}, {}, [], [], [], [])

    r = build_portfolio_run_dir(tmp_path, "run1")
    p = r / "result.json"

    write_portfolio_construction_result_json(p, res)
    assert p.exists()

    data = read_portfolio_construction_result_json(p)
    assert data["run_id"] == "run"
    assert data["status"] == "COMPLETED"

def test_write_read_allocations(tmp_path):
    a = AllocationResult("1", "AAPL", "1d", AllocationMethod.EQUAL_WEIGHT, AllocationStatus.ALLOCATED, 0.1, 100, 10, 0.1, 100, False, [], [], [])

    r = build_portfolio_run_dir(tmp_path, "run1")
    p = r / "allocations.jsonl"

    write_allocations_jsonl(p, [a])
    assert p.exists()

    data = read_allocations_jsonl(p)
    assert len(data) == 1
    assert data[0]["symbol"] == "AAPL"

def test_store_summary(tmp_path):
    r1 = build_portfolio_run_dir(tmp_path, "run1")
    req = AllocationRequest("r1", [], 100, 100, AllocationMethod.EQUAL_WEIGHT, 0.8, "utc")
    res = PortfolioConstructionResult("run", "utc", PortfolioConstructionStatus.COMPLETED, req, {}, {}, [], [], [], [])
    write_portfolio_construction_result_json(r1 / "result.json", res)

    summary = portfolio_store_summary(tmp_path)
    assert summary["run_count"] == 1
    assert summary["latest_run"] == "run1"
