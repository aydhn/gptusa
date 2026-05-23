from typing import Any
from usa_signal_bot.paper_sandbox_bridge.sandbox_bridge_models import NoOrderPaperSessionEmulation, NoOrderSessionStep
def analyze_no_order_session(session: NoOrderPaperSessionEmulation) -> dict[str, Any]: return {}
def count_no_order_step_statuses(steps: list[NoOrderSessionStep]) -> dict[str, int]: return {}
def no_order_session_has_order_attempt(session: NoOrderPaperSessionEmulation) -> bool: return False
def no_order_session_has_write_attempt(session: NoOrderPaperSessionEmulation) -> bool: return False
def no_order_session_requires_followup(session: NoOrderPaperSessionEmulation) -> bool: return False
def no_order_session_analyzer_to_text(payload: dict[str, Any]) -> str: return ""
