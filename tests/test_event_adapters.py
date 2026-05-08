from usa_signal_bot.observability.event_adapters import observability_event_from_exception

def test_event_from_exception():
    try:
        raise ValueError("Oops")
    except Exception as e:
        ev = observability_event_from_exception("test", e)
        assert "Oops" in ev.message
        assert ev.severity.value == "ERROR"
