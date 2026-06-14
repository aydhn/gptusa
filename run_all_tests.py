import sys
import unittest
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

# mock pytest and pandas
sys.modules['pytest'] = MagicMock()
sys.modules['pandas'] = MagicMock()

if __name__ == "__main__":
    # run specifically on trading_days test
    unittest.main(module=None, argv=['unittest', 'test_trading_days'])
