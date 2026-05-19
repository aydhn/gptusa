from datetime import datetime, timezone
import json
from typing import Any, Dict, List, Optional
from usa_signal_bot.release_packaging.packaging_models import FrozenArtifact, create_frozen_artifact_id
from usa_signal_bot.release_packaging.checksum import stable_payload_hash
from usa_signal_bot.release_packaging.safety_scanner import scan_payload_safety
from usa_signal_bot.core.enums import FrozenArtifactSource, FrozenArtifactStatus, BundleValidationStatus, BundleSafetyFlag

def freeze_artifact_payload(payload: Dict[str, Any], source: FrozenArtifactSource, artifact_type: str, source_ref: Optional[str] = None) -> FrozenArtifact:
    hash_val = stable_payload_hash(payload)
    size = len(json.dumps(payload))
    flags = scan_payload_safety(payload)

    status = FrozenArtifactStatus.FROZEN
    if BundleSafetyFlag.SECRET_LEAK_RISK in flags or BundleSafetyFlag.BROKER_FIELD_RISK in flags:
        status = FrozenArtifactStatus.BLOCKED

    return FrozenArtifact(
        artifact_id=create_frozen_artifact_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        source=source,
        artifact_type=artifact_type,
        source_ref=source_ref,
        status=status,
        path=None,
        payload_hash=hash_val,
        payload_size_bytes=size,
        summary={"frozen": True},
        safety_flags=flags,
        warnings=[],
        errors=[],
        metadata={}
    )

def freeze_artifact_payloads(payloads: List[Dict[str, Any]], source: FrozenArtifactSource = FrozenArtifactSource.MANUAL_PAYLOAD) -> List[FrozenArtifact]:
    return [freeze_artifact_payload(p, source, "manual") for p in payloads]

def verify_frozen_artifact(artifact: FrozenArtifact, payload: Optional[Dict[str, Any]] = None) -> BundleValidationStatus:
    if artifact.status in [FrozenArtifactStatus.BLOCKED, FrozenArtifactStatus.INVALID]:
        return BundleValidationStatus.BLOCKED
    if payload:
        if stable_payload_hash(payload) != artifact.payload_hash:
            return BundleValidationStatus.FAIL
    return BundleValidationStatus.PASS

def frozen_artifact_summary(artifacts: List[FrozenArtifact]) -> Dict[str, Any]:
    return {"count": len(artifacts)}

def artifact_freezer_to_text(artifacts: List[FrozenArtifact], limit: int = 100) -> str:
    return f"Frozen Artifacts: {len(artifacts)} frozen."
