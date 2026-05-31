from typing import Any, Dict, List
from usa_signal_bot.regime_classification.final_closure.phase135_models import (
    RegimeResearchFreezeIngestionResult,
    RegimeArtifactChainValidationResult,
    RegimeFinalClosureResult,
    RegimeFreezeSeal,
    RegimeFreezeSealKind,
    RegimeFreezeSealStatus,
    create_regime_freeze_seal_id
)
from usa_signal_bot.regime_classification.final_closure.final_closure_hashing import (
    compute_artifact_chain_hash,
    compute_closure_hash,
    compute_freeze_seal_hash
)
from datetime import datetime, timezone

def build_regime_freeze_seal(
    ingestion: RegimeResearchFreezeIngestionResult,
    chain_validation: RegimeArtifactChainValidationResult,
    closure_result: RegimeFinalClosureResult,
    seal_kind: RegimeFreezeSealKind = RegimeFreezeSealKind.COMBINED_FINAL_SEAL
) -> RegimeFreezeSeal:

    status = determine_freeze_seal_status(closure_result, chain_validation)

    seal = RegimeFreezeSeal(
        seal_id=create_regime_freeze_seal_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        seal_kind=seal_kind,
        seal_status=status,
        source_closure_result_id=closure_result.closure_result_id,
        source_freeze_review_id=ingestion.source_review_id,
        artifact_chain_hash=compute_artifact_chain_hash(chain_validation),
        closure_hash=compute_closure_hash(closure_result),
    )
    seal.seal_hash = compute_freeze_seal_hash({"id": seal.seal_id})
    return seal

def determine_freeze_seal_status(closure_result: RegimeFinalClosureResult, chain_validation: RegimeArtifactChainValidationResult) -> RegimeFreezeSealStatus:
    if closure_result.closure_passed and chain_validation.chain_valid:
        return RegimeFreezeSealStatus.SEALED
    return RegimeFreezeSealStatus.FAILED

def validate_regime_freeze_seal(seal: RegimeFreezeSeal) -> List[str]:
    return []

def freeze_seal_summary(seal: RegimeFreezeSeal) -> Dict[str, Any]:
    return {"status": seal.seal_status.name}

def freeze_seal_to_text(seal: RegimeFreezeSeal, limit: int = 300) -> str:
    return f"Seal Status: {seal.seal_status.name}"
