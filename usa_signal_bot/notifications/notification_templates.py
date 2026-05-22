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
