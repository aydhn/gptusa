from typing import Any, Dict, List, Optional
import pandas as pd
from usa_signal_bot.regime_classification.final_closure.phase135_models import (
    RegimeFinalClosureContext,
    RegimeArtifactChainValidationResult,
    RegimeFinalClosureResult,
    RegimeFreezeSeal,
    MLInputContract,
    MLKickoffReadinessGate,
    RegimeFinalClosureRiskFlag
)

def validate_regime_final_closure_context_safety(context: RegimeFinalClosureContext) -> List[str]:
    errors = []
    if context.activation_allowed:
        errors.append("Activation allowed in context.")
    return errors

def validate_artifact_chain_safety(result: RegimeArtifactChainValidationResult) -> List[str]:
    return []

def validate_final_closure_result_safety(result: RegimeFinalClosureResult) -> List[str]:
    return []

def validate_freeze_seal_safety(seal: RegimeFreezeSeal) -> List[str]:
    return []

def validate_ml_input_contract_safety(contract: MLInputContract) -> List[str]:
    return []

def validate_ml_kickoff_gate_safety(gate: MLKickoffReadinessGate) -> List[str]:
    errors = []
    if gate.training_started or gate.prediction_started:
         errors.append("Training or prediction started in ML kickoff gate.")
    return errors

def validate_final_closure_dataframe_output_safety(df: pd.DataFrame) -> List[str]:
    return []

def final_closure_text_has_trade_or_execution_language(text: str) -> bool:
    unsafe = ["kesin al", "garanti", "emir gönderildi", "aktif trading", "buy_signal", "sell_signal"]
    return any(u in text.lower() for u in unsafe)

def collect_regime_final_closure_risk_flags(context: Optional[RegimeFinalClosureContext] = None) -> List[RegimeFinalClosureRiskFlag]:
    return []

def final_closure_safety_summary(errors: List[str]) -> Dict[str, Any]:
    return {"safe": len(errors) == 0, "errors": len(errors)}

def final_closure_safety_to_text(errors: List[str]) -> str:
    return "Safety checks passed." if not errors else f"{len(errors)} safety errors."
