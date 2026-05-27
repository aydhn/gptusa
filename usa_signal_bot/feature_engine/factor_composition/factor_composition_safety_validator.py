from typing import Any
from usa_signal_bot.core.enums import FactorCompositionRiskFlag
from usa_signal_bot.feature_engine.factor_composition.phase120_models import (
    FactorCompositionContext,
    FactorCandidateDefinition,
    FeatureSelectionMetadata,
    FactorReadinessGate
)

def factor_composition_text_has_trade_or_execution_language(text: str) -> bool:
    if not text:
        return False
    t = text.lower()
    forbidden = [
        "emir gönderildi", "aktif trading başladı", "paper'a alındı",
        "canlıya alındı", "kesin al", "kesin sat", "garanti kâr",
        "buy signal", "sell signal", "strong buy", "strong sell",
        "live_order", "sent_to_broker", "demo_order"
    ]
    return any(f in t for f in forbidden)

def validate_factor_feature_columns_safety(columns: list[str]) -> list[str]:
    errors = []
    forbidden_fragments = [
        "buy", "sell", "entry", "exit", "order", "broker",
        "position", "portfolio_weight", "target_weight", "allocation",
        "paper_state", "real_fill_id"
    ]
    for col in columns:
        c = col.lower()
        if any(f in c for f in forbidden_fragments):
            errors.append(f"Forbidden column name detected: {col}")
        if "signal" in c and "macd_signal" not in c:
            errors.append(f"Forbidden 'signal' column name detected: {col}")
    return errors

def validate_factor_candidates_safety(candidates: list[FactorCandidateDefinition]) -> list[str]:
    errors = []
    for c in candidates:
        if c.produces_trade_signal: errors.append(f"Candidate {c.factor_name} produces_trade_signal is True")
        if c.produces_order_decision: errors.append(f"Candidate {c.factor_name} produces_order_decision is True")
        if c.produces_portfolio_weights: errors.append(f"Candidate {c.factor_name} produces_portfolio_weights is True")
        if not c.research_metadata_only: errors.append(f"Candidate {c.factor_name} research_metadata_only is False")

        errors.extend(validate_factor_feature_columns_safety(c.input_feature_columns))
        errors.extend(validate_factor_feature_columns_safety([c.output_column]))

        if factor_composition_text_has_trade_or_execution_language(c.description):
            errors.append(f"Candidate {c.factor_name} description has execution language")

    return errors

def validate_feature_selection_metadata_safety(items: list[FeatureSelectionMetadata]) -> list[str]:
    errors = []
    for m in items:
        if m.produces_trade_signal: errors.append(f"Metadata {m.feature_column} produces_trade_signal is True")
        if m.produces_order_decision: errors.append(f"Metadata {m.feature_column} produces_order_decision is True")
        if m.produces_portfolio_weights: errors.append(f"Metadata {m.feature_column} produces_portfolio_weights is True")
        if not m.research_metadata_only: errors.append(f"Metadata {m.feature_column} research_metadata_only is False")

        errors.extend(validate_factor_feature_columns_safety([m.feature_column]))
    return errors

def validate_factor_readiness_gate_safety(gate: FactorReadinessGate) -> list[str]:
    errors = []
    if gate.activation_allowed: errors.append("Gate activation_allowed is True")
    if gate.strategy_activation_allowed: errors.append("Gate strategy_activation_allowed is True")
    if gate.produces_trade_signal: errors.append("Gate produces_trade_signal is True")
    if gate.produces_order_decision: errors.append("Gate produces_order_decision is True")
    if gate.produces_portfolio_weights: errors.append("Gate produces_portfolio_weights is True")
    if gate.broker_execution_enabled: errors.append("Gate broker_execution_enabled is True")
    if gate.order_creation_enabled: errors.append("Gate order_creation_enabled is True")
    if gate.paper_state_mutation_enabled: errors.append("Gate paper_state_mutation_enabled is True")
    if not gate.research_data_only: errors.append("Gate research_data_only is False")
    return errors

