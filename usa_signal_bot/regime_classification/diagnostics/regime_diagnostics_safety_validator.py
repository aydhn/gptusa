import pandas as pd
import re
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.exceptions import RegimeDiagnosticsSafetyValidationError
from usa_signal_bot.core.enums import RegimeTransitionRiskFlag
from usa_signal_bot.regime_classification.diagnostics.phase129_models import (
    RegimeTransitionContext,
    RegimeTransitionAnalyticsResult,
    RegimeDiagnosticsReadinessGate
)

UNSAFE_PATTERNS = [
    re.compile(r"\b(buy|sell)\b", re.IGNORECASE),
    re.compile(r"\b(kesin al|kesin sat|güçlü al|garanti kâr)\b", re.IGNORECASE),
    re.compile(r"\b(order|broker|position|portfolio_weight|target_weight|allocation)\b", re.IGNORECASE),
    re.compile(r"\b(sent_to_broker|live_order|demo_order)\b", re.IGNORECASE),
]

def regime_diagnostics_text_has_trade_or_execution_language(text: str) -> bool:
    if not text:
        return False
    for pat in UNSAFE_PATTERNS:
        if pat.search(text):
            return True
    return False

def validate_regime_diagnostics_dataframe_output_safety(df: pd.DataFrame) -> List[str]:
    from usa_signal_bot.regime_classification.diagnostics.regime_diagnostics_schema_validator import validate_no_forbidden_regime_diagnostics_columns
    errors = validate_no_forbidden_regime_diagnostics_columns(list(df.columns))
    return errors

def collect_regime_transition_risk_flags(context: Optional[RegimeTransitionContext] = None) -> List[RegimeTransitionRiskFlag]:
    flags = []
    if context:
        flags.extend(context.risk_flags)
        if context.activation_allowed or context.strategy_activation_allowed or context.deployment_allowed:
            flags.append(RegimeTransitionRiskFlag.DEPLOYMENT_RISK)
        if context.broker_execution_enabled or context.paper_state_mutation_enabled:
            flags.append(RegimeTransitionRiskFlag.BROKER_RISK)
        if context.produces_trade_signal or context.produces_order_decision or context.produces_portfolio_weights:
            flags.append(RegimeTransitionRiskFlag.TRADE_SIGNAL_COLUMN_RISK)
        if context.model_training_used or context.model_prediction_used:
            flags.append(RegimeTransitionRiskFlag.MODEL_TRAINING_ATTEMPTED)
    return list(set(flags))

def validate_regime_transition_analytics_safety(result: RegimeTransitionAnalyticsResult) -> List[str]:
    errors = []
    if result.activation_allowed or result.strategy_activation_allowed or result.deployment_allowed:
        errors.append("Analytics result allows activation or deployment.")
    if result.produces_trade_signal or result.produces_order_decision or result.produces_portfolio_weights:
        errors.append("Analytics result produces execution outputs.")
    if result.investment_advice:
        errors.append("Analytics result produces investment advice.")
    if result.model_training_used or result.model_prediction_used:
        errors.append("Analytics result used model training/prediction.")
    return errors

def validate_regime_diagnostics_readiness_gate_safety(gate: RegimeDiagnosticsReadinessGate) -> List[str]:
    errors = []
    if gate.activation_allowed or gate.strategy_activation_allowed or gate.deployment_allowed:
        errors.append("Gate allows activation or deployment.")
    if gate.produces_trade_signal or gate.produces_order_decision:
        errors.append("Gate produces execution outputs.")
    if gate.model_training_used or gate.model_prediction_used:
        errors.append("Gate used model training/prediction.")
    return errors

def validate_regime_transition_context_safety(context: RegimeTransitionContext) -> List[str]:
    errors = []
    if context.activation_allowed or context.strategy_activation_allowed or context.deployment_allowed:
        errors.append("Context allows activation or deployment.")
    if context.active_paper_enabled or context.broker_execution_enabled or context.order_creation_enabled or context.paper_state_mutation_enabled:
        errors.append("Context enables paper trading or broker execution.")
    if context.telegram_real_send_enabled or context.dashboard_enabled or context.network_default_enabled:
        errors.append("Context enables telegram, dashboard or network.")
    if context.scraping_enabled or context.html_parse_enabled or context.paid_api_enabled:
        errors.append("Context enables scraping, HTML parsing, or paid APIs.")
    if context.produces_trade_signal or context.produces_order_decision or context.produces_portfolio_weights:
        errors.append("Context produces execution outputs.")
    if context.investment_advice:
        errors.append("Context produces investment advice.")
    if context.model_training_used or context.model_prediction_used or context.heavy_ml_dependency_used:
        errors.append("Context used model training, prediction, or heavy ML dependency.")
    return errors

def regime_diagnostics_safety_summary(errors: List[str]) -> Dict[str, Any]:
    return {"safe": len(errors) == 0, "error_count": len(errors)}

def regime_diagnostics_safety_to_text(errors: List[str]) -> str:
    if not errors:
        return "Safety check passed."
    return "Safety check failed:\n" + "\n".join([f" - {e}" for e in errors])
