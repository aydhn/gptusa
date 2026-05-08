from usa_signal_bot.observability.safety_monitor import build_safety_monitor_report

def test_safety_monitor():
    d = {"project": {"broker_integration_enabled": True}}
    r = build_safety_monitor_report(config_dict=d)
    assert r.status.value == "BLOCKED"
