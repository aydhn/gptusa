from typing import Any, Dict, List, Optional
import pandas as pd
import json
from usa_signal_bot.ml_research.dataset_assembly.phase137_models import (
    MLDatasetAssemblyContext,
    MLMatrixAssemblyResult,
    MLAssembledDatasetManifest,
    MLSplitAssignment,
    MLLeakageAuditResult,
    MLDatasetAssemblyReadinessGate,
    MLDatasetAssemblyRiskFlag
)
from usa_signal_bot.ml_research.dataset_assembly.dataset_assembly_schema_validator import validate_no_forbidden_dataset_assembly_columns

def _check_flags(obj: Any, name: str) -> List[str]:
    errors = []
    if getattr(obj, "activation_allowed", False):
        errors.append(f"{name} has activation_allowed=True")
    if getattr(obj, "strategy_activation_allowed", False):
        errors.append(f"{name} has strategy_activation_allowed=True")
    if getattr(obj, "deployment_allowed", False):
        errors.append(f"{name} has deployment_allowed=True")
    if getattr(obj, "active_paper_enabled", False):
        errors.append(f"{name} has active_paper_enabled=True")
    if getattr(obj, "broker_execution_enabled", False):
        errors.append(f"{name} has broker_execution_enabled=True")
    if getattr(obj, "order_creation_enabled", False):
        errors.append(f"{name} has order_creation_enabled=True")
    if getattr(obj, "paper_state_mutation_enabled", False):
        errors.append(f"{name} has paper_state_mutation_enabled=True")
    if getattr(obj, "telegram_real_send_enabled", False):
        errors.append(f"{name} has telegram_real_send_enabled=True")
    if getattr(obj, "training_started", False):
        errors.append(f"{name} has training_started=True")
    if getattr(obj, "prediction_started", False):
        errors.append(f"{name} has prediction_started=True")
    if getattr(obj, "model_training_used", False):
        errors.append(f"{name} has model_training_used=True")
    if getattr(obj, "model_prediction_used", False):
        errors.append(f"{name} has model_prediction_used=True")
    if getattr(obj, "heavy_ml_dependency_used", False):
        errors.append(f"{name} has heavy_ml_dependency_used=True")
    if getattr(obj, "produces_trade_signal", False):
        errors.append(f"{name} has produces_trade_signal=True")
    if getattr(obj, "produces_order_decision", False):
        errors.append(f"{name} has produces_order_decision=True")
    if getattr(obj, "produces_portfolio_weights", False):
        errors.append(f"{name} has produces_portfolio_weights=True")
    if getattr(obj, "investment_advice", False):
        errors.append(f"{name} has investment_advice=True")
    return errors

def validate_dataset_assembly_context_safety(context: MLDatasetAssemblyContext) -> List[str]:
    return _check_flags(context, "MLDatasetAssemblyContext")

def validate_matrix_assembly_safety(result: MLMatrixAssemblyResult) -> List[str]:
    return _check_flags(result, "MLMatrixAssemblyResult") + validate_no_forbidden_dataset_assembly_columns(result.columns)

def validate_dataset_manifest_safety(manifest: MLAssembledDatasetManifest) -> List[str]:
    return _check_flags(manifest, "MLAssembledDatasetManifest")

def validate_split_assignment_safety(assignment: MLSplitAssignment) -> List[str]:
    return _check_flags(assignment, "MLSplitAssignment")

def validate_leakage_audit_safety(result: MLLeakageAuditResult) -> List[str]:
    return _check_flags(result, "MLLeakageAuditResult")

def validate_dataset_assembly_readiness_gate_safety(gate: MLDatasetAssemblyReadinessGate) -> List[str]:
    return _check_flags(gate, "MLDatasetAssemblyReadinessGate")

def validate_dataset_assembly_dataframe_output_safety(df: pd.DataFrame) -> List[str]:
    return validate_no_forbidden_dataset_assembly_columns(list(df.columns))

def dataset_assembly_text_has_trade_or_execution_language(text: str) -> bool:
    t = text.lower()
    phrases = ["kesin al", "kesin sat", "güçlü al", "güçlü sat", "garanti kâr", "emir gönderildi", "aktif trading başladı"]
    return any(p in t for p in phrases)

def collect_dataset_assembly_risk_flags(context: Optional[MLDatasetAssemblyContext] = None) -> List[MLDatasetAssemblyRiskFlag]:
    flags = set()
    if context:
        if context.produces_trade_signal:
            flags.add(MLDatasetAssemblyRiskFlag.TRADE_SIGNAL_COLUMN_RISK)
        if context.produces_order_decision:
            flags.add(MLDatasetAssemblyRiskFlag.ORDER_DECISION_COLUMN_RISK)
        if context.produces_portfolio_weights:
            flags.add(MLDatasetAssemblyRiskFlag.PORTFOLIO_WEIGHT_COLUMN_RISK)
        if context.investment_advice:
            flags.add(MLDatasetAssemblyRiskFlag.INVESTMENT_ADVICE_LANGUAGE_RISK)
        if context.activation_allowed or context.strategy_activation_allowed or context.deployment_allowed:
            flags.add(MLDatasetAssemblyRiskFlag.DEPLOYMENT_RISK)
        if context.model_training_used:
            flags.add(MLDatasetAssemblyRiskFlag.MODEL_TRAINING_ATTEMPTED)
        if context.model_prediction_used:
            flags.add(MLDatasetAssemblyRiskFlag.MODEL_PREDICTION_ATTEMPTED)

    return list(flags)

def dataset_assembly_safety_summary(errors: List[str]) -> Dict[str, Any]:
    return {"safe": len(errors) == 0, "error_count": len(errors), "errors": errors}

def dataset_assembly_safety_to_text(errors: List[str]) -> str:
    return json.dumps(dataset_assembly_safety_summary(errors), indent=2)
