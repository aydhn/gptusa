import pytest
from pathlib import Path
import json
from usa_signal_bot.core.exceptions import ResultLoaderError
from usa_signal_bot.comparison.result_loaders import (
    load_paper_run_for_comparison, load_backtest_run_for_comparison,
    load_basket_run_for_comparison, load_scan_run_for_comparison,
    load_signal_file_for_drift, normalize_trade_records,
    normalize_order_records, normalize_fill_records
)

def test_load_paper_run(tmp_path):
    d = tmp_path / "paper_run"
    d.mkdir()

    with open(d / "paper_trades.jsonl", "w") as f:
        f.write(json.dumps({"symbol": "AAPL", "trade_id": "t1"}) + "\n")

    with open(d / "performance_report.json", "w") as f:
        f.write(json.dumps({"total_return_pct": 5.0}))

    res = load_paper_run_for_comparison(d)
    assert res.source_summary.record_count == 1
    assert res.source_summary.symbols == ["AAPL"]
    assert "performance" in res.records

def test_load_backtest_run(tmp_path):
    d = tmp_path / "bt_run"
    d.mkdir()

    with open(d / "trades.jsonl", "w") as f:
        f.write(json.dumps({"symbol": "MSFT", "id": "t2"}) + "\n")

    res = load_backtest_run_for_comparison(d)
    assert res.source_summary.record_count == 1
    assert res.source_summary.symbols == ["MSFT"]

def test_missing_path():
    with pytest.raises(ResultLoaderError):
        load_paper_run_for_comparison(Path("/does/not/exist"))

def test_normalizers():
    recs = {"trades": [{"id": 1}], "orders": [{"id": 2}], "fills": [{"id": 3}]}
    assert len(normalize_trade_records(recs, None)) == 1
    assert len(normalize_order_records(recs, None)) == 1
    assert len(normalize_fill_records(recs, None)) == 1
