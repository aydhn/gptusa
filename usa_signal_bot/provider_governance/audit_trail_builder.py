from usa_signal_bot.provider_governance.phase113_models import AuditTrailEvent, ProviderExpansionEvidenceItem, DataLineageGraph, create_audit_trail_event_id
from usa_signal_bot.core.enums import AuditTrailEventKind
from typing import Any, Optional, List, Dict
from datetime import datetime, timezone

def build_audit_trail_events(evidence_items: List[ProviderExpansionEvidenceItem], lineage_graph: Optional[DataLineageGraph] = None) -> List[AuditTrailEvent]:
    return []

def build_audit_event(event_kind: AuditTrailEventKind, message: str, source_phase: Optional[int] = None, source_ref_id: Optional[str] = None, artifact_path: Optional[str] = None, artifact_hash: Optional[str] = None) -> AuditTrailEvent:
    return AuditTrailEvent(
        audit_event_id=create_audit_trail_event_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        event_kind=event_kind,
        source_phase=source_phase,
        source_ref_id=source_ref_id,
        message=message,
        artifact_path=artifact_path,
        artifact_hash=artifact_hash,
        metadata_only=True,
        contains_secret=False,
        contains_execution=False,
        contains_order=False,
        contains_trade_signal=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def audit_trail_summary(events: List[AuditTrailEvent]) -> Dict[str, Any]:
    return {}

def audit_trail_to_text(events: List[AuditTrailEvent], limit: int = 200) -> str:
    return "Events"
