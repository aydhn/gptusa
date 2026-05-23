from typing import Any
from usa_signal_bot.core.enums import PaperSandboxBridgeDryRunDecision, PaperSandboxBridgeDryRunStatus, PaperSandboxBridgeRiskFlag
def evaluate_bridge_dry_run_eligibility(transition_payload: dict[str, Any]) -> PaperSandboxBridgeDryRunDecision: return PaperSandboxBridgeDryRunDecision.RUN_BRIDGE_DRY_RUN
def bridge_dry_run_eligibility_reasons(transition_payload: dict[str, Any]) -> list[str]: return []
def bridge_safety_flags_from_transition(payload: dict[str, Any]) -> list[PaperSandboxBridgeRiskFlag]: return []
def bridge_dry_run_status_from_decision(decision: PaperSandboxBridgeDryRunDecision) -> PaperSandboxBridgeDryRunStatus: return PaperSandboxBridgeDryRunStatus.READY
def eligibility_checker_to_text(payload: dict[str, Any]) -> str: return ""
