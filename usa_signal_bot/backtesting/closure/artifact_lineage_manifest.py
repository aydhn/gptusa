import json
import hashlib
from typing import Any
from usa_signal_bot.backtesting.closure.phase152_models import (
    ArtifactLineageManifest, ClosureArtifactReference, BacktestBandPhase,
    ClosureArtifactKind, BacktestClosureRiskFlag
)
from usa_signal_bot.core.exceptions import ArtifactLineageManifestError

def build_closure_artifact_reference(phase: BacktestBandPhase, artifact_kind: ClosureArtifactKind, payload: dict[str, Any], source_path: str | None = None, required: bool = True) -> ClosureArtifactReference:
    ref = ClosureArtifactReference()
    ref.phase = phase
    ref.artifact_kind = artifact_kind
    ref.artifact_name = f"{phase.value}_{artifact_kind.value}"
    ref.source_path = source_path
    ref.required = required
    ref.available = payload is not None and len(payload) > 0
    ref.read_only = True

    if ref.available:
        ref.source_hash = compute_artifact_payload_hash(payload)
        ref.valid = True
    else:
        if required:
            ref.errors.append("Required artifact missing or empty")
            ref.risk_flags.append(BacktestClosureRiskFlag.CROSS_PHASE_ARTIFACT_MISSING)
        ref.valid = not required

    return ref

def compute_artifact_payload_hash(payload: dict[str, Any]) -> str:
    payload_str = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(payload_str.encode('utf-8')).hexdigest()

def compute_artifact_lineage_hash(manifest: ArtifactLineageManifest) -> str:
    hash_list = [a.source_hash for a in manifest.artifacts if a.source_hash]
    return hashlib.sha256("".join(sorted(hash_list)).encode('utf-8')).hexdigest()

def build_artifact_lineage_manifest(payloads: dict[str, dict[str, Any]]) -> ArtifactLineageManifest:
    manifest = ArtifactLineageManifest()
    manifest.phase_order = [
        BacktestBandPhase.PHASE146_FOUNDATION,
        BacktestBandPhase.PHASE147_BACKTEST_RUN,
        BacktestBandPhase.PHASE148_ANALYTICS,
        BacktestBandPhase.PHASE149_BENCHMARK,
        BacktestBandPhase.PHASE150_WALK_FORWARD,
        BacktestBandPhase.PHASE151_STRESS_MONTE_CARLO
    ]

    kinds = {
        BacktestBandPhase.PHASE146_FOUNDATION: ClosureArtifactKind.FOUNDATION_REVIEW,
        BacktestBandPhase.PHASE147_BACKTEST_RUN: ClosureArtifactKind.BACKTEST_RUN_REVIEW,
        BacktestBandPhase.PHASE148_ANALYTICS: ClosureArtifactKind.ANALYTICS_REVIEW,
        BacktestBandPhase.PHASE149_BENCHMARK: ClosureArtifactKind.BENCHMARK_REVIEW,
        BacktestBandPhase.PHASE150_WALK_FORWARD: ClosureArtifactKind.WALK_FORWARD_REVIEW,
        BacktestBandPhase.PHASE151_STRESS_MONTE_CARLO: ClosureArtifactKind.STRESS_ROBUSTNESS_REVIEW
    }

    for phase in manifest.phase_order:
        phase_str = phase.name
        payload = payloads.get(phase_str, {})
        kind = kinds[phase]
        ref = build_closure_artifact_reference(phase, kind, payload, required=True)
        manifest.artifacts.append(ref)
        if ref.errors:
            manifest.errors.extend(ref.errors)
            manifest.risk_flags.extend(ref.risk_flags)

    manifest.all_required_available = all(a.available for a in manifest.artifacts if a.required)
    manifest.deterministic_hashes_available = all(a.source_hash is not None for a in manifest.artifacts if a.available)
    manifest.lineage_hash = compute_artifact_lineage_hash(manifest)
    manifest.manifest_valid = manifest.all_required_available and manifest.deterministic_hashes_available

    if not manifest.manifest_valid:
        manifest.risk_flags.append(BacktestClosureRiskFlag.ARTIFACT_LINEAGE_INVALID)

    return manifest

def validate_artifact_lineage_manifest(manifest: ArtifactLineageManifest) -> list[str]:
    errors = []
    if not manifest.manifest_valid:
        errors.append("Manifest is invalid")
    if not manifest.all_required_available:
        errors.append("Not all required artifacts are available")
    if not manifest.deterministic_hashes_available:
        errors.append("Missing deterministic hashes")
    return errors

def artifact_lineage_manifest_summary(manifest: ArtifactLineageManifest) -> dict[str, Any]:
    return {
        "valid": manifest.manifest_valid,
        "artifact_count": len(manifest.artifacts),
        "hash": manifest.lineage_hash
    }

def artifact_lineage_manifest_to_text(manifest: ArtifactLineageManifest, limit: int = 300) -> str:
    return f"ArtifactLineageManifest(valid={manifest.manifest_valid}, artifacts={len(manifest.artifacts)})"
