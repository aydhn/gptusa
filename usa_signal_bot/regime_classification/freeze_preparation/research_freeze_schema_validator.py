from typing import Any, Dict, List
from usa_signal_bot.regime_classification.freeze_preparation.phase134_models import (
    MonitoringValidationResult,
    DriftReportDocument,
    ResearchFreezePackage,
    RegimeResearchFreezeContext
)
from usa_signal_bot.regime_classification.freeze_preparation.research_freeze_safety_validator import FORBIDDEN_FRAGMENTS

def validate_monitoring_validation_result_schema(item: MonitoringValidationResult) -> List[str]:
    errors = []
    if not item.validation_id:
        errors.append("Missing validation_id")
    if not item.rules:
        errors.append("Missing rules")
    return errors

def validate_drift_report_document_schema(item: DriftReportDocument) -> List[str]:
    errors = []
    if not item.document_id:
        errors.append("Missing document_id")
    if not item.sections:
        errors.append("Missing sections")
    return errors

def validate_research_freeze_package_schema(item: ResearchFreezePackage) -> List[str]:
    errors = []
    if not item.package_id:
        errors.append("Missing package_id")
    if not item.artifact_references:
        errors.append("Missing artifact_references")
    if not item.drift_report:
        errors.append("Missing drift_report")
    if not item.monitoring_validation:
        errors.append("Missing monitoring_validation")
    return errors

def validate_research_freeze_context_schema(context: RegimeResearchFreezeContext) -> List[str]:
    errors = []
    if not context.context_id:
        errors.append("Missing context_id")
    if not context.ingestion:
        errors.append("Missing ingestion")
    return errors

def validate_no_forbidden_research_freeze_columns(columns: List[str]) -> List[str]:
    errors = []
    for col in columns:
        col_lower = str(col).lower()
        if "signal" in col_lower:
            if "macd_signal" not in col_lower and "signal" in col_lower.replace("macd_signal", ""):
                errors.append(f"Forbidden column detected: {col}")
                continue
        for frag in FORBIDDEN_FRAGMENTS:
            if frag in col_lower and frag != "signal":
                errors.append(f"Forbidden column detected: {col}")
                break
    return errors

def validate_research_freeze_column_names(columns: List[str]) -> List[str]:
    return validate_no_forbidden_research_freeze_columns(columns)

def research_freeze_schema_summary(errors: List[str]) -> Dict[str, Any]:
    return {
        "valid": len(errors) == 0,
        "error_count": len(errors),
        "errors": errors
    }

def research_freeze_schema_to_text(errors: List[str]) -> str:
    if not errors:
        return "Schema Validation Passed."
    return f"Schema Validation Failed with {len(errors)} errors:\n" + "\n".join(f"- {e}" for e in errors)
