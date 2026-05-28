import datetime
from typing import Any, Dict, List
from usa_signal_bot.core.enums import FinalClosureRuleKind, FinalClosureRuleStatus, FinalClosureQuality, FinalClosureRiskFlag
from usa_signal_bot.feature_engine.final_closure.phase125_models import (
    FreezePreparationIngestionResult,
    FinalClosureArtifactReference,
    FinalClosureRule,
    FinalClosureResult,
    create_final_closure_rule_id,
    create_final_closure_result_id
)

def _create_rule(kind: FinalClosureRuleKind, passed: bool, rationale: str) -> FinalClosureRule:
    return FinalClosureRule(
        rule_id=create_final_closure_rule_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        rule_kind=kind,
        name=kind.value,
        status=FinalClosureRuleStatus.PASS if passed else FinalClosureRuleStatus.FAIL,
        required=True,
        passed=passed,
        expected_value=True,
        observed_value=passed,
        rationale=rationale,
        warnings=[],
        errors=[] if passed else [rationale],
        risk_flags=[],
        metadata={}
    )

def rule_phase124_freeze_preparation_valid(ingestion: FreezePreparationIngestionResult) -> FinalClosureRule:
    passed = ingestion.valid_for_phase125
    return _create_rule(FinalClosureRuleKind.PHASE124_FREEZE_PREPARATION_VALID, passed, "Freeze preparation must be valid")

def rule_artifact_chain_complete(artifacts: List[FinalClosureArtifactReference]) -> FinalClosureRule:
    passed = all(a.available for a in artifacts if a.required)
    return _create_rule(FinalClosureRuleKind.ARTIFACT_CHAIN_COMPLETE, passed, "Artifact chain must be complete")

def rule_integration_rehearsal_passed(ingestion: FreezePreparationIngestionResult) -> FinalClosureRule:
    passed = ingestion.integration_rehearsal_ready
    return _create_rule(FinalClosureRuleKind.INTEGRATION_REHEARSAL_PASSED, passed, "Integration rehearsal must be passed")

def rule_report_qa_accepted(ingestion: FreezePreparationIngestionResult) -> FinalClosureRule:
    passed = ingestion.report_qa_accepted
    return _create_rule(FinalClosureRuleKind.REPORT_QA_ACCEPTED, passed, "Report QA must be accepted")

def rule_freeze_candidate_ready(ingestion: FreezePreparationIngestionResult) -> FinalClosureRule:
    passed = ingestion.freeze_candidate_ready
    return _create_rule(FinalClosureRuleKind.FREEZE_CANDIDATE_READY, passed, "Freeze candidate must be ready")

def rule_freeze_readiness_gate_passed(ingestion: FreezePreparationIngestionResult) -> FinalClosureRule:
    passed = ingestion.freeze_readiness_gate_ready
    return _create_rule(FinalClosureRuleKind.FREEZE_READINESS_GATE_PASSED, passed, "Freeze readiness gate must be passed")

def rule_no_signal_order_portfolio_execution(ingestion: FreezePreparationIngestionResult, artifacts: List[FinalClosureArtifactReference]) -> FinalClosureRule:
    passed = (
        not ingestion.produces_trade_signal and
        not ingestion.produces_order_decision and
        not ingestion.produces_portfolio_weights and
        not ingestion.broker_execution_enabled and
        not ingestion.order_creation_enabled and
        not ingestion.paper_state_mutation_enabled and
        not ingestion.investment_advice
    )
    return _create_rule(FinalClosureRuleKind.NO_SIGNAL_OUTPUT, passed, "Must not produce signals, orders, portfolio weights, or execution")


def build_final_closure_rules(ingestion: FreezePreparationIngestionResult, artifacts: List[FinalClosureArtifactReference]) -> List[FinalClosureRule]:
    return [
        rule_phase124_freeze_preparation_valid(ingestion),
        rule_artifact_chain_complete(artifacts),
        rule_integration_rehearsal_passed(ingestion),
        rule_report_qa_accepted(ingestion),
        rule_freeze_candidate_ready(ingestion),
        rule_freeze_readiness_gate_passed(ingestion),
        rule_no_signal_order_portfolio_execution(ingestion, artifacts)
    ]

def final_closure_quality_from_rules(rules: List[FinalClosureRule]) -> FinalClosureQuality:
    if all(r.passed for r in rules):
        return FinalClosureQuality.HIGH
    if any(r.status == FinalClosureRuleStatus.BLOCKED for r in rules):
        return FinalClosureQuality.BLOCKED
    return FinalClosureQuality.INVALID

def run_final_closure_checks(ingestion: FreezePreparationIngestionResult, artifacts: List[FinalClosureArtifactReference]) -> FinalClosureResult:
    rules = build_final_closure_rules(ingestion, artifacts)
    passed_rules = sum(1 for r in rules if r.passed)
    failed_rules = sum(1 for r in rules if r.status == FinalClosureRuleStatus.FAIL)

    missing_required_artifact_count = sum(1 for a in artifacts if a.required and not a.available)
    unsafe_artifact_count = sum(1 for a in artifacts if a.contains_secret or a.contains_forbidden_columns or a.contains_execution_language)

    closure_passed = failed_rules == 0 and unsafe_artifact_count == 0

    return FinalClosureResult(
        closure_result_id=create_final_closure_result_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        rules=rules,
        total_rules=len(rules),
        passed_rules=passed_rules,
        warning_rules=0,
        failed_rules=failed_rules,
        blocked_rules=0,
        closure_passed=closure_passed,
        quality=final_closure_quality_from_rules(rules),
        artifact_count=len(artifacts),
        missing_required_artifact_count=missing_required_artifact_count,
        unsafe_artifact_count=unsafe_artifact_count,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def final_closure_checks_summary(result: FinalClosureResult) -> Dict[str, Any]:
    return {
        "passed": result.closure_passed,
        "quality": result.quality.value,
        "passed_rules": result.passed_rules,
        "failed_rules": result.failed_rules
    }

def final_closure_checks_to_text(result: FinalClosureResult, limit: int = 300) -> str:
    summary = final_closure_checks_summary(result)
    return f"ClosureChecks: Passed={summary['passed']}, Quality={summary['quality']}, Rules Passed={summary['passed_rules']}"
