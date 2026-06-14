import sys
from unittest.mock import MagicMock

class MockEnum(str):
    def __getattr__(self, name):
        return name

class EnumsMock:
    MarketCalendarName = MockEnum("MarketCalendarName")
    MarketSessionType = MockEnum("MarketSessionType")
    MarketDayType = MockEnum("MarketDayType")
    CalendarDataSource = MockEnum("CalendarDataSource")
    TimezoneID = MockEnum("TimezoneID")
    SessionStatus = MockEnum("SessionStatus")
    CalendarActionType = MockEnum("CalendarActionType")
    SessionValidationStatus = MockEnum("SessionValidationStatus")
    CalendarReportType = MockEnum("CalendarReportType")

sys.modules['usa_signal_bot.core.enums'] = EnumsMock

import unittest
from usa_signal_bot.calendar.trading_days import missing_trading_days_for_rows, align_rows_to_trading_days
from usa_signal_bot.calendar.market_calendar import LocalMarketCalendar

class TestTradingDays(unittest.TestCase):
    def test_missing_trading_days_for_rows(self):
        cal = LocalMarketCalendar()
        # Mock trading_days_between
        cal.trading_days_between = MagicMock(return_value=["2023-01-03", "2023-01-04", "2023-01-05"])

        rows = [
            {"date": "2023-01-03"},
            {"timestamp": "2023-01-05T12:00:00"},
        ]

        missing = missing_trading_days_for_rows(rows, cal)
        self.assertEqual(missing, ["2023-01-04"])

if __name__ == "__main__":
    unittest.main()
