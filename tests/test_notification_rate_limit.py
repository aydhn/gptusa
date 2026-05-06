from usa_signal_bot.notifications.notification_rate_limit import NotificationRateLimiter

def test_notification_rate_limit():
    rl = NotificationRateLimiter(rate_limit_per_minute=2)

    # 1st msg
    allowed, _ = rl.allow()
    assert allowed
    rl.record_send()

    # 2nd msg
    allowed, _ = rl.allow()
    assert allowed
    rl.record_send()

    # 3rd msg (should fail)
    allowed, _ = rl.allow()
    assert not allowed
