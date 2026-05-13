"""Test trading days helpers."""
from usa_signal_bot.calendar.trading_days import parse_date, format_date, count_trading_days, align_rows_to_trading_days, missing_trading_days_for_rows, non_trading_day_rows
from usa_signal_bot.calendar.market_calendar import LocalMarketCalendar

def test_trading_days_helpers():
    cal = LocalMarketCalendar()
    # 2024-01-02 to 2024-01-05 (Tue-Fri, no holidays typically)
    rows = [
        {"date": "2024-01-02"},
        {"date": "2024-01-04"},
        {"date": "2024-01-06"} # Saturday
    ]

    res = align_rows_to_trading_days(rows, cal)
    assert res["aligned_count"] == 2
    assert "2024-01-03" in res["missing_days"]
    assert "2024-01-06" in res["extra_days"]

    missing = missing_trading_days_for_rows(rows, cal)
    assert "2024-01-03" in missing

    non_trading = non_trading_day_rows(rows, cal)
    assert len(non_trading) == 1
    assert non_trading[0]["date"] == "2024-01-06"
