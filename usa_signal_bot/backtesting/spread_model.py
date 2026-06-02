from datetime import datetime, timezone
from typing import Any

from usa_signal_bot.backtesting.phase146_models import (
    SpreadModel,
    create_spread_model_id
)
from usa_signal_bot.core.enums import SpreadModelKind

def build_default_spread_model() -> SpreadModel:
    return SpreadModel(
        model_id=create_spread_model_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        spread_kind=SpreadModelKind.FIXED_BPS_SPREAD,
        fixed_bps=2.0,
        price_bucket_rules=[],
        volume_bucket_rules=[],
        spread_model_valid=True,
        live_quote_required=False,
        research_data_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_zero_spread_control_model() -> SpreadModel:
    return SpreadModel(
        model_id=create_spread_model_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        spread_kind=SpreadModelKind.ZERO_SPREAD_CONTROL,
        fixed_bps=0.0,
        price_bucket_rules=[],
        volume_bucket_rules=[],
        spread_model_valid=True,
        live_quote_required=False,
        research_data_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def estimate_spread_cost_bps(price: float, volume: float | None, model: SpreadModel) -> float:
    if model.spread_kind == SpreadModelKind.ZERO_SPREAD_CONTROL:
        return 0.0
    if model.spread_kind == SpreadModelKind.FIXED_BPS_SPREAD and model.fixed_bps is not None:
        return model.fixed_bps
    return 0.0

def validate_spread_model(model: SpreadModel) -> list[str]:
    errors = []
    if model.live_quote_required:
        errors.append("live_quote_required must be False")
    return errors

def spread_model_summary(model: SpreadModel) -> dict[str, Any]:
    return {"valid": model.spread_model_valid, "kind": model.spread_kind.value}

def spread_model_to_text(model: SpreadModel, limit: int = 300) -> str:
    return f"SpreadModel(valid={model.spread_model_valid}, live_quote={model.live_quote_required})"
