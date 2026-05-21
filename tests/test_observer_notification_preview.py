from usa_signal_bot.paper_observer.notification_preview import (
    build_observer_notification_preview,
    validate_observer_notification_safe
)
from usa_signal_bot.paper_observer.observer_runtime_context import build_mock_observer_runtime_context

def test_build_observer_notification_preview():
    context = build_mock_observer_runtime_context()
    preview = build_observer_notification_preview(context, [])

    assert preview.is_real_order is False
    assert preview.sends_telegram_real is False

    errors = validate_observer_notification_safe(preview)
    assert len(errors) == 0

def test_validate_observer_notification_safe_unsafe_word():
    errors = validate_observer_notification_safe("Bu kesin al emridir.")
    assert len(errors) == 1
    assert "kesin al" in errors[0]
