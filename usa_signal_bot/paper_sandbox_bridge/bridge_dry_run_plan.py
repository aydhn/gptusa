from typing import Any
from usa_signal_bot.paper_sandbox_bridge.sandbox_bridge_models import PaperSandboxBridgeDryRunPlan
from usa_signal_bot.core.enums import PaperSandboxBridgeDryRunDecision
from datetime import datetime
def build_paper_sandbox_bridge_dry_run_plan(transition_payload: dict[str, Any]) -> PaperSandboxBridgeDryRunPlan: return build_default_bridge_dry_run_plan()
def build_default_bridge_dry_run_plan(candidate_id: str | None = None) -> PaperSandboxBridgeDryRunPlan:
    return PaperSandboxBridgeDryRunPlan(plan_id="mock", created_at_utc=datetime.utcnow().isoformat() + "Z", candidate_id=candidate_id, source_transition_review_id=None, source_dossier_id=None, source_bridge_id=None, decision=PaperSandboxBridgeDryRunDecision.RUN_BRIDGE_DRY_RUN, required_inputs=[], planned_steps=[], expected_outputs=[], require_no_order_session=True, require_bridge_replay=True, require_route_guard=True, execution_enabled=False, active_paper_enabled=False, broker_execution_enabled=False, paper_state_mutation_enabled=False, config_patch_enabled=False, telegram_real_send_enabled=False, warnings=[], errors=[])
def default_bridge_dry_run_steps() -> list[str]: return []
def required_bridge_dry_run_inputs() -> list[str]: return []
def required_bridge_dry_run_outputs() -> list[str]: return []
def validate_bridge_dry_run_plan_safety(plan: PaperSandboxBridgeDryRunPlan) -> list[str]: return []
def bridge_dry_run_plan_summary(plan: PaperSandboxBridgeDryRunPlan) -> dict[str, Any]: return {}
def bridge_dry_run_plan_to_text(plan: PaperSandboxBridgeDryRunPlan) -> str: return ""
