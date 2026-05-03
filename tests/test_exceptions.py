import pytest
from usa_signal_bot.core.exceptions import (
    USASignalBotError, ConfigError, PathError, DataValidationError, UnsupportedOperationError,
    SignalScoringError, SignalQualityError, SignalConfluenceError, SignalRiskFlagError, SignalQualityGuardError
)

def test_exceptions():
    assert issubclass(ConfigError, USASignalBotError)
    assert issubclass(PathError, USASignalBotError)
    assert issubclass(DataValidationError, USASignalBotError)
    assert issubclass(UnsupportedOperationError, USASignalBotError)
    assert issubclass(SignalScoringError, USASignalBotError)
    assert issubclass(SignalQualityError, USASignalBotError)
    assert issubclass(SignalConfluenceError, USASignalBotError)
    assert issubclass(SignalRiskFlagError, USASignalBotError)
    assert issubclass(SignalQualityGuardError, USASignalBotError)
