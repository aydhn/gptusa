from datetime import datetime, timezone
from typing import Any

from usa_signal_bot.backtesting.phase146_models import (
    TransactionCostModel,
    create_transaction_cost_model_id
)
from usa_signal_bot.core.enums import TransactionCostKind

def build_default_transaction_cost_model() -> TransactionCostModel:
    return build_flat_bps_transaction_cost_model(flat_bps=1.0)

def build_zero_cost_control_model() -> TransactionCostModel:
    return TransactionCostModel(
        model_id=create_transaction_cost_model_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        cost_kind=TransactionCostKind.ZERO_COST_FOR_CONTROL,
        flat_bps=0.0,
        flat_per_share=0.0,
        min_cost=0.0,
        max_cost=0.0,
        applies_to_buy_side=True,
        applies_to_sell_side=True,
        cost_model_valid=True,
        live_broker_fee_sync_enabled=False,
        research_data_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_flat_bps_transaction_cost_model(flat_bps: float = 1.0) -> TransactionCostModel:
    return TransactionCostModel(
        model_id=create_transaction_cost_model_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        cost_kind=TransactionCostKind.FLAT_BPS,
        flat_bps=flat_bps,
        flat_per_share=None,
        min_cost=0.0,
        max_cost=None,
        applies_to_buy_side=True,
        applies_to_sell_side=True,
        cost_model_valid=True,
        live_broker_fee_sync_enabled=False,
        research_data_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def estimate_transaction_cost_notional(notional: float, model: TransactionCostModel) -> float:
    if model.cost_kind == TransactionCostKind.ZERO_COST_FOR_CONTROL:
        return 0.0
    if model.cost_kind == TransactionCostKind.FLAT_BPS and model.flat_bps is not None:
        cost = notional * (model.flat_bps / 10000.0)
        if model.min_cost is not None and cost < model.min_cost:
            return model.min_cost
        if model.max_cost is not None and cost > model.max_cost:
            return model.max_cost
        return cost
    return 0.0

def validate_transaction_cost_model(model: TransactionCostModel) -> list[str]:
    errors = []
    if model.live_broker_fee_sync_enabled:
        errors.append("live_broker_fee_sync_enabled must be False in Phase 146.")
    return errors

def transaction_cost_model_summary(model: TransactionCostModel) -> dict[str, Any]:
    return {"valid": model.cost_model_valid, "kind": model.cost_kind.value}

def transaction_cost_model_to_text(model: TransactionCostModel, limit: int = 300) -> str:
    return f"TransactionCostModel(valid={model.cost_model_valid}, live_sync={model.live_broker_fee_sync_enabled})"
