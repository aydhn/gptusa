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

class NotificationMessage:
    pass

def format_backtest_analytics_report_message(review: BacktestAnalyticsFullReview) -> NotificationMessage:
    raise NotImplementedError()

def format_backtest_analytics_warning_message(report: BacktestAnalyticsReport) -> NotificationMessage:
    raise NotImplementedError()

def format_backtest_run_validation_warning_message(report: RunValidationReport) -> NotificationMessage:
    raise NotImplementedError()

def notifications_from_backtest_analytics_review(review: BacktestAnalyticsFullReview) -> list[NotificationMessage]:
    raise NotImplementedError()
