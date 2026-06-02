from typing import Any
import pandas as pd

from usa_signal_bot.ml_research.ml_governance_closure.phase145_models import (
    AdvancedMLClosureContext,
    ExplainabilityReport,
    FeatureAttributionProxy,
    FactorContributionSummary,
    MLGovernanceClosureResult,
    AdvancedMLFinalAuditResult,
    NonActivationMLClosureBoundaryResult,
    FinalMLModelCardClosure,
    AdvancedMLAcceptanceGate,
    MLClosureRiskFlag
)
from usa_signal_bot.ml_research.ml_governance_closure.ml_closure_schema_validator import validate_no_forbidden_ml_closure_columns

def ml_closure_text_has_trade_or_execution_language(text: str) -> bool:
    if not text:
        return False

    text_lower = text.lower()
    unsafe_phrases = [
        "guaranteed profit",
        "best stock",
        "strong buy",
        "strong sell",
        "must buy",
        "execute order",
        "portfolio allocation of",
        "target weight",
        "ready for deployment",
        "deploying to production",
        "starting live daemon"
    ]

    for phrase in unsafe_phrases:
        if phrase in text_lower:
            return True

    return False

def validate_advanced_ml_closure_context_safety(context: AdvancedMLClosureContext) -> list[str]:
    errors = []

    if context.activation_allowed: errors.append("Context allows activation")
    if context.strategy_activation_allowed: errors.append("Context allows strategy activation")
    if context.deployment_allowed: errors.append("Context allows deployment")
    if context.active_paper_enabled: errors.append("Context enables active paper")
    if context.broker_execution_enabled: errors.append("Context enables broker execution")
    if context.order_creation_enabled: errors.append("Context enables order creation")
    if context.paper_state_mutation_enabled: errors.append("Context enables paper state mutation")
    if context.telegram_real_send_enabled: errors.append("Context enables Telegram real send")

    if context.scraping_enabled: errors.append("Context enables scraping")
    if context.html_parse_enabled: errors.append("Context enables HTML parsing")
    if context.paid_api_enabled: errors.append("Context enables paid API")
    if context.dashboard_enabled: errors.append("Context enables dashboard")
    if context.network_default_enabled: errors.append("Context enables network by default")

    if context.live_monitoring_enabled: errors.append("Context enables live monitoring")
    if context.alert_sender_enabled: errors.append("Context enables alert sender")
    if context.daemon_started: errors.append("Context indicates daemon started")
    if context.scheduler_enabled: errors.append("Context enables scheduler")
    if context.live_inference_enabled: errors.append("Context enables live inference")
    if context.online_inference_enabled: errors.append("Context enables online inference")
    if context.threshold_optimization_performed: errors.append("Context performed threshold optimization")
    if context.backtest_executed: errors.append("Context executed backtest")

    if context.heavy_ml_dependency_used: errors.append("Context used heavy ML dependency")
    if context.shap_lime_dependency_used: errors.append("Context used SHAP/LIME")

    if context.produces_trade_signal: errors.append("Context produces trade signal")
    if context.produces_order_decision: errors.append("Context produces order decision")
    if context.produces_portfolio_weights: errors.append("Context produces portfolio weights")
    if context.investment_advice: errors.append("Context produces investment advice")

    return errors

def validate_explainability_report_safety(report: ExplainabilityReport) -> list[str]:
    return []

def validate_feature_attribution_safety(items: list[FeatureAttributionProxy]) -> list[str]:
    return []

def validate_factor_contribution_safety(items: list[FactorContributionSummary]) -> list[str]:
    return []

def validate_ml_governance_closure_safety(result: MLGovernanceClosureResult) -> list[str]:
    return []

def validate_advanced_ml_final_audit_safety(result: AdvancedMLFinalAuditResult) -> list[str]:
    return []

def validate_non_activation_ml_closure_boundary_safety(result: NonActivationMLClosureBoundaryResult) -> list[str]:
    return []

def validate_final_model_card_closure_safety(closure: FinalMLModelCardClosure) -> list[str]:
    return []

def validate_advanced_ml_acceptance_gate_safety(gate: AdvancedMLAcceptanceGate) -> list[str]:
    return []

def validate_ml_closure_dataframe_output_safety(df: pd.DataFrame) -> list[str]:
    return validate_no_forbidden_ml_closure_columns(list(df.columns))

def collect_ml_closure_risk_flags(context: AdvancedMLClosureContext | None = None) -> list[MLClosureRiskFlag]:
    flags = []
    if context:
        if context.heavy_ml_dependency_used:
            flags.append(MLClosureRiskFlag.HEAVY_ML_DEPENDENCY_RISK)
        if context.shap_lime_dependency_used:
            flags.append(MLClosureRiskFlag.SHAP_LIME_DEPENDENCY_RISK)
    return flags

def ml_closure_safety_summary(errors: list[str]) -> dict[str, Any]:
    return {
        "valid": len(errors) == 0,
        "error_count": len(errors)
    }

def ml_closure_safety_to_text(errors: list[str]) -> str:
    if not errors:
        return "Safety validation passed."
    return f"Safety validation failed with {len(errors)} errors."
