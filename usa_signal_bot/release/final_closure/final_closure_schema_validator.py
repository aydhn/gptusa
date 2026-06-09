from typing import List, Dict, Any
from usa_signal_bot.release.final_closure.phase160_models import (
    FinalInputReference,
    FinalArtifactIndex,
    FinalPhaseLineage,
    FinalSystemAuditReport,
    FinalDeliveryCertificate,
    ProjectClosureReport,
    ProjectClosureManifest,
    FinalClosureContext
)

def validate_final_input_reference_schema(item: FinalInputReference) -> List[str]:
    errors = []
    if not hasattr(item, "input_ref_id"):
        errors.append("Missing input_ref_id")
    return errors

def validate_final_artifact_index_schema(index: FinalArtifactIndex) -> List[str]:
    errors = []
    if not hasattr(index, "index_id"):
        errors.append("Missing index_id")
    return errors

def validate_final_phase_lineage_schema(lineage: FinalPhaseLineage) -> List[str]:
    errors = []
    if not hasattr(lineage, "lineage_id"):
        errors.append("Missing lineage_id")
    return errors

def validate_final_system_audit_report_schema(report: FinalSystemAuditReport) -> List[str]:
    errors = []
    if not hasattr(report, "audit_id"):
        errors.append("Missing audit_id")
    return errors

def validate_final_delivery_certificate_schema(certificate: FinalDeliveryCertificate) -> List[str]:
    errors = []
    if not hasattr(certificate, "certificate_id"):
        errors.append("Missing certificate_id")
    return errors

def validate_project_closure_report_schema(report: ProjectClosureReport) -> List[str]:
    errors = []
    if not hasattr(report, "report_id"):
        errors.append("Missing report_id")
    return errors

def validate_project_closure_manifest_schema(manifest: ProjectClosureManifest) -> List[str]:
    errors = []
    if not hasattr(manifest, "manifest_id"):
        errors.append("Missing manifest_id")
    return errors

def validate_final_closure_context_schema(context: FinalClosureContext) -> List[str]:
    errors = []
    if not hasattr(context, "context_id"):
        errors.append("Missing context_id")
    return errors

def validate_no_forbidden_final_closure_columns(columns: List[str]) -> List[str]:
    from usa_signal_bot.release.final_closure.final_input_resolver import detect_forbidden_final_closure_columns
    forbidden = detect_forbidden_final_closure_columns(columns)
    if forbidden:
        return [f"Forbidden final closure columns found: {forbidden}"]
    return []

def validate_final_closure_column_names(columns: List[str]) -> List[str]:
    return validate_no_forbidden_final_closure_columns(columns)

def final_closure_schema_summary(errors: List[str]) -> Dict[str, Any]:
    return {"valid": len(errors) == 0, "error_count": len(errors), "errors": errors}

def final_closure_schema_to_text(errors: List[str]) -> str:
    return f"Schema Validation: Valid={len(errors) == 0}, Errors={len(errors)}"
