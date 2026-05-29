from typing import Any
import pandas as pd
from usa_signal_bot.regime_classification.alignment.phase131_models import (
    RegimeAlignmentContext, RegimeContextCompatibilityResult, MarketBehaviorOverlayResult,
    RegimeAlignmentReadinessGate
)
from usa_signal_bot.core.enums import RegimeAlignmentRiskFlag
from usa_signal_bot.regime_classification.alignment.compatibility_schema_validator import FORBIDDEN_FRAGMENTS

def validate_regime_alignment_context_safety(context: RegimeAlignmentContext) -> list[str]:
    errs = []
    if context.activation_allowed: errs.append("activation_allowed is true")
    if context.strategy_activation_allowed: errs.append("strategy_activation_allowed is true")
    if context.deployment_allowed: errs.append("deployment_allowed is true")
    if context.active_paper_enabled: errs.append("active_paper_enabled is true")
    if context.broker_execution_enabled: errs.append("broker_execution_enabled is true")
    if context.order_creation_enabled: errs.append("order_creation_enabled is true")
    if context.paper_state_mutation_enabled: errs.append("paper_state_mutation_enabled is true")
    if context.telegram_real_send_enabled: errs.append("telegram_real_send_enabled is true")
    if context.model_training_used: errs.append("model_training_used is true")
    if context.model_prediction_used: errs.append("model_prediction_used is true")
    if context.produces_trade_signal: errs.append("produces_trade_signal is true")
    if context.investment_advice: errs.append("investment_advice is true")

    errs.extend(validate_compatibility_results_safety(context.compatibility_results))
    errs.extend(validate_overlay_results_safety(context.overlay_results))
    if context.readiness_gate:
        errs.extend(validate_alignment_readiness_gate_safety(context.readiness_gate))
    return errs

def validate_compatibility_results_safety(results: list[RegimeContextCompatibilityResult]) -> list[str]:
    errs = []
    for r in results:
        if r.produces_trade_signal: errs.append(f"Result {r.compatibility_id} produces signal")
        if r.activation_allowed: errs.append(f"Result {r.compatibility_id} allows activation")
    return errs

def validate_overlay_results_safety(results: list[MarketBehaviorOverlayResult]) -> list[str]:
    errs = []
    for r in results:
        if r.produces_trade_signal: errs.append(f"Overlay {r.overlay_id} produces signal")
    return errs

def validate_alignment_readiness_gate_safety(gate: RegimeAlignmentReadinessGate) -> list[str]:
    errs = []
    if gate.activation_allowed: errs.append("Gate allows activation")
    if gate.model_training_used: errs.append("Gate uses model training")
    return errs

def validate_alignment_dataframe_output_safety(df: pd.DataFrame) -> list[str]:
    errs = []
    for c in df.columns:
        cl = c.lower()
        if any(f in cl for f in FORBIDDEN_FRAGMENTS if f != "signal" or cl != "macd_signal_9"):
            errs.append(f"DF has forbidden column {c}")
    return errs

def alignment_text_has_trade_or_execution_language(text: str) -> bool:
    tl = text.lower()
    unsafe = ["kesin al", "kesin sat", "garanti", "emir gönderildi", "aktif trading başladı"]
    return any(u in tl for u in unsafe)

def collect_regime_alignment_risk_flags(context: RegimeAlignmentContext | None = None) -> list[RegimeAlignmentRiskFlag]:
    if not context: return []
    return context.risk_flags

def compatibility_safety_summary(errors: list[str]) -> dict[str, Any]:
    return {"error_count": len(errors)}

def compatibility_safety_to_text(errors: list[str]) -> str:
    if not errors: return "Safety OK"
    return f"Safety ERRORS: {', '.join(errors)}"
