import subprocess

def test_notification_info_cli():
    result = subprocess.run(["python", "-m", "usa_signal_bot", "notification-info"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "NOTIFICATION CONFIG" in result.stdout

def test_telegram_status_cli():
    result = subprocess.run(["python", "-m", "usa_signal_bot", "telegram-status"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "TELEGRAM CONFIG STATUS" in result.stdout

def test_notification_template_preview_cli():
    result = subprocess.run(["python", "-m", "usa_signal_bot", "notification-template-preview", "--type", "scan_summary"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "PREVIEW TEMPLATE: SCAN_SUMMARY" in result.stdout

def test_notification_dispatch_dry_run_cli():
    result = subprocess.run(["python", "-m", "usa_signal_bot", "notification-dispatch-dry-run", "--count", "2"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "DISPATCH DRY RUN (2 messages)" in result.stdout

def test_notification_send_test_cli():
    result = subprocess.run(["python", "-m", "usa_signal_bot", "notification-send-test"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "SendResult[test_send]" in result.stdout

def test_notification_summary_cli():
    result = subprocess.run(["python", "-m", "usa_signal_bot", "notification-summary"], capture_output=True, text=True)
    assert result.returncode == 0

def test_notification_latest_cli():
    result = subprocess.run(["python", "-m", "usa_signal_bot", "notification-latest"], capture_output=True, text=True)
    assert result.returncode == 0
