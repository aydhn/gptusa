from dataclasses import dataclass, field
from typing import Optional, Tuple
from usa_signal_bot.core.enums import SlippageModelType, LiquidityBucket, BacktestOrderSide
from usa_signal_bot.core.exceptions import SlippageModelError
from usa_signal_bot.data.models import OHLCVBar

@dataclass
class SlippageConfig:
    model_type: SlippageModelType
    fixed_bps: float = 0.0
    spread_bps: float = 0.0
    volume_participation_rate: float = 0.01
    volume_impact_factor: float = 10.0
    volatility_multiplier: float = 1.0
    max_slippage_bps: float = 100.0

@dataclass
class SlippageBreakdown:
    model_type: SlippageModelType
    base_price: float
    adjusted_price: float
    side: BacktestOrderSide
    slippage_bps: float
    slippage_amount_per_share: float
    total_slippage_cost: float
    liquidity_bucket: LiquidityBucket
    warnings: list[str] = field(default_factory=list)

def default_slippage_config() -> SlippageConfig:
    return SlippageConfig(
        model_type=SlippageModelType.FIXED_BPS,
        fixed_bps=2.0
    )

def validate_slippage_config(config: SlippageConfig) -> None:
    if config.fixed_bps < 0 or config.spread_bps < 0:
        raise SlippageModelError("fixed_bps and spread_bps cannot be negative")
    if not (0.0 <= config.volume_participation_rate <= 1.0):
        raise SlippageModelError("volume_participation_rate must be between 0.0 and 1.0")
    if config.volume_impact_factor < 0:
        raise SlippageModelError("volume_impact_factor cannot be negative")
    if config.max_slippage_bps <= 0:
        raise SlippageModelError("max_slippage_bps must be positive")

def estimate_liquidity_bucket(bar: OHLCVBar, dollar_volume: Optional[float] = None) -> LiquidityBucket:
    dv = dollar_volume if dollar_volume is not None else (bar.close * bar.volume)
    if dv >= 50_000_000:
        return LiquidityBucket.VERY_LIQUID
    elif dv >= 10_000_000:
        return LiquidityBucket.LIQUID
    elif dv >= 1_000_000:
        return LiquidityBucket.NORMAL
    elif dv >= 100_000:
        return LiquidityBucket.ILLIQUID
    else:
        return LiquidityBucket.VERY_ILLIQUID

def calculate_fixed_bps_slippage(price: float, side: BacktestOrderSide, fixed_bps: float) -> Tuple[float, float]:
    slippage_amount = price * fixed_bps / 10000.0
    adjusted_price = price + slippage_amount if side == BacktestOrderSide.BUY else price - slippage_amount
    return adjusted_price, fixed_bps

def calculate_spread_proxy_slippage(price: float, side: BacktestOrderSide, spread_bps: float) -> Tuple[float, float]:
    # Assume half the spread is paid as slippage
    slippage_bps = spread_bps / 2.0
    return calculate_fixed_bps_slippage(price, side, slippage_bps)

def calculate_volume_participation_slippage(price: float, quantity: float, bar_volume: float, side: BacktestOrderSide, config: SlippageConfig) -> Tuple[float, float]:
    if bar_volume <= 0:
        return calculate_fixed_bps_slippage(price, side, config.max_slippage_bps)

    participation_ratio = quantity / bar_volume
    if participation_ratio <= config.volume_participation_rate:
        # Expected participation, nominal slippage
        slippage_bps = 1.0
    else:
        # High participation, exponential penalty
        excess_ratio = participation_ratio - config.volume_participation_rate
        slippage_bps = 1.0 + (excess_ratio * config.volume_impact_factor * 10000.0)

    return calculate_fixed_bps_slippage(price, side, slippage_bps)

def calculate_volatility_adjusted_slippage(price: float, bar: OHLCVBar, side: BacktestOrderSide, config: SlippageConfig) -> Tuple[float, float]:
    if bar.low > 0 and bar.high >= bar.low:
        volatility_proxy = (bar.high - bar.low) / bar.low
    else:
        volatility_proxy = 0.0

    base_slippage_bps = 2.0
    slippage_bps = base_slippage_bps + (volatility_proxy * 10000.0 * config.volatility_multiplier)

    return calculate_fixed_bps_slippage(price, side, slippage_bps)

