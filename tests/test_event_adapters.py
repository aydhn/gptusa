from usa_signal_bot.observability.event_adapters import observability_event_from_exception

def test_event_from_exception():
    try:
        raise ValueError("Oops")
    except Exception as e:
        ev = observability_event_from_exception("test", e)
        assert "Oops" in ev.message
        assert ev.severity.value == "ERROR"

import unittest.mock
from usa_signal_bot.observability.event_adapters import observability_event_from_runtime_event

def test_observability_event_from_runtime_event_exception():
    class DummyEvent:
        @property
        def event_type(self):
            raise ValueError("Intentional failure")

    with unittest.mock.patch("usa_signal_bot.observability.event_adapters.logger.warning") as mock_warning:
        observability_event_from_runtime_event(DummyEvent())
        mock_warning.assert_called_once()
        args, _ = mock_warning.call_args
        assert args[0] == "Failed to extract event_type from runtime_event: %s"
        assert isinstance(args[1], ValueError)
