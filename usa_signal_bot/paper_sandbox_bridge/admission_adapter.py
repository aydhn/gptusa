from typing import Any
from usa_signal_bot.paper_sandbox_bridge.sandbox_bridge_models import PaperSandboxBridgeFullReview
def bridge_evidence_from_admission(payload: dict[str, Any]) -> list[str]: return []
def admission_supports_bridge_dry_run(payload: dict[str, Any]) -> tuple[bool, list[str]]: return True, []
def attach_bridge_hint_to_admission_payload(payload: dict[str, Any], review: PaperSandboxBridgeFullReview) -> dict[str, Any]: return payload
def admission_bridge_summary(payload: dict[str, Any]) -> dict[str, Any]: return {}
def admission_adapter_to_text(payload: dict[str, Any]) -> str: return ""
