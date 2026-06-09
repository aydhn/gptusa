from typing import Any, Dict, List


from usa_signal_bot.release.phase159_models import (
    AdvancedAcceptanceInputReference,
    AcceptanceScenarioMatrix,
    AdvancedDryRunStep,
    AcceptanceEvidenceBundle,
    ReleaseCandidateAudit,
    FinalFreezeCertificate,
    Phase160HandoffPackage,
    AdvancedAcceptanceContext
)

def validate_advanced_acceptance_input_reference_schema(item: AdvancedAcceptanceInputReference) -> List[str]:
    errors = []
    if not hasattr(item, "input_ref_id"):
        errors.append("Missing input_ref_id")
    if not hasattr(item, "input_kind"):
        errors.append("Missing input_kind")
    if not hasattr(item, "valid"):
        errors.append("Missing valid")
    return errors

def validate_acceptance_scenario_matrix_schema(matrix: AcceptanceScenarioMatrix) -> List[str]:
    errors = []
    if not hasattr(matrix, "matrix_id"):
        errors.append("Missing matrix_id")
    if not hasattr(matrix, "scenarios"):
        errors.append("Missing scenarios")
    return errors

def validate_advanced_dry_run_steps_schema(items: List[AdvancedDryRunStep]) -> List[str]:
    errors = []
    for i, item in enumerate(items):
        if not hasattr(item, "step_id"):
            errors.append(f"Step {i} missing step_id")
        if not hasattr(item, "status"):
            errors.append(f"Step {i} missing status")
    return errors

def validate_acceptance_evidence_bundle_schema(bundle: AcceptanceEvidenceBundle) -> List[str]:
    errors = []
    if not hasattr(bundle, "bundle_id"):
        errors.append("Missing bundle_id")
    if not hasattr(bundle, "evidence_items"):
        errors.append("Missing evidence_items")
    return errors

def validate_release_candidate_audit_schema(audit: ReleaseCandidateAudit) -> List[str]:
    errors = []
    if not hasattr(audit, "audit_id"):
        errors.append("Missing audit_id")
    if not hasattr(audit, "audit_status"):
        errors.append("Missing audit_status")
    return errors

def validate_final_freeze_certificate_schema(certificate: FinalFreezeCertificate) -> List[str]:
    errors = []
    if not hasattr(certificate, "certificate_id"):
        errors.append("Missing certificate_id")
    if not hasattr(certificate, "frozen"):
        errors.append("Missing frozen")
    return errors

def validate_phase160_handoff_package_schema(package: Phase160HandoffPackage) -> List[str]:
    errors = []
    if not hasattr(package, "package_id"):
        errors.append("Missing package_id")
    if not hasattr(package, "package_valid"):
        errors.append("Missing package_valid")
    return errors

def validate_advanced_acceptance_context_schema(context: AdvancedAcceptanceContext) -> List[str]:
    errors = []
    if not hasattr(context, "context_id"):
        errors.append("Missing context_id")
    if not hasattr(context, "status"):
        errors.append("Missing status")
    return errors

def validate_advanced_acceptance_column_names(columns: List[str]) -> List[str]:
    from usa_signal_bot.release.advanced_acceptance_input_resolver import detect_forbidden_advanced_acceptance_columns
    return detect_forbidden_advanced_acceptance_columns(columns)

def validate_no_forbidden_advanced_acceptance_columns(columns: List[str]) -> List[str]:
    forbidden = validate_advanced_acceptance_column_names(columns)
    if forbidden:
        return [f"Forbidden column detected: {c}" for c in forbidden]
    return []

def advanced_acceptance_schema_summary(errors: List[str]) -> Dict[str, Any]:
    return {
        "valid": len(errors) == 0,
        "error_count": len(errors)
    }

def advanced_acceptance_schema_to_text(errors: List[str]) -> str:
    if not errors:
        return "Schema Validation: PASSED"
    lines = ["Schema Validation: FAILED"]
    for e in errors:
        lines.append(f" - {e}")
    return "\n".join(lines)
