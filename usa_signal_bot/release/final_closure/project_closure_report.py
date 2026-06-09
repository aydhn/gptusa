from typing import List, Dict, Any
from usa_signal_bot.release.final_closure.phase160_models import (
    ProjectClosureReport,
    FinalDeliveryCertificate,
    FinalSystemAuditReport,
    FinalSafetyClosure,
    FinalLimitationRegister,
    FinalDocumentationIndex,
    FinalRunbookIndex,
    FinalTestEvidenceSummary,
    FinalQualityObservabilitySummary,
    ProjectClosureStatus,
    FinalClosureRiskFlag,
    create_project_closure_report_id,
    generate_timestamp
)
import hashlib
import json

def compute_project_closure_report_hash(report: ProjectClosureReport) -> str:
    state = {
        "project_name": report.project_name,
        "total_phases": report.total_phases,
        "final_delivery_certificate_hash": report.final_delivery_certificate.certificate_hash,
        "final_audit_report_hash": report.final_audit_report.audit_hash,
        "closure_status": report.closure_status.value,
        "project_closed": report.project_closed
    }
    data = json.dumps(state, sort_keys=True)
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def build_project_closure_report(
    certificate: FinalDeliveryCertificate,
    audit: FinalSystemAuditReport,
    safety: FinalSafetyClosure,
    limitations: FinalLimitationRegister,
    docs: FinalDocumentationIndex,
    runbooks: FinalRunbookIndex,
    tests: FinalTestEvidenceSummary,
    quality: FinalQualityObservabilitySummary
) -> ProjectClosureReport:

    closed = (
        certificate.delivered and
        audit.audit_passed and
        safety.safety_closure_passed and
        docs.index_valid and
        runbooks.index_valid and
        tests.summary_valid and
        quality.summary_valid
    )

    status = ProjectClosureStatus.CLOSED if closed else ProjectClosureStatus.FAILED

    errors = []
    risk_flags = []
    if not closed:
        errors.append("Project closure failed due to unmet dependencies or certificates.")
        risk_flags.append(FinalClosureRiskFlag.PROJECT_CLOSURE_REPORT_INVALID)

    report = ProjectClosureReport(
        report_id=create_project_closure_report_id(),
        created_at_utc=generate_timestamp(),
        project_name="USA Signal Bot",
        total_phases=160,
        final_delivery_certificate=certificate,
        final_audit_report=audit,
        final_safety_closure=safety,
        limitation_register=limitations,
        documentation_index=docs,
        runbook_index=runbooks,
        test_evidence_summary=tests,
        quality_observability_summary=quality,
        closure_status=status,
        project_closed=closed,
        report_hash=None,
        not_deployment_approval=True,
        not_trading_approval=True,
        not_investment_advice=True,
        warnings=[],
        errors=errors,
        risk_flags=risk_flags,
        metadata={}
    )

    report.report_hash = compute_project_closure_report_hash(report)
    return report

def validate_project_closure_report(report: ProjectClosureReport) -> List[str]:
    errors = []
    if not report.project_closed:
        errors.extend(report.errors)
    return errors

def project_closure_report_to_text(report: ProjectClosureReport, limit: int = 300) -> str:
    return f"Project Closure Report: Closed={report.project_closed}, Status={report.closure_status.value}"
