import pytest
from pathlib import Path
from usa_signal_bot.paper.paper_store import (
    paper_store_dir, build_paper_account_dir, build_paper_run_dir,
    write_virtual_account_json, read_virtual_account_json,
    write_paper_engine_run_result_json, read_paper_engine_run_result_json,
    paper_store_summary
)
from usa_signal_bot.paper.virtual_account import create_virtual_account
from usa_signal_bot.paper.paper_engine import PaperTradingEngine, PaperEngineConfig
from usa_signal_bot.core.enums import PaperExecutionMode

def test_paper_store_dirs(tmp_path):
    root = tmp_path

    sd = paper_store_dir(root)
    assert sd.exists()

    ad = build_paper_account_dir(root, "acct1")
    assert ad.exists()
    assert ad.name == "acct1"

    rd = build_paper_run_dir(root, "run1")
    assert rd.exists()
    assert rd.name == "run1"

def test_write_read_account(tmp_path):
    acct = create_virtual_account("test", 1000.0)
    p = tmp_path / "acct.json"

    write_virtual_account_json(p, acct)
    assert p.exists()

    data = read_virtual_account_json(p)
    assert data["name"] == "test"
    assert data["starting_cash"] == 1000.0

def test_paper_store_summary(tmp_path):
    acct_dir = build_paper_account_dir(tmp_path, "acct1")
    run_dir = build_paper_run_dir(tmp_path, "run1")

    summ = paper_store_summary(tmp_path)
    assert summ["total_accounts"] == 1
    assert summ["total_runs"] == 1
