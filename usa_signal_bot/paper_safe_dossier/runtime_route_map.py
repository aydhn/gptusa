from typing import Any, Dict, List
from datetime import datetime, timezone
from usa_signal_bot.core.enums import RuntimeRoutePermission
from usa_signal_bot.paper_safe_dossier.paper_safe_dossier_models import RuntimeRouteMapItem, create_runtime_route_id

def utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def default_runtime_route_names() -> List[str]:
    return [
        "read_market_data_route",
        "read_signal_preview_route",
        "read_risk_preview_route",
        "read_paper_snapshot_route",
        "notification_preview_route",
        "audit_read_route",
        "validation_read_route",
        "paper_state_write_route",
        "paper_order_create_route",
        "broker_order_send_route",
        "config_patch_route",
        "telegram_real_send_route",
        "active_paper_enable_route",
        "paper_admission_route"
    ]

def build_runtime_route_map_items(paper_safe_payload: Dict[str, Any]) -> List[RuntimeRouteMapItem]:
    items = []
    for name in default_runtime_route_names():
        items.append(runtime_route_for_name(name))
    return items

def runtime_route_for_name(route_name: str) -> RuntimeRouteMapItem:
    permission = RuntimeRoutePermission.READ_ONLY_ALLOWED
    if "preview" in route_name:
         permission = RuntimeRoutePermission.PREVIEW_ALLOWED
    elif "write" in route_name:
         permission = RuntimeRoutePermission.WRITE_DENIED
    elif "broker" in route_name:
         permission = RuntimeRoutePermission.BROKER_DENIED
    elif "order" in route_name:
         permission = RuntimeRoutePermission.ORDER_DENIED
    elif "config" in route_name:
         permission = RuntimeRoutePermission.CONFIG_PATCH_DENIED
    elif "telegram" in route_name:
         permission = RuntimeRoutePermission.TELEGRAM_REAL_SEND_DENIED
    elif "enable" in route_name:
         permission = RuntimeRoutePermission.ACTIVATION_DENIED
    elif "admission" in route_name:
         permission = RuntimeRoutePermission.PAPER_ADMISSION_DENIED

    return RuntimeRouteMapItem(
        route_id=create_runtime_route_id(),
        created_at_utc=utcnow_iso(),
        route_name=route_name,
        source_component=None,
        target_component=None,
        permission=permission,
        read_only_allowed=permission in [RuntimeRoutePermission.READ_ONLY_ALLOWED, RuntimeRoutePermission.PREVIEW_ALLOWED],
        preview_allowed=permission == RuntimeRoutePermission.PREVIEW_ALLOWED,
        dry_run_allowed=False,
        write_allowed=False,
        order_allowed=False,
        broker_allowed=False,
        config_patch_allowed=False,
        telegram_real_send_allowed=False,
        activation_allowed=False,
        paper_admission_allowed=False,
        risk_flags=[],
        warnings=[],
        errors=[],
        metadata={}
    )

def validate_runtime_route_map_complete(routes: List[RuntimeRouteMapItem]) -> List[str]:
    errors = []
    names = [r.route_name for r in routes]
    for required in default_runtime_route_names():
         if required not in names:
             errors.append(f"Missing required route: {required}")
    return errors

def runtime_route_map_summary(routes: List[RuntimeRouteMapItem]) -> Dict[str, Any]:
    denied = len([r for r in routes if not r.read_only_allowed and not r.preview_allowed])
    allowed = len([r for r in routes if r.read_only_allowed or r.preview_allowed])
    return {
        "total": len(routes),
        "denied_routes": denied,
        "read_only_routes": allowed
    }

def runtime_route_map_to_text(routes: List[RuntimeRouteMapItem], limit: int = 100) -> str:
    summary = runtime_route_map_summary(routes)
    lines = [f"Route Map Summary - Total: {summary['total']} | Denied: {summary['denied_routes']} | Allowed: {summary['read_only_routes']}"]
    for i, r in enumerate(routes[:limit]):
        lines.append(f" - {r.route_name}: {r.permission.value}")
    if len(routes) > limit:
         lines.append(f" - ... and {len(routes)-limit} more.")
    return "\n".join(lines)
