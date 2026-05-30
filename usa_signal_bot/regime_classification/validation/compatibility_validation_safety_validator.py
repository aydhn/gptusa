import pandas as pd
from typing import Any
from usa_signal_bot.core.enums import RegimeContextValidationRiskFlag
from usa_signal_bot.regime_classification.validation.phase132_models import (
    RegimeContextValidationContext,
    CompatibilityValidationResult,
    ConditionalDiagnosticResult,
    RegimeAwareAcceptanceGate
)
from usa_signal_bot.regime_classification.validation.compatibility_validation_schema_validator import validate_no_forbidden_context_validation_columns

def context_validation_text_has_trade_or_execution_language(text: str) -> bool:
    forbidden = [
        "kesin al", "kesin sat", "güçlü al", "güçlü sat", "garanti kâr",
        "emir gönderildi", "aktif trading başladı", "buy", "sell", "execution order"
    ]
    t = text.lower()
    return any(f in t for f in forbidden)

def validate_regime_context_validation_context_safety(context: RegimeContextValidationContext) -> list[str]:
    errors = []
    for attr in [
        "activation_allowed", "strategy_activation_allowed", "deployment_allowed",
        "active_paper_enabled", "broker_execution_enabled", "order_creation_enabled",
        "paper_state_mutation_enabled", "telegram_real_send_enabled", "scraping_enabled",
        "html_parse_enabled", "paid_api_enabled", "dashboard_enabled", "network_default_enabled",
        "model_training_used", "model_prediction_used", "heavy_ml_dependency_used",
        "produces_trade_signal", "produces_order_decision", "produces_portfolio_weights", "investment_advice"
    ]:
        if getattr(context, attr):
            errors.append(f"Unsafe boolean flag detected: {attr} must be false")
    return errors

def validate_compatibility_validation_safety(result: CompatibilityValidationResult) -> list[str]:
    errors = []
    for attr in [
        "activation_allowed", "strategy_activation_allowed", "deployment_allowed",
        "model_training_used", "model_prediction_used", "produces_trade_signal",
        "produces_order_decision", "produces_portfolio_weights", "investment_advice"
    ]:
        if getattr(result, attr):
            errors.append(f"Unsafe boolean flag detected in compatibility result: {attr} must be false")
    return errors

def validate_conditional_diagnostics_safety(items: list[ConditionalDiagnosticResult]) -> list[str]:
    errors = []
    unsafe_actions = ["buy", "sell", "order", "execute", "trade", "broker", "paper", "live", "deploy"]
    for i, item in enumerate(items):
        if context_validation_text_has_trade_or_execution_language(item.diagnostic_text):
            errors.append(f"Execution language found in diagnostic text at idx {i}")

        act = item.recommended_action_type.lower()
        if any(u in act for u in unsafe_actions):
            errors.append(f"Unsafe recommended_action_type '{item.recommended_action_type}' at idx {i}")
    return errors

def validate_regime_acceptance_gate_safety(gate: RegimeAwareAcceptanceGate) -> list[str]:
    errors = []
    for attr in [
        "activation_allowed", "strategy_activation_allowed", "deployment_allowed",
        "model_training_used", "model_prediction_used", "produces_trade_signal",
        "produces_order_decision", "produces_portfolio_weights", "investment_advice"
    ]:
        if getattr(gate, attr):
            errors.append(f"Unsafe boolean flag detected in acceptance gate: {attr} must be false")
    return errors

def validate_context_validation_dataframe_output_safety(df: pd.DataFrame) -> list[str]:
    return validate_no_forbidden_context_validation_columns(list(df.columns))

def collect_regime_context_validation_risk_flags(context: RegimeContextValidationContext | None = None) -> list[RegimeContextValidationRiskFlag]:
    if not context:
        return []
    flags = set()
    flags.update(context.ingestion.risk_flags)
    flags.update(context.validation_result.risk_flags)
    for d in context.conditional_diagnostics:
        flags.update(d.risk_flags)
    flags.update(context.acceptance_gate.risk_flags)
    return list(flags)

def compatibility_validation_safety_summary(errors: list[str]) -> dict[str, Any]:
    return {"safety_violations": len(errors)}

def compatibility_validation_safety_to_text(errors: list[str]) -> str:
    if not errors:
        return "Safety validation passed."
    return f"Safety validation failed with {len(errors)} violations."
