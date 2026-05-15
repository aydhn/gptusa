from dataclasses import dataclass
from typing import Any

from usa_signal_bot.core.enums import NotificationType
from usa_signal_bot.regime_map.regime_map_models import RegimeMapReview, RegimeTransitionSignal, SymbolRegimeAlignment

@dataclass
class NotificationMessage:
    notification_type: NotificationType
    channel: str
    subject: str
    body: str

def format_regime_map_report_message(review: RegimeMapReview) -> NotificationMessage:
    from usa_signal_bot.regime_map.regime_map_reporting import regime_map_review_to_text
    return NotificationMessage(
        notification_type=NotificationType.REGIME_MAP_REPORT,
        channel="dry_run",
        subject=f"Regime Map Report: {review.universe_name}",
        body=regime_map_review_to_text(review, limit=10)
    )

def format_regime_transition_warning_message(signals: list[RegimeTransitionSignal]) -> NotificationMessage:
    from usa_signal_bot.regime_map.transition_risk import transition_risk_to_text
    return NotificationMessage(
        notification_type=NotificationType.REGIME_TRANSITION_WARNING,
        channel="dry_run",
        subject="WARNING: Regime Transition Detected",
        body=transition_risk_to_text(signals)
    )

def format_regime_alignment_warning_message(alignments: list[SymbolRegimeAlignment]) -> NotificationMessage:
    body = "Alignment Conflicts:\n"
    for a in alignments:
        if a.status.value in ["CONFLICTED", "DIVERGENT"]:
             body += f"- {a.symbol}: {a.status.value}\n"
    return NotificationMessage(
        notification_type=NotificationType.REGIME_ALIGNMENT_WARNING,
        channel="dry_run",
        subject="WARNING: Regime Alignment Conflicts",
        body=body
    )

def notifications_from_regime_map_review(review: RegimeMapReview) -> list[NotificationMessage]:
    msgs = []
    msgs.append(format_regime_map_report_message(review))

    from usa_signal_bot.regime_map.transition_risk import aggregate_transition_risk
    if review.transition_signals and aggregate_transition_risk(review.transition_signals).value in ["HIGH", "CRITICAL"]:
         msgs.append(format_regime_transition_warning_message(review.transition_signals))

    conflicts = [a for a in review.alignments if a.status.value in ["CONFLICTED", "DIVERGENT"]]
    if conflicts:
         msgs.append(format_regime_alignment_warning_message(conflicts))

    return msgs
