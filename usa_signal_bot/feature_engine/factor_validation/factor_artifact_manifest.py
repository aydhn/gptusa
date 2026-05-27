from pathlib import Path
from typing import Any
import hashlib
from datetime import datetime, timezone
from usa_signal_bot.feature_engine.factor_validation.phase122_models import (
    FactorArtifactManifest,
    FactorArtifactManifestItem,
    FactorArtifactKind,
    create_factor_artifact_manifest_id,
    create_factor_manifest_item_id,
    validate_factor_artifact_manifest
)
from usa_signal_bot.feature_engine.factor_validation.factor_persistence_safety_validator import factor_persistence_text_has_trade_or_execution_language

def compute_file_sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def detect_secret_or_execution_language_in_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"secret": False, "execution": False, "forbidden_col": False}

    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read().lower()
            secret = any(x in content for x in ['api_key', 'token', 'secret', 'password'])
            execution = factor_persistence_text_has_trade_or_execution_language(content)
            forbidden = any(x in content for x in ['buy_signal', 'sell_signal', 'portfolio_weight', 'target_weight', 'allocation'])
            return {"secret": secret, "execution": execution, "forbidden_col": forbidden}
    except:
        return {"secret": False, "execution": False, "forbidden_col": False}

def build_manifest_item(kind: FactorArtifactKind, path: Path | None, required: bool = True) -> FactorArtifactManifestItem:
    available = path is not None and path.exists()
    size = path.stat().st_size if available else None
    h = compute_file_sha256(path) if available else None

    scan = detect_secret_or_execution_language_in_file(path) if available else {"secret": False, "execution": False, "forbidden_col": False}

    return FactorArtifactManifestItem(
        artifact_id=create_factor_manifest_item_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        artifact_kind=kind,
        path=str(path) if path else None,
        artifact_hash=h,
        size_bytes=size,
        required=required,
        available=available,
        immutable=False,
        contains_secret=scan["secret"],
        contains_forbidden_columns=scan["forbidden_col"],
        contains_execution_language=scan["execution"],
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_factor_artifact_manifest(version_id: str | None, artifacts: list[dict[str, Any]]) -> FactorArtifactManifest:
    items = []
    for art in artifacts:
        items.append(build_manifest_item(art["kind"], art.get("path"), art.get("required", True)))

    available_items = sum(1 for i in items if i.available)
    missing_items = sum(1 for i in items if i.required and not i.available)
    secret_violation_count = sum(1 for i in items if i.contains_secret)
    forbidden_column_violation_count = sum(1 for i in items if i.contains_forbidden_columns)
    execution_language_violation_count = sum(1 for i in items if i.contains_execution_language)

    # naive hash of the items
    manifest_hash = hashlib.sha256(str([i.artifact_hash for i in items]).encode('utf-8')).hexdigest()

    manifest = FactorArtifactManifest(
        manifest_id=create_factor_artifact_manifest_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        version_id=version_id,
        items=items,
        total_items=len(items),
        available_items=available_items,
        missing_items=missing_items,
        invalid_items=0,
        secret_violation_count=secret_violation_count,
        forbidden_column_violation_count=forbidden_column_violation_count,
        execution_language_violation_count=execution_language_violation_count,
        manifest_hash=manifest_hash,
        manifest_valid=missing_items == 0,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    validate_factor_artifact_manifest(manifest)
    return manifest

def factor_artifact_manifest_summary(manifest: FactorArtifactManifest) -> dict[str, Any]:
    return {"total": manifest.total_items, "available": manifest.available_items}

def factor_artifact_manifest_to_text(manifest: FactorArtifactManifest, limit: int = 200) -> str:
    return f"Manifest has {manifest.available_items}/{manifest.total_items} items available."
