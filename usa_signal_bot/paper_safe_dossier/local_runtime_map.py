from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import json
import hashlib
from usa_signal_bot.core.enums import RuntimeComponentMode, PrePaperRuntimeMapStatus, PrePaperRuntimeMapDecision
from usa_signal_bot.paper_safe_dossier.paper_safe_dossier_models import (
    RuntimeComponentMapItem, PrePaperLocalRuntimeMap, create_runtime_component_id, create_pre_paper_runtime_map_id
)
from usa_signal_bot.paper_safe_dossier.runtime_route_map import build_runtime_route_map_items
from usa_signal_bot.paper_safe_dossier.paper_safe_ingestion import extract_paper_safe_candidate_id, extract_final_paper_safe_gate

def utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def default_runtime_component_names() -> List[str]:
    return [
        "market_data_reader",
        "feature_engine_preview",
        "signal_preview_engine",
        "risk_preview_engine",
        "paper_snapshot_reader",
        "notification_preview",
        "audit_reader",
        "validation_runner",
        "paper_state_writer_blocked",
        "paper_order_creator_blocked",
        "broker_sender_blocked",
        "config_patch_blocked",
        "telegram_real_sender_blocked",
        "active_paper_enabler_blocked",
        "paper_admission_gate_blocked"
    ]

def build_runtime_component_map_items(paper_safe_payload: Dict[str, Any]) -> List[RuntimeComponentMapItem]:
    items = []
    for name in default_runtime_component_names():
        mode = RuntimeComponentMode.READ_ONLY_METADATA
        if "preview" in name:
            mode = RuntimeComponentMode.PREVIEW_ONLY
        elif "blocked" in name:
             if "write" in name: mode = RuntimeComponentMode.WRITE_BLOCKED
             elif "order" in name: mode = RuntimeComponentMode.ORDER_BLOCKED
             elif "broker" in name: mode = RuntimeComponentMode.BROKER_BLOCKED
             elif "config" in name: mode = RuntimeComponentMode.CONFIG_PATCH_BLOCKED
             elif "telegram" in name: mode = RuntimeComponentMode.TELEGRAM_REAL_SEND_BLOCKED
             elif "enabler" in name: mode = RuntimeComponentMode.ACTIVATION_BLOCKED
             elif "admission" in name: mode = RuntimeComponentMode.ACTIVATION_BLOCKED

        item = RuntimeComponentMapItem(
            component_id=create_runtime_component_id(),
            created_at_utc=utcnow_iso(),
            component_name=name,
            component_path=None,
            mode=mode,
            read_only=mode in [RuntimeComponentMode.READ_ONLY_METADATA, RuntimeComponentMode.PREVIEW_ONLY],
            preview_only=mode == RuntimeComponentMode.PREVIEW_ONLY,
            dry_run_only=False,
            write_allowed=False,
            order_allowed=False,
            broker_allowed=False,
            config_patch_allowed=False,
            telegram_real_send_allowed=False,
            activation_allowed=False,
            paper_admission_allowed=False,
            description=f"Runtime component mapping for {name}",
            risk_flags=[],
            warnings=[],
            errors=[]
        )
        items.append(item)
    return items

def build_pre_paper_local_runtime_map(paper_safe_payload: Dict[str, Any]) -> PrePaperLocalRuntimeMap:
    candidate_id = extract_paper_safe_candidate_id(paper_safe_payload)
    gate = extract_final_paper_safe_gate(paper_safe_payload)
    gate_id = gate.get("gate_id") if gate else None

    components = build_runtime_component_map_items(paper_safe_payload)
    routes = build_runtime_route_map_items(paper_safe_payload)

    runtime_map = PrePaperLocalRuntimeMap(
        runtime_map_id=create_pre_paper_runtime_map_id(),
        created_at_utc=utcnow_iso(),
        status=PrePaperRuntimeMapStatus.VALIDATED_READ_ONLY,
        decision=PrePaperRuntimeMapDecision.CREATE_PRE_PAPER_RUNTIME_MAP,
        candidate_id=candidate_id,
        source_paper_safe_gate_id=gate_id,
        component_items=components,
        route_items=routes,
        runtime_map_hash=None,
        map_is_metadata_only=True,
        read_only_boundary_confirmed=True,
        all_write_routes_denied=True,
        all_order_routes_denied=True,
        all_broker_routes_denied=True,
        all_config_patch_routes_denied=True,
        all_telegram_real_send_routes_denied=True,
        all_activation_routes_denied=True,
        all_paper_admission_routes_denied=True,
        risk_flags=[],
        required_followups=[],
        warnings=[],
        errors=[]
    )
    runtime_map.runtime_map_hash = stable_runtime_map_hash(paper_safe_payload)
    return runtime_map

def build_default_pre_paper_local_runtime_map(candidate_id: Optional[str] = None) -> PrePaperLocalRuntimeMap:
    return PrePaperLocalRuntimeMap(
        runtime_map_id=create_pre_paper_runtime_map_id(),
        created_at_utc=utcnow_iso(),
        status=PrePaperRuntimeMapStatus.VALIDATED_READ_ONLY,
        decision=PrePaperRuntimeMapDecision.CREATE_PRE_PAPER_RUNTIME_MAP,
        candidate_id=candidate_id,
        source_paper_safe_gate_id=None,
        component_items=[],
        route_items=[],
        runtime_map_hash=None,
        map_is_metadata_only=True,
        read_only_boundary_confirmed=True,
        all_write_routes_denied=True,
        all_order_routes_denied=True,
        all_broker_routes_denied=True,
        all_config_patch_routes_denied=True,
        all_telegram_real_send_routes_denied=True,
        all_activation_routes_denied=True,
        all_paper_admission_routes_denied=True,
        risk_flags=[],
        required_followups=[],
        warnings=[],
        errors=[]
    )

def stable_runtime_map_hash(payload: Dict[str, Any]) -> str:
    s = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def runtime_component_map_summary(items: List[RuntimeComponentMapItem]) -> Dict[str, Any]:
    return {
        "total": len(items),
        "read_only": len([i for i in items if i.read_only]),
        "preview": len([i for i in items if i.preview_only])
    }

def pre_paper_local_runtime_map_summary(runtime_map: PrePaperLocalRuntimeMap) -> Dict[str, Any]:
    return {
        "id": runtime_map.runtime_map_id,
        "status": runtime_map.status.value,
        "components": len(runtime_map.component_items),
        "routes": len(runtime_map.route_items)
    }

def pre_paper_local_runtime_map_to_text(runtime_map: PrePaperLocalRuntimeMap, limit: int = 100) -> str:
    lines = [
        f"Pre-Paper Local Runtime Map: {runtime_map.runtime_map_id}",
        f"Status: {runtime_map.status.value}",
        f"Map is Metadata Only: {runtime_map.map_is_metadata_only}",
        f"Components: {len(runtime_map.component_items)} | Routes: {len(runtime_map.route_items)}"
    ]
    return "\n".join(lines)
