from typing import Any
from usa_signal_bot.core.enums import ProviderOrchestrationRiskFlag
from usa_signal_bot.provider_orchestration.phase110_models import (
    ProviderOrchestrationContext, ProviderRouteResult, DataAvailabilityReport
)

def validate_provider_orchestration_context_safety(context: ProviderOrchestrationContext) -> list[str]:
    errors = []
    if context.produces_trade_signal: errors.append("produces_trade_signal must be False")
    if context.produces_order_decision: errors.append("produces_order_decision must be False")
    if context.network_used: errors.append("network_used must be False")
    if context.paid_api_used: errors.append("paid_api_used must be False")
    if context.scraping_used: errors.append("scraping_used must be False")
    if context.html_parsing_used: errors.append("html_parsing_used must be False")
    if context.broker_used: errors.append("broker_used must be False")
    if context.order_created: errors.append("order_created must be False")
    if context.paper_state_mutated: errors.append("paper_state_mutated must be False")
    if context.telegram_real_sent: errors.append("telegram_real_sent must be False")
    if context.dashboard_started: errors.append("dashboard_started must be False")
    return errors

def validate_route_results_safety(results: list[ProviderRouteResult]) -> list[str]:
    errors = []
    for r in results:
        if r.network_used: errors.append(f"Route {r.route_plan_id}: network_used must be False")
        if r.broker_used: errors.append(f"Route {r.route_plan_id}: broker_used must be False")
        if r.order_created: errors.append(f"Route {r.route_plan_id}: order_created must be False")
        if r.paper_state_mutated: errors.append(f"Route {r.route_plan_id}: paper_state_mutated must be False")
    return errors

def validate_availability_report_safety(report: DataAvailabilityReport) -> list[str]:
    errors = []
    if report.network_used: errors.append("network_used must be False")
    if report.paid_api_used: errors.append("paid_api_used must be False")
    if report.scraping_used: errors.append("scraping_used must be False")
    if report.html_parsing_used: errors.append("html_parsing_used must be False")
    return errors

def collect_provider_orchestration_risk_flags(context: ProviderOrchestrationContext | None = None) -> list[ProviderOrchestrationRiskFlag]:
    flags = []
    if not context: return flags
    if context.produces_trade_signal: flags.append(ProviderOrchestrationRiskFlag.TRADE_SIGNAL_LANGUAGE_RISK)
    if context.produces_order_decision: flags.append(ProviderOrchestrationRiskFlag.ORDER_RISK)
    if context.network_used: flags.append(ProviderOrchestrationRiskFlag.NETWORK_FETCH_ATTEMPTED)
    if context.broker_used: flags.append(ProviderOrchestrationRiskFlag.BROKER_RISK)
    if context.paper_state_mutated: flags.append(ProviderOrchestrationRiskFlag.PAPER_MUTATION_RISK)
    if context.telegram_real_sent: flags.append(ProviderOrchestrationRiskFlag.TELEGRAM_REAL_SEND_RISK)
    return list(set(flags))

def provider_orchestration_safety_summary(errors: list[str]) -> dict[str, Any]:
    return {"safe": len(errors) == 0, "error_count": len(errors)}

def provider_orchestration_safety_to_text(errors: list[str]) -> str:
    if not errors: return "Provider Orchestration Context is SAFE."
    return "Provider Orchestration Context is UNSAFE:\n" + "\n".join(errors)
