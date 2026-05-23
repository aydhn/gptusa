from typing import Any, Dict, List
from usa_signal_bot.paper_safe_dossier.paper_safe_dossier_models import PrePaperLocalRuntimeMap, RuntimeComponentMapItem, RuntimeRouteMapItem

def validate_runtime_component_no_execution(item: RuntimeComponentMapItem) -> List[str]:
    errors = []
    if item.write_allowed: errors.append(f"Component {item.component_name} allows write.")
    if item.order_allowed: errors.append(f"Component {item.component_name} allows order.")
    if item.broker_allowed: errors.append(f"Component {item.component_name} allows broker.")
    if item.config_patch_allowed: errors.append(f"Component {item.component_name} allows config patch.")
    if item.telegram_real_send_allowed: errors.append(f"Component {item.component_name} allows telegram real send.")
    if item.activation_allowed: errors.append(f"Component {item.component_name} allows activation.")
    if item.paper_admission_allowed: errors.append(f"Component {item.component_name} allows paper admission.")
    return errors

def validate_runtime_route_no_execution(item: RuntimeRouteMapItem) -> List[str]:
    errors = []
    if item.write_allowed: errors.append(f"Route {item.route_name} allows write.")
    if item.order_allowed: errors.append(f"Route {item.route_name} allows order.")
    if item.broker_allowed: errors.append(f"Route {item.route_name} allows broker.")
    if item.config_patch_allowed: errors.append(f"Route {item.route_name} allows config patch.")
    if item.telegram_real_send_allowed: errors.append(f"Route {item.route_name} allows telegram real send.")
    if item.activation_allowed: errors.append(f"Route {item.route_name} allows activation.")
    if item.paper_admission_allowed: errors.append(f"Route {item.route_name} allows paper admission.")
    return errors

def validate_pre_paper_runtime_map_safety(runtime_map: PrePaperLocalRuntimeMap) -> List[str]:
    errors = []
    if not runtime_map.map_is_metadata_only:
        errors.append("Runtime map is not metadata only.")
    if not runtime_map.all_write_routes_denied:
         errors.append("All write routes are not denied.")
    if not runtime_map.all_order_routes_denied:
         errors.append("All order routes are not denied.")
    if not runtime_map.all_broker_routes_denied:
         errors.append("All broker routes are not denied.")
    if not runtime_map.all_config_patch_routes_denied:
         errors.append("All config patch routes are not denied.")
    if not runtime_map.all_telegram_real_send_routes_denied:
         errors.append("All telegram real send routes are not denied.")
    if not runtime_map.all_activation_routes_denied:
         errors.append("All activation routes are not denied.")
    if not runtime_map.all_paper_admission_routes_denied:
         errors.append("All paper admission routes are not denied.")

    for comp in runtime_map.component_items:
        errors.extend(validate_runtime_component_no_execution(comp))

    for route in runtime_map.route_items:
        errors.extend(validate_runtime_route_no_execution(route))

    return errors

def runtime_map_allows_execution(runtime_map: PrePaperLocalRuntimeMap) -> bool:
    for comp in runtime_map.component_items:
         if validate_runtime_component_no_execution(comp): return True
    for route in runtime_map.route_items:
         if validate_runtime_route_no_execution(route): return True
    return False

def runtime_map_requires_followup(runtime_map: PrePaperLocalRuntimeMap) -> bool:
    return len(runtime_map.required_followups) > 0 or len(runtime_map.warnings) > 0

def runtime_map_validator_summary(runtime_map: PrePaperLocalRuntimeMap) -> Dict[str, Any]:
    errors = validate_pre_paper_runtime_map_safety(runtime_map)
    return {
        "is_safe": len(errors) == 0,
        "error_count": len(errors),
        "allows_execution": runtime_map_allows_execution(runtime_map)
    }

def runtime_map_validator_to_text(payload: Dict[str, Any]) -> str:
    lines = [f"Runtime Map Is Safe: {payload.get('is_safe', False)}"]
    if payload.get("error_count", 0) > 0:
        lines.append(f"Errors: {payload.get('error_count')}")
    if payload.get("allows_execution", False):
        lines.append("WARNING: Runtime map allows execution!")
    return "\n".join(lines)
