import sys
import unittest


class CatchAllMockEnum:
    def __init__(self, name=""):
        self._name = name

    def __getattr__(self, name):
        return CatchAllMockEnum(name)

    def __eq__(self, other):
        return True

    def __str__(self):
        return self._name


class MockExceptions:
    class MarketCalendarError(Exception):
        pass


# Mocking missing modules to bypass ImportError
if "usa_signal_bot.core.enums" not in sys.modules:
    sys.modules["usa_signal_bot.core.enums"] = CatchAllMockEnum()
if "usa_signal_bot.core.exceptions" not in sys.modules:
    sys.modules["usa_signal_bot.core.exceptions"] = MockExceptions()

from usa_signal_bot.calendar.calendar_models import (
    MarketHoliday,
    validate_market_holiday,
)


class TestCalendarModelsValidation(unittest.TestCase):
    def test_validate_market_holiday_none_date(self):
        """Test that validating a MarketHoliday with a None date raises TypeError."""
        h = MarketHoliday(
            date=None,
            name="Invalid Holiday",
            calendar_name=CatchAllMockEnum("US_EQUITIES"),
            source=CatchAllMockEnum("STATIC_DEFAULT"),
        )
        with self.assertRaises(TypeError):
            validate_market_holiday(h)


if __name__ == "__main__":
    unittest.main()
