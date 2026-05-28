from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import FinalClosureRiskFlag
from usa_signal_bot.feature_engine.final_closure.phase125_models import (
    FinalClosureContext,
    FinalClosureManifest,
    FreezeSealMetadata,
    EngineReadinessCertificate,
    Phase126KickoffGate
)

FORBIDDEN_FRAGMENTS = [
    "buy", "sell", "entry", "exit", "order", "broker", "position",
    "portfolio_weight", "target_weight", "allocation", "paper", "live",
    "demo_order", "live_order", "sent_to_broker", "deploy", "production_patch"
]

UNSAFE_LANGUAGE = [
    "kesin al", "kesin sat", "güçlü al", "güçlü sat", "garanti kâr", "risksiz kazanç",
    "buy signal", "sell signal", "strong buy", "strong sell", "emir gönderildi",
    "aktif trading başladı", "paper’a alındı", "canlıya alındı", "deploy edildi",
    "production’a alındı"
]

def validate_final_closure_context_safety(context: FinalClosureContext) -> List[str]:
    errs = []
    if context.activation_allowed: errs.append("activation_allowed is true")
    if context.produces_trade_signal: errs.append("produces_trade_signal is true")
    if context.broker_execution_enabled: errs.append("broker_execution_enabled is true")
    return errs

def validate_final_manifest_safety(manifest: FinalClosureManifest) -> List[str]:
    errs = []
    if not manifest.no_secret_leak: errs.append("no_secret_leak is false")
    if not manifest.no_forbidden_columns: errs.append("no_forbidden_columns is false")
    if not manifest.no_execution_language: errs.append("no_execution_language is false")
    if manifest.activation_allowed: errs.append("activation_allowed is true")
    return errs

def validate_freeze_seal_safety(seal: FreezeSealMetadata) -> List[str]:
    errs = []
    if seal.activation_allowed: errs.append("activation_allowed is true")
    if seal.produces_trade_signal: errs.append("produces_trade_signal is true")
    return errs

def validate_engine_certificate_safety(certificate: EngineReadinessCertificate) -> List[str]:
    errs = []
    if certificate.certified_for_trading_activation: errs.append("certified_for_trading_activation is true")
    if certificate.certified_for_deployment: errs.append("certified_for_deployment is true")
    return errs

def validate_phase126_kickoff_gate_safety(gate: Phase126KickoffGate) -> List[str]:
    errs = []
    if gate.activation_allowed: errs.append("activation_allowed is true")
    if gate.strategy_activation_allowed: errs.append("strategy_activation_allowed is true")
    return errs

def validate_final_closure_columns_safety(columns: List[str]) -> List[str]:
    errs = []
    for c in columns:
        cl = c.lower()
        if cl == "signal" or cl == "macd_signal_9":
            continue # whitelist
        for frag in FORBIDDEN_FRAGMENTS:
            if frag in cl:
                errs.append(f"Forbidden fragment '{frag}' in column '{c}'")
    return errs

def final_closure_text_has_trade_or_execution_language(text: str) -> bool:
    tl = text.lower()
    for phrase in UNSAFE_LANGUAGE:
        if phrase in tl:
            return True
    return False

def collect_final_closure_risk_flags(context: Optional[FinalClosureContext] = None) -> List[FinalClosureRiskFlag]:
    flags = []
    if context:
        if not context.final_artifacts_ready:
            flags.append(FinalClosureRiskFlag.ARTIFACT_CHAIN_INCOMPLETE)
        if not context.final_checks_passed:
            flags.append(FinalClosureRiskFlag.FINAL_CHECK_FAILED)
        if not context.freeze_seal_ready:
            flags.append(FinalClosureRiskFlag.FREEZE_SEAL_INVALID)
        if not context.engine_certificate_ready:
            flags.append(FinalClosureRiskFlag.ENGINE_CERTIFICATE_INVALID)
        if not context.phase126_kickoff_gate_ready:
            flags.append(FinalClosureRiskFlag.PHASE126_KICKOFF_GATE_FAILED)
    return flags

def final_closure_safety_summary(errors: List[str]) -> Dict[str, Any]:
    return {"safe": len(errors) == 0, "errors": len(errors)}

def final_closure_safety_to_text(errors: List[str]) -> str:
    return f"Safety: {'Pass' if not errors else 'Fail with ' + str(len(errors)) + ' errors'}"
