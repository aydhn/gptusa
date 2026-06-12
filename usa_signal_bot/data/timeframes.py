from usa_signal_bot.core.enums import TimeFrame
from usa_signal_bot.core.exceptions import DataProviderError

_TIMEFRAME_TO_YFINANCE_MAP = {
    TimeFrame.M1.value: "1m",
    TimeFrame.M5.value: "5m",
    TimeFrame.M15.value: "15m",
    TimeFrame.M30.value: "30m",
    TimeFrame.H1.value: "1h",
    TimeFrame.D1.value: "1d",
    TimeFrame.W1.value: "1wk",
    # Also support common string formats directly
    "1m": "1m",
    "5m": "5m",
    "15m": "15m",
    "30m": "30m",
    "1h": "1h",
    "1d": "1d",
    "1wk": "1wk",
}

_YFINANCE_INTRADAY = {"1m", "5m", "15m", "30m", "1h"}
_YFINANCE_DAILY_UP = {"1d", "1wk"}


def timeframe_to_yfinance_interval(timeframe: str) -> str:
    """Converts a Project TimeFrame or standard string to yfinance interval string."""
    try:
        # Check if it's an enum first
        if hasattr(TimeFrame, timeframe):
            tf_val = TimeFrame[timeframe].value
        else:
            # Could be enum value directly or custom string
            tf_val = timeframe

        interval = _TIMEFRAME_TO_YFINANCE_MAP.get(tf_val)
        if interval is None:
            # Fallback if string is directly passed but not in map (should be rare)
            interval = _TIMEFRAME_TO_YFINANCE_MAP.get(tf_val.lower())

        if interval:
            return interval
        raise DataProviderError(f"Unsupported timeframe for yfinance: {timeframe}")
    except KeyError:
        raise DataProviderError(f"Unsupported timeframe for yfinance: {timeframe}")


def normalize_timeframe(timeframe: str) -> str:
    """Returns the standardized interval representation for internal use, usually matching the yfinance standard format for ease."""
    return timeframe_to_yfinance_interval(timeframe)


def validate_timeframe_for_yfinance(timeframe: str) -> None:
    """Validates if the timeframe is supported by yfinance. Raises DataProviderError if not."""
    timeframe_to_yfinance_interval(timeframe)  # Raises if invalid


def is_intraday_timeframe(timeframe: str) -> bool:
    """Checks if the timeframe is intraday (< 1 day)."""
    interval = timeframe_to_yfinance_interval(timeframe)
    return interval in _YFINANCE_INTRADAY


def is_daily_or_higher_timeframe(timeframe: str) -> bool:
    """Checks if the timeframe is daily or higher (>= 1 day)."""
    interval = timeframe_to_yfinance_interval(timeframe)
    return interval in _YFINANCE_DAILY_UP
