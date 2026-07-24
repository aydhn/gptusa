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
    MarketSession,
    validate_market_session,
)


class TestCalendarModelsValidation(unittest.TestCase):
    def _create_valid_session(self, **kwargs):
        base = {
            "session_id": "test_session",
            "calendar_name": CatchAllMockEnum("US_EQUITIES"),
            "date": "2023-01-01",
            "session_type": CatchAllMockEnum("REGULAR"),
            "open_time_local": "09:30",
            "close_time_local": "16:00",
            "timezone": "America/New_York",
            "is_trading_session": True,
            "is_early_close": False,
            "source": CatchAllMockEnum("STATIC_DEFAULT"),
        }
        base.update(kwargs)
        return MarketSession(**base)

    def test_validate_market_session_valid(self):
        """Test that a valid MarketSession passes validation."""
        session = self._create_valid_session()
        validate_market_session(session)

    def test_validate_market_session_empty_timezone(self):
        """Test that an empty timezone raises MarketCalendarError."""
        from usa_signal_bot.core.exceptions import MarketCalendarError

        session = self._create_valid_session(timezone="")
        with self.assertRaises(MarketCalendarError) as context:
            validate_market_session(session)
        self.assertIn("Timezone cannot be empty", str(context.exception))

    def test_validate_market_session_invalid_date(self):
        """Test that an invalid date format raises MarketCalendarError."""
        from usa_signal_bot.core.exceptions import MarketCalendarError

        session = self._create_valid_session(date="2023/01/01")
        with self.assertRaises(MarketCalendarError) as context:
            validate_market_session(session)
        self.assertIn("Invalid date format", str(context.exception))

    def test_validate_market_session_invalid_open_time(self):
        """Test that an invalid open time format raises MarketCalendarError."""
        from usa_signal_bot.core.exceptions import MarketCalendarError

        session = self._create_valid_session(open_time_local="9:30 AM")
        with self.assertRaises(MarketCalendarError) as context:
            validate_market_session(session)
        self.assertIn("Invalid time format", str(context.exception))

    def test_validate_market_session_invalid_close_time(self):
        """Test that an invalid close time format raises MarketCalendarError."""
        from usa_signal_bot.core.exceptions import MarketCalendarError

        session = self._create_valid_session(close_time_local="4:00 PM")
        with self.assertRaises(MarketCalendarError) as context:
            validate_market_session(session)
        self.assertIn("Invalid time format", str(context.exception))

    def test_validate_market_session_close_before_open(self):
        """Test that close time before open time raises MarketCalendarError."""
        from usa_signal_bot.core.exceptions import MarketCalendarError

        session = self._create_valid_session(
            open_time_local="16:00", close_time_local="09:30"
        )
        with self.assertRaises(MarketCalendarError) as context:
            validate_market_session(session)
        self.assertIn("must be after open time", str(context.exception))

    def test_validate_market_session_close_equals_open(self):
        """Test that close time equal to open time raises MarketCalendarError."""
        from usa_signal_bot.core.exceptions import MarketCalendarError

        session = self._create_valid_session(
            open_time_local="12:00", close_time_local="12:00"
        )
        with self.assertRaises(MarketCalendarError) as context:
            validate_market_session(session)
        self.assertIn("must be after open time", str(context.exception))

    def test_validate_market_session_none_times(self):
        """Test that None for open/close times passes validation."""
        session = self._create_valid_session(
            open_time_local=None, close_time_local=None
        )
        validate_market_session(session)

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


    def test_validate_market_holiday_happy_path(self):
        """Test that validating a valid MarketHoliday passes without error."""
        h = MarketHoliday(
            date="2023-01-01",
            name="Valid Holiday",
            calendar_name=CatchAllMockEnum("US_EQUITIES"),
            source=CatchAllMockEnum("STATIC_DEFAULT"),
        )
        validate_market_holiday(h)

    def test_validate_market_holiday_invalid_date(self):
        """Test that validating a MarketHoliday with an invalid date string raises MarketCalendarError."""
        from usa_signal_bot.core.exceptions import MarketCalendarError

        h = MarketHoliday(
            date="2023/01/01",
            name="Invalid Holiday",
            calendar_name=CatchAllMockEnum("US_EQUITIES"),
            source=CatchAllMockEnum("STATIC_DEFAULT"),
        )
        with self.assertRaises(MarketCalendarError) as context:
            validate_market_holiday(h)
        self.assertIn("Invalid date format", str(context.exception))

if __name__ == "__main__":
    unittest.main()
