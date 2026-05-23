from typing import Any
import datetime
from usa_signal_bot.core.enums import SandboxBridgeRouteType, SandboxBridgeRouteStatus
from usa_signal_bot.paper_no_write_transition.no_write_transition_models import PaperSandboxBridgeRoute, create_bridge_route_id

def read_only_sandbox_route_types() -> list[SandboxBridgeRouteType]:
    return [
        SandboxBridgeRouteType.READ_MARKET_DATA,
        SandboxBridgeRouteType.READ_SIGNAL_PREVIEW,
        SandboxBridgeRouteType.READ_RISK_PREVIEW,
        SandboxBridgeRouteType.READ_PAPER_SNAPSHOT
    ]

def denied_sandbox_route_types() -> list[SandboxBridgeRouteType]:
    return [
        SandboxBridgeRouteType.WRITE_PAPER_STATE,
        SandboxBridgeRouteType.CREATE_PAPER_ORDER,
        SandboxBridgeRouteType.UPDATE_POSITION,
        SandboxBridgeRouteType.UPDATE_PORTFOLIO,
        SandboxBridgeRouteType.PATCH_CONFIG,
        SandboxBridgeRouteType.ENABLE_ACTIVE_PAPER,
        SandboxBridgeRouteType.SEND_BROKER_ORDER,
        SandboxBridgeRouteType.SEND_TELEGRAM_REAL
    ]

def route_for_sandbox_bridge_type(route_type: SandboxBridgeRouteType) -> PaperSandboxBridgeRoute:
    if route_type in read_only_sandbox_route_types():
        status = SandboxBridgeRouteStatus.READ_ONLY_ALLOWED
        read_only = True
    else:
        # Determine specific denial status
        if route_type in [SandboxBridgeRouteType.CREATE_PAPER_ORDER, SandboxBridgeRouteType.SEND_BROKER_ORDER]:
             status = SandboxBridgeRouteStatus.ORDER_DENIED if route_type == SandboxBridgeRouteType.CREATE_PAPER_ORDER else SandboxBridgeRouteStatus.BROKER_DENIED
        elif route_type == SandboxBridgeRouteType.PATCH_CONFIG:
             status = SandboxBridgeRouteStatus.CONFIG_PATCH_DENIED
        elif route_type == SandboxBridgeRouteType.ENABLE_ACTIVE_PAPER:
             status = SandboxBridgeRouteStatus.ACTIVATION_DENIED
        elif route_type == SandboxBridgeRouteType.SEND_TELEGRAM_REAL:
             status = SandboxBridgeRouteStatus.TELEGRAM_REAL_SEND_DENIED
        else:
             status = SandboxBridgeRouteStatus.WRITE_DENIED
        read_only = False

    return PaperSandboxBridgeRoute(
        route_id=create_bridge_route_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        route_type=route_type,
        status=status,
        read_only=read_only,
        write_allowed=False,
        order_allowed=False,
        broker_allowed=False,
        telegram_real_send_allowed=False,
        config_patch_allowed=False,
        activation_allowed=False,
        description=f"Auto-generated route config for {route_type.value}",
        risk_flags=[],
        warnings=[],
        errors=[]
    )

def default_sandbox_bridge_routes() -> list[PaperSandboxBridgeRoute]:
    routes = []
    for rt in SandboxBridgeRouteType:
        if rt == SandboxBridgeRouteType.UNKNOWN:
            continue
        routes.append(route_for_sandbox_bridge_type(rt))
    return routes

def validate_sandbox_bridge_routes_complete(routes: list[PaperSandboxBridgeRoute]) -> list[str]:
    provided_types = {r.route_type for r in routes}
    errors = []
    for rt in SandboxBridgeRouteType:
        if rt != SandboxBridgeRouteType.UNKNOWN and rt not in provided_types:
            errors.append(f"Missing route configuration for {rt.value}")
    return errors

def sandbox_bridge_route_summary(routes: list[PaperSandboxBridgeRoute]) -> dict[str, Any]:
    return {
        "total": len(routes),
        "read_only": sum(1 for r in routes if r.read_only),
        "denied": sum(1 for r in routes if not r.read_only)
    }

def sandbox_bridge_routes_to_text(routes: list[PaperSandboxBridgeRoute], limit: int = 100) -> str:
    lines = ["Sandbox Bridge Routes:"]
    for r in routes[:limit]:
        lines.append(f"  - {r.route_type.value}: {r.status.value}")
    return "\n".join(lines)
