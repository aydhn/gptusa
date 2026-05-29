with open("usa_signal_bot/notifications/notification_templates.py", "r") as f:
    content = f.read()

notif_add = """
from usa_signal_bot.regime_classification.behavior_reporting.phase130_models import (
    MarketBehaviorFullReview, BehaviorReportQaRuleResult, MarketBehaviorProfile
)

def format_market_behavior_report_message(review: MarketBehaviorFullReview) -> NotificationMessage:
    return NotificationMessage(
        title=f"Market Behavior Report: {review.review_id}",
        body=f"Ready for Phase 131: {review.readiness_gate.ready_for_phase131 if review.readiness_gate else False}",
        type="MARKET_BEHAVIOR_REPORT"
    )

def format_behavior_report_qa_warning_message(results: list[BehaviorReportQaRuleResult]) -> NotificationMessage:
    return NotificationMessage(
        title="Behavior Report QA Warning",
        body=f"Failed rules: {len([r for r in results if not r.passed])}",
        type="BEHAVIOR_REPORT_QA_WARNING"
    )

def format_market_behavior_profile_warning_message(profiles: list[MarketBehaviorProfile]) -> NotificationMessage:
    return NotificationMessage(
        title="Market Behavior Profile Warning",
        body=f"Profiles with warnings/errors: {len([p for p in profiles if p.errors or p.warnings])}",
        type="MARKET_BEHAVIOR_PROFILE_WARNING"
    )

def notifications_from_market_behavior_review(review: MarketBehaviorFullReview) -> list[NotificationMessage]:
    msgs = [format_market_behavior_report_message(review)]
    if review.qa_results and not all(r.passed for r in review.qa_results):
        msgs.append(format_behavior_report_qa_warning_message(review.qa_results))
    if any(p.errors or p.warnings for p in review.behavior_profiles):
        msgs.append(format_market_behavior_profile_warning_message(review.behavior_profiles))
    return msgs
"""

if "format_market_behavior_report_message" not in content:
    with open("usa_signal_bot/notifications/notification_templates.py", "a") as f:
        f.write("\n" + notif_add)

print("Updated notification_templates.py")
