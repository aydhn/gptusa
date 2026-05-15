from typing import Any

class MetricsCollector:
    def __init__(self):
        self.metrics = {}

    def record_regime_map_metrics(self, review: Any) -> None:
        if not review:
            return

        if review.cross_sectional_map:
             self.metrics["latest_cross_sectional_regime"] = review.cross_sectional_map.cross_sectional_regime.value
             self.metrics["latest_breadth_regime"] = review.cross_sectional_map.breadth_regime.value

        if review.transition_signals:
             from usa_signal_bot.regime_map.transition_risk import aggregate_transition_risk
             self.metrics["latest_regime_transition_risk"] = aggregate_transition_risk(review.transition_signals).value
             self.metrics["high_transition_risk_count"] = sum(1 for s in review.transition_signals if s.risk.value in ["HIGH", "CRITICAL"])

        conflicts = sum(1 for a in review.alignments if a.status.value in ["CONFLICTED", "DIVERGENT"])
        self.metrics["regime_alignment_conflict_count"] = conflicts
        self.metrics["confirmed_regime_count"] = sum(1 for c in review.timeframe_confirmations if c.status.value == "CONFIRMED")
        self.metrics["regime_map_warning_count"] = len(review.warnings)
