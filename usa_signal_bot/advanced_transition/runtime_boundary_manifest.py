from typing import List, Dict, Any
from datetime import datetime, timezone
from usa_signal_bot.core.enums import RuntimeCapabilityStatus, AdvancedTransitionRiskFlag
from usa_signal_bot.advanced_transition.phase101_models import RuntimeBoundaryManifest, RuntimeCapabilityRecord, create_runtime_boundary_manifest_id
from usa_signal_bot.advanced_transition.capability_matrix import build_phase101_capability_matrix

def build_runtime_boundary_manifest(records: List[RuntimeCapabilityRecord] | None = None) -> RuntimeBoundaryManifest:
    if records is None:
        records = build_phase101_capability_matrix()

    allowed = [r for r in records if r.status == RuntimeCapabilityStatus.ALLOWED_READ_ONLY]
    blocked = [r for r in records if r.status == RuntimeCapabilityStatus.BLOCKED]
    metadata_only = [r for r in records if r.status == RuntimeCapabilityStatus.ALLOWED_METADATA_ONLY]

    return RuntimeBoundaryManifest(
        manifest_id=create_runtime_boundary_manifest_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        allowed_capabilities=allowed,
        blocked_capabilities=blocked,
        read_only_capabilities=[],
        metadata_only_capabilities=metadata_only,
        all_execution_blocked=True,
        active_paper_blocked=True,
        broker_execution_blocked=True,
        paper_state_mutation_blocked=True,
        telegram_real_send_blocked=True,
        scraping_blocked=True,
        dashboard_blocked=True,
        risk_flags=[],
        warnings=[],
        errors=[],
        metadata={}
    )

def validate_runtime_boundary_safety(manifest: RuntimeBoundaryManifest) -> List[str]:
    errors = []
    if not manifest.all_execution_blocked: errors.append("all_execution_blocked must be True")
    if not manifest.active_paper_blocked: errors.append("active_paper_blocked must be True")
    if not manifest.broker_execution_blocked: errors.append("broker_execution_blocked must be True")
    if not manifest.paper_state_mutation_blocked: errors.append("paper_state_mutation_blocked must be True")
    if not manifest.telegram_real_send_blocked: errors.append("telegram_real_send_blocked must be True")
    if not manifest.scraping_blocked: errors.append("scraping_blocked must be True")
    if not manifest.dashboard_blocked: errors.append("dashboard_blocked must be True")
    return errors

def runtime_boundary_summary(manifest: RuntimeBoundaryManifest) -> Dict[str, Any]:
    return {"manifest_id": manifest.manifest_id, "safe": not bool(validate_runtime_boundary_safety(manifest))}

def runtime_boundary_to_text(manifest: RuntimeBoundaryManifest) -> str:
    return f"Boundary ID: {manifest.manifest_id}\nSafe: {manifest.all_execution_blocked}"
