import pytest
from usa_signal_bot.universe_lifecycle.missing_history_detector import check_symbol_history, history_rows_first_last_dates
from usa_signal_bot.core.enums import SymbolHistoryStatus
import datetime

def test_history_rows_first_last_dates():
    rows = [
        {"timestamp_utc": "2023-01-01T00:00:00Z"},
        {"timestamp_utc": "2023-01-05T00:00:00Z"}
    ]
    first, last = history_rows_first_last_dates(rows)
    assert first == "2023-01-01"
    assert last == "2023-01-05"

def test_check_symbol_history_missing():
    res = check_symbol_history("AAPL", [])
    assert res.status == SymbolHistoryStatus.MISSING_HISTORY

def test_check_symbol_history_short():
    rows = [{"timestamp_utc": "2026-05-13T16:03:45.160532+00:00"} for _ in range(50)] # less than min 120
    res = check_symbol_history("AAPL", rows, min_rows=120)
    assert res.status == SymbolHistoryStatus.SHORT_HISTORY

def test_check_symbol_history_stale():
    # Make a stale date (100 days ago)
    past = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=100)
    past_str = past.isoformat()
    rows = [{"timestamp_utc": past_str} for _ in range(150)]
    res = check_symbol_history("AAPL", rows, min_rows=120, max_stale_days=14)
    assert res.status == SymbolHistoryStatus.STALE_HISTORY

def test_check_symbol_history_sufficient():
    now = datetime.datetime.now(datetime.timezone.utc)
    past = now - datetime.timedelta(days=200)
    rows = [{"timestamp_utc": (past + datetime.timedelta(days=i)).isoformat()} for i in range(200)]

    res = check_symbol_history("AAPL", rows, min_rows=120, min_history_days=180, max_stale_days=14)
    assert res.status == SymbolHistoryStatus.SUFFICIENT
