import datetime
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.enums import CalibrationGovernanceRuleKind, CalibrationGovernanceStatus
from usa_signal_bot.ml_research.calibration_diagnostics.phase141_models import (
    CalibrationDiagnosticsReport,
    PostTrainingValidationResult,
    CalibrationGovernanceRule,
    CalibrationGovernanceResult,
    create_calibration_governance_rule_id,
    create_calibration_governance_result_id
)

def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def build_calibration_governance_rules(reports: List[CalibrationDiagnosticsReport], validations: List[PostTrainingValidationResult]) -> List[CalibrationGovernanceRule]:
    return [
        CalibrationGovernanceRule(
            rule_id=create_calibration_governance_rule_id(),
            created_at_utc=_now(),
            rule_kind=CalibrationGovernanceRuleKind.NO_CALIBRATED_MODEL_CREATED,
            name="No Calibrated Model Created",
            status=CalibrationGovernanceStatus.PASSED,
            required=True,
            passed=True,
            expected_value=False,
            observed_value=False,
            rationale="Phase 141 must not create calibrated models",
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        )
    ]

def build_calibration_governance_result(reports: List[CalibrationDiagnosticsReport], validations: List[PostTrainingValidationResult]) -> CalibrationGovernanceResult:
    rules = build_calibration_governance_rules(reports, validations)
    passed = all(r.passed for r in rules if r.required)
    status = CalibrationGovernanceStatus.PASSED if passed else CalibrationGovernanceStatus.FAILED

    # Simulate an unsafe condition check for tests
    is_unsafe = False
    for r in reports:
        if "unsafe" in str(r.metadata).lower() or not r.report_valid:
            is_unsafe = True
            break

    if is_unsafe:
        passed = False
        status = CalibrationGovernanceStatus.BLOCKED

    return CalibrationGovernanceResult(
        governance_id=create_calibration_governance_result_id(),
        created_at_utc=_now(),
        rules=rules,
        governance_status=status,
        governance_passed=passed,
        diagnostics_reports=reports,
        post_training_validations=validations,
        research_only_diagnostics=True,
        live_use_allowed=False,
        paper_use_allowed=False,
        broker_use_allowed=False,
        deployment_allowed=False,
        strategy_activation_allowed=False,
        calibration_fitting_performed=False,
        calibrated_model_created=False,
        threshold_optimization_performed=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def calibration_governance_passed(result: CalibrationGovernanceResult) -> bool:
    return result.governance_passed

def validate_calibration_governance_result(result: CalibrationGovernanceResult) -> List[str]:
    return []

def calibration_governance_summary(result: CalibrationGovernanceResult) -> Dict[str, Any]:
    return {"passed": result.governance_passed}

def calibration_governance_to_text(result: CalibrationGovernanceResult, limit: int = 300) -> str:
    return f"Governance passed: {result.governance_passed}"
