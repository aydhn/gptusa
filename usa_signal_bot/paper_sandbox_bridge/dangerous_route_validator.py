from typing import Any
from usa_signal_bot.paper_sandbox_bridge.sandbox_bridge_models import BridgeRouteAttempt
from usa_signal_bot.core.enums import BridgeRouteAttemptType, PaperSandboxBridgeRiskFlag
def dangerous_bridge_route_attempt_types() -> list[BridgeRouteAttemptType]: return []
def validate_dangerous_route_attempt_denied(attempt: BridgeRouteAttempt) -> list[str]: return []
def validate_all_dangerous_routes_denied(attempts: list[BridgeRouteAttempt]) -> list[str]: return []
def dangerous_route_risk_flags(attempts: list[BridgeRouteAttempt]) -> list[PaperSandboxBridgeRiskFlag]: return []
def dangerous_route_validator_summary(attempts: list[BridgeRouteAttempt]) -> dict[str, Any]: return {}
def dangerous_route_validator_to_text(payload: dict[str, Any]) -> str: return ""
