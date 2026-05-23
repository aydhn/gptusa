from typing import Any
from usa_signal_bot.paper_sandbox_bridge.sandbox_bridge_models import PaperSandboxBridgeDryRun, PaperSandboxBridgeDryRunPlan, NoOrderPaperSessionEmulation, BridgeReplayResult
from usa_signal_bot.core.enums import PaperSandboxBridgeDryRunStatus, PaperSandboxBridgeDryRunDecision
from usa_signal_bot.paper_sandbox_bridge.no_order_session_emulator import NoOrderPaperSessionEmulator
from usa_signal_bot.paper_sandbox_bridge.bridge_firewall_replay import BridgeFirewallReplayEngine
from usa_signal_bot.paper_sandbox_bridge.bridge_replay_plan import build_default_bridge_replay_plan
from datetime import datetime

class PaperSandboxBridgeDryRunRunner:
    def __init__(self, conservative: bool = True): pass
    def run_dry_run(self, plan: PaperSandboxBridgeDryRunPlan, transition_payload: dict[str, Any] | None = None, paper_snapshot: dict[str, Any] | None = None) -> PaperSandboxBridgeDryRun: return PaperSandboxBridgeDryRun(dry_run_id="mock", created_at_utc=datetime.utcnow().isoformat() + "Z", status=PaperSandboxBridgeDryRunStatus.COMPLETED_NO_WRITE, decision=PaperSandboxBridgeDryRunDecision.RUN_BRIDGE_DRY_RUN, candidate_id=None, plan=plan, no_order_session=self.build_no_order_session_for_run(), bridge_replay_result=self.build_bridge_replay_for_run(), route_attempts=[], read_only_snapshot_hash=None, output_summary={}, activation_denied=True, activation_allowed=False, transition_allowed=False, all_writes_blocked=True, order_created=False, mutation_detected=False, safety_flags=[], started_at_utc=None, completed_at_utc=None, output_paths={}, warnings=[], errors=[])
    def build_no_order_session_for_run(self, transition_payload: dict[str, Any] | None = None, paper_snapshot: dict[str, Any] | None = None) -> NoOrderPaperSessionEmulation: return NoOrderPaperSessionEmulator().run_session()
    def build_bridge_replay_for_run(self, transition_payload: dict[str, Any] | None = None) -> BridgeReplayResult: return BridgeFirewallReplayEngine().replay(build_default_bridge_replay_plan())
    def validate_dry_run_safety(self, run: PaperSandboxBridgeDryRun) -> list[str]: return []
    def determine_dry_run_decision(self, session: NoOrderPaperSessionEmulation | None, replay_result: BridgeReplayResult | None) -> PaperSandboxBridgeDryRunDecision: return PaperSandboxBridgeDryRunDecision.RUN_BRIDGE_DRY_RUN
    def bridge_dry_run_summary(self, run: PaperSandboxBridgeDryRun) -> dict[str, Any]: return {}
