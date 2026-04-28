import pytest
from pathlib import Path
from usa_signal_bot.universe.loader import load_universe_csv, load_universe_from_rows, save_universe_csv
from usa_signal_bot.core.exceptions import UniverseValidationError, UniverseLoadError

def test_load_universe_from_rows():
    rows = [
        {"symbol": "AAPL", "asset_type": "stock"},
        {"symbol": "MSFT", "asset_type": "stock", "active": "false"},
        {"symbol": "AAPL", "asset_type": "stock"}, # Duplicate
        {"symbol": "INVALID STUFF", "asset_type": "stock"}, # Invalid symbol format (will be skipped and error logged)
        {"symbol": "", "asset_type": "stock"} # Empty symbol
    ]

    res = load_universe_from_rows(rows, "test")

    assert res.row_count == 5
    assert res.valid_count == 2
    assert res.duplicate_count == 1
    assert res.invalid_count == 2

    symbols = [s.symbol for s in res.universe.symbols]
    assert symbols == ["AAPL", "MSFT"]
    assert len(res.errors) == 2
    assert len(res.warnings) == 1

def test_load_universe_from_rows_empty():
    rows = []
    with pytest.raises(UniverseValidationError, match="No valid symbols"):
        load_universe_from_rows(rows, "test")

def test_save_and_load_csv(tmp_path):
    rows = [
        {"symbol": "SPY", "asset_type": "etf"},
        {"symbol": "QQQ", "asset_type": "etf"}
    ]

    res1 = load_universe_from_rows(rows, "test")
    p = tmp_path / "test_univ.csv"

    save_universe_csv(p, res1.universe)
    assert p.exists()

    res2 = load_universe_csv(p)
    assert res2.valid_count == 2
    assert res2.universe.symbols[0].symbol == "SPY"
    assert res2.universe.symbols[1].symbol == "QQQ"
