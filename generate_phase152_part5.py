import os
import textwrap

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(textwrap.dedent(content).lstrip())

# 15. CLOSURE BLOCKER DETECTOR
write_file("usa_signal_bot/backtesting/closure/closure_blocker_detector.py", """
from typing import Any
from usa_signal_bot.backtesting.closure.phase152_models import (
    ClosureBlocker, BacktestClosureRiskFlag, BacktestBandPhase
)

def blocker_from_risk_flag(flag: BacktestClosureRiskFlag, message: str, source_phase: BacktestBandPhase | None = None) -> ClosureBlocker:
    return ClosureBlocker(
        blocker_name=flag.name,
        blocker_detected=True,
        severity="CRITICAL",
        message=message,
        source_phase=source_phase,
        risk_flag=flag,
        resolution_hint="Review documentation and ensure constraints are met."
    )

def detect_closure_blockers(final_audit_inputs: dict[str, Any]) -> list[ClosureBlocker]:
    blockers = []

    # Check ingestion
    ingestion = final_audit_inputs.get("ingestion")
    if ingestion and not ingestion.valid_for_phase152:
        blockers.append(blocker_from_risk_flag(BacktestClosureRiskFlag.PHASE151_NOT_READY, "Phase 151 ingestion not valid"))

    # Check safety audits
    safety = final_audit_inputs.get("safety_audit")
    if safety and not safety.audit_passed:
        blockers.append(blocker_from_risk_flag(BacktestClosureRiskFlag.SAFETY_COMPLIANCE_FAILED, "Safety audit failed"))

    research = final_audit_inputs.get("research_boundary_audit")
    if research and not research.audit_passed:
        blockers.append(blocker_from_risk_flag(BacktestClosureRiskFlag.RESEARCH_BOUNDARY_FAILED, "Research boundary audit failed"))

    # Check lineage/determinism
    manifest = final_audit_inputs.get("artifact_lineage")
    if manifest and not manifest.manifest_valid:
         blockers.append(blocker_from_risk_flag(BacktestClosureRiskFlag.ARTIFACT_LINEAGE_INVALID, "Artifact lineage invalid"))

    determinism = final_audit_inputs.get("determinism_audit")
    if determinism and not determinism.audit_passed:
         blockers.append(blocker_from_risk_flag(BacktestClosureRiskFlag.DETERMINISM_COMPLIANCE_FAILED, "Determinism compliance failed"))

    return blockers

def has_blocking_closure_issue(blockers: list[ClosureBlocker]) -> bool:
    return any(b.blocker_detected for b in blockers)

def closure_blockers_summary(blockers: list[ClosureBlocker]) -> dict[str, Any]:
    return {"count": len(blockers), "has_blockers": has_blocking_closure_issue(blockers)}

def closure_blockers_to_text(blockers: list[ClosureBlocker], limit: int = 300) -> str:
    return f"ClosureBlockers(count={len(blockers)}, has_blockers={has_blocking_closure_issue(blockers)})"
""")

# 16. CLOSURE WARNING COLLECTOR
write_file("usa_signal_bot/backtesting/closure/closure_warning_collector.py", """
from typing import Any

def deduplicate_closure_warnings(warnings: list[str]) -> list[str]:
    return list(dict.fromkeys(warnings))

def collect_closure_warnings(payloads: dict[str, dict[str, Any]], audits: dict[str, Any]) -> list[str]:
    warnings = []

    # Collect warnings from audits
    for name, audit in audits.items():
        if hasattr(audit, 'warnings') and audit.warnings:
            warnings.extend(audit.warnings)

    return deduplicate_closure_warnings(warnings)

def closure_warnings_summary(warnings: list[str]) -> dict[str, Any]:
    return {"count": len(warnings)}

def closure_warnings_to_text(warnings: list[str], limit: int = 300) -> str:
    return f"Closure Warnings: {len(warnings)}"
""")

# 17. BACKTEST FINAL AUDIT REPORT
write_file("usa_signal_bot/backtesting/closure/backtest_final_audit_report.py", """
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
""")

# 18. CLOSURE CERTIFICATE
write_file("usa_signal_bot/backtesting/closure/backtest_band_closure_certificate.py", """
import hashlib
from typing import Any
from usa_signal_bot.backtesting.closure.phase152_models import (
    BacktestBandClosureCertificate, BacktestFinalAuditReport,
    ClosureComplianceStatus, BacktestClosureRiskFlag
)

def compute_backtest_band_closure_certificate_hash(certificate: BacktestBandClosureCertificate) -> str:
    content = f"{certificate.final_audit_report_id}_{certificate.closed}_{certificate.start_phase}_{certificate.end_phase}"
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def build_backtest_band_closure_certificate(final_audit_report: BacktestFinalAuditReport) -> BacktestBandClosureCertificate:
    cert = BacktestBandClosureCertificate()
    cert.final_audit_report_id = final_audit_report.report_id
    cert.acceptance_summary_id = final_audit_report.acceptance_summary.summary_id

    cert.closed = final_audit_report.final_audit_passed
    cert.closure_status = ClosureComplianceStatus.PASSED if cert.closed else ClosureComplianceStatus.FAILED

    if cert.closed:
        cert.ready_for_phase153 = True
    else:
        cert.risk_flags.append(BacktestClosureRiskFlag.CLOSURE_CERTIFICATE_INVALID)
        cert.errors.append("Cannot close band: final audit failed")

    cert.closure_hash = compute_backtest_band_closure_certificate_hash(cert)

    return cert

def validate_backtest_band_closure_certificate(certificate: BacktestBandClosureCertificate) -> list[str]:
    errors = []
    if not certificate.closed:
        errors.append("Certificate indicates band is not closed")
    return errors

def backtest_band_closure_certificate_summary(certificate: BacktestBandClosureCertificate) -> dict[str, Any]:
    return {"closed": certificate.closed, "ready_for_phase153": certificate.ready_for_phase153}

def backtest_band_closure_certificate_to_text(certificate: BacktestBandClosureCertificate, limit: int = 300) -> str:
    return f"BacktestBandClosureCertificate(closed={certificate.closed}, ready153={certificate.ready_for_phase153})"
""")
