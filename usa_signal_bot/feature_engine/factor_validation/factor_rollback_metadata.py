from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.feature_engine.factor_validation.phase122_models import (
    FactorRollbackMetadata,
    create_factor_rollback_id,
    validate_factor_rollback_metadata
)

def build_factor_rollback_metadata(current_version: str | None, rollback_version: str | None = None, rollback_reason: str | None = None) -> FactorRollbackMetadata:
    meta = FactorRollbackMetadata(
        rollback_id=create_factor_rollback_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        current_version=current_version,
        rollback_version=rollback_version,
        rollback_available=rollback_version is not None,
        rollback_reason=rollback_reason,
        rollback_metadata_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        order_creation_allowed=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    validate_factor_rollback_metadata(meta)
    return meta

def factor_rollback_metadata_summary(metadata: FactorRollbackMetadata) -> dict[str, Any]:
    return {"rollback_available": metadata.rollback_available}

def factor_rollback_metadata_to_text(metadata: FactorRollbackMetadata) -> str:
    return f"Rollback available: {metadata.rollback_available}"
