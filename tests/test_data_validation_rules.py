from usa_signal_bot.data.validation_rules import (
    validate_single_bar, validate_duplicate_bars, validate_bar_sequence,
    validate_missing_symbols, validate_empty_dataset
)
from usa_signal_bot.data.models import OHLCVBar

def test_validate_single_bar_valid():
    bar = OHLCVBar(symbol="AAPL", timestamp_utc="1", timeframe="1d", open=10.0, high=12.0, low=9.0, close=11.0, volume=100.0)
    res = validate_single_bar(bar)
    assert all(r.passed for r in res) or len([r for r in res if not r.passed]) == 0

def test_validate_single_bar_invalid_price():
    bar = OHLCVBar.__new__(OHLCVBar)
    bar.symbol = "AAPL"
    bar.timestamp_utc = "1"
    bar.open = 10.0
    bar.high = 8.0 # < low
    bar.low = 9.0
    bar.close = 11.0
    bar.volume = 100.0

    res = validate_single_bar(bar)
    failed = [r for r in res if not r.passed]
    assert len(failed) > 0
    assert any(r.field == "high" for r in failed)

def test_validate_single_bar_zero_volume():
    bar = OHLCVBar.__new__(OHLCVBar)
    bar.symbol = "AAPL"
    bar.timestamp_utc = "1"
    bar.open = 10.0
    bar.high = 12.0
    bar.low = 9.0
    bar.close = 11.0
    bar.volume = 0.0

    from usa_signal_bot.data.validation_rules import validate_volume
    res = validate_volume(bar, allow_zero_volume=False) # Will emit warning
    warnings = [r for r in res if r.severity.value == "WARNING"]
    assert len(warnings) > 0

def test_validate_duplicate_bars():
    bar1 = OHLCVBar(symbol="AAPL", timestamp_utc="1", timeframe="1d", open=10.0, high=12.0, low=9.0, close=11.0, volume=100.0)
    bar2 = OHLCVBar(symbol="AAPL", timestamp_utc="1", timeframe="1d", open=10.0, high=12.0, low=9.0, close=11.0, volume=100.0)
    res = validate_duplicate_bars([bar1, bar2])
    assert len(res) == 1
    assert not res[0].passed
    assert res[0].rule_name == "duplicate"

def test_validate_missing_symbols():
    bar1 = OHLCVBar(symbol="AAPL", timestamp_utc="1", timeframe="1d", open=10.0, high=12.0, low=9.0, close=11.0, volume=100.0)
    res = validate_missing_symbols([bar1], ["AAPL", "MSFT"])
    assert len(res) == 1
    assert not res[0].passed
    assert res[0].symbol == "MSFT"

def test_validate_empty_dataset():
    res = validate_empty_dataset([])
    assert len(res) == 1
    assert not res[0].passed
    assert res[0].rule_name == "empty_dataset"
