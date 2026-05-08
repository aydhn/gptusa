import pytest
from pathlib import Path
from usa_signal_bot.regression.golden_fixtures import (
    generate_deterministic_ohlcv_rows,
    generate_golden_ohlcv_dataset,
    generate_golden_signal_records,
    generate_golden_candidate_records,
    generate_golden_risk_decision_records,
    generate_golden_portfolio_allocation_records,
    write_golden_fixture_files,
    calculate_fixture_checksum
)
from usa_signal_bot.regression.regression_models import GoldenDatasetSpec, GoldenDatasetStatus

def test_deterministic_ohlcv_rows():
    rows1 = generate_deterministic_ohlcv_rows("AAPL", "2024-01-01", 10, 150.0)
    rows2 = generate_deterministic_ohlcv_rows("AAPL", "2024-01-01", 10, 150.0)
    assert rows1 == rows2
    assert len(rows1) == 10

    # check OHLCV consistency
    for r in rows1:
        assert r["high"] >= max(r["open"], r["close"])
        assert r["low"] <= min(r["open"], r["close"])
        assert r["volume"] > 0

def test_golden_ohlcv_dataset():
    ds = generate_golden_ohlcv_dataset(["AAPL", "SPY"], "2024-01-01", 5)
    assert "AAPL" in ds
    assert "SPY" in ds
    assert len(ds["AAPL"]) == 5

def test_golden_signal_records():
    sigs = generate_golden_signal_records(["AAPL", "SPY"])
    assert len(sigs) == 2
    assert sigs[0]["symbol"] in ["AAPL", "SPY"]

def test_golden_candidate_records():
    cands = generate_golden_candidate_records(["AAPL", "SPY"])
    assert len(cands) == 2
    assert "score" in cands[0]

def test_golden_risk_decision_records():
    risks = generate_golden_risk_decision_records(["AAPL", "SPY"])
    assert len(risks) == 2
    assert "approved" in risks[0]

def test_golden_portfolio_allocation_records():
    allocs = generate_golden_portfolio_allocation_records(["AAPL", "SPY"])
    # May only allocate to half, but length should be > 0
    assert len(allocs) > 0

def test_write_golden_fixture_files(tmp_path):
    spec = GoldenDatasetSpec(
        dataset_id="test", name="test_ds", symbols=["AAPL"], timeframe="1d",
        start_date="2024-01-01", end_date="2024-01-10", row_count_per_symbol=5,
        status=GoldenDatasetStatus.CREATED, created_at_utc="now"
    )
    paths = write_golden_fixture_files(tmp_path, spec)
    assert "ohlcv_AAPL" in paths
    assert "signals" in paths
    assert "candidates" in paths
    assert "risk_decisions" in paths
    assert "allocations" in paths

    assert Path(paths["ohlcv_AAPL"]).exists()

def test_checksum_deterministic():
    data = {"a": 1, "b": [1, 2, 3]}
    cs1 = calculate_fixture_checksum(data)
    cs2 = calculate_fixture_checksum(data)
    assert cs1 == cs2
