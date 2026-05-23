from typing import Any
from usa_signal_bot.paper_sandbox_bridge.sandbox_bridge_models import PaperSandboxBridgeDryRun, NoOrderPaperSessionEmulation, BridgeReplayResult
from usa_signal_bot.core.enums import PaperSandboxBridgeRiskFlag
def validate_bridge_no_write_continuity(dry_run: PaperSandboxBridgeDryRun | None = None, session: NoOrderPaperSessionEmulation | None = None, replay_result: BridgeReplayResult | None = None) -> list[str]: return []
def bridge_no_write_continuity_flags(payload: dict[str, Any]) -> list[PaperSandboxBridgeRiskFlag]: return []
def bridge_no_write_continuity_is_preserved(payload: dict[str, Any]) -> bool: return True
def bridge_no_write_continuity_summary(payload: dict[str, Any]) -> dict[str, Any]: return {}
def bridge_no_write_continuity_to_text(payload: dict[str, Any]) -> str: return ""
