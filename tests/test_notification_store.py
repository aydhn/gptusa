from pathlib import Path
from usa_signal_bot.notifications.notification_store import build_notification_run_dir, write_notification_dispatch_result_json, notification_store_summary
from usa_signal_bot.notifications.notification_models import NotificationDispatchResult
from usa_signal_bot.core.enums import NotificationDispatchStatus, NotificationChannel

def test_notification_store(tmp_path):
    run_dir = build_notification_run_dir(tmp_path, "dispatch_123")
    assert run_dir.exists()

    res = NotificationDispatchResult(
        dispatch_id="dispatch_123",
        created_at_utc="now",
        status=NotificationDispatchStatus.COMPLETED,
        channel=NotificationChannel.DRY_RUN,
        total_messages=1, sent_count=1, failed_count=0, skipped_count=0, dry_run_count=0, suppressed_count=0,
        results=[], warnings=[], errors=[]
    )

    write_notification_dispatch_result_json(run_dir / "res.json", res)
    assert (run_dir / "res.json").exists()

    summary = notification_store_summary(tmp_path)
    assert summary["total_runs"] == 1
