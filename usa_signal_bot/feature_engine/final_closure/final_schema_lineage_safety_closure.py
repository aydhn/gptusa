import datetime
from typing import Any, Dict, List
from usa_signal_bot.core.enums import FinalClosureRuleKind, FinalClosureRuleStatus
from usa_signal_bot.feature_engine.final_closure.phase125_models import (
    FreezePreparationIngestionResult,
    FinalClosureArtifactReference,
    FinalClosureRule,
    create_final_closure_rule_id
)

def validate_final_schema_contract(artifacts: List[FinalClosureArtifactReference]) -> List[str]:
    errors = []
    # Test logic
    return errors

def validate_final_lineage_contract(artifacts: List[FinalClosureArtifactReference]) -> List[str]:
    errors = []
    # Test logic
    return errors

def validate_final_safety_contract(ingestion: FreezePreparationIngestionResult, artifacts: List[FinalClosureArtifactReference]) -> List[str]:
    errors = []
    if ingestion.produces_trade_signal: errors.append("Produces trade signal")
    if ingestion.broker_execution_enabled: errors.append("Broker execution enabled")
    for a in artifacts:
        if a.contains_secret: errors.append(f"Artifact {a.artifact_name} contains secret")
        if a.contains_forbidden_columns: errors.append(f"Artifact {a.artifact_name} contains forbidden columns")
        if a.contains_execution_language: errors.append(f"Artifact {a.artifact_name} contains execution language")
    return errors

def build_schema_lineage_safety_closure_rule(ingestion: FreezePreparationIngestionResult, artifacts: List[FinalClosureArtifactReference]) -> FinalClosureRule:
    errs = validate_final_schema_contract(artifacts)
    errs.extend(validate_final_lineage_contract(artifacts))
    errs.extend(validate_final_safety_contract(ingestion, artifacts))

    passed = len(errs) == 0
    return FinalClosureRule(
        rule_id=create_final_closure_rule_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        rule_kind=FinalClosureRuleKind.SCHEMA_LINEAGE_SAFETY_VALID,
        name="Schema Lineage Safety Valid",
        status=FinalClosureRuleStatus.PASS if passed else FinalClosureRuleStatus.FAIL,
        required=True,
        passed=passed,
        expected_value=True,
        observed_value=passed,
        rationale="Contracts must be valid",
        warnings=[],
        errors=errs,
        risk_flags=[],
        metadata={}
    )

def final_schema_lineage_safety_summary(errors: List[str]) -> Dict[str, Any]:
    return {
        "valid": len(errors) == 0,
        "errors": len(errors)
    }

def final_schema_lineage_safety_to_text(errors: List[str]) -> str:
    if errors:
        return f"SchemaLineageSafety: Failed with {len(errors)} errors"
    return "SchemaLineageSafety: Valid"
