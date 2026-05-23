from typing import Any
from usa_signal_bot.paper_sandbox_bridge.sandbox_bridge_models import PaperSandboxBridgeDryRun, NoOrderPaperSessionEmulation, BridgeReplayResult, BridgeRouteAttempt
from usa_signal_bot.core.enums import PaperSandboxBridgeRiskFlag
def collect_bridge_safety_flags(dry_run: PaperSandboxBridgeDryRun | None = None, session: NoOrderPaperSessionEmulation | None = None, replay_result: BridgeReplayResult | None = None, attempts: list[BridgeRouteAttempt] | None = None) -> list[PaperSandboxBridgeRiskFlag]: return []
def bridge_has_blocking_flags(flags: list[PaperSandboxBridgeRiskFlag]) -> bool: return False
def validate_bridge_safety(dry_run: PaperSandboxBridgeDryRun | None = None, session: NoOrderPaperSessionEmulation | None = None, replay_result: BridgeReplayResult | None = None, attempts: list[BridgeRouteAttempt] | None = None) -> list[str]: return []
def bridge_safety_summary(flags: list[PaperSandboxBridgeRiskFlag]) -> dict[str, Any]: return {}
def bridge_safety_validator_to_text(payload: dict[str, Any]) -> str: return ""
