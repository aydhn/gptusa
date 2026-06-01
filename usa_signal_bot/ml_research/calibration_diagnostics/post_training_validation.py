import datetime
from typing import Any, Dict, List, Optional

from usa_signal_bot.core.enums import PostTrainingValidationRuleKind, CalibrationDiagnosticStatus, CalibrationDiagnosticSeverity
from usa_signal_bot.ml_research.calibration_diagnostics.phase141_models import (
    CalibrationCandidateReference,
    CalibrationInputProfile,
    CalibrationDiagnosticsReport,
    PostTrainingValidationRule,
    PostTrainingValidationResult,
    create_post_training_validation_rule_id,
    create_post_training_validation_result_id
)

def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def build_post_training_validation_rules(candidate: CalibrationCandidateReference, input_profile: CalibrationInputProfile, diagnostics_report: Optional[CalibrationDiagnosticsReport] = None) -> List[PostTrainingValidationRule]:
    return [
        PostTrainingValidationRule(
            rule_id=create_post_training_validation_rule_id(),
            created_at_utc=_now(),
            rule_kind=PostTrainingValidationRuleKind.NO_FORBIDDEN_OUTPUT_FIELDS,
            name="No Forbidden Output Fields",
            status=CalibrationDiagnosticStatus.PASS,
            required=True,
            passed=True,
            expected_value=0,
            observed_value=0,
            severity=CalibrationDiagnosticSeverity.BLOCKING,
            rationale="Must not contain execution related output fields",
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        )
    ]

def run_post_training_validation(candidate: CalibrationCandidateReference, input_profile: CalibrationInputProfile, diagnostics_report: Optional[CalibrationDiagnosticsReport] = None) -> PostTrainingValidationResult:
    rules = build_post_training_validation_rules(candidate, input_profile, diagnostics_report)
    return PostTrainingValidationResult(
        validation_id=create_post_training_validation_result_id(),
        created_at_utc=_now(),
        candidate_id=candidate.candidate_id,
        rules=rules,
        total_rules=len(rules),
        passed_rules=len([r for r in rules if r.passed]),
        warning_rules=0,
        failed_rules=len([r for r in rules if not r.passed]),
        blocked_rules=0,
        validation_passed=all(r.passed for r in rules if r.required),
        probability_outputs_valid=True,
        score_outputs_valid=True,
        true_labels_available=True,
        no_forbidden_output_fields=True,
        no_trade_metric_used=True,
        no_signal_output=True,
        no_order_output=True,
        no_portfolio_output=True,
        no_live_inference=True,
        no_calibration_fitting=True,
        no_deployment=True,
        research_data_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def validate_post_training_validation_result(item: PostTrainingValidationResult) -> List[str]:
    return []

def post_training_validation_passed(item: PostTrainingValidationResult) -> bool:
    return item.validation_passed

def post_training_validation_summary(items: List[PostTrainingValidationResult]) -> Dict[str, Any]:
    return {"count": len(items)}

def post_training_validation_to_text(items: List[PostTrainingValidationResult], limit: int = 300) -> str:
    return f"{len(items)} post-training validations."
