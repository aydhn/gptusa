from typing import Any, Dict, List, Optional
from usa_signal_bot.provider_freeze.phase114_models import (
    ProviderFreezeContext,
    DataLayerRehearsalReport,
    MultiProviderFinalReviewReport
)

def validate_no_execution_final(
    context: Optional[ProviderFreezeContext] = None,
    rehearsal_report: Optional[DataLayerRehearsalReport] = None,
    review: Optional[MultiProviderFinalReviewReport] = None
) -> List[str]:
    errors = []

    if context:
        if context.activation_allowed: errors.append("Context allows activation.")
        if context.active_paper_enabled: errors.append("Context allows active paper.")
        if context.broker_execution_enabled: errors.append("Context allows broker execution.")
        if context.order_creation_enabled: errors.append("Context allows order creation.")
        if context.paper_state_mutation_enabled: errors.append("Context allows paper mutation.")
        if context.telegram_real_send_enabled: errors.append("Context allows Telegram real send.")
        if context.scraping_enabled: errors.append("Context allows scraping.")
        if context.html_parse_enabled: errors.append("Context allows HTML parsing.")
        if context.paid_api_enabled: errors.append("Context allows paid API.")
        if context.dashboard_enabled: errors.append("Context allows dashboard.")
        if context.network_default_enabled: errors.append("Context allows network default.")

        if context.network_used: errors.append("Context indicates network used.")
        if context.order_created: errors.append("Context indicates order created.")
        if context.paper_state_mutated: errors.append("Context indicates paper mutated.")
        if context.produces_trade_signal: errors.append("Context indicates trade signals produced.")
        if context.produces_order_decision: errors.append("Context indicates order decision produced.")

    if rehearsal_report:
        if rehearsal_report.network_used: errors.append("Rehearsal indicates network used.")
        if rehearsal_report.order_created: errors.append("Rehearsal indicates order created.")
        if rehearsal_report.produces_trade_signal: errors.append("Rehearsal indicates trade signals produced.")

    if review:
        if not review.no_execution_boundary_passed: errors.append("Review indicates no execution boundary failed.")

    return errors

def no_execution_final_passed(errors: List[str]) -> bool:
    return len(errors) == 0

def no_execution_final_summary(errors: List[str]) -> Dict[str, Any]:
    return {
        "valid": len(errors) == 0,
        "error_count": len(errors),
        "errors": errors
    }

def no_execution_final_to_text(errors: List[str]) -> str:
    if not errors:
        return "No-Execution Final Validation Passed."
    return "No-Execution Final Validation Errors:\n" + "\n".join(f" - {e}" for e in errors)
