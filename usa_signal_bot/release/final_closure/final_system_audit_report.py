from typing import List, Dict, Any
from usa_signal_bot.release.final_closure.phase160_models import (
    FinalSystemAuditReport,
    FinalSystemAuditChecklist,
    FinalArtifactIndex,
    FinalPhaseLineage,
    FinalAuditStatus,
    FinalClosureRiskFlag,
    create_final_system_audit_report_id,
    generate_timestamp
)
import hashlib
import json

def compute_final_system_audit_report_hash(report: FinalSystemAuditReport) -> str:
    # Use basic components that define this report's state
    state = {
        "checklist_hash": report.checklist.checklist_hash,
        "artifact_index_hash": report.artifact_index.index_hash,
        "phase_lineage_hash": report.phase_lineage.lineage_hash,
        "audit_passed": report.audit_passed,
        "audit_status": report.audit_status.value
    }
    data = json.dumps(state, sort_keys=True)
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def build_final_system_audit_report(
    checklist: FinalSystemAuditChecklist,
    index: FinalArtifactIndex,
    lineage: FinalPhaseLineage
) -> FinalSystemAuditReport:

    passed = checklist.checklist_valid and index.index_valid and lineage.lineage_valid
    status = FinalAuditStatus.PASSED if passed else FinalAuditStatus.FAILED

    errors = []
    risk_flags = []
    if not passed:
        errors.append("Audit failed due to invalid checklist, index, or lineage.")
        risk_flags.append(FinalClosureRiskFlag.FINAL_SYSTEM_AUDIT_FAILED)

    report = FinalSystemAuditReport(
        audit_id=create_final_system_audit_report_id(),
        created_at_utc=generate_timestamp(),
        checklist=checklist,
        artifact_index=index,
        phase_lineage=lineage,
        audit_status=status,
        audit_passed=passed,
        audit_hash=None,
        not_deployment_approval=True,
        not_trading_approval=True,
        not_investment_advice=True,
        warnings=[],
        errors=errors,
        risk_flags=risk_flags,
        metadata={}
    )

    report.audit_hash = compute_final_system_audit_report_hash(report)
    return report

def validate_final_system_audit_report(report: FinalSystemAuditReport) -> List[str]:
    errors = []
    if not report.audit_passed:
        errors.extend(report.errors)
    return errors

def final_system_audit_report_to_text(report: FinalSystemAuditReport, limit: int = 300) -> str:
    return f"Final System Audit Report: Passed={report.audit_passed}, Status={report.audit_status.value}"
