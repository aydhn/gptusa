import pytest
from pathlib import Path
from usa_signal_bot.core.enums import ComparisonReportType, ComparisonStatus
from usa_signal_bot.comparison.comparison_models import ComparisonRunRequest
from usa_signal_bot.comparison.comparison_engine import PaperBacktestComparisonEngine
import json


def test_engine_empty_sources(tmp_path):
    req = ComparisonRunRequest("test1", ComparisonReportType.FULL_COMPARISON, paper_run_id="missing", backtest_run_id="missing", write_outputs=False)
    engine = PaperBacktestComparisonEngine(tmp_path)

    # Needs to handle missing source gracefully without raising
    # Or in our case since the loader raises an error we catch it
    import pytest
    from usa_signal_bot.core.exceptions import ResultLoaderError
    with pytest.raises(ResultLoaderError):
        res = engine.run(req)

def test_engine_writes_files(tmp_path):
    # Setup fake backtest and paper runs
    p_dir = tmp_path / "paper_runs" / "p1"
    p_dir.mkdir(parents=True)
    with open(p_dir / "paper_trades.jsonl", "w") as f:
        f.write(json.dumps({"symbol": "AAPL", "trade_id": "pt1"}) + "\n")

    b_dir = tmp_path / "backtests" / "b1"
    b_dir.mkdir(parents=True)
    with open(b_dir / "trades.jsonl", "w") as f:
        f.write(json.dumps({"symbol": "AAPL", "id": "bt1"}) + "\n")

    req = ComparisonRunRequest("test1", ComparisonReportType.FULL_COMPARISON, paper_run_id="p1", backtest_run_id="b1", write_outputs=True)
    engine = PaperBacktestComparisonEngine(tmp_path)

    res = engine.run(req)

    assert res.status == ComparisonStatus.COMPLETED
    assert res.paper_source is not None
    assert len(res.matched_trades) == 1

    # check files written
    c_dir = list((tmp_path / "comparison").glob("comparison_*"))
    assert len(c_dir) == 1
    assert (c_dir[0] / "result.json").exists()
    assert (c_dir[0] / "matched_trades.jsonl").exists()
