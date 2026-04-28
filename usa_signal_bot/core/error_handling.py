"""Standardized error handling utilities."""

import sys
import traceback
from typing import Optional

from usa_signal_bot.core.exceptions import USASignalBotError
from usa_signal_bot.core.events import SystemEvent, create_event
from usa_signal_bot.utils.text_utils import redact_sensitive_text

def is_sensitive_text(text: str) -> bool:
    """Checks if a string contains typical sensitive key words."""
    from usa_signal_bot.utils.text_utils import contains_sensitive_key
    return contains_sensitive_key(text)

def exception_to_safe_message(exc: Exception) -> str:
    """Converts an exception to a string and redacts sensitive information."""
    raw_message = str(exc)
    return redact_sensitive_text(raw_message)

def exception_to_event(exc: Exception, component: str, event_type: str = "RUNTIME_ERROR") -> SystemEvent:
    """Creates a SystemEvent from an exception."""
    safe_msg = exception_to_safe_message(exc)
    severity = "CRITICAL" if isinstance(exc, USASignalBotError) else "ERROR"
    return create_event(
        event_type=event_type,
        severity=severity,
        message=safe_msg,
        component=component,
        details={"exception_type": type(exc).__name__}
    )

def format_error_for_console(exc: Exception, verbose: bool = False) -> str:
    """Formats an error message for console output."""
    safe_msg = exception_to_safe_message(exc)
    error_type = type(exc).__name__

    if verbose:
        tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
        safe_tb = redact_sensitive_text(tb)
        return f"{error_type}: {safe_msg}\n\nTraceback:\n{safe_tb}"

    return f"{error_type}: {safe_msg}"

def handle_cli_exception(exc: Exception) -> int:
    """Handles an exception caught in the CLI and returns an appropriate exit code."""
    safe_msg = exception_to_safe_message(exc)

    if isinstance(exc, USASignalBotError):
        print(f"Error: {safe_msg}", file=sys.stderr)
        return 1
    else:
        print(f"Unexpected Error: {safe_msg}", file=sys.stderr)
        return 2
