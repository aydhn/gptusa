import hashlib
from typing import Any
from usa_signal_bot.provider_final_acceptance.phase115_models import (
    ProviderLayerClosureBundle,
    ProviderLayerClosureItem,
    ProviderLayerClosureStatus,
    ProviderLayerClosureDecision,
    ProviderFreezeIngestionResult,
    create_provider_layer_closure_item_id,
    create_provider_layer_closure_id,
    _utc_now
)

def build_provider_layer_closure_items(ingestion: ProviderFreezeIngestionResult) -> list[ProviderLayerClosureItem]:
    names = [
        "phase106_provider_abstraction",
        "phase107_provider_runtime",
        "phase108_provider_cache",
        "phase109_provider_quality",
        "phase110_provider_orchestration",
        "phase111_event_metadata",
        "phase112_event_impact",
        "phase113_provider_governance",
        "phase114_provider_freeze",
        "final_data_contract",
        "feature_factor_kickoff_gate"
    ]
    items = []
    for i, name in enumerate(names):
        items.append(ProviderLayerClosureItem(
            closure_item_id=create_provider_layer_closure_item_id(),
            created_at_utc=_utc_now(),
            source_phase=106 + i if i < 9 else 115,
            closure_name=name,
            source_ref_id=ingestion.ingestion_id,
            source_path=None,
            status=ProviderLayerClosureStatus.CLOSED if ingestion.valid_for_phase115 else ProviderLayerClosureStatus.FAILED,
            closed=ingestion.valid_for_phase115,
            frozen=ingestion.valid_for_phase115,
            immutable=True,
            metadata_only=True,
            research_data_only=True,
            artifact_hash=hashlib.sha256(name.encode('utf-8')).hexdigest(),
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        ))
    return items

def build_provider_layer_closure_bundle(ingestion: ProviderFreezeIngestionResult) -> ProviderLayerClosureBundle:
    items = build_provider_layer_closure_items(ingestion)
    all_closed = all(i.closed for i in items)

    return ProviderLayerClosureBundle(
        closure_id=create_provider_layer_closure_id(),
        created_at_utc=_utc_now(),
        status=ProviderLayerClosureStatus.CLOSED if all_closed else ProviderLayerClosureStatus.FAILED,
        decision=ProviderLayerClosureDecision.CLOSE_PHASE106_115_PROVIDER_LAYER if all_closed else ProviderLayerClosureDecision.BLOCK,
        phase_start=106,
        phase_end=115,
        next_phase=116,
        final_phase=160,
        items=items,
        closure_hash=stable_provider_layer_closure_hash(items),
        closed=all_closed,
        frozen=all_closed,
        immutable=True,
        metadata_only=True,
        research_data_only=True,
        total_items=len(items),
        closed_items=sum(1 for i in items if i.closed),
        warning_items=sum(1 for i in items if i.status == ProviderLayerClosureStatus.WARNING),
        failed_items=sum(1 for i in items if i.status == ProviderLayerClosureStatus.FAILED),
        blocked_items=sum(1 for i in items if i.status == ProviderLayerClosureStatus.BLOCKED),
        closure_valid=all_closed,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def stable_provider_layer_closure_hash(items: list[ProviderLayerClosureItem]) -> str:
    combined = "".join([i.closure_item_id + (i.artifact_hash or "") for i in items])
    return hashlib.sha256(combined.encode('utf-8')).hexdigest()

def provider_layer_closure_summary(bundle: ProviderLayerClosureBundle) -> dict[str, Any]:
    return {
        "status": bundle.status,
        "decision": bundle.decision,
        "closed": bundle.closed
    }

def provider_layer_closure_to_text(bundle: ProviderLayerClosureBundle, limit: int = 300) -> str:
    return f"Closure Bundle [{bundle.status}] - Decision: {bundle.decision}, Valid: {bundle.closure_valid}"
