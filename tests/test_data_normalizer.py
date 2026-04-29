import pytest
import pandas as pd
from usa_signal_bot.data.normalizer import (
    normalize_timestamp_to_utc,
    dataframe_row_to_ohlcv_bar,
    extract_symbol_dataframe,
    normalize_single_symbol_dataframe,
    normalize_yfinance_dataframe
)
from usa_signal_bot.core.exceptions import DataNormalizationError

def test_normalize_timestamp_to_utc():
    ts = pd.Timestamp("2023-01-01 10:00:00")
    utc_str = normalize_timestamp_to_utc(ts)
    assert "2023-01-01T10:00:00+00:00" in utc_str

def test_dataframe_row_to_ohlcv_bar():
    row = pd.Series({"Open": 100, "High": 105, "Low": 95, "Close": 101, "Volume": 1000, "Adj Close": 102})
    ts = pd.Timestamp("2023-01-01 10:00:00")
    bar = dataframe_row_to_ohlcv_bar("AAPL", ts, row, "1d", "yfinance")
    assert bar.symbol == "AAPL"
    assert bar.open == 100.0
    assert bar.adjusted_close == 102.0

def test_dataframe_row_missing_data():
    row = pd.Series({"High": 105, "Low": 95, "Close": 101}) # missing open
    ts = pd.Timestamp("2023-01-01")
    with pytest.raises(DataNormalizationError):
        dataframe_row_to_ohlcv_bar("AAPL", ts, row, "1d", "yf")

def test_extract_symbol_dataframe_single():
    df = pd.DataFrame({"Open": [1], "High": [2], "Low": [1], "Close": [2]})
    res = extract_symbol_dataframe(df, "AAPL")
    assert not res.empty

def test_extract_symbol_dataframe_multi():
    cols = pd.MultiIndex.from_tuples([("Open", "AAPL"), ("Close", "AAPL"), ("Open", "MSFT"), ("Close", "MSFT")])
    df = pd.DataFrame([[1, 2, 3, 4]], columns=cols)
    res = extract_symbol_dataframe(df, "AAPL")
    assert "Open" in res.columns
    assert "Close" in res.columns
    assert list(res["Open"]) == [1]

def test_normalize_single_symbol_dataframe():
    df = pd.DataFrame({
        "Open": [100], "High": [105], "Low": [95], "Close": [101], "Volume": [1000]
    }, index=[pd.Timestamp("2023-01-01")])
    bars = normalize_single_symbol_dataframe(df, "AAPL", "1d")
    assert len(bars) == 1
    assert bars[0].symbol == "AAPL"

def test_normalize_yfinance_dataframe():
    cols = pd.MultiIndex.from_tuples([
        ("Open", "AAPL"), ("High", "AAPL"), ("Low", "AAPL"), ("Close", "AAPL"),
        ("Open", "MSFT"), ("High", "MSFT"), ("Low", "MSFT"), ("Close", "MSFT")
    ])
    df = pd.DataFrame([[100, 105, 95, 101, 200, 205, 195, 201]], columns=cols, index=[pd.Timestamp("2023-01-01")])
    bars = normalize_yfinance_dataframe(df, ["AAPL", "MSFT"], "1d")
    assert len(bars) == 2
    symbols = [b.symbol for b in bars]
    assert "AAPL" in symbols
    assert "MSFT" in symbols
