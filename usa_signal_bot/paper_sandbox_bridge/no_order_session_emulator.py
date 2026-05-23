from typing import Any
from usa_signal_bot.paper_sandbox_bridge.sandbox_bridge_models import NoOrderPaperSessionEmulation, NoOrderSessionStep
from usa_signal_bot.core.enums import NoOrderPaperSessionStatus, NoOrderPaperSessionDecision
from datetime import datetime
class NoOrderPaperSessionEmulator:
    def __init__(self, conservative: bool = True): pass
    def run_session(self, transition_payload: dict[str, Any] | None = None, paper_snapshot: dict[str, Any] | None = None) -> NoOrderPaperSessionEmulation: return NoOrderPaperSessionEmulation(session_id="mock", created_at_utc=datetime.utcnow().isoformat() + "Z", status=NoOrderPaperSessionStatus.COMPLETED_NO_ORDER, decision=NoOrderPaperSessionDecision.PASS_NO_ORDER_SESSION_EMULATION, candidate_id=None, source_bridge_id=None, source_dossier_id=None, steps=[], read_only_snapshot_hash=None, output_summary={}, activation_denied=True, activation_allowed=False, transition_allowed=False, all_writes_blocked=True, order_created=False, mutation_detected=False, safety_flags=[], started_at_utc=None, completed_at_utc=None, output_paths={}, warnings=[], errors=[])
    def run_step(self, step_name: str, paper_snapshot: dict[str, Any]) -> NoOrderSessionStep: return None
    def default_session_steps(self) -> list[str]: return []
    def validate_session_safety(self, session: NoOrderPaperSessionEmulation) -> list[str]: return []
    def determine_session_decision(self, steps: list[NoOrderSessionStep]) -> NoOrderPaperSessionDecision: return NoOrderPaperSessionDecision.PASS_NO_ORDER_SESSION_EMULATION
    def no_order_session_summary(self, session: NoOrderPaperSessionEmulation) -> dict[str, Any]: return {}
