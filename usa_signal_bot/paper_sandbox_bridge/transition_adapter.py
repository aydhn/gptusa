from typing import Any
from usa_signal_bot.paper_sandbox_bridge.sandbox_bridge_models import PaperSandboxBridgeDryRunPlan, PaperSandboxBridgeDryRun, NoOrderPaperSessionEmulation, BridgeReplayResult, PaperSandboxBridgeFullReview
from usa_signal_bot.paper_sandbox_bridge.bridge_dry_run_plan import build_default_bridge_dry_run_plan
from usa_signal_bot.paper_sandbox_bridge.bridge_dry_run_runner import PaperSandboxBridgeDryRunRunner
from usa_signal_bot.paper_sandbox_bridge.no_order_session_emulator import NoOrderPaperSessionEmulator
from usa_signal_bot.paper_sandbox_bridge.bridge_firewall_replay import BridgeFirewallReplayEngine
from usa_signal_bot.paper_sandbox_bridge.bridge_replay_plan import build_default_bridge_replay_plan
from usa_signal_bot.paper_sandbox_bridge.bridge_report import build_paper_sandbox_bridge_full_review

def bridge_dry_run_plan_from_transition(payload: dict[str, Any]) -> PaperSandboxBridgeDryRunPlan: return build_default_bridge_dry_run_plan()
def bridge_dry_run_from_transition(payload: dict[str, Any]) -> PaperSandboxBridgeDryRun: return PaperSandboxBridgeDryRunRunner().run_dry_run(build_default_bridge_dry_run_plan())
def no_order_session_from_transition(payload: dict[str, Any]) -> NoOrderPaperSessionEmulation: return NoOrderPaperSessionEmulator().run_session()
def bridge_replay_from_transition(payload: dict[str, Any]) -> BridgeReplayResult: return BridgeFirewallReplayEngine().replay(build_default_bridge_replay_plan())
def bridge_full_review_from_transition(payload: dict[str, Any]) -> PaperSandboxBridgeFullReview: return build_paper_sandbox_bridge_full_review({})
def attach_bridge_metadata_to_transition_payload(payload: dict[str, Any], review: PaperSandboxBridgeFullReview) -> dict[str, Any]: return payload
def transition_bridge_summary(payload: dict[str, Any]) -> dict[str, Any]: return {}
def transition_adapter_to_text(payload: dict[str, Any]) -> str: return ""