def validate_factor_composition_context_safety(context: FactorCompositionContext) -> list[str]:
    errors = []
    if context.activation_allowed: errors.append("Context activation_allowed is True")
    if context.active_paper_enabled: errors.append("Context active_paper_enabled is True")
    if context.broker_execution_enabled: errors.append("Context broker_execution_enabled is True")
    if context.order_creation_enabled: errors.append("Context order_creation_enabled is True")
    if context.paper_state_mutation_enabled: errors.append("Context paper_state_mutation_enabled is True")
    if context.telegram_real_send_enabled: errors.append("Context telegram_real_send_enabled is True")
    if context.scraping_enabled: errors.append("Context scraping_enabled is True")
    if context.html_parse_enabled: errors.append("Context html_parse_enabled is True")
    if context.paid_api_enabled: errors.append("Context paid_api_enabled is True")
    if context.dashboard_enabled: errors.append("Context dashboard_enabled is True")
    if context.network_default_enabled: errors.append("Context network_default_enabled is True")
    if context.produces_trade_signal: errors.append("Context produces_trade_signal is True")
    if context.produces_order_decision: errors.append("Context produces_order_decision is True")
    if context.produces_portfolio_weights: errors.append("Context produces_portfolio_weights is True")

    if context.network_used: errors.append("Context network_used is True")
    if context.paid_api_used: errors.append("Context paid_api_used is True")
    if context.scraping_used: errors.append("Context scraping_used is True")
    if context.html_parsing_used: errors.append("Context html_parsing_used is True")
    if context.broker_used: errors.append("Context broker_used is True")
    if context.order_created: errors.append("Context order_created is True")
    if context.paper_state_mutated: errors.append("Context paper_state_mutated is True")
    if context.telegram_real_sent: errors.append("Context telegram_real_sent is True")
    if context.dashboard_started: errors.append("Context dashboard_started is True")

    if not context.metadata_only: errors.append("Context metadata_only is False")
    if not context.research_data_only: errors.append("Context research_data_only is False")

    errors.extend(validate_factor_candidates_safety(context.factor_candidates))
    errors.extend(validate_feature_selection_metadata_safety(context.selection_metadata))
    if context.readiness_gate:
        errors.extend(validate_factor_readiness_gate_safety(context.readiness_gate))

    return errors

def collect_factor_composition_risk_flags(context: FactorCompositionContext | None = None) -> list[FactorCompositionRiskFlag]:
    flags = set()
    if not context:
        return list(flags)

    if context.produces_trade_signal: flags.add(FactorCompositionRiskFlag.TRADE_SIGNAL_COLUMN_RISK)
    if context.produces_order_decision: flags.add(FactorCompositionRiskFlag.ORDER_DECISION_COLUMN_RISK)
    if context.produces_portfolio_weights: flags.add(FactorCompositionRiskFlag.PORTFOLIO_WEIGHT_COLUMN_RISK)
    if context.broker_used or context.broker_execution_enabled: flags.add(FactorCompositionRiskFlag.BROKER_RISK)
    if context.paper_state_mutated or context.paper_state_mutation_enabled: flags.add(FactorCompositionRiskFlag.PAPER_MUTATION_RISK)
    if context.telegram_real_sent or context.telegram_real_send_enabled: flags.add(FactorCompositionRiskFlag.TELEGRAM_REAL_SEND_RISK)
    if context.dashboard_started or context.dashboard_enabled: flags.add(FactorCompositionRiskFlag.DASHBOARD_RISK)
    if context.scraping_used or context.scraping_enabled: flags.add(FactorCompositionRiskFlag.SCRAPING_RISK)
    if context.html_parsing_used or context.html_parse_enabled: flags.add(FactorCompositionRiskFlag.HTML_PARSE_RISK)
    if context.paid_api_used or context.paid_api_enabled: flags.add(FactorCompositionRiskFlag.PAID_API_RISK)
    if context.network_used or context.network_default_enabled: flags.add(FactorCompositionRiskFlag.NETWORK_DEFAULT_ENABLED_RISK)

    # Check coverage/missingness
    if any(p.average_coverage_ratio < 0.70 for p in context.coverage_profiles):
        flags.add(FactorCompositionRiskFlag.FEATURE_COVERAGE_LOW)

    return list(flags)

def factor_composition_safety_summary(errors: list[str]) -> dict[str, Any]:
    return {
        "safe": len(errors) == 0,
        "violation_count": len(errors)
    }

def factor_composition_safety_to_text(errors: list[str]) -> str:
    if not errors:
        return "Factor Composition Safety: PASSED (0 violations)"

    lines = [f"Factor Composition Safety: FAILED ({len(errors)} violations)"]
    for e in errors:
        lines.append(f"  - {e}")
    return "\n".join(lines)
