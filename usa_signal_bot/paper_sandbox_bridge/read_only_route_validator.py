from typing import Any
from usa_signal_bot.paper_sandbox_bridge.sandbox_bridge_models import BridgeRouteAttempt
from usa_signal_bot.core.enums import BridgeRouteAttemptType
def read_only_route_attempt_types() -> list[BridgeRouteAttemptType]: return []
def validate_read_only_route_attempt(attempt: BridgeRouteAttempt) -> list[str]: return []
def validate_read_only_routes(attempts: list[BridgeRouteAttempt]) -> list[str]: return []
def read_only_route_summary(attempts: list[BridgeRouteAttempt]) -> dict[str, Any]: return {}
def read_only_route_validator_to_text(payload: dict[str, Any]) -> str: return ""
