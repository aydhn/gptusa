from datetime import datetime, timezone
from typing import Any

from usa_signal_bot.backtesting.phase146_models import (
    PartialFillAssumption,
    create_partial_fill_assumption_id
)
from usa_signal_bot.core.enums import PartialFillAssumptionKind

def build_default_partial_fill_assumption() -> PartialFillAssumption:
    return PartialFillAssumption(
        assumption_id=create_partial_fill_assumption_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        assumption_kind=PartialFillAssumptionKind.VOLUME_CAP_PARTIAL_FILL,
        volume_cap_rate=0.01,
        allow_partial_fill_metadata=True,
        no_fill_if_illiquid=True,
        live_fill_tracking_enabled=False,
        assumption_valid=True,
        research_data_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def validate_partial_fill_assumption(item: PartialFillAssumption) -> list[str]:
    errors = []
    if item.live_fill_tracking_enabled:
        errors.append("live_fill_tracking_enabled must be False")
    return errors

def partial_fill_assumption_summary(item: PartialFillAssumption) -> dict[str, Any]:
    return {"valid": item.assumption_valid, "kind": item.assumption_kind.value}

def partial_fill_assumption_to_text(item: PartialFillAssumption, limit: int = 300) -> str:
    return f"PartialFillAssumption(valid={item.assumption_valid}, live_tracking={item.live_fill_tracking_enabled})"
