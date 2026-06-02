import pytest
from pathlib import Path
from usa_signal_bot.backtesting.backtest_foundation_store import (
    backtest_foundation_store_dir,
    write_backtest_foundation_full_review_json,
    read_backtest_foundation_full_review_json
)
from usa_signal_bot.backtesting.backtest_foundation_report import build_backtest_foundation_full_review

def test_store(tmp_path):
    d = backtest_foundation_store_dir(tmp_path)
    assert d.exists()

    rev = build_backtest_foundation_full_review()
    p = d / "test.json"
    write_backtest_foundation_full_review_json(p, rev)

    loaded = read_backtest_foundation_full_review_json(p)
    assert loaded["review_id"] == rev.review_id
