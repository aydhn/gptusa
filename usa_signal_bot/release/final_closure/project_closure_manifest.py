from typing import List, Dict, Any, Optional
from usa_signal_bot.release.final_closure.phase160_models import (
    ProjectClosureManifest,
    ProjectClosureReport,
    ProjectClosureStatus,
    FinalClosureRiskFlag,
    create_project_closure_manifest_id,
    generate_timestamp
)
import hashlib
import json

def compute_project_closure_manifest_hash(manifest: ProjectClosureManifest) -> str:
    state = {
        "project_name": manifest.project_name,
        "total_phases": manifest.total_phases,
        "final_phase": manifest.final_phase,
        "closure_report_id": manifest.closure_report_id,
        "project_closed": manifest.project_closed,
        "closure_status": manifest.closure_status.value
    }
    data = json.dumps(state, sort_keys=True)
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def build_project_closure_manifest(
    report: ProjectClosureReport,
    final_review_id: Optional[str] = None
) -> ProjectClosureManifest:

    closed = report.project_closed
    status = report.closure_status

    errors = []
    risk_flags = []
    if not closed:
        errors.append("Manifest indicates project closure failed.")
        risk_flags.append(FinalClosureRiskFlag.PROJECT_CLOSURE_MANIFEST_INVALID)

    manifest = ProjectClosureManifest(
        manifest_id=create_project_closure_manifest_id(),
        created_at_utc=generate_timestamp(),
        project_name="USA Signal Bot",
        total_phases=160,
        final_phase=160,
        closure_report_id=report.report_id,
        final_delivery_certificate_id=report.final_delivery_certificate.certificate_id,
        final_review_id=final_review_id,
        manifest_hash=None,
        project_closed=closed,
        closure_status=status,
        read_only=True,
        local_only=True,
        no_deployment=True,
        no_trading_activation=True,
        no_broker_activation=True,
        not_investment_advice=True,
        warnings=[],
        errors=errors,
        risk_flags=risk_flags,
        metadata={}
    )

    manifest.manifest_hash = compute_project_closure_manifest_hash(manifest)
    return manifest

def validate_project_closure_manifest(manifest: ProjectClosureManifest) -> List[str]:
    errors = []
    if not manifest.project_closed:
        errors.extend(manifest.errors)
    if manifest.project_name != "USA Signal Bot":
        errors.append("Project name must be 'USA Signal Bot'.")
    if manifest.total_phases != 160 or manifest.final_phase != 160:
        errors.append("Total phases and final phase must be 160.")
    return errors

def project_closure_manifest_to_text(manifest: ProjectClosureManifest, limit: int = 300) -> str:
    return f"Project Closure Manifest: Closed={manifest.project_closed}, Status={manifest.closure_status.value}"
