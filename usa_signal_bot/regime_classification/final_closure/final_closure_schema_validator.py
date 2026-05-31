from typing import Any, Dict, List
import pandas as pd
from usa_signal_bot.regime_classification.final_closure.phase135_models import (
    RegimeArtifactChainValidationResult,
    RegimeFinalClosureResult,
    RegimeFreezeSeal,
    MLInputContract,
    MLKickoffReadinessGate,
    RegimeFinalClosureContext
)

def validate_artifact_chain_validation_schema(item: RegimeArtifactChainValidationResult) -> List[str]:
    return []

def validate_final_closure_result_schema(item: RegimeFinalClosureResult) -> List[str]:
    return []

def validate_freeze_seal_schema(item: RegimeFreezeSeal) -> List[str]:
    return []

def validate_ml_input_contract_schema(item: MLInputContract) -> List[str]:
    return []

def validate_ml_kickoff_gate_schema(item: MLKickoffReadinessGate) -> List[str]:
    return []

def validate_final_closure_context_schema(context: RegimeFinalClosureContext) -> List[str]:
    return []

def validate_final_closure_column_names(columns: List[str]) -> List[str]:
    return validate_no_forbidden_final_closure_columns(columns)

def validate_no_forbidden_final_closure_columns(columns: List[str]) -> List[str]:
    forbidden = [
        "buy", "sell", "entry", "exit", "order", "broker", "position",
        "portfolio_weight", "target_weight", "allocation", "paper",
        "live", "demo_order", "live_order", "sent_to_broker", "deploy",
        "production_patch"
    ]
    errors = []
    for col in columns:
        col_lower = col.lower()
        if col_lower == "macd_signal_9":
            continue
        if "signal" in col_lower:
            errors.append(f"Forbidden column name: {col}")
        for f in forbidden:
            if f in col_lower:
                errors.append(f"Forbidden column name: {col}")
    return errors

def final_closure_schema_summary(errors: List[str]) -> Dict[str, Any]:
    return {"valid": len(errors) == 0, "errors": len(errors)}

def final_closure_schema_to_text(errors: List[str]) -> str:
    return "Schema valid." if not errors else f"{len(errors)} schema errors."
