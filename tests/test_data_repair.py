from usa_signal_bot.data.repair import drop_duplicate_bars, drop_invalid_price_bars, fill_missing_volume_with_zero, repair_ohlcv_bars, repair_report_to_text, write_repair_report_json
from usa_signal_bot.data.models import OHLCVBar

def test_drop_duplicate_bars():
    bar1 = OHLCVBar(symbol="AAPL", timestamp_utc="1", timeframe="1d", open=10.0, high=12.0, low=9.0, close=11.0, volume=100.0)
    bar2 = OHLCVBar(symbol="AAPL", timestamp_utc="1", timeframe="1d", open=10.0, high=12.0, low=9.0, close=11.0, volume=100.0)
    repaired, actions = drop_duplicate_bars([bar1, bar2])
    assert len(repaired) == 1
    assert len(actions) == 1
    assert actions[0].action_type.value == "DROP_DUPLICATE_BAR"

def test_drop_invalid_price_bars():
    bar1 = OHLCVBar(symbol="AAPL", timestamp_utc="1", timeframe="1d", open=10.0, high=12.0, low=9.0, close=11.0, volume=100.0)
    bar2 = OHLCVBar.__new__(OHLCVBar)
    bar2.symbol = "AAPL"
    bar2.timestamp_utc = "2"
    bar2.timeframe = "1d"
    bar2.open = -10.0
    bar2.high = 12.0
    bar2.low = 9.0
    bar2.close = 11.0
    bar2.volume = 100.0

    repaired, actions = drop_invalid_price_bars([bar1, bar2])
    assert len(repaired) == 1
    assert len(actions) == 1
    assert actions[0].action_type.value == "DROP_INVALID_BAR"

def test_fill_missing_volume_with_zero():
    bar = OHLCVBar.__new__(OHLCVBar)
    bar.symbol = "AAPL"
    bar.timestamp_utc = "1"
    bar.timeframe = "1d"
    bar.open = 10.0
    bar.high = 12.0
    bar.low = 9.0
    bar.close = 11.0
    bar.volume = None

    repaired, actions = fill_missing_volume_with_zero([bar])
    assert len(repaired) == 1
    assert repaired[0].volume == 0.0
    assert len(actions) == 1
    assert actions[0].action_type.value == "FILL_MISSING_VOLUME_WITH_ZERO"

def test_repair_ohlcv_bars():
    bar1 = OHLCVBar(symbol="AAPL", timestamp_utc="2", timeframe="1d", open=10.0, high=12.0, low=9.0, close=11.0, volume=100.0)
    bar2 = OHLCVBar(symbol="AAPL", timestamp_utc="1", timeframe="1d", open=10.0, high=12.0, low=9.0, close=11.0, volume=100.0)
    bar3 = OHLCVBar(symbol="AAPL", timestamp_utc="1", timeframe="1d", open=10.0, high=12.0, low=9.0, close=11.0, volume=100.0)

    bars, report = repair_ohlcv_bars([bar1, bar2, bar3])
    assert len(bars) == 2
    assert report.dropped_bar_count == 1
    assert bars[0].timestamp_utc == "1" # sorted

    txt = repair_report_to_text(report)
    assert "Original: 3 | Repaired: 2 | Dropped: 1" in txt

def test_write_repair_report_json(tmp_path):
    bar = OHLCVBar(symbol="AAPL", timestamp_utc="1", timeframe="1d", open=10.0, high=12.0, low=9.0, close=11.0, volume=100.0)
    bars, report = repair_ohlcv_bars([bar])
    path = tmp_path / "repair.json"
    write_repair_report_json(path, report)
    assert path.exists()
