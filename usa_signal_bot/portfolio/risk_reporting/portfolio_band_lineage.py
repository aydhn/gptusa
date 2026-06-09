from typing import Any, Dict, List, Optional
import datetime
import hashlib
import json

from usa_signal_bot.portfolio.risk_reporting.phase157_models import (
    PortfolioBandLineage,
    PortfolioBandArtifactReference,
    create_portfolio_band_lineage_id,
    create_portfolio_band_artifact_reference_id
)
from usa_signal_bot.core.enums import PortfolioBandPhase

def build_portfolio_band_lineage(payloads: Dict[str, Any]) -> PortfolioBandLineage:
    artifacts = []

    lineage = PortfolioBandLineage(
        lineage_id=create_portfolio_band_lineage_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        artifacts=artifacts,
        phase_order=[
            PortfolioBandPhase.PHASE153_FOUNDATION,
            PortfolioBandPhase.PHASE154_SIZING_PROTOTYPES,
            PortfolioBandPhase.PHASE155_ALLOCATION_SANDBOX,
            PortfolioBandPhase.PHASE156_OPTIMIZER_SANDBOX,
            PortfolioBandPhase.PHASE157_RISK_REPORTING_CLOSURE
        ],
        lineage_hash=None,
        lineage_valid=True,
        all_required_available=True,
        deterministic_hashes_available=True,
        research_data_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    lineage.lineage_hash = compute_portfolio_band_lineage_hash(lineage)
    return lineage

def build_portfolio_band_artifact_reference(phase: PortfolioBandPhase, artifact_name: str, payload: Dict[str, Any], source_path: Optional[str] = None, required: bool = True) -> PortfolioBandArtifactReference:
    return PortfolioBandArtifactReference(
        artifact_ref_id=create_portfolio_band_artifact_reference_id(),
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        phase=phase,
        artifact_name=artifact_name,
        source_path=source_path,
        source_hash=compute_portfolio_band_payload_hash(payload) if payload else None,
        available=payload is not None,
        read_only=True,
        required=required,
        valid=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def compute_portfolio_band_payload_hash(payload: Dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode('utf-8')).hexdigest()

def compute_portfolio_band_lineage_hash(lineage: PortfolioBandLineage) -> str:
    from usa_signal_bot.portfolio.risk_reporting.phase157_models import portfolio_band_lineage_to_dict
    d = portfolio_band_lineage_to_dict(lineage)
    d.pop("lineage_hash", None)
    return hashlib.sha256(json.dumps(d, sort_keys=True).encode('utf-8')).hexdigest()

def validate_portfolio_band_lineage(lineage: PortfolioBandLineage) -> List[str]:
    return []

def portfolio_band_lineage_to_text(lineage: PortfolioBandLineage, limit: int = 300) -> str:
    return f"Lineage {lineage.lineage_id} with {len(lineage.artifacts)} artifacts."
