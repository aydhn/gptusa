"""Core primitives: enums, exceptions, config, types, paths.

Boundary: depends on nothing else in usa_signal_bot. Heavy modules (e.g. ``health``) are
intentionally not imported here; import them from their own module.
"""

from usa_signal_bot.core.enums import DataProviderName, RunLockScope, SignalAction
from usa_signal_bot.core.exceptions import USASignalBotError

__all__ = ["DataProviderName", "RunLockScope", "SignalAction", "USASignalBotError"]
