"""Freeze Preparation Safety Validator."""
from typing import Any

from .phase124_models import (
    FreezePreparationContext,
    FreezeCandidateManifest,
    FreezePreparationGate,
    IntegrationRehearsalResult,
    FreezePreparationRiskFlag
)

def validate_freeze_preparation_context_safety(context: FreezePreparationContext) -> list[str]:
    errors = []
    if context.activation_allowed:
        errors.append("context.activation_allowed must be False")
    if context.strategy_activation_allowed:
         errors.append("context.strategy_activation_allowed must be False")
    if context.broker_execution_enabled:
         errors.append("context.broker_execution_enabled must be False")
    return errors

def validate_freeze_manifest_safety(manifest: FreezeCandidateManifest) -> list[str]:
    errors = []
    if manifest.activation_allowed:
        errors.append("manifest.activation_allowed must be False")
    return errors

def validate_freeze_gate_safety(gate: FreezePreparationGate) -> list[str]:
    errors = []
    if gate.activation_allowed:
        errors.append("gate.activation_allowed must be False")
    return errors

def validate_integration_rehearsal_safety(result: IntegrationRehearsalResult) -> list[str]:
    return []

def validate_freeze_columns_safety(columns: list[str]) -> list[str]:
    errors = []
    forbidden = [
        "buy", "sell", "entry", "exit", "order", "broker", "position",
        "portfolio_weight", "target_weight", "allocation", "paper", "live",
        "demo_order", "live_order", "sent_to_broker"
    ]
    for col in columns:
        cl = col.lower()
        if cl == "macd_signal_9":
             continue
        for f in forbidden:
             if f in cl:
                 errors.append(f"Forbidden column text found: {f} in {col}")
    return errors

def freeze_preparation_text_has_trade_or_execution_language(text: str) -> bool:
    unsafe = [
        "kesin al", "kesin sat", "güçlü al", "güçlü sat", "garanti kâr",
        "risksiz kazanç", "buy signal", "sell signal", "strong buy",
        "strong sell", "emir gönderildi", "aktif trading başladı",
        "paper'a alındı", "canlıya alındı"
    ]
    tl = text.lower()
    for u in unsafe:
        if u in tl:
             return True
    return False

def collect_freeze_preparation_risk_flags(context: FreezePreparationContext | None = None) -> list[FreezePreparationRiskFlag]:
    flags = []
    if context:
        flags.extend(context.risk_flags)
        if context.ingestion:
            flags.extend(context.ingestion.risk_flags)
    return list(set(flags))

def freeze_preparation_safety_summary(errors: list[str]) -> dict[str, Any]:
    return {"safe": len(errors) == 0, "error_count": len(errors)}

def freeze_preparation_safety_to_text(errors: list[str]) -> str:
    return "Safety Valid: " + ("PASS" if len(errors) == 0 else "FAIL")
