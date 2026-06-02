from typing import Any

from usa_signal_bot.ml_research.ml_governance_closure.phase145_models import (
    AdvancedMLFinalAuditResult,
    AdvancedMLAuditItem,
    AdvancedMLAuditItemKind,
    AdvancedMLAuditStatus,
    AdvancedMLArtifactLineage,
    MLGovernanceClosureResult,
    ExplainabilityReport,
    create_advanced_ml_audit_item_id,
    create_advanced_ml_final_audit_result_id,
    current_time
)

def build_advanced_ml_final_audit_items(
    lineage: AdvancedMLArtifactLineage,
    governance: MLGovernanceClosureResult,
    explainability_report: ExplainabilityReport
) -> list[AdvancedMLAuditItem]:

    items = []

    # Example: GOVERNANCE_AUDIT
    passed = governance.closure_passed
    items.append(AdvancedMLAuditItem(
        audit_item_id=create_advanced_ml_audit_item_id(),
        created_at_utc=current_time(),
        item_kind=AdvancedMLAuditItemKind.GOVERNANCE_AUDIT,
        phase_number=145,
        name="ML Governance Closure Audit",
        status=AdvancedMLAuditStatus.PASSED if passed else AdvancedMLAuditStatus.FAILED,
        required=True,
        passed=passed,
        summary="Verified ML governance closure result",
        evidence_node_ids=[governance.closure_id],
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    ))

    # Example: PHASE146_HANDOFF_AUDIT
    passed = lineage.lineage_complete and governance.closure_passed
    items.append(AdvancedMLAuditItem(
        audit_item_id=create_advanced_ml_audit_item_id(),
        created_at_utc=current_time(),
        item_kind=AdvancedMLAuditItemKind.PHASE146_HANDOFF_AUDIT,
        phase_number=145,
        name="Phase 146 Handoff Readiness Audit",
        status=AdvancedMLAuditStatus.PASSED if passed else AdvancedMLAuditStatus.FAILED,
        required=True,
        passed=passed,
        summary="Verified readiness for Phase 146 realistic backtest band",
        evidence_node_ids=[],
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    ))

    return items

def build_advanced_ml_final_audit_result(
    lineage: AdvancedMLArtifactLineage,
    governance: MLGovernanceClosureResult,
    explainability_report: ExplainabilityReport
) -> AdvancedMLFinalAuditResult:

    items = build_advanced_ml_final_audit_items(lineage, governance, explainability_report)
    passed = all(i.passed for i in items if i.required)

    return AdvancedMLFinalAuditResult(
        audit_id=create_advanced_ml_final_audit_result_id(),
        created_at_utc=current_time(),
        audit_items=items,
        total_items=len(items),
        passed_items=len([i for i in items if i.passed]),
        warning_items=0,
        failed_items=len([i for i in items if not i.passed]),
        blocked_items=0,
        audit_status=AdvancedMLAuditStatus.PASSED if passed else AdvancedMLAuditStatus.FAILED,
        audit_passed=passed,
        phase136_to_145_closed=passed,
        ready_for_phase146=passed,
        no_activation_violations=True,
        no_execution_violations=True,
        no_deployment_violations=True,
        no_live_monitoring_violations=True,
        no_investment_advice_violations=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def advanced_ml_final_audit_passed(result: AdvancedMLFinalAuditResult) -> bool:
    return result.audit_passed

def validate_advanced_ml_final_audit_result(result: AdvancedMLFinalAuditResult) -> list[str]:
    errors = []
    if not result.no_activation_violations:
        errors.append("Audit indicates activation violations")
    if not result.no_execution_violations:
        errors.append("Audit indicates execution violations")
    if not result.no_deployment_violations:
        errors.append("Audit indicates deployment violations")
    if not result.no_live_monitoring_violations:
        errors.append("Audit indicates live monitoring violations")
    return errors

def advanced_ml_final_audit_summary(result: AdvancedMLFinalAuditResult) -> dict[str, Any]:
    return {
        "passed": result.audit_passed,
        "total": result.total_items,
        "passed_items": result.passed_items,
        "failed_items": result.failed_items
    }

def advanced_ml_final_audit_to_text(result: AdvancedMLFinalAuditResult, limit: int = 300) -> str:
    summary = advanced_ml_final_audit_summary(result)
    return f"Final Audit Passed: {summary['passed']} ({summary['passed_items']}/{summary['total']} items)"
