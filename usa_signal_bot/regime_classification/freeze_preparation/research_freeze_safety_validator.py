from typing import Any, Dict, List

try:
    import pandas as pd
except ImportError:
    pd = None

from usa_signal_bot.core.enums import ResearchFreezeRiskFlag
from usa_signal_bot.regime_classification.freeze_preparation.phase134_models import (
    RegimeResearchFreezeContext,
    MonitoringValidationResult,
    DriftReportDocument,
    ResearchFreezePackage,
    ResearchFreezeReadinessGate
)

FORBIDDEN_FRAGMENTS = [
    "buy", "sell", "entry", "exit", "order", "broker", "position",
    "portfolio_weight", "target_weight", "allocation", "paper", "live",
    "demo_order", "live_order", "sent_to_broker", "deploy", "production_patch",
    "kesin al", "kesin sat", "güçlü al", "garanti", "api_key", "token", "secret", "password"
]

def research_freeze_text_has_trade_or_execution_language(text: str) -> bool:
    if not text:
        return False
    lower_text = text.lower()
    # allow 'signal' only if part of technical like macd_signal_9
    if "signal" in lower_text:
        # crude check
        if "macd_signal" not in lower_text and "signal" in lower_text.replace("macd_signal", ""):
            return True

    for frag in FORBIDDEN_FRAGMENTS:
        if frag in lower_text:
            return True
    return False

def validate_regime_research_freeze_context_safety(context: RegimeResearchFreezeContext) -> List[str]:
    errors = []
    if context.activation_allowed:
        errors.append("activation_allowed must be false")
    if context.strategy_activation_allowed:
        errors.append("strategy_activation_allowed must be false")
    if context.deployment_allowed:
        errors.append("deployment_allowed must be false")
    if context.active_paper_enabled:
        errors.append("active_paper_enabled must be false")
    if context.broker_execution_enabled:
        errors.append("broker_execution_enabled must be false")
    if context.order_creation_enabled:
        errors.append("order_creation_enabled must be false")
    if context.paper_state_mutation_enabled:
        errors.append("paper_state_mutation_enabled must be false")
    if context.telegram_real_send_enabled:
        errors.append("telegram_real_send_enabled must be false")
    if context.scraping_enabled:
        errors.append("scraping_enabled must be false")
    if context.html_parse_enabled:
        errors.append("html_parse_enabled must be false")
    if context.paid_api_enabled:
        errors.append("paid_api_enabled must be false")
    if context.dashboard_enabled:
        errors.append("dashboard_enabled must be false")
    if context.network_default_enabled:
        errors.append("network_default_enabled must be false")
    if context.daemon_started:
        errors.append("daemon_started must be false")
    if context.scheduler_enabled:
        errors.append("scheduler_enabled must be false")
    if context.model_training_used:
        errors.append("model_training_used must be false")
    if context.model_prediction_used:
        errors.append("model_prediction_used must be false")
    if context.heavy_ml_dependency_used:
        errors.append("heavy_ml_dependency_used must be false")
    if context.produces_trade_signal:
        errors.append("produces_trade_signal must be false")
    if context.produces_order_decision:
        errors.append("produces_order_decision must be false")
    if context.produces_portfolio_weights:
        errors.append("produces_portfolio_weights must be false")
    if context.investment_advice:
        errors.append("investment_advice must be false")
    return errors

def validate_monitoring_validation_safety(result: MonitoringValidationResult) -> List[str]:
    errors = []
    if result.activation_allowed:
        errors.append("activation_allowed must be false")
    if result.strategy_activation_allowed:
        errors.append("strategy_activation_allowed must be false")
    if result.deployment_allowed:
        errors.append("deployment_allowed must be false")
    if result.model_training_used:
        errors.append("model_training_used must be false")
    if result.model_prediction_used:
        errors.append("model_prediction_used must be false")
    if result.produces_trade_signal:
        errors.append("produces_trade_signal must be false")
    if result.produces_order_decision:
        errors.append("produces_order_decision must be false")
    if result.produces_portfolio_weights:
        errors.append("produces_portfolio_weights must be false")
    if result.investment_advice:
        errors.append("investment_advice must be false")
    return errors

def validate_drift_report_safety(document: DriftReportDocument) -> List[str]:
    errors = []
    if document.investment_advice:
        errors.append("investment_advice must be false")
    if document.produces_trade_signal:
        errors.append("produces_trade_signal must be false")
    if document.produces_order_decision:
        errors.append("produces_order_decision must be false")
    if document.produces_portfolio_weights:
        errors.append("produces_portfolio_weights must be false")
    return errors

def validate_freeze_package_safety(package: ResearchFreezePackage) -> List[str]:
    errors = []
    if package.activation_allowed:
        errors.append("activation_allowed must be false")
    if package.strategy_activation_allowed:
        errors.append("strategy_activation_allowed must be false")
    if package.deployment_allowed:
        errors.append("deployment_allowed must be false")
    if package.model_training_used:
        errors.append("model_training_used must be false")
    if package.model_prediction_used:
        errors.append("model_prediction_used must be false")
    if package.produces_trade_signal:
        errors.append("produces_trade_signal must be false")
    if package.produces_order_decision:
        errors.append("produces_order_decision must be false")
    if package.produces_portfolio_weights:
        errors.append("produces_portfolio_weights must be false")
    if package.investment_advice:
        errors.append("investment_advice must be false")
    return errors

def validate_research_freeze_readiness_gate_safety(gate: ResearchFreezeReadinessGate) -> List[str]:
    errors = []
    if gate.activation_allowed:
        errors.append("activation_allowed must be false")
    if gate.strategy_activation_allowed:
        errors.append("strategy_activation_allowed must be false")
    if gate.deployment_allowed:
        errors.append("deployment_allowed must be false")
    if gate.model_training_used:
        errors.append("model_training_used must be false")
    if gate.model_prediction_used:
        errors.append("model_prediction_used must be false")
    if gate.produces_trade_signal:
        errors.append("produces_trade_signal must be false")
    if gate.produces_order_decision:
        errors.append("produces_order_decision must be false")
    if gate.produces_portfolio_weights:
        errors.append("produces_portfolio_weights must be false")
    if gate.investment_advice:
        errors.append("investment_advice must be false")
    return errors

def validate_research_freeze_dataframe_output_safety(df: Any) -> List[str]:
    errors = []
    columns = df.columns.tolist()
    for col in columns:
        if research_freeze_text_has_trade_or_execution_language(str(col)):
            errors.append(f"Forbidden column name detected: {col}")
    return errors

def collect_research_freeze_risk_flags(context: RegimeResearchFreezeContext | None = None) -> List[ResearchFreezeRiskFlag]:
    flags = set()
    if context:
        flags.update(context.risk_flags)
        flags.update(context.ingestion.risk_flags)
        flags.update(context.monitoring_validation.risk_flags)
        flags.update(context.drift_report.risk_flags)
        flags.update(context.freeze_package.risk_flags)
        flags.update(context.readiness_gate.risk_flags)
    return list(flags)

def research_freeze_safety_summary(errors: List[str]) -> Dict[str, Any]:
    return {
        "valid": len(errors) == 0,
        "error_count": len(errors),
        "errors": errors
    }

def research_freeze_safety_to_text(errors: List[str]) -> str:
    if not errors:
        return "Safety Validation Passed."
    return f"Safety Validation Failed with {len(errors)} errors:\n" + "\n".join(f"- {e}" for e in errors)
