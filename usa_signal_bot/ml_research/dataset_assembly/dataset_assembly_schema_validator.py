from typing import Any, Dict, List
from usa_signal_bot.ml_research.dataset_assembly.phase137_models import (
    MLDatasetSourceReference,
    MLMatrixAssemblyResult,
    MLAssembledDatasetManifest,
    MLSplitPolicy,
    MLSplitAssignment,
    MLLeakageAuditResult,
    MLDatasetAssemblyContext
)
import json

def validate_dataset_source_reference_schema(item: MLDatasetSourceReference) -> List[str]:
    errors = []
    if not item.source_ref_id:
        errors.append("source_ref_id missing")
    if not item.source_name:
        errors.append("source_name missing")
    return errors

def validate_matrix_assembly_result_schema(item: MLMatrixAssemblyResult) -> List[str]:
    errors = []
    if not item.result_id:
        errors.append("result_id missing")
    if item.row_count < 0:
        errors.append("row_count cannot be negative")
    return errors

def validate_dataset_manifest_schema(item: MLAssembledDatasetManifest) -> List[str]:
    errors = []
    if not item.manifest_id:
        errors.append("manifest_id missing")
    return errors

def validate_split_policy_schema(item: MLSplitPolicy) -> List[str]:
    errors = []
    if not item.policy_id:
        errors.append("policy_id missing")
    return errors

def validate_split_assignment_schema(item: MLSplitAssignment) -> List[str]:
    errors = []
    if not item.assignment_id:
        errors.append("assignment_id missing")
    return errors

def validate_leakage_audit_schema(item: MLLeakageAuditResult) -> List[str]:
    errors = []
    if not item.audit_id:
        errors.append("audit_id missing")
    return errors

def validate_dataset_assembly_context_schema(context: MLDatasetAssemblyContext) -> List[str]:
    errors = []
    if not context.context_id:
        errors.append("context_id missing")
    return errors

def validate_no_forbidden_dataset_assembly_columns(columns: List[str]) -> List[str]:
    forbidden = ["buy", "sell", "order", "broker", "position", "portfolio_weight", "target_weight", "allocation", "paper", "live", "demo_order", "live_order", "sent_to_broker", "deploy", "production_patch", "strategy_active", "deployment_enabled"]
    errors = []
    for c in columns:
        cl = c.lower()
        if "signal" in cl and cl != "macd_signal_9":
            errors.append(f"Forbidden column name: {c}")
        elif "entry" in cl or "exit" in cl:
            errors.append(f"Forbidden column name: {c}")
        elif any(f in cl for f in forbidden):
            errors.append(f"Forbidden column name: {c}")
    return errors

def validate_dataset_assembly_column_names(columns: List[str]) -> List[str]:
    return validate_no_forbidden_dataset_assembly_columns(columns)

def dataset_assembly_schema_summary(errors: List[str]) -> Dict[str, Any]:
    return {"valid": len(errors) == 0, "error_count": len(errors), "errors": errors}

def dataset_assembly_schema_to_text(errors: List[str]) -> str:
    return json.dumps(dataset_assembly_schema_summary(errors), indent=2)
