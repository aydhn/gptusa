from typing import Any
from usa_signal_bot.core.enums import TradabilityStatus, ExecutionRiskLevel
from usa_signal_bot.execution.liquidity_models import TradabilityGuardResult

def attach_tradability_to_signal(signal: dict[str, Any], guard_result: TradabilityGuardResult) -> dict[str, Any]:
    if "metadata" not in signal:
        signal["metadata"] = {}

    signal["metadata"]["tradability_status"] = guard_result.status.value
    signal["metadata"]["tradability_risk_level"] = guard_result.risk_level.value

    if guard_result.status == TradabilityStatus.BLOCK_SIGNAL:
        signal["metadata"]["suppressed_by_execution_guard"] = True

    return signal

def attach_execution_realism_to_candidate(candidate: dict[str, Any], guard_result: TradabilityGuardResult) -> dict[str, Any]:
    if "metadata" not in candidate:
        candidate["metadata"] = {}

    candidate["metadata"]["tradability_status"] = guard_result.status.value
    candidate["metadata"]["execution_risk"] = guard_result.risk_level.value

    if guard_result.slippage_estimate:
        candidate["metadata"]["estimated_slippage_bps"] = guard_result.slippage_estimate.slippage_proxy_bps

    if guard_result.spread_estimate:
        candidate["metadata"]["estimated_spread_bps"] = guard_result.spread_estimate.spread_proxy_bps

    return candidate

def suppress_candidate_if_untradable(candidate: dict[str, Any], guard_result: TradabilityGuardResult) -> dict[str, Any]:
    if guard_result.status == TradabilityStatus.BLOCK_SIGNAL:
        if "metadata" not in candidate:
            candidate["metadata"] = {}
        candidate["metadata"]["suppressed"] = True
        candidate["metadata"]["suppressed_reason"] = "Tradability block"
    return candidate

def rank_penalty_from_tradability_guard(guard_result: TradabilityGuardResult) -> float:
    if guard_result.status == TradabilityStatus.BLOCK_SIGNAL:
        return 1000.0 # Huge penalty
    if guard_result.risk_level == ExecutionRiskLevel.CRITICAL:
        return 500.0
    if guard_result.risk_level == ExecutionRiskLevel.HIGH:
        return 100.0
    if guard_result.risk_level == ExecutionRiskLevel.MODERATE:
        return 20.0
    return 0.0

def signal_execution_metadata_summary(signal: dict[str, Any]) -> dict[str, Any]:
    meta = signal.get("metadata", {})
    return {
        "tradability_status": meta.get("tradability_status", "UNKNOWN"),
        "tradability_risk_level": meta.get("tradability_risk_level", "UNKNOWN"),
        "suppressed": meta.get("suppressed_by_execution_guard", False)
    }
