# Stub for notification_templates.py
class NotificationMessage:
    def __init__(self, type_str, content):
        self.type_str = type_str
        self.content = content

def format_paper_readiness_board_report_message(review) -> str:
    return "paper-readiness board review required"
def format_write_blocked_adapter_warning_message(proofs) -> str:
    return "write blocked warning"
def format_activation_firewall_warning_message(events) -> str:
    return "activation firewall warning"
def notifications_from_paper_readiness_board_review(review) -> list:
    return [format_paper_readiness_board_report_message(review)]


from usa_signal_bot.paper_no_write_admission.no_write_admission_models import NoWriteAdmissionFullReview, ActivationReplayResult, PaperModePreflightRun
def format_no_write_admission_report_message(review: NoWriteAdmissionFullReview) -> NotificationMessage:
    return NotificationMessage(message_type=NotificationType.NO_WRITE_ADMISSION_REPORT, content="Report")

def format_activation_replay_warning_message(results: list[ActivationReplayResult]) -> NotificationMessage:
    return NotificationMessage(message_type=NotificationType.ACTIVATION_REPLAY_WARNING, content="Warning")

def format_paper_mode_preflight_warning_message(preflights: list[PaperModePreflightRun]) -> NotificationMessage:
    return NotificationMessage(message_type=NotificationType.PAPER_MODE_PREFLIGHT_WARNING, content="Warning")

def notifications_from_no_write_admission_review(review: NoWriteAdmissionFullReview) -> list[NotificationMessage]:
    return []

def format_dry_admission_report_message(review: dict) -> dict:
    return {
        "title": "Dry Admission Report",
        "message": "Dry admission review required. This is NOT a live activation.",
        "urgency": "high",
        "metadata": {"review_id": review.get("review_id")}
    }
def format_write_lock_refresh_warning_message(refreshes: list) -> dict:
    return {
        "title": "Write Lock Refresh Warning",
        "message": "Write lock refresh warnings detected.",
        "urgency": "medium",
        "metadata": {"count": len(refreshes)}
    }
def format_human_approval_ledger_warning_message(ledgers: list) -> dict:
    return {
        "title": "Human Approval Ledger Warning",
        "message": "Human approval ledger warnings detected.",
        "urgency": "medium",
        "metadata": {"count": len(ledgers)}
    }
def notifications_from_dry_admission_review(review: dict) -> list:
    return [format_dry_admission_report_message(review)]
