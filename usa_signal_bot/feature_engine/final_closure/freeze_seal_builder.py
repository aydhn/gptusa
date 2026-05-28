import datetime
import hashlib
import json
from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import FreezeSealStatus
from usa_signal_bot.feature_engine.final_closure.phase125_models import (
    FinalClosureArtifactReference,
    FinalClosureManifest,
    FreezeSealMetadata,
    create_final_closure_manifest_id,
    create_freeze_seal_id
)

def compute_final_manifest_hash(manifest: FinalClosureManifest) -> str:
    # A simplified hash
    return hashlib.sha256(manifest.manifest_id.encode()).hexdigest()

def build_final_closure_manifest(artifacts: List[FinalClosureArtifactReference]) -> FinalClosureManifest:
    m = FinalClosureManifest(
        manifest_id=create_final_closure_manifest_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        artifacts=artifacts,
        total_artifacts=len(artifacts),
        required_artifacts=sum(1 for a in artifacts if a.required),
        available_artifacts=sum(1 for a in artifacts if a.available),
        missing_required_artifacts=sum(1 for a in artifacts if a.required and not a.available),
        manifest_hash=None,
        manifest_version="phase125.v1",
        immutable=True,
        research_data_only=True,
        no_secret_leak=not any(a.contains_secret for a in artifacts),
        no_forbidden_columns=not any(a.contains_forbidden_columns for a in artifacts),
        no_execution_language=not any(a.contains_execution_language for a in artifacts),
        final_manifest_valid=False,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

    m.final_manifest_valid = (
        m.no_secret_leak and m.no_forbidden_columns and m.no_execution_language and m.missing_required_artifacts == 0
    )
    m.manifest_hash = compute_final_manifest_hash(m)
    return m


def compute_freeze_seal_hash(manifest_hash: Optional[str], seal_version: str, phase_range: str = "116-125") -> str:
    s = f"{manifest_hash}:{seal_version}:{phase_range}"
    return hashlib.sha256(s.encode()).hexdigest()

def build_freeze_seal_metadata(manifest: FinalClosureManifest, seal_version: str = "phase125.v1") -> FreezeSealMetadata:
    sealed = manifest.final_manifest_valid
    s = FreezeSealMetadata(
        seal_id=create_freeze_seal_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        status=FreezeSealStatus.SEALED if sealed else FreezeSealStatus.BLOCKED,
        seal_version=seal_version,
        source_manifest_id=manifest.manifest_id,
        source_manifest_hash=manifest.manifest_hash,
        seal_hash=None,
        sealed=sealed,
        immutable=True,
        freeze_scope=[a.artifact_name for a in manifest.artifacts],
        phase_range="116-125",
        research_data_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        broker_execution_enabled=False,
        order_creation_enabled=False,
        paper_state_mutation_enabled=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        warnings=[],
        errors=[] if sealed else ["Manifest invalid"],
        risk_flags=[],
        metadata={}
    )
    s.seal_hash = compute_freeze_seal_hash(s.source_manifest_hash, s.seal_version, s.phase_range)
    return s

def validate_freeze_seal_metadata(seal: FreezeSealMetadata) -> List[str]:
    errs = []
    if not seal.sealed: errs.append("Not sealed")
    if not seal.immutable: errs.append("Not immutable")
    if not seal.research_data_only: errs.append("Not research data only")
    if seal.activation_allowed: errs.append("Activation allowed")
    return errs

def freeze_seal_valid(seal: FreezeSealMetadata) -> bool:
    return len(validate_freeze_seal_metadata(seal)) == 0

def freeze_seal_summary(seal: FreezeSealMetadata) -> Dict[str, Any]:
    return {
        "sealed": seal.sealed,
        "status": seal.status.value,
        "valid": freeze_seal_valid(seal)
    }

def freeze_seal_to_text(seal: FreezeSealMetadata, limit: int = 200) -> str:
    return f"FreezeSeal({seal.seal_id}): Sealed={seal.sealed}, Status={seal.status.value}"