def cap_slippage_bps(slippage_bps: float, max_slippage_bps: float) -> float:
    return min(slippage_bps, max_slippage_bps)

def calculate_slippage(price: float, quantity: float, side: BacktestOrderSide, bar: OHLCVBar, config: Optional[SlippageConfig] = None) -> SlippageBreakdown:
    if price <= 0:
        raise SlippageModelError("price must be positive")
    if quantity < 0:
        raise SlippageModelError("quantity cannot be negative")

    config = config or default_slippage_config()
    validate_slippage_config(config)

    warnings = []
    adjusted_price = price
    slippage_bps = 0.0

    if config.model_type == SlippageModelType.NONE:
        pass
    elif config.model_type == SlippageModelType.FIXED_BPS:
        adjusted_price, slippage_bps = calculate_fixed_bps_slippage(price, side, config.fixed_bps)
    elif config.model_type == SlippageModelType.SPREAD_PROXY:
        adjusted_price, slippage_bps = calculate_spread_proxy_slippage(price, side, config.spread_bps)
    elif config.model_type == SlippageModelType.VOLUME_PARTICIPATION:
        if bar.volume <= 0:
            warnings.append("Bar volume is zero or negative. Applying max slippage.")
        adjusted_price, slippage_bps = calculate_volume_participation_slippage(price, quantity, bar.volume, side, config)
    elif config.model_type == SlippageModelType.VOLATILITY_ADJUSTED:
        adjusted_price, slippage_bps = calculate_volatility_adjusted_slippage(price, bar, side, config)
    else:
        warnings.append(f"Unknown slippage model type: {config.model_type}, assuming NONE.")

    if slippage_bps > config.max_slippage_bps:
        slippage_bps = config.max_slippage_bps
        adjusted_price, _ = calculate_fixed_bps_slippage(price, side, slippage_bps)

    # Ensure adjusted price doesn't go below 0 for SELL
    if side == BacktestOrderSide.SELL and adjusted_price < 0:
        adjusted_price = 0.0
        slippage_amount_per_share = price
        slippage_bps = 10000.0
    else:
        slippage_amount_per_share = abs(adjusted_price - price)

    total_slippage_cost = slippage_amount_per_share * quantity
    liquidity_bucket = estimate_liquidity_bucket(bar)

    return SlippageBreakdown(
        model_type=config.model_type,
        base_price=price,
        adjusted_price=adjusted_price,
        side=side,
        slippage_bps=slippage_bps,
        slippage_amount_per_share=slippage_amount_per_share,
        total_slippage_cost=total_slippage_cost,
        liquidity_bucket=liquidity_bucket,
        warnings=warnings
    )

def slippage_breakdown_to_dict(breakdown: SlippageBreakdown) -> dict:
    return {
        "model_type": breakdown.model_type.value if hasattr(breakdown.model_type, 'value') else breakdown.model_type,
        "base_price": breakdown.base_price,
        "adjusted_price": breakdown.adjusted_price,
        "side": breakdown.side.value if hasattr(breakdown.side, 'value') else breakdown.side,
        "slippage_bps": breakdown.slippage_bps,
        "slippage_amount_per_share": breakdown.slippage_amount_per_share,
        "total_slippage_cost": breakdown.total_slippage_cost,
        "liquidity_bucket": breakdown.liquidity_bucket.value if hasattr(breakdown.liquidity_bucket, 'value') else breakdown.liquidity_bucket,
        "warnings": breakdown.warnings
    }

def slippage_breakdown_to_text(breakdown: SlippageBreakdown) -> str:
    lines = [
        f"Slippage Breakdown ({breakdown.model_type.value if hasattr(breakdown.model_type, 'value') else breakdown.model_type})",
        f"  Base Price: {breakdown.base_price:.4f} -> Adjusted Price: {breakdown.adjusted_price:.4f}",
        f"  Slippage BPS: {breakdown.slippage_bps:.2f}",
        f"  Total Slippage Cost: {breakdown.total_slippage_cost:.4f}",
        f"  Liquidity: {breakdown.liquidity_bucket.value if hasattr(breakdown.liquidity_bucket, 'value') else breakdown.liquidity_bucket}"
    ]
    if breakdown.warnings:
        lines.append("  Warnings:")
        for w in breakdown.warnings:
            lines.append(f"    - {w}")
    return "\n".join(lines)
