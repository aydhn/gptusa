from typing import Any
from usa_signal_bot.paper_sandbox_bridge.sandbox_bridge_models import PaperSandboxBridgeFullReview, PaperSandboxBridgeDryRunPlan, PaperSandboxBridgeDryRun, NoOrderPaperSessionEmulation, BridgeReplayResult
from usa_signal_bot.core.enums import PaperSandboxBridgeReportType
from usa_signal_bot.paper_sandbox_bridge.bridge_dry_run_plan import build_default_bridge_dry_run_plan
from datetime import datetime
def build_paper_sandbox_bridge_full_review(transition_payload: dict[str, Any]) -> PaperSandboxBridgeFullReview: return build_bridge_review_from_parts(build_default_bridge_dry_run_plan())
def build_bridge_review_from_parts(plan: PaperSandboxBridgeDryRunPlan, dry_run: PaperSandboxBridgeDryRun | None = None, session: NoOrderPaperSessionEmulation | None = None, replay_result: BridgeReplayResult | None = None) -> PaperSandboxBridgeFullReview: return PaperSandboxBridgeFullReview(review_id="mock", created_at_utc=datetime.utcnow().isoformat() + "Z", report_type=PaperSandboxBridgeReportType.FULL_PAPER_SANDBOX_BRIDGE_REVIEW, dry_run_plans=[plan], dry_runs=[], no_order_sessions=[], bridge_replay_plans=[], bridge_replay_results=[], route_attempts=[], audit_entries=[], output_paths={}, warnings=[], errors=[])
def paper_sandbox_bridge_full_review_summary(review: PaperSandboxBridgeFullReview) -> dict[str, Any]: return {}
def paper_sandbox_bridge_limitations_text() -> str: return ""
def paper_sandbox_bridge_full_review_to_text(review: PaperSandboxBridgeFullReview, limit: int = 100) -> str: return ""
