import pytest
from usa_signal_bot.advanced_runtime.notification_boundary_normalizer import normalize_notification_boundary

def test_notif():
    res = normalize_notification_boundary({})
    assert res["dry_run"] is True
