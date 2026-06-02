from typing import Any

from usa_signal_bot.ml_research.ml_governance_closure.phase145_models import (
    MLGovernanceClosureResult,
    MLGovernanceClosureRule,
    MLGovernanceRuleKind,
    MLGovernanceClosureRuleStatus,
    ExplainabilityReport,
    AdvancedMLArtifactLineage,
    create_ml_governance_closure_rule_id,
    create_ml_governance_closure_result_id,
    current_time
)

def build_ml_governance_closure_rules(explainability_report: ExplainabilityReport, lineage: AdvancedMLArtifactLineage) -> list[MLGovernanceClosureRule]:
    rules = []

    # Example for EXPLAINABILITY_METADATA_VALID
    passed = explainability_report.report_valid and explainability_report.explainability_metadata_only
    rules.append(MLGovernanceClosureRule(
        rule_id=create_ml_governance_closure_rule_id(),
        created_at_utc=current_time(),
        rule_kind=MLGovernanceRuleKind.EXPLAINABILITY_METADATA_VALID,
        name="Explainability Metadata Only Check",
        status=MLGovernanceClosureRuleStatus.PASSED if passed else MLGovernanceClosureRuleStatus.FAILED,
        required=True,
        passed=passed,
        expected_value=True,
        observed_value=explainability_report.explainability_metadata_only,
        rationale="Explainability output must be research metadata only",
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    ))

    # Example for ARTIFACT_LINEAGE_COMPLETE
    rules.append(MLGovernanceClosureRule(
        rule_id=create_ml_governance_closure_rule_id(),
        created_at_utc=current_time(),
        rule_kind=MLGovernanceRuleKind.ARTIFACT_LINEAGE_COMPLETE,
        name="Artifact Lineage Complete Check",
        status=MLGovernanceClosureRuleStatus.PASSED if lineage.lineage_complete else MLGovernanceClosureRuleStatus.FAILED,
        required=True,
        passed=lineage.lineage_complete,
        expected_value=True,
        observed_value=lineage.lineage_complete,
        rationale="Phase 136-145 lineage must be complete",
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    ))

    # Example for NO_SIGNAL_OUTPUT
    passed = not explainability_report.produces_trade_signal
    rules.append(MLGovernanceClosureRule(
        rule_id=create_ml_governance_closure_rule_id(),
        created_at_utc=current_time(),
        rule_kind=MLGovernanceRuleKind.NO_SIGNAL_OUTPUT,
        name="No Trade Signal Output Check",
        status=MLGovernanceClosureRuleStatus.PASSED if passed else MLGovernanceClosureRuleStatus.FAILED,
        required=True,
        passed=passed,
        expected_value=False,
        observed_value=explainability_report.produces_trade_signal,
        rationale="Research artifacts must not produce trade signals",
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    ))

    return rules

def build_ml_governance_closure_result(
    explainability_report: ExplainabilityReport,
    lineage: AdvancedMLArtifactLineage
) -> MLGovernanceClosureResult:

    rules = build_ml_governance_closure_rules(explainability_report, lineage)
    passed = all(r.passed for r in rules if r.required)

    return MLGovernanceClosureResult(
        closure_id=create_ml_governance_closure_result_id(),
        created_at_utc=current_time(),
        rules=rules,
        closure_status=MLGovernanceClosureRuleStatus.PASSED if passed else MLGovernanceClosureRuleStatus.FAILED,
        closure_passed=passed,
        explainability_report=explainability_report,
        research_only_ml_outputs=True,
        live_use_allowed=False,
        paper_use_allowed=False,
        broker_use_allowed=False,
        deployment_allowed=False,
        strategy_activation_allowed=False,
        live_monitoring_allowed=False,
        alert_sender_allowed=False,
        backtest_execution_allowed=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def ml_governance_closure_passed(result: MLGovernanceClosureResult) -> bool:
    return result.closure_passed

def validate_ml_governance_closure_result(result: MLGovernanceClosureResult) -> list[str]:
    errors = []
    if result.live_use_allowed or result.paper_use_allowed or result.broker_use_allowed or result.deployment_allowed:
        errors.append("Governance closure allows execution or deployment")
    if result.strategy_activation_allowed or result.live_monitoring_allowed or result.alert_sender_allowed or result.backtest_execution_allowed:
        errors.append("Governance closure allows activation, monitoring or backtest execution")
    return errors

def ml_governance_closure_summary(result: MLGovernanceClosureResult) -> dict[str, Any]:
    return {
        "passed": result.closure_passed,
        "rule_count": len(result.rules),
        "failed_rules": [r.rule_kind.value for r in result.rules if not r.passed]
    }

def ml_governance_closure_to_text(result: MLGovernanceClosureResult, limit: int = 300) -> str:
    summary = ml_governance_closure_summary(result)
    return f"Governance Closure Passed: {summary['passed']}. Failed rules: {summary['failed_rules']}"
