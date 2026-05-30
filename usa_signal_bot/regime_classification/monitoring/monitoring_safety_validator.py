from typing import Any, Dict, List
import pandas as pd
from usa_signal_bot.regime_classification.monitoring.phase133_models import (
    RegimeMonitoringContext,
    RegimeMonitoringBaseline,
    RegimeMonitoringSnapshot,
    RegimeDriftTrackingResult,
    ContextDegradationDiagnostic,
    RegimeMonitoringReadinessGate,
    RegimeMonitoringRiskFlag
)
from usa_signal_bot.regime_classification.monitoring.monitoring_schema_validator import validate_no_forbidden_monitoring_columns

def monitoring_text_has_trade_or_execution_language(text: str) -> bool:
    unsafe_words = ["buy_signal", "sell_signal", "entry", "exit", "order", "portfolio_weight", "target_weight", "allocation", "live_order", "demo_order", "kesin al", "garanti"]
    text_lower = text.lower()
    return any(w in text_lower for w in unsafe_words)

def validate_regime_monitoring_context_safety(context: RegimeMonitoringContext) -> List[str]:
    errors = []
    if context.activation_allowed: errors.append("activation_allowed is true")
    if context.strategy_activation_allowed: errors.append("strategy_activation_allowed is true")
    if context.deployment_allowed: errors.append("deployment_allowed is true")
    if context.active_paper_enabled: errors.append("active_paper_enabled is true")
    if context.broker_execution_enabled: errors.append("broker_execution_enabled is true")
    if context.order_creation_enabled: errors.append("order_creation_enabled is true")
    if context.paper_state_mutation_enabled: errors.append("paper_state_mutation_enabled is true")
    if context.telegram_real_send_enabled: errors.append("telegram_real_send_enabled is true")
    if context.scraping_enabled: errors.append("scraping_enabled is true")
    if context.html_parse_enabled: errors.append("html_parse_enabled is true")
    if context.paid_api_enabled: errors.append("paid_api_enabled is true")
    if context.dashboard_enabled: errors.append("dashboard_enabled is true")
    if context.network_default_enabled: errors.append("network_default_enabled is true")
    if context.model_training_used: errors.append("model_training_used is true")
    if context.model_prediction_used: errors.append("model_prediction_used is true")
    if context.heavy_ml_dependency_used: errors.append("heavy_ml_dependency_used is true")
    if context.produces_trade_signal: errors.append("produces_trade_signal is true")
    if context.produces_order_decision: errors.append("produces_order_decision is true")
    if context.produces_portfolio_weights: errors.append("produces_portfolio_weights is true")
    if context.investment_advice: errors.append("investment_advice is true")
    if not context.metadata_only: errors.append("metadata_only is false")
    if not context.research_data_only: errors.append("research_data_only is false")
    return errors

def validate_monitoring_baseline_safety(item: RegimeMonitoringBaseline) -> List[str]:
    errors = []
    if item.produces_trade_signal: errors.append("produces_trade_signal is true")
    return errors

def validate_monitoring_snapshot_safety(item: RegimeMonitoringSnapshot) -> List[str]:
    errors = []
    if item.produces_trade_signal: errors.append("produces_trade_signal is true")
    return errors

def validate_drift_tracking_safety(result: RegimeDriftTrackingResult) -> List[str]:
    errors = []
    if result.produces_trade_signal: errors.append("produces_trade_signal is true")
    return errors

def validate_context_degradation_safety(items: List[ContextDegradationDiagnostic]) -> List[str]:
    errors = []
    allowed_actions = ["research_review", "data_quality_review", "documentation_review", "monitor_context", "baseline_refresh_review"]
    for i in items:
        if i.produces_trade_signal: errors.append(f"{i.diagnostic_id} produces_trade_signal is true")
        if i.recommended_action_type not in allowed_actions:
            errors.append(f"{i.diagnostic_id} has unsafe recommended action: {i.recommended_action_type}")
    return errors

def validate_monitoring_readiness_gate_safety(gate: RegimeMonitoringReadinessGate) -> List[str]:
    errors = []
    if gate.produces_trade_signal: errors.append("produces_trade_signal is true")
    return errors

def validate_monitoring_dataframe_output_safety(df: pd.DataFrame) -> List[str]:
    return validate_no_forbidden_monitoring_columns(list(df.columns))

def collect_regime_monitoring_risk_flags(context: RegimeMonitoringContext = None) -> List[RegimeMonitoringRiskFlag]:
    flags = []
    if context:
        flags.extend(context.risk_flags)
    return list(set(flags))

def monitoring_safety_summary(errors: List[str]) -> Dict[str, Any]:
    return {"error_count": len(errors)}

def monitoring_safety_to_text(errors: List[str]) -> str:
    return f"Safety Errors: {len(errors)}"
