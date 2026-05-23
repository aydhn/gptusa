from typing import Any
from usa_signal_bot.paper_sandbox_bridge.sandbox_bridge_models import BridgeReplayPlan
from usa_signal_bot.core.enums import BridgeRouteAttemptType
from datetime import datetime
def required_bridge_route_attempts() -> list[BridgeRouteAttemptType]: return []
def build_bridge_replay_plan(transition_payload: dict[str, Any]) -> BridgeReplayPlan: return build_default_bridge_replay_plan()
def build_default_bridge_replay_plan(candidate_id: str | None = None) -> BridgeReplayPlan: return BridgeReplayPlan(replay_plan_id="mock", created_at_utc=datetime.utcnow().isoformat() + "Z", candidate_id=candidate_id, source_bridge_id=None, source_dossier_id=None, required_route_attempts=[], require_all_dangerous_routes_denied=True, allow_read_only_routes=True, execution_enabled=False, active_paper_enabled=False, broker_execution_enabled=False, paper_state_mutation_enabled=False, config_patch_enabled=False, telegram_real_send_enabled=False, warnings=[], errors=[])
def validate_bridge_replay_plan_safety(plan: BridgeReplayPlan) -> list[str]: return []
def bridge_replay_plan_summary(plan: BridgeReplayPlan) -> dict[str, Any]: return {}
def bridge_replay_plan_to_text(plan: BridgeReplayPlan) -> str: return ""
