from typing import Any
from usa_signal_bot.paper_sandbox_bridge.sandbox_bridge_models import BridgeRouteAttempt
from usa_signal_bot.core.enums import BridgeRouteAttemptType, BridgeRouteAttemptDecision, PaperSandboxBridgeRiskFlag
from datetime import datetime
def simulate_bridge_route_attempts() -> list[BridgeRouteAttempt]: return []
def simulate_bridge_route_attempt(attempt_type: BridgeRouteAttemptType) -> BridgeRouteAttempt: return BridgeRouteAttempt(attempt_id="mock", created_at_utc=datetime.utcnow().isoformat() + "Z", attempt_type=attempt_type, decision=BridgeRouteAttemptDecision.BLOCK, blocked=True, read_only=False, write_attempted=False, order_attempted=False, broker_send_attempted=False, config_patch_attempted=False, telegram_real_send_attempted=False, active_paper_enable_attempted=False, source_component=None, payload_summary={}, risk_flags=[], warnings=[], errors=[])
def bridge_route_attempt_decision(attempt_type: BridgeRouteAttemptType) -> BridgeRouteAttemptDecision: return BridgeRouteAttemptDecision.BLOCK
def bridge_route_attempt_is_dangerous(attempt_type: BridgeRouteAttemptType) -> bool: return True
def bridge_route_attempt_risk_flags(attempt_type: BridgeRouteAttemptType, allowed: bool = False) -> list[PaperSandboxBridgeRiskFlag]: return []
def bridge_route_attempt_simulator_summary(attempts: list[BridgeRouteAttempt]) -> dict[str, Any]: return {}
def bridge_route_attempt_simulator_to_text(attempts: list[BridgeRouteAttempt], limit: int = 100) -> str: return ""
