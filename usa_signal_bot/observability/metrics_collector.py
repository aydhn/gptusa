from typing import Any, Dict

class PaperObserverMetricsCollector:
    def __init__(self):
        self.metrics = {
            "latest_observer_enrollment_count": 0,
            "latest_observer_enrolled_count": 0,
            "latest_observer_blocked_count": 0,
            "latest_observer_session_count": 0,
            "latest_observer_output_count": 0,
            "latest_observer_drift_event_count": 0,
            "latest_observer_safety_flag_count": 0,
            "latest_observer_locked_runtime_count": 0,
            "paper_observer_warning_count": 0
        }

    def collect_from_observer_review(self, review: Any) -> None:
        # Mock logic
        self.metrics["latest_observer_session_count"] += len(review.sessions)
        for s in review.sessions:
            self.metrics["latest_observer_output_count"] += len(s.outputs)
            self.metrics["latest_observer_drift_event_count"] += len(s.drift_events)
            self.metrics["latest_observer_safety_flag_count"] += len(s.safety_flags)

    def get_metrics(self) -> Dict[str, int]:
        return self.metrics.copy()

observer_metrics_collector = PaperObserverMetricsCollector()
