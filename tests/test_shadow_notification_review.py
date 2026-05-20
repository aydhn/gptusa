def test_notification():
    from usa_signal_bot.paper_shadow_governance.notification_review import review_shadow_notification_preview
    r = review_shadow_notification_preview({})
    assert r["safe"]
