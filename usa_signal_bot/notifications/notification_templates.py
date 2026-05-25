
from usa_signal_bot.event_impact.phase112_models import EventImpactFullReview, CalendarAwareValidationResult, MacroRegimeMetadata

def format_event_impact_report_message(review: EventImpactFullReview) -> str:
    return f"Event Impact Report: {review.review_id}"

def format_calendar_validation_warning_message(results: list[CalendarAwareValidationResult]) -> str:
    return f"Calendar Validation Warnings: {len(results)}"

def format_macro_regime_metadata_warning_message(items: list[MacroRegimeMetadata]) -> str:
    return f"Macro Regime Warnings: {len(items)}"

def notifications_from_event_impact_review(review: EventImpactFullReview) -> list[str]:
    return [format_event_impact_report_message(review)]
