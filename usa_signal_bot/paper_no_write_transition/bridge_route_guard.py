from typing import Any
from usa_signal_bot.core.enums import NoWriteTransitionRiskFlag
from usa_signal_bot.paper_no_write_transition.no_write_transition_models import PaperSandboxBridgeRoute

def bridge_route_allows_dangerous_operation(route: PaperSandboxBridgeRoute) -> bool:
    return any([
        route.write_allowed,
        route.order_allowed,
        route.broker_allowed,
        route.telegram_real_send_allowed,
        route.config_patch_allowed,
        route.activation_allowed
    ])

def validate_bridge_route_no_write(route: PaperSandboxBridgeRoute) -> list[str]:
    errors = []
    if route.write_allowed: errors.append(f"Route {route.route_type.value} allows write.")
    if route.order_allowed: errors.append(f"Route {route.route_type.value} allows order.")
    if route.broker_allowed: errors.append(f"Route {route.route_type.value} allows broker.")
    if route.telegram_real_send_allowed: errors.append(f"Route {route.route_type.value} allows Telegram real send.")
    if route.config_patch_allowed: errors.append(f"Route {route.route_type.value} allows config patch.")
    if route.activation_allowed: errors.append(f"Route {route.route_type.value} allows activation.")
    return errors

def validate_all_bridge_routes_no_write(routes: list[PaperSandboxBridgeRoute]) -> list[str]:
    errors = []
    for r in routes:
        errors.extend(validate_bridge_route_no_write(r))
    return errors

def collect_bridge_route_risk_flags(routes: list[PaperSandboxBridgeRoute]) -> list[NoWriteTransitionRiskFlag]:
    flags = set()
    for route in routes:
        if route.write_allowed: flags.add(NoWriteTransitionRiskFlag.SANDBOX_BRIDGE_WRITE_ROUTE_RISK)
        if route.order_allowed: flags.add(NoWriteTransitionRiskFlag.SANDBOX_BRIDGE_ORDER_ROUTE_RISK)
        if route.broker_allowed: flags.add(NoWriteTransitionRiskFlag.SANDBOX_BRIDGE_BROKER_ROUTE_RISK)
        if route.activation_allowed: flags.add(NoWriteTransitionRiskFlag.SANDBOX_BRIDGE_ACTIVATION_ROUTE_RISK)

        errs = validate_bridge_route_no_write(route)
        if errs:
            flags.add(NoWriteTransitionRiskFlag.BRIDGE_GUARD_FAILED)

    return list(flags)

def bridge_route_guard_summary(routes: list[PaperSandboxBridgeRoute]) -> dict[str, Any]:
    flags = collect_bridge_route_risk_flags(routes)
    return {
        "is_safe": len(flags) == 0,
        "risk_flags": [f.value for f in flags]
    }

def bridge_route_guard_to_text(payload: dict[str, Any]) -> str:
    return f"Bridge Route Guard: Safe={payload.get('is_safe')} Flags={payload.get('risk_flags')}"
