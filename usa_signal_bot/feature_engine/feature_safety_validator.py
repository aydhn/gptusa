from typing import Any
from usa_signal_bot.core.enums import FeatureFoundationRiskFlag
from usa_signal_bot.feature_engine.phase116_models import (
    FeatureFoundationContext, IndicatorDefinition, FeatureDefinition,
    FactorDefinition, FeatureComputationResult
)

def feature_text_has_trade_or_execution_language(text: str) -> bool:
    if not text:
        return False
    s = text.lower()
    unsafe = [
        "buy", "sell", "signal", "order", "broker", "live_order", "paper_order",
        "kesin al", "kesin sat", "garanti", "strong buy", "strong sell", "aktif trading",
        "emir", "canlıya al"
    ]
    return any(u in s for u in unsafe)

def validate_feature_foundation_context_safety(context: FeatureFoundationContext) -> list[str]:
    errors = []
    if context.produces_trade_signal:
        errors.append("Context produces_trade_signal is true")
    if context.produces_order_decision:
        errors.append("Context produces_order_decision is true")
    if context.activation_allowed:
        errors.append("activation_allowed is true")
    if context.active_paper_enabled:
        errors.append("active_paper_enabled is true")
    if context.broker_execution_enabled:
        errors.append("broker_execution_enabled is true")
    if context.order_creation_enabled:
        errors.append("order_creation_enabled is true")
    if context.paper_state_mutation_enabled:
        errors.append("paper_state_mutation_enabled is true")
    if context.telegram_real_send_enabled:
        errors.append("telegram_real_send_enabled is true")
    if context.scraping_enabled:
        errors.append("scraping_enabled is true")
    if context.html_parse_enabled:
        errors.append("html_parse_enabled is true")
    if context.paid_api_enabled:
        errors.append("paid_api_enabled is true")
    if context.dashboard_enabled:
        errors.append("dashboard_enabled is true")
    if context.network_default_enabled:
        errors.append("network_default_enabled is true")
    if context.network_used:
        errors.append("network_used is true")
    if context.paid_api_used:
        errors.append("paid_api_used is true")
    if context.scraping_used:
        errors.append("scraping_used is true")
    if context.html_parsing_used:
        errors.append("html_parsing_used is true")
    if context.broker_used:
        errors.append("broker_used is true")
    if context.order_created:
        errors.append("order_created is true")
    if context.paper_state_mutated:
        errors.append("paper_state_mutated is true")
    if context.telegram_real_sent:
        errors.append("telegram_real_sent is true")
    if context.dashboard_started:
        errors.append("dashboard_started is true")
    return errors

def validate_indicator_definitions_safety(indicators: list[IndicatorDefinition]) -> list[str]:
    errors = []
    for ind in indicators:
        if ind.produces_trade_signal:
            errors.append(f"Indicator {ind.name} produces trade signal")
        if ind.produces_order_decision:
            errors.append(f"Indicator {ind.name} produces order decision")
        if feature_text_has_trade_or_execution_language(ind.name):
            errors.append(f"Indicator name {ind.name} has unsafe language")
        if feature_text_has_trade_or_execution_language(ind.description):
            errors.append(f"Indicator description {ind.name} has unsafe language")
    return errors

def validate_feature_definitions_safety(features: list[FeatureDefinition]) -> list[str]:
    errors = []
    for f in features:
        if f.produces_trade_signal:
            errors.append(f"Feature {f.name} produces trade signal")
        if f.produces_order_decision:
            errors.append(f"Feature {f.name} produces order decision")
        if feature_text_has_trade_or_execution_language(f.name):
            errors.append(f"Feature name {f.name} has unsafe language")
        if feature_text_has_trade_or_execution_language(f.description):
            errors.append(f"Feature description {f.name} has unsafe language")
    return errors

def validate_factor_definitions_safety(factors: list[FactorDefinition]) -> list[str]:
    errors = []
    for f in factors:
        if f.produces_trade_signal:
            errors.append(f"Factor {f.name} produces trade signal")
        if f.produces_order_decision:
            errors.append(f"Factor {f.name} produces order decision")
        if feature_text_has_trade_or_execution_language(f.name):
            errors.append(f"Factor name {f.name} has unsafe language")
        if feature_text_has_trade_or_execution_language(f.description):
            errors.append(f"Factor description {f.name} has unsafe language")
    return errors

def validate_feature_computation_results_safety(results: list[FeatureComputationResult]) -> list[str]:
    errors = []
    for r in results:
        if r.produced_trade_signal:
            errors.append(f"Result {r.result_id} produced trade signal")
        if r.produced_order_decision:
            errors.append(f"Result {r.result_id} produced order decision")
        if r.network_used:
            errors.append(f"Result {r.result_id} used network")
        if r.broker_used:
            errors.append(f"Result {r.result_id} used broker")
        if r.order_created:
            errors.append(f"Result {r.result_id} created order")
        if r.paper_state_mutated:
            errors.append(f"Result {r.result_id} mutated paper state")
    return errors

def collect_feature_foundation_risk_flags(context: FeatureFoundationContext | None = None) -> list[FeatureFoundationRiskFlag]:
    flags = []
    if context:
        flags.extend(context.risk_flags)
    return list(set(flags))

def feature_safety_summary(errors: list[str]) -> dict[str, Any]:
    return {"safe": len(errors) == 0, "error_count": len(errors)}

def feature_safety_to_text(errors: list[str]) -> str:
    if not errors:
        return "Feature Foundation is SAFE."
    return "Feature Foundation Safety Errors:\n" + "\n".join(errors)
