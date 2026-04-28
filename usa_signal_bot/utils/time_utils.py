"""Time and date utility functions."""

from datetime import datetime, timezone

def utc_now() -> datetime:
    """Returns the current UTC datetime."""
    return datetime.now(timezone.utc)

def local_now() -> datetime:
    """Returns the current local datetime."""
    return datetime.now()

def format_timestamp(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Formats a datetime object as a string."""
    return dt.strftime(fmt)
