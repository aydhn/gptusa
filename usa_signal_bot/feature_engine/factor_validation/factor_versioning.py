from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.feature_engine.factor_validation.phase122_models import (
    FactorVersionMetadata,
    FactorVersionStatus,
    FactorSchemaSignature,
    create_factor_version_id,
    validate_factor_version_metadata
)

def generate_factor_version(created_at_utc: str | None = None, prefix: str = "factor") -> str:
    dt = created_at_utc or datetime.now(timezone.utc).isoformat()
    # simplified representation
    return f"{prefix}-{dt[:10]}"

def build_factor_version_metadata(source_review_id: str | None, schema_signature: FactorSchemaSignature, artifact_hashes: dict[str, str] | None = None, parent_version: str | None = None) -> FactorVersionMetadata:
    meta = FactorVersionMetadata(
        version_id=create_factor_version_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        version=generate_factor_version(),
        status=FactorVersionStatus.CREATED,
        source_review_id=source_review_id,
        schema_signature_id=schema_signature.signature_id,
        artifact_hashes=artifact_hashes or {},
        parent_version=parent_version,
        sealed=False,
        immutable=False,
        supersedes=parent_version,
        rollback_candidate=False,
        research_data_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    validate_factor_version_metadata(meta)
    return meta

def seal_factor_version(metadata: FactorVersionMetadata) -> FactorVersionMetadata:
    metadata.sealed = True
    metadata.immutable = True
    metadata.status = FactorVersionStatus.SEALED
    validate_factor_version_metadata(metadata)
    return metadata

def factor_versioning_summary(metadata: FactorVersionMetadata) -> dict[str, Any]:
    return {"version": metadata.version, "sealed": metadata.sealed}

def factor_versioning_to_text(metadata: FactorVersionMetadata) -> str:
    return f"Version {metadata.version} (sealed: {metadata.sealed})"
