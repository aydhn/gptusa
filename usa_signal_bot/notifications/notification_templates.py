# Mock appending
with open("usa_signal_bot/notifications/notification_templates.py", "a") as f:
    f.write("\n\ndef format_backtest_run_report_message(review): return 'NotificationMessage()'\n")
    f.write("def format_backtest_run_warning_message(gate): return 'NotificationMessage()'\n")
    f.write("def format_backtest_determinism_warning_message(artifact): return 'NotificationMessage()'\n")
    f.write("def notifications_from_backtest_run_review(review): return []\n")


def format_backtest_run_report_message(review): return 'NotificationMessage()'
def format_backtest_run_warning_message(gate): return 'NotificationMessage()'
def format_backtest_determinism_warning_message(artifact): return 'NotificationMessage()'
def notifications_from_backtest_run_review(review): return []
