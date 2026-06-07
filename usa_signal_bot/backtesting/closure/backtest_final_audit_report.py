import hashlib
import json
from typing import Any
from usa_signal_bot.backtesting.closure.phase152_models import (
    BacktestFinalAuditReport, ArtifactLineageManifest, ArtifactAvailabilityAudit,
    DeterminismComplianceAudit, SafetyComplianceAudit, ResearchBoundaryAudit,
    BacktestMetricInventoryItem, BacktestRiskNote, RobustnessEvidenceRecord,
    AcceptanceSummary, ClosureBlocker, BacktestClosureRiskFlag
)

def compute_backtest_final_audit_report_hash(report: BacktestFinalAuditReport) -> str:
    # simple deterministic hash
    content = f"{report.artifact_lineage.lineage_hash}_{report.acceptance_summary.passed_count}_{report.final_audit_passed}"
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def build_backtest_final_audit_report(
    artifact_lineage: ArtifactLineageManifest,
    availability_audit: ArtifactAvailabilityAudit,
    determinism_audit: DeterminismComplianceAudit,
    safety_audit: SafetyComplianceAudit,
    research_boundary_audit: ResearchBoundaryAudit,
    metric_inventory: list[BacktestMetricInventoryItem],
    risk_notes: list[BacktestRiskNote],
    robustness_evidence: list[RobustnessEvidenceRecord],
    acceptance_summary: AcceptanceSummary,
    blockers: list[ClosureBlocker]) -> BacktestFinalAuditReport:

    report = BacktestFinalAuditReport()
    report.artifact_lineage = artifact_lineage
    report.availability_audit = availability_audit
    report.determinism_audit = determinism_audit
    report.safety_audit = safety_audit
    report.research_boundary_audit = research_boundary_audit
    report.metric_inventory = metric_inventory
    report.risk_notes = risk_notes
    report.robustness_evidence = robustness_evidence
    report.acceptance_summary = acceptance_summary
    report.blockers = blockers

    report.final_audit_passed = acceptance_summary.acceptance_passed and len(blockers) == 0
    report.report_valid = True

    report.report_hash = compute_backtest_final_audit_report_hash(report)

    if not report.final_audit_passed:
        report.risk_flags.append(BacktestClosureRiskFlag.FINAL_AUDIT_REPORT_INVALID)
        report.errors.append("Final audit failed")

    return report

def validate_backtest_final_audit_report(report: BacktestFinalAuditReport) -> list[str]:
    errors = []
    if not report.report_valid:
        errors.append("Final audit report is invalid")
    return errors

def backtest_final_audit_report_summary(report: BacktestFinalAuditReport) -> dict[str, Any]:
    return {"passed": report.final_audit_passed, "hash": report.report_hash}

def backtest_final_audit_report_to_text(report: BacktestFinalAuditReport, limit: int = 300) -> str:
    return f"BacktestFinalAuditReport(passed={report.final_audit_passed})"
