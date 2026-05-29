from typing import Any

from usa_signal_bot.core.enums import MarketBehaviorRiskFlag
from usa_signal_bot.regime_classification.behavior_reporting.phase130_models import (
    MarketBehaviorContext, MarketBehaviorProfile, RegimeBehaviorSummary,
    BehaviorReportDocument, MarketBehaviorReadinessGate
)

def market_behavior_text_has_trade_or_execution_language(text: str) -> bool:
    bad = ["buy", "sell", "entry", "exit", "order", "broker", "position", "portfolio_weight",
           "target_weight", "allocation", "live_order", "demo_order", "sent_to_broker",
           "deploy", "production_patch"]
    # Allow MACD signal
    if "macd_signal_9" in text:
        text = text.replace("macd_signal_9", "")
    for b in bad:
        if b in text.lower():
            return True
    return False

def validate_market_behavior_columns_safety(columns: list[str]) -> list[str]:
    errs = []
    for c in columns:
        if market_behavior_text_has_trade_or_execution_language(c):
            errs.append(f"Unsafe column: {c}")
    return errs

def validate_market_behavior_profiles_safety(profiles: list[MarketBehaviorProfile]) -> list[str]:
    errs = []
    for p in profiles:
        if market_behavior_text_has_trade_or_execution_language(p.summary):
            errs.append(f"Unsafe language in profile {p.profile_id}")
    return errs

def validate_regime_behavior_summaries_safety(summaries: list[RegimeBehaviorSummary]) -> list[str]:
    errs = []
    for s in summaries:
        if market_behavior_text_has_trade_or_execution_language(s.summary_text):
            errs.append(f"Unsafe language in summary {s.summary_id}")
    return errs

def validate_behavior_report_safety(document: BehaviorReportDocument) -> list[str]:
    errs = []
    for s in document.sections:
        if market_behavior_text_has_trade_or_execution_language(s.body):
            errs.append(f"Unsafe language in report section {s.title}")
    return errs

def validate_behavior_readiness_gate_safety(gate: MarketBehaviorReadinessGate) -> list[str]:
    errs = []
    if gate.activation_allowed: errs.append("gate activation_allowed is true")
    return errs

def validate_market_behavior_context_safety(context: MarketBehaviorContext) -> list[str]:
    errs = []
    if context.activation_allowed: errs.append("context activation_allowed is true")
    if context.strategy_activation_allowed: errs.append("strategy_activation_allowed is true")
    if context.deployment_allowed: errs.append("deployment_allowed is true")
    if context.active_paper_enabled: errs.append("active_paper_enabled is true")
    if context.broker_execution_enabled: errs.append("broker_execution_enabled is true")
    if context.order_creation_enabled: errs.append("order_creation_enabled is true")
    if context.paper_state_mutation_enabled: errs.append("paper_state_mutation_enabled is true")
    if context.telegram_real_send_enabled: errs.append("telegram_real_send_enabled is true")
    if context.scraping_enabled: errs.append("scraping_enabled is true")
    if context.html_parse_enabled: errs.append("html_parse_enabled is true")
    if context.paid_api_enabled: errs.append("paid_api_enabled is true")
    if context.dashboard_enabled: errs.append("dashboard_enabled is true")
    if context.network_default_enabled: errs.append("network_default_enabled is true")
    if context.model_training_used: errs.append("model_training_used is true")
    if context.model_prediction_used: errs.append("model_prediction_used is true")
    if context.heavy_ml_dependency_used: errs.append("heavy_ml_dependency_used is true")
    if context.produces_trade_signal: errs.append("produces_trade_signal is true")
    if context.produces_order_decision: errs.append("produces_order_decision is true")
    if context.produces_portfolio_weights: errs.append("produces_portfolio_weights is true")
    if context.investment_advice: errs.append("investment_advice is true")
    return errs

def collect_market_behavior_risk_flags(context: MarketBehaviorContext | None = None) -> list[MarketBehaviorRiskFlag]:
    return context.risk_flags if context else []

def market_behavior_safety_summary(errors: list[str]) -> dict[str, Any]:
    return {"error_count": len(errors)}

def market_behavior_safety_to_text(errors: list[str]) -> str:
    return "Safe" if not errors else f"Unsafe: {errors}"
