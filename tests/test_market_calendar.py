"""Test market calendar engine."""
from usa_signal_bot.calendar.market_calendar import LocalMarketCalendar
from usa_signal_bot.calendar.holiday_store import default_us_equities_holidays, default_us_equities_early_closes

def test_local_market_calendar():
    holidays = default_us_equities_holidays()
    closes = default_us_equities_early_closes()

    cal = LocalMarketCalendar(holidays=holidays, early_closes=closes)

    # 2024-01-01 was Monday, New Year's Day
    assert cal.is_holiday("2024-01-01") is True
    assert cal.is_trading_day("2024-01-01") is False

    # 2024-01-06 was Saturday
    assert cal.is_weekend("2024-01-06") is True
    assert cal.is_trading_day("2024-01-06") is False

    # 2024-01-02 was Tuesday
    assert cal.is_trading_day("2024-01-02") is True

    # Next trading day after 2023-12-29 (Friday) -> skip weekend -> skip holiday -> 2024-01-02
    # Wait, New Year 2024 was Jan 1. 2023-12-30, 31 weekend.
    assert cal.next_trading_day("2023-12-29") == "2024-01-02"

    # Previous trading day before 2024-01-02
    assert cal.previous_trading_day("2024-01-02") == "2023-12-29"

    # Early close
    # 2024-07-03 in defaults
    assert cal.is_early_close("2024-07-03") is True
    session = cal.session_for_date("2024-07-03")
    assert session.close_time_local == "13:00"

    days = cal.trading_days_between("2024-01-01", "2024-01-03")
    assert days == ["2024-01-02", "2024-01-03"]
