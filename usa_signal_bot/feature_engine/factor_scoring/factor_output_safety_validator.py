from typing import Any
import pandas as pd

from usa_signal_bot.feature_engine.factor_scoring.phase121_models import (
    FactorScoringContext,
    FactorScoringResult,
    FactorTableResult,
    FactorScoringRiskFlag
)

def factor_output_text_has_trade_or_execution_language(text: str) -> bool:
    t = text.lower()
    forbidden = [
        "emir gönderildi", "aktif trading başladı", "paper'a alındı",
        "canlıya alındı", "kesin al", "kesin sat", "garanti kâr",
        "buy signal", "sell signal", "strong buy", "strong sell",
        "sent to broker", "live order"
    ]
    for f in forbidden:
        if f in t:
            return True
    return False

def validate_factor_scoring_context_safety(context: FactorScoringContext) -> list[str]:
    errors = []
    if context.activation_allowed: errors.append("activation_allowed is true")
    if context.strategy_activation_allowed: errors.append("strategy_activation_allowed is true")
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
    if context.produces_trade_signal: errors.append("produces_trade_signal is true")
    if context.produces_order_decision: errors.append("produces_order_decision is true")
    if context.produces_portfolio_weights: errors.append("produces_portfolio_weights is true")
    if context.network_used: errors.append("network_used is true")
    if context.paid_api_used: errors.append("paid_api_used is true")
    if context.scraping_used: errors.append("scraping_used is true")
    if context.html_parsing_used: errors.append("html_parsing_used is true")
    if context.broker_used: errors.append("broker_used is true")
    if context.order_created: errors.append("order_created is true")
    if context.paper_state_mutated: errors.append("paper_state_mutated is true")
    if context.telegram_real_sent: errors.append("telegram_real_sent is true")
    if context.dashboard_started: errors.append("dashboard_started is true")
    return errors

def validate_factor_scoring_results_safety(results: list[FactorScoringResult]) -> list[str]:
    errors = []
    for r in results:
        if r.produced_trade_signal: errors.append("produced_trade_signal is true")
        if r.produced_order_decision: errors.append("produced_order_decision is true")
        if r.produced_portfolio_weights: errors.append("produced_portfolio_weights is true")
        if r.network_used: errors.append("network_used is true")
        if r.paid_api_used: errors.append("paid_api_used is true")
        if r.scraping_used: errors.append("scraping_used is true")
        if r.html_parsing_used: errors.append("html_parsing_used is true")
        if r.broker_used: errors.append("broker_used is true")
        if r.order_created: errors.append("order_created is true")
        if r.paper_state_mutated: errors.append("paper_state_mutated is true")
        if r.telegram_real_sent: errors.append("telegram_real_sent is true")
        if r.dashboard_started: errors.append("dashboard_started is true")
    return errors

def validate_factor_table_safety(table: FactorTableResult) -> list[str]:
    errors = []
    if table.produced_trade_signal: errors.append("produced_trade_signal is true")
    if table.produced_order_decision: errors.append("produced_order_decision is true")
    if table.produced_portfolio_weights: errors.append("produced_portfolio_weights is true")
    if table.network_used: errors.append("network_used is true")
    if table.broker_used: errors.append("broker_used is true")
    if table.order_created: errors.append("order_created is true")
    if table.paper_state_mutated: errors.append("paper_state_mutated is true")
    return errors

def validate_factor_dataframe_output_safety(df: pd.DataFrame) -> list[str]:
    errors = []
    from usa_signal_bot.feature_engine.factor_scoring.factor_table_schema import validate_no_forbidden_factor_columns
    errors.extend(validate_no_forbidden_factor_columns(list(df.columns)))
    return errors

def collect_factor_scoring_risk_flags(context: FactorScoringContext | None = None) -> list[FactorScoringRiskFlag]:
    flags = []
    if context:
        if context.produces_trade_signal: flags.append(FactorScoringRiskFlag.TRADE_SIGNAL_COLUMN_RISK)
        if context.produces_order_decision: flags.append(FactorScoringRiskFlag.ORDER_DECISION_COLUMN_RISK)
        if context.produces_portfolio_weights: flags.append(FactorScoringRiskFlag.PORTFOLIO_WEIGHT_COLUMN_RISK)
        if context.activation_allowed: flags.append(FactorScoringRiskFlag.PAPER_MUTATION_RISK)
        if context.broker_execution_enabled: flags.append(FactorScoringRiskFlag.BROKER_RISK)
    return flags

def factor_output_safety_summary(errors: list[str]) -> dict[str, Any]:
    return {"status": "ok"}

def factor_output_safety_to_text(errors: list[str]) -> str:
    return f"Errors: {len(errors)}"
