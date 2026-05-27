"""Artifact Chain Loader."""
import json
import hashlib
from pathlib import Path
from typing import Any
from datetime import datetime, timezone

from .phase124_models import (
    ArtifactChainReference,
    ArtifactChainPhase,
    create_artifact_chain_reference_id
)

def build_expected_artifact_chain(data_root: Path | None = None) -> list[ArtifactChainReference]:
    now = datetime.now(timezone.utc).isoformat()
    phases = [
        ArtifactChainPhase.PHASE_116_FEATURE_FOUNDATION,
        ArtifactChainPhase.PHASE_117_CORE_INDICATORS,
        ArtifactChainPhase.PHASE_118_ADVANCED_FEATURES,
        ArtifactChainPhase.PHASE_119_ENRICHED_FEATURES,
        ArtifactChainPhase.PHASE_120_FACTOR_COMPOSITION,
        ArtifactChainPhase.PHASE_121_FACTOR_SCORING,
        ArtifactChainPhase.PHASE_122_FACTOR_VALIDATION,
        ArtifactChainPhase.PHASE_123_FACTOR_EXPLAINABILITY
    ]

    chain = []
    for p in phases:
        chain.append(ArtifactChainReference(
            reference_id=create_artifact_chain_reference_id(),
            created_at_utc=now,
            phase=p,
            artifact_name=f"{p.value}_artifact",
            artifact_path=None,
            artifact_hash=None,
            artifact_required=True,
            artifact_available=False,
            schema_signature=None,
            lineage_ref=None,
            safety_boundary_ref=None
        ))
    return chain

def load_artifact_chain_from_payload(payload: dict[str, Any]) -> list[ArtifactChainReference]:
    chain = []
    artifacts = payload.get("artifacts", [])
    now = datetime.now(timezone.utc).isoformat()
    for a in artifacts:
        try:
            phase = ArtifactChainPhase(a.get("phase"))
        except:
            phase = ArtifactChainPhase.UNKNOWN

        chain.append(ArtifactChainReference(
            reference_id=create_artifact_chain_reference_id(),
            created_at_utc=now,
            phase=phase,
            artifact_name=a.get("artifact_name", "unknown"),
            artifact_path=a.get("artifact_path"),
            artifact_hash=a.get("artifact_hash"),
            artifact_required=a.get("artifact_required", True),
            artifact_available=a.get("artifact_available", False),
            schema_signature=a.get("schema_signature"),
            lineage_ref=a.get("lineage_ref"),
            safety_boundary_ref=a.get("safety_boundary_ref")
        ))
    return chain

def resolve_artifact_reference_paths(data_root: Path, references: list[ArtifactChainReference]) -> list[ArtifactChainReference]:
    # Prevent path traversal
    safe_root = data_root.resolve()
    for r in references:
        if r.artifact_path:
            p = Path(r.artifact_path)
            if not p.is_absolute():
                p = (safe_root / p).resolve()
            else:
                 p = p.resolve()

            try:
                p.relative_to(safe_root)
                r.artifact_path = str(p)
                if p.exists():
                     r.artifact_available = True
                     if r.artifact_hash is None:
                         r.artifact_hash = compute_artifact_reference_hash(p)
                else:
                     r.artifact_available = False
            except ValueError:
                r.artifact_available = False
                r.errors.append("Path traversal detected")
    return references

def compute_artifact_reference_hash(path: Path | None) -> str | None:
    if not path or not path.exists():
        return None
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                h.update(chunk)
        return h.hexdigest()
    except:
        return None

def validate_artifact_chain_references(references: list[ArtifactChainReference]) -> list[str]:
    errors = []
    for r in references:
        if r.artifact_required and not r.artifact_available:
            errors.append(f"Missing required artifact: {r.phase.value}")
    return errors

def artifact_chain_loader_summary(references: list[ArtifactChainReference]) -> dict[str, Any]:
    return {
        "total": len(references),
        "available": sum(1 for r in references if r.artifact_available),
        "required_missing": sum(1 for r in references if r.artifact_required and not r.artifact_available)
    }

def artifact_chain_loader_to_text(references: list[ArtifactChainReference], limit: int = 200) -> str:
    s = artifact_chain_loader_summary(references)
    return f"Chain Loader: {s['available']}/{s['total']} available, {s['required_missing']} required missing"
