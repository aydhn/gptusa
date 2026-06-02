from datetime import datetime, timezone
from typing import Any

from usa_signal_bot.backtesting.phase146_models import (
    ExecutionLatencyAssumption,
    create_execution_latency_assumption_id
)
from usa_signal_bot.core.enums import ExecutionLatencyKind

def build_default_execution_latency_assumption() -> ExecutionLatencyAssumption:
    return ExecutionLatencyAssumption(
        assumption_id=create_execution_latency_assumption_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        latency_kind=ExecutionLatencyKind.ONE_BAR_LATENCY,
        latency_bars=1,
        latency_sessions=0,
        configurable_metadata_only=True,
        live_latency_tracking_enabled=False,
        assumption_valid=True,
        research_data_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def validate_execution_latency_assumption(item: ExecutionLatencyAssumption) -> list[str]:
    errors = []
    if item.live_latency_tracking_enabled:
        errors.append("live_latency_tracking_enabled must be False")
    return errors

def execution_latency_assumption_summary(item: ExecutionLatencyAssumption) -> dict[str, Any]:
    return {"valid": item.assumption_valid, "kind": item.latency_kind.value}

def execution_latency_assumption_to_text(item: ExecutionLatencyAssumption, limit: int = 300) -> str:
    return f"ExecutionLatencyAssumption(valid={item.assumption_valid}, live_tracking={item.live_latency_tracking_enabled})"
