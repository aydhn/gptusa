from typing import Any, Dict, List
from usa_signal_bot.provider_freeze.phase114_models import (
    MultiProviderFinalReviewReport,
    DataLayerRehearsalReport
)
from usa_signal_bot.provider_freeze.freeze_safety_validator import freeze_text_has_trade_or_execution_language

def validate_multi_provider_final_review_safety(report: MultiProviderFinalReviewReport) -> List[str]:
    errors = []
    if report.produces_trade_signal: errors.append("Review indicates trade signals produced.")
    if report.produces_order_decision: errors.append("Review indicates order decisions produced.")
    if not report.no_execution_boundary_passed: errors.append("No execution boundary failed in review.")
    if not report.no_broker_order_boundary_passed: errors.append("No broker/order boundary failed in review.")

    for item in report.items:
        if freeze_text_has_trade_or_execution_language(item.rationale):
            errors.append(f"Review item {item.name} rationale contains execution language.")

    return errors

def validate_rehearsal_final_review_safety(report: DataLayerRehearsalReport) -> List[str]:
    errors = []
    if report.produces_trade_signal: errors.append("Rehearsal indicates trade signals produced.")
    if report.produces_order_decision: errors.append("Rehearsal indicates order decisions produced.")
    if report.network_used or report.paid_api_used or report.scraping_used or report.html_parsing_used or report.broker_used or report.order_created or report.paper_state_mutated or report.telegram_real_sent or report.dashboard_started:
        errors.append("Rehearsal violated execution boundaries.")

    for step in report.steps:
        if freeze_text_has_trade_or_execution_language(step.message):
            errors.append(f"Rehearsal step {step.step_name} message contains execution language.")

    return errors

def final_review_text_has_trade_or_advice_language(text: str) -> bool:
    return freeze_text_has_trade_or_execution_language(text)

def final_review_safety_summary(errors: List[str]) -> Dict[str, Any]:
    return {
        "valid": len(errors) == 0,
        "error_count": len(errors),
        "errors": errors
    }

def final_review_safety_to_text(errors: List[str]) -> str:
    if not errors:
        return "Final Review Safety Validation Passed."
    return "Final Review Safety Validation Errors:\n" + "\n".join(f" - {e}" for e in errors)
