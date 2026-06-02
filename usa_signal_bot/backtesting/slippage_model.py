from datetime import datetime, timezone
from typing import Any

from usa_signal_bot.backtesting.phase146_models import (
    SlippageModel,
    create_slippage_model_id
)
from usa_signal_bot.core.enums import SlippageModelKind

def build_default_slippage_model() -> SlippageModel:
    return SlippageModel(
        model_id=create_slippage_model_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        slippage_kind=SlippageModelKind.FIXED_BPS_SLIPPAGE,
        fixed_bps=3.0,
        volume_participation_rate=None,
        volatility_multiplier=None,
        conservative_buffer_bps=1.0,
        slippage_model_valid=True,
        live_quote_required=False,
        research_data_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_zero_slippage_control_model() -> SlippageModel:
    return SlippageModel(
        model_id=create_slippage_model_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        slippage_kind=SlippageModelKind.ZERO_SLIPPAGE_CONTROL,
        fixed_bps=0.0,
        volume_participation_rate=None,
        volatility_multiplier=None,
        conservative_buffer_bps=0.0,
        slippage_model_valid=True,
        live_quote_required=False,
        research_data_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def estimate_slippage_bps(price: float, volume: float | None, volatility: float | None, model: SlippageModel) -> float:
    if model.slippage_kind == SlippageModelKind.ZERO_SLIPPAGE_CONTROL:
        return 0.0
    if model.slippage_kind == SlippageModelKind.FIXED_BPS_SLIPPAGE and model.fixed_bps is not None:
        return model.fixed_bps
    return 0.0

def validate_slippage_model(model: SlippageModel) -> list[str]:
    errors = []
    if model.live_quote_required:
        errors.append("live_quote_required must be False")
    return errors

def slippage_model_summary(model: SlippageModel) -> dict[str, Any]:
    return {"valid": model.slippage_model_valid, "kind": model.slippage_kind.value}

def slippage_model_to_text(model: SlippageModel, limit: int = 300) -> str:
    return f"SlippageModel(valid={model.slippage_model_valid}, live_quote={model.live_quote_required})"
