from dataclasses import dataclass, field
from typing import Optional
from usa_signal_bot.core.enums import TransactionCostModelType
from usa_signal_bot.core.exceptions import TransactionCostError

@dataclass
class TransactionCostConfig:
    model_type: TransactionCostModelType
    flat_fee: float = 0.0
    fee_bps: float = 0.0
    per_share_fee: float = 0.0
    min_fee: float = 0.0
    max_fee: Optional[float] = None

@dataclass
class TransactionCostBreakdown:
    model_type: TransactionCostModelType
    notional: float
    quantity: float
    flat_fee_component: float
    bps_fee_component: float
    per_share_fee_component: float
    total_fee: float
    effective_fee_bps: float
    warnings: list[str] = field(default_factory=list)

def default_transaction_cost_config() -> TransactionCostConfig:
    return TransactionCostConfig(
        model_type=TransactionCostModelType.BPS,
        fee_bps=1.0
    )

def validate_transaction_cost_config(config: TransactionCostConfig) -> None:
    if config.flat_fee < 0 or config.fee_bps < 0 or config.per_share_fee < 0 or config.min_fee < 0:
        raise TransactionCostError("Fee values cannot be negative")
    if config.max_fee is not None and config.max_fee < config.min_fee:
        raise TransactionCostError("max_fee must be greater than or equal to min_fee")

def apply_min_max_fee(fee: float, config: TransactionCostConfig) -> float:
    fee = max(fee, config.min_fee)
    if config.max_fee is not None:
        fee = min(fee, config.max_fee)
    return fee

def calculate_transaction_cost(notional: float, quantity: float, config: Optional[TransactionCostConfig] = None) -> TransactionCostBreakdown:
    if notional < 0:
        raise TransactionCostError("notional cannot be negative")
    if quantity < 0:
        raise TransactionCostError("quantity cannot be negative")

    config = config or default_transaction_cost_config()
    validate_transaction_cost_config(config)

    warnings = []
    flat_fee = 0.0
    bps_fee = 0.0
    per_share_fee = 0.0

    if config.model_type == TransactionCostModelType.NONE:
        pass
    elif config.model_type == TransactionCostModelType.FLAT_FEE:
        flat_fee = config.flat_fee
    elif config.model_type == TransactionCostModelType.BPS:
        bps_fee = notional * config.fee_bps / 10000.0
    elif config.model_type == TransactionCostModelType.PER_SHARE:
        per_share_fee = quantity * config.per_share_fee
    elif config.model_type == TransactionCostModelType.COMBINED:
        flat_fee = config.flat_fee
        bps_fee = notional * config.fee_bps / 10000.0
        per_share_fee = quantity * config.per_share_fee
    else:
        warnings.append(f"Unknown transaction cost model type: {config.model_type}, assuming NONE.")

    total_fee = flat_fee + bps_fee + per_share_fee

    if config.model_type != TransactionCostModelType.NONE:
        total_fee = apply_min_max_fee(total_fee, config)

    effective_fee_bps = (total_fee / notional * 10000.0) if notional > 0 else 0.0

    return TransactionCostBreakdown(
        model_type=config.model_type,
        notional=notional,
        quantity=quantity,
        flat_fee_component=flat_fee,
        bps_fee_component=bps_fee,
        per_share_fee_component=per_share_fee,
        total_fee=total_fee,
        effective_fee_bps=effective_fee_bps,
        warnings=warnings
    )

def transaction_cost_breakdown_to_dict(breakdown: TransactionCostBreakdown) -> dict:
    return {
        "model_type": breakdown.model_type.value if isinstance(breakdown.model_type, TransactionCostModelType) else str(breakdown.model_type),
        "notional": breakdown.notional,
        "quantity": breakdown.quantity,
        "flat_fee_component": breakdown.flat_fee_component,
        "bps_fee_component": breakdown.bps_fee_component,
        "per_share_fee_component": breakdown.per_share_fee_component,
        "total_fee": breakdown.total_fee,
        "effective_fee_bps": breakdown.effective_fee_bps,
        "warnings": breakdown.warnings
    }

def transaction_cost_breakdown_to_text(breakdown: TransactionCostBreakdown) -> str:
    lines = [
        f"Transaction Cost Breakdown ({breakdown.model_type.value if hasattr(breakdown.model_type, 'value') else breakdown.model_type})",
        f"  Total Fee: {breakdown.total_fee:.4f}",
        f"  Effective BPS: {breakdown.effective_fee_bps:.2f}"
    ]
    if breakdown.warnings:
        lines.append("  Warnings:")
        for w in breakdown.warnings:
            lines.append(f"    - {w}")
    return "\n".join(lines)
