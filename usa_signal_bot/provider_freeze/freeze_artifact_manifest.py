from typing import Any, Dict, List
from usa_signal_bot.provider_freeze.phase114_models import (
    ProviderFreezeArtifactManifest,
    ProviderExpansionFreezeBundle,
    create_freeze_artifact_manifest_id,
    _utcnow_str
)
from usa_signal_bot.core.enums import ProviderFreezeRiskFlag

def build_provider_freeze_artifact_manifest(freeze_bundle: ProviderExpansionFreezeBundle) -> ProviderFreezeArtifactManifest:
    manifest = ProviderFreezeArtifactManifest(
        manifest_id=create_freeze_artifact_manifest_id(),
        created_at_utc=_utcnow_str(),
        freeze_id=freeze_bundle.freeze_id
    )

    artifacts = []
    for item in freeze_bundle.evidence_items:
        art = {
            "evidence_name": item.evidence_name,
            "artifact_hash": item.artifact_hash or "unhashed",
            "valid": item.valid,
            "contains_secret": item.contains_secret,
            "contains_execution": item.contains_execution,
            "contains_trade_signal": item.contains_trade_signal,
            "contains_order_decision": item.contains_order_decision
        }
        artifacts.append(art)

        if not item.available:
            manifest.missing_artifacts += 1
        if not item.valid:
            manifest.invalid_artifacts += 1
        if item.artifact_hash:
            manifest.hashed_artifacts += 1

        manifest.secret_violation_count += (1 if item.contains_secret else 0)
        manifest.execution_violation_count += (1 if item.contains_execution else 0)
        manifest.trade_signal_violation_count += (1 if item.contains_trade_signal else 0)
        manifest.order_decision_violation_count += (1 if item.contains_order_decision else 0)

    manifest.artifacts = artifacts
    manifest.total_artifacts = len(artifacts)

    manifest.manifest_valid = (
        manifest.missing_artifacts == 0 and
        manifest.invalid_artifacts == 0 and
        manifest.secret_violation_count == 0 and
        manifest.execution_violation_count == 0 and
        manifest.trade_signal_violation_count == 0 and
        manifest.order_decision_violation_count == 0
    )

    return manifest

def validate_provider_freeze_artifact_manifest(manifest: ProviderFreezeArtifactManifest) -> List[str]:
    errors = []
    if manifest.missing_artifacts > 0: errors.append(f"Manifest missing {manifest.missing_artifacts} artifacts.")
    if manifest.invalid_artifacts > 0: errors.append(f"Manifest has {manifest.invalid_artifacts} invalid artifacts.")
    if manifest.secret_violation_count > 0: errors.append(f"Manifest has {manifest.secret_violation_count} secret violations.")
    if manifest.execution_violation_count > 0: errors.append(f"Manifest has {manifest.execution_violation_count} execution violations.")
    if manifest.trade_signal_violation_count > 0: errors.append(f"Manifest has {manifest.trade_signal_violation_count} trade signal violations.")
    if manifest.order_decision_violation_count > 0: errors.append(f"Manifest has {manifest.order_decision_violation_count} order decision violations.")
    return errors

def provider_freeze_artifact_manifest_summary(manifest: ProviderFreezeArtifactManifest) -> Dict[str, Any]:
    return {
        "manifest_valid": manifest.manifest_valid,
        "total_artifacts": manifest.total_artifacts,
        "secret_violations": manifest.secret_violation_count,
        "execution_violations": manifest.execution_violation_count
    }

def provider_freeze_artifact_manifest_to_text(manifest: ProviderFreezeArtifactManifest, limit: int = 200) -> str:
    lines = [
        f"Artifact Manifest: {manifest.manifest_id} (Valid: {manifest.manifest_valid})",
        f"Total: {manifest.total_artifacts}, Missing: {manifest.missing_artifacts}, Invalid: {manifest.invalid_artifacts}",
        f"Violations - Secrets: {manifest.secret_violation_count}, Execution: {manifest.execution_violation_count}, Trade: {manifest.trade_signal_violation_count}, Order: {manifest.order_decision_violation_count}"
    ]
    return "\n".join(lines)
