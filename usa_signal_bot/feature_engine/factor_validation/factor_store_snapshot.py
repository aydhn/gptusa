from pathlib import Path
from typing import Any
from datetime import datetime, timezone
import hashlib
from usa_signal_bot.feature_engine.factor_validation.phase122_models import (
    FactorStoreSnapshot,
    FactorArtifactManifest,
    create_factor_store_snapshot_id,
    validate_factor_store_snapshot
)

def build_factor_store_snapshot(version_id: str | None, manifest: FactorArtifactManifest, snapshot_path: Path | None = None) -> FactorStoreSnapshot:
    inc = [i.path for i in manifest.items if i.available and i.path]
    h = hashlib.sha256(str(inc).encode('utf-8')).hexdigest()

    snap = FactorStoreSnapshot(
        snapshot_id=create_factor_store_snapshot_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        version_id=version_id,
        snapshot_path=str(snapshot_path) if snapshot_path else None,
        included_artifacts=inc,
        snapshot_hash=h,
        artifact_count=len(inc),
        snapshot_valid=True,
        immutable=True,
        research_data_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    validate_factor_store_snapshot(snap)
    return snap

def factor_store_snapshot_summary(snapshot: FactorStoreSnapshot) -> dict[str, Any]:
    return {"artifact_count": snapshot.artifact_count}

def factor_store_snapshot_to_text(snapshot: FactorStoreSnapshot) -> str:
    return f"Snapshot with {snapshot.artifact_count} artifacts."
