import pandas as pd
from typing import Any
from usa_signal_bot.core.enums import RegimeLabelingRiskFlag
from usa_signal_bot.regime_classification.labeling.phase128_models import (
    RegimeLabelingContext,
    HeuristicRegimeLabelResult,
    RegimeCandidateValidationResult,
    RegimeLabelingReadinessGate
)
from usa_signal_bot.regime_classification.labeling.regime_label_schema_validator import validate_regime_label_dataframe_schema

def regime_label_text_has_trade_or_execution_language(text: str) -> bool:
    if not text:
        return False
    text_lower = text.lower()
    forbidden = [
        "buy signal", "sell signal", "strong buy", "strong sell",
        "kesin al", "kesin sat", "güçlü al", "güçlü sat", "garanti kâr",
        "paper'a alındı", "canlıya alındı", "emir gönderildi", "aktif trading başladı",
        "deploy", "production_patch"
    ]
    for f in forbidden:
        if f in text_lower:
            return True
    return False

def validate_regime_labeling_context_safety(context: RegimeLabelingContext) -> list[str]:
    errors = []

    if context.activation_allowed:
        errors.append("Context has activation_allowed=True")
    if context.strategy_activation_allowed:
        errors.append("Context has strategy_activation_allowed=True")
    if context.deployment_allowed:
        errors.append("Context has deployment_allowed=True")

    flags = [
        ("active_paper_enabled", context.active_paper_enabled),
        ("broker_execution_enabled", context.broker_execution_enabled),
        ("order_creation_enabled", context.order_creation_enabled),
        ("paper_state_mutation_enabled", context.paper_state_mutation_enabled),
        ("telegram_real_send_enabled", context.telegram_real_send_enabled),
        ("scraping_enabled", context.scraping_enabled),
        ("html_parse_enabled", context.html_parse_enabled),
        ("paid_api_enabled", context.paid_api_enabled),
        ("dashboard_enabled", context.dashboard_enabled),
        ("network_default_enabled", context.network_default_enabled),
        ("network_used", context.network_used),
        ("paid_api_used", context.paid_api_used),
        ("scraping_used", context.scraping_used),
        ("html_parsing_used", context.html_parsing_used),
        ("broker_used", context.broker_used),
        ("order_created", context.order_created),
        ("paper_state_mutated", context.paper_state_mutated),
        ("telegram_real_sent", context.telegram_real_sent),
        ("dashboard_started", context.dashboard_started),
        ("model_training_used", context.model_training_used),
        ("model_prediction_used", context.model_prediction_used),
        ("heavy_ml_dependency_used", context.heavy_ml_dependency_used),
        ("produces_trade_signal", context.produces_trade_signal),
        ("produces_order_decision", context.produces_order_decision),
        ("produces_portfolio_weights", context.produces_portfolio_weights),
        ("investment_advice", context.investment_advice)
    ]

    for name, val in flags:
        if val:
            errors.append(f"Context has {name}=True")

    return errors

def validate_heuristic_label_results_safety(results: list[HeuristicRegimeLabelResult]) -> list[str]:
    errors = []
    for r in results:
        if r.produces_trade_signal or r.produces_order_decision or r.produces_portfolio_weights:
            errors.append(f"Label result {r.label_result_id} produces execution outputs")
        if r.model_prediction or r.model_training_used:
            errors.append(f"Label result {r.label_result_id} uses ML prediction/training")
    return errors

def validate_candidate_validation_safety(result: RegimeCandidateValidationResult) -> list[str]:
    errors = []
    if result.produces_trade_signal or result.produces_order_decision or result.produces_portfolio_weights:
        errors.append("Candidate validation produces execution outputs")
    if not result.no_model_training or not result.no_model_prediction:
        errors.append("Candidate validation allowed model prediction/training")
    return errors

def validate_regime_labeling_readiness_gate_safety(gate: RegimeLabelingReadinessGate) -> list[str]:
    errors = []
    if gate.produces_trade_signal or gate.produces_order_decision or gate.produces_portfolio_weights:
        errors.append("Readiness gate produces execution outputs")
    if gate.model_training_used or gate.model_prediction_used:
        errors.append("Readiness gate allowed model prediction/training")
    return errors

def validate_regime_label_dataframe_output_safety(df: pd.DataFrame) -> list[str]:
    return validate_regime_label_dataframe_schema(df)

def collect_regime_labeling_risk_flags(context: RegimeLabelingContext | None = None) -> list[RegimeLabelingRiskFlag]:
    flags = set()
    if not context:
        return list(flags)

    for r in context.risk_flags:
        flags.add(r)

    if context.ingestion:
        for r in context.ingestion.risk_flags:
            flags.add(r)

    if context.readiness_gate:
        for r in context.readiness_gate.risk_flags:
            flags.add(r)

    return list(flags)

def regime_label_safety_summary(errors: list[str]) -> dict[str, Any]:
    return {
        "safe": len(errors) == 0,
        "error_count": len(errors)
    }

def regime_label_safety_to_text(errors: list[str]) -> str:
    if not errors:
        return "Safety validation passed"
    return f"Safety validation failed with {len(errors)} errors: {', '.join(errors[:3])}"
