from typing import Any

class MetricsCollector:
    def __init__(self):
        self.metrics = {
            "latest_board_dossier_count": 0,
            "latest_board_dossier_blocked_count": 0,
            "latest_acceptance_board_seal_count": 0,
            "latest_acceptance_board_seal_failed_count": 0,
            "latest_shadow_launch_blocker_event_count": 0,
            "latest_shadow_launch_attempt_blocked_count": 0,
            "latest_shadow_launch_attempt_not_blocked_count": 0,
            "latest_shadow_launch_allowed_violation_count": 0,
            "latest_board_dossier_safety_flag_count": 0,
            "board_dossier_warning_count": 0
        }

    def collect_board_dossier_metrics(self, review: Any) -> None:
        self.metrics["latest_board_dossier_count"] = len(review.dossiers)
        self.metrics["latest_board_dossier_blocked_count"] = sum(1 for d in review.dossiers if d.status.name == "BLOCKED")
        self.metrics["latest_acceptance_board_seal_count"] = len(review.acceptance_board_seals)
        self.metrics["latest_shadow_launch_blocker_event_count"] = len(review.shadow_launch_blocker_events)
        self.metrics["latest_shadow_launch_attempt_blocked_count"] = sum(1 for e in review.shadow_launch_blocker_events if e.blocked)
        self.metrics["latest_shadow_launch_attempt_not_blocked_count"] = sum(1 for e in review.shadow_launch_blocker_events if not e.blocked)
