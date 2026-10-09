from usa_signal_bot.core import enums, exceptions


def test_recovered_enums_present():
    for name in ("SignalAction", "DataProviderName", "RunLockScope", "RebalanceStatus"):
        assert hasattr(enums, name), name


def test_recovered_exceptions_present_and_raisable():
    for name in ("FeatureFoundationValidationError", "ObserverValidationError", "GovernanceValidationError"):
        cls = getattr(exceptions, name)
        assert issubclass(cls, Exception)
