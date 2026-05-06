from usa_signal_bot.notifications.notification_templates import (
    chunk_message_text,
    sanitize_message_text,
    append_disclaimer,
    format_scan_summary_message
)
from usa_signal_bot.notifications.notification_models import NotificationConfig
from usa_signal_bot.core.enums import NotificationChannel
from usa_signal_bot.runtime.runtime_models import MarketScanResult, MarketScanRequest
from usa_signal_bot.core.enums import RuntimeMode, ScanScope, RuntimeRunStatus

def test_append_disclaimer():
    cfg = NotificationConfig(
        enabled=True,
        default_channel=NotificationChannel.DRY_RUN,
        dry_run=True,
        log_only=True,
        max_message_length=1000,
        max_queue_size=10,
        suppress_duplicates=False,
        duplicate_window_seconds=10,
        rate_limit_per_minute=10,
        include_disclaimer=True,
        disclaimer_text="Test Disclaimer"
    )
    res = append_disclaimer("Body", cfg)
    assert "Test Disclaimer" in res

def test_chunk_message_text():
    text = "A" * 4000
    chunks = chunk_message_text(text, 3500)
    assert len(chunks) == 2
    assert len(chunks[0]) == 3500

def test_sanitize_message_text():
    text = "Markdown *bold* _italic_"
    sanitized = sanitize_message_text(text)
    assert "\\*" in sanitized

def test_format_scan_summary_message():
    req = MarketScanRequest("test", RuntimeMode.DRY_RUN, ScanScope.SMALL_TEST_SET)
    res = MarketScanResult("run1", "now", req, RuntimeRunStatus.COMPLETED)
    res.candidate_count = 5
    msg = format_scan_summary_message(res)
    assert "run1" in msg.title
    assert "Candidates Found:** 5" in msg.body
