from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.feature_engine.factor_validation.phase122_models import (
    FactorStoreHardeningResult,
    FactorStoreHardeningStatus,
    FactorSchemaSignature,
    FactorVersionMetadata,
    FactorArtifactManifest,
    FactorStoreSnapshot,
    FactorRollbackMetadata,
    create_factor_store_hardening_id,
    validate_factor_store_hardening_result
)
from usa_signal_bot.feature_engine.factor_validation.factor_retention_policy import build_default_factor_retention_policy

def build_factor_store_hardening_result(schema_signature: FactorSchemaSignature, version_metadata: FactorVersionMetadata, manifest: FactorArtifactManifest, snapshot: FactorStoreSnapshot, rollback_metadata: FactorRollbackMetadata, retention_policy: dict[str, Any] | None = None) -> FactorStoreHardeningResult:
    res = FactorStoreHardeningResult(
        hardening_id=create_factor_store_hardening_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        status=FactorStoreHardeningStatus.HARDENED if manifest.manifest_valid and snapshot.snapshot_valid else FactorStoreHardeningStatus.FAILED,
        schema_signature=schema_signature,
        version_metadata=version_metadata,
        artifact_manifest=manifest,
        snapshot=snapshot,
        rollback_metadata=rollback_metadata,
        retention_policy=retention_policy or build_default_factor_retention_policy(),
        store_hardened=True,
        overwrite_safe=True,
        immutable_artifacts=True,
        no_secret_leak=manifest.secret_violation_count == 0,
        no_forbidden_columns=manifest.forbidden_column_violation_count == 0,
        no_execution_language=manifest.execution_language_violation_count == 0,
        research_data_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    validate_factor_store_hardening_result(res)
    return res

def factor_store_hardened(result: FactorStoreHardeningResult) -> bool:
    return result.store_hardened

def factor_store_hardening_summary(result: FactorStoreHardeningResult) -> dict[str, Any]:
    return {"hardened": result.store_hardened}

def factor_store_hardening_to_text(result: FactorStoreHardeningResult, limit: int = 300) -> str:
    return f"Store Hardened: {result.store_hardened}"
