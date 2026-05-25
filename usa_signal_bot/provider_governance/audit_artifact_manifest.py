from usa_signal_bot.provider_governance.phase113_models import AuditArtifactManifest, ProviderExpansionEvidenceItem, AuditTrailEvent, create_audit_artifact_manifest_id
from usa_signal_bot.core.enums import AuditArtifactStatus
from pathlib import Path
from typing import Any, List, Dict
from datetime import datetime, timezone

def build_audit_artifact_manifest(evidence_items: List[ProviderExpansionEvidenceItem], audit_events: List[AuditTrailEvent]) -> AuditArtifactManifest:
    return AuditArtifactManifest(
        manifest_id=create_audit_artifact_manifest_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=AuditArtifactStatus.VALIDATED,
        artifacts=[],
        audit_events=audit_events,
        total_artifacts=0,
        hashed_artifacts=0,
        missing_artifacts=0,
        secret_violation_count=0,
        execution_violation_count=0,
        order_violation_count=0,
        trade_signal_violation_count=0,
        manifest_valid=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def artifact_manifest_from_paths(paths: List[Path]) -> AuditArtifactManifest:
    return build_audit_artifact_manifest([], [])

def validate_audit_artifact_manifest_safety(manifest: AuditArtifactManifest) -> List[str]:
    return []

def audit_artifact_manifest_summary(manifest: AuditArtifactManifest) -> Dict[str, Any]:
    return {}

def audit_artifact_manifest_to_text(manifest: AuditArtifactManifest, limit: int = 200) -> str:
    return "Manifest"
