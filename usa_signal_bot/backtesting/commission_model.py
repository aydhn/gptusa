from datetime import datetime, timezone
from typing import Any

from usa_signal_bot.backtesting.phase146_models import (
    CommissionModel,
    create_commission_model_id
)
from usa_signal_bot.core.enums import TransactionCostKind

def build_default_commission_model() -> CommissionModel:
    return CommissionModel(
        model_id=create_commission_model_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        cost_kind=TransactionCostKind.FLAT_PER_SHARE,
        per_share_commission=0.005,
        flat_ticket_fee=0.0,
        bps_commission=0.0,
        min_commission=1.0,
        commission_model_valid=True,
        live_broker_fee_sync_enabled=False,
        research_data_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_zero_commission_control_model() -> CommissionModel:
    return CommissionModel(
        model_id=create_commission_model_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        cost_kind=TransactionCostKind.ZERO_COST_FOR_CONTROL,
        per_share_commission=0.0,
        flat_ticket_fee=0.0,
        bps_commission=0.0,
        min_commission=0.0,
        commission_model_valid=True,
        live_broker_fee_sync_enabled=False,
        research_data_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def estimate_commission(shares: float, notional: float, model: CommissionModel) -> float:
    if model.cost_kind == TransactionCostKind.ZERO_COST_FOR_CONTROL:
        return 0.0

    cost = 0.0
    if model.per_share_commission is not None:
        cost += shares * model.per_share_commission
    if model.bps_commission is not None:
        cost += notional * (model.bps_commission / 10000.0)
    if model.flat_ticket_fee is not None:
        cost += model.flat_ticket_fee

    if model.min_commission is not None and cost < model.min_commission:
        return model.min_commission
    return cost

def validate_commission_model(model: CommissionModel) -> list[str]:
    errors = []
    if model.live_broker_fee_sync_enabled:
        errors.append("live_broker_fee_sync_enabled must be False")
    return errors

def commission_model_summary(model: CommissionModel) -> dict[str, Any]:
    return {"valid": model.commission_model_valid, "kind": model.cost_kind.value}

def commission_model_to_text(model: CommissionModel, limit: int = 300) -> str:
    return f"CommissionModel(valid={model.commission_model_valid}, live_sync={model.live_broker_fee_sync_enabled})"
