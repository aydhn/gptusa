import pytest
from usa_signal_bot.data.multitimeframe import (
    TimeframeSpec, MultiTimeframeDataRequest, MultiTimeframeDataResult,
    TimeframeDownloadResult, parse_timeframe_list, default_timeframe_specs,
    build_timeframe_specs_from_list
)
from usa_signal_bot.core.enums import TimeframeRole, PipelineRunStatus

def test_timeframe_spec_valid():
    spec = TimeframeSpec(timeframe="1d", role=TimeframeRole.PRIMARY)
    assert spec.timeframe == "1d"
    assert spec.enabled is True

def test_timeframe_spec_invalid_timeframe():
    with pytest.raises(Exception):
        TimeframeSpec(timeframe="invalid_tf")

def test_multitimeframe_data_request_valid():
    req = MultiTimeframeDataRequest(
        symbols=["AAPL"],
        provider_name="yfinance",
        timeframe_specs=[TimeframeSpec(timeframe="1d")]
    )
    assert len(req.symbols) == 1
    assert req.provider_name == "yfinance"

def test_multitimeframe_data_request_empty_symbols():
    with pytest.raises(ValueError):
        MultiTimeframeDataRequest(
            symbols=[],
            timeframe_specs=[TimeframeSpec(timeframe="1d")]
        )

def test_multitimeframe_data_request_no_enabled_specs():
    with pytest.raises(ValueError):
        MultiTimeframeDataRequest(
            symbols=["AAPL"],
            timeframe_specs=[TimeframeSpec(timeframe="1d", enabled=False)]
        )

def test_parse_timeframe_list():
    assert parse_timeframe_list("1d, 1h, 15m") == ["1d", "1h", "15m"]
    assert parse_timeframe_list("") == []

def test_default_timeframe_specs():
    specs = default_timeframe_specs()
    assert len(specs) == 3
    tfs = [s.timeframe for s in specs]
    assert "1d" in tfs
    assert "1h" in tfs
    assert "15m" in tfs

def test_multitimeframe_data_result_helpers():
    res = MultiTimeframeDataResult(
        results=[
            TimeframeDownloadResult(timeframe="1d", success=True, symbols_returned=["AAPL"]),
            TimeframeDownloadResult(timeframe="1h", success=False, errors=["Error"]),
            TimeframeDownloadResult(timeframe="15m", success=True, symbols_returned=["AAPL", "MSFT"])
        ]
    )

    assert res.successful_timeframes() == ["1d", "15m"]
    assert res.failed_timeframes() == ["1h"]
    assert set(res.symbols_with_any_data()) == {"AAPL", "MSFT"}
