import math
from dataclasses import dataclass

from usa_signal_bot.core.enums import PositionSizingMethod
from usa_signal_bot.core.exceptions import PositionSizingError
from usa_signal_bot.risk.risk_models import PositionSizingRequest, PositionSizingResult

@dataclass
class PositionSizingConfig:
    method: PositionSizingMethod
    fixed_notional: float
    fixed_fraction_pct: float
    risk_per_trade_pct: float
    atr_multiplier: float
    volatility_target_pct: float
    min_notional: float
    max_notional: float
    allow_fractional_quantity: bool

def default_position_sizing_config() -> PositionSizingConfig:
    return PositionSizingConfig(
        method=PositionSizingMethod.FIXED_NOTIONAL,
        fixed_notional=5000.0,
        fixed_fraction_pct=0.05,
        risk_per_trade_pct=0.01,
        atr_multiplier=2.0,
        volatility_target_pct=0.02,
        min_notional=0.0,
        max_notional=10000.0,
        allow_fractional_quantity=True
    )

def validate_position_sizing_config(config: PositionSizingConfig) -> None:
    if config.fixed_notional < 0:
        raise PositionSizingError("fixed_notional cannot be negative")
    if not (0 <= config.fixed_fraction_pct <= 1):
        raise PositionSizingError("fixed_fraction_pct must be between 0 and 1")
    if not (0 <= config.risk_per_trade_pct <= 1):
        raise PositionSizingError("risk_per_trade_pct must be between 0 and 1")
    if config.atr_multiplier <= 0:
        raise PositionSizingError("atr_multiplier must be positive")
    if config.volatility_target_pct <= 0:
        raise PositionSizingError("volatility_target_pct must be positive")
    if config.min_notional < 0:
        raise PositionSizingError("min_notional cannot be negative")
    if config.max_notional <= 0 or config.min_notional > config.max_notional:
        raise PositionSizingError("Invalid max_notional configuration")

def notional_to_quantity(notional: float, price: float, allow_fractional: bool = True) -> float:
    qty = notional / price
    if not allow_fractional:
        qty = math.floor(qty)
    return max(0.0, qty)

def apply_size_caps(raw_notional: float, request: PositionSizingRequest, config: PositionSizingConfig) -> tuple[float, list[str]]:
    cap_reasons = []
    capped_notional = raw_notional

    if capped_notional > config.max_notional:
        capped_notional = config.max_notional
        cap_reasons.append(f"Capped to max_notional: {config.max_notional}")

    if capped_notional > request.available_cash:
        capped_notional = request.available_cash
        cap_reasons.append(f"Capped to available_cash: {request.available_cash}")

    if capped_notional < config.min_notional:
        capped_notional = 0.0
        cap_reasons.append(f"Below min_notional: {config.min_notional}, set to 0")

    return capped_notional, cap_reasons

def calculate_fixed_notional_size(request: PositionSizingRequest, config: PositionSizingConfig) -> PositionSizingResult:
    raw_notional = config.fixed_notional
    capped_notional, cap_reasons = apply_size_caps(raw_notional, request, config)
    qty = notional_to_quantity(capped_notional, request.price, config.allow_fractional_quantity)
    actual_notional = qty * request.price

    return PositionSizingResult(
        candidate_id=request.candidate_id,
        method=PositionSizingMethod.FIXED_NOTIONAL,
        approved_quantity=qty,
        approved_notional=actual_notional,
        raw_quantity=raw_notional / request.price,
        raw_notional=raw_notional,
        capped=len(cap_reasons) > 0,
        cap_reasons=cap_reasons,
        warnings=[],
        errors=[]
    )

def calculate_fixed_fractional_size(request: PositionSizingRequest, config: PositionSizingConfig) -> PositionSizingResult:
    raw_notional = request.portfolio_equity * config.fixed_fraction_pct
    capped_notional, cap_reasons = apply_size_caps(raw_notional, request, config)
    qty = notional_to_quantity(capped_notional, request.price, config.allow_fractional_quantity)
    actual_notional = qty * request.price

    return PositionSizingResult(
        candidate_id=request.candidate_id,
        method=PositionSizingMethod.FIXED_FRACTIONAL,
        approved_quantity=qty,
        approved_notional=actual_notional,
        raw_quantity=raw_notional / request.price,
        raw_notional=raw_notional,
        capped=len(cap_reasons) > 0,
        cap_reasons=cap_reasons,
        warnings=[],
        errors=[]
    )

def calculate_volatility_adjusted_size(request: PositionSizingRequest, config: PositionSizingConfig) -> PositionSizingResult:
    if request.volatility_value is None or request.volatility_value <= 0:
        res = calculate_fixed_notional_size(request, config)
        res.warnings.append("Missing or invalid volatility_value, fallback to FIXED_NOTIONAL")
        res.method = PositionSizingMethod.VOLATILITY_ADJUSTED
        return res

    raw_notional = request.portfolio_equity * (config.volatility_target_pct / request.volatility_value)
    capped_notional, cap_reasons = apply_size_caps(raw_notional, request, config)
    qty = notional_to_quantity(capped_notional, request.price, config.allow_fractional_quantity)
    actual_notional = qty * request.price

    return PositionSizingResult(
        candidate_id=request.candidate_id,
        method=PositionSizingMethod.VOLATILITY_ADJUSTED,
        approved_quantity=qty,
        approved_notional=actual_notional,
        raw_quantity=raw_notional / request.price,
        raw_notional=raw_notional,
        capped=len(cap_reasons) > 0,
        cap_reasons=cap_reasons,
        warnings=[],
        errors=[]
    )

def calculate_atr_risk_size(request: PositionSizingRequest, config: PositionSizingConfig) -> PositionSizingResult:
    if request.atr_value is None or request.atr_value <= 0:
        return calculate_zero_size(request, "Missing or invalid atr_value for ATR_RISK sizing")

    risk_amount = request.portfolio_equity * config.risk_per_trade_pct
    risk_per_share = request.atr_value * config.atr_multiplier

    if risk_per_share <= 0:
         return calculate_zero_size(request, "Calculated risk_per_share is 0")

    raw_quantity = risk_amount / risk_per_share
    raw_notional = raw_quantity * request.price

    capped_notional, cap_reasons = apply_size_caps(raw_notional, request, config)
    qty = notional_to_quantity(capped_notional, request.price, config.allow_fractional_quantity)
    actual_notional = qty * request.price

    return PositionSizingResult(
        candidate_id=request.candidate_id,
        method=PositionSizingMethod.ATR_RISK,
        approved_quantity=qty,
        approved_notional=actual_notional,
        raw_quantity=raw_quantity,
        raw_notional=raw_notional,
        capped=len(cap_reasons) > 0,
        cap_reasons=cap_reasons,
        warnings=[],
        errors=[]
    )

def calculate_equal_weight_size(request: PositionSizingRequest, target_positions: int, config: PositionSizingConfig) -> PositionSizingResult:
    if target_positions <= 0:
        return calculate_zero_size(request, "target_positions must be > 0 for EQUAL_WEIGHT")

    raw_notional = request.portfolio_equity / target_positions
    capped_notional, cap_reasons = apply_size_caps(raw_notional, request, config)
    qty = notional_to_quantity(capped_notional, request.price, config.allow_fractional_quantity)
    actual_notional = qty * request.price

    return PositionSizingResult(
        candidate_id=request.candidate_id,
        method=PositionSizingMethod.EQUAL_WEIGHT,
        approved_quantity=qty,
        approved_notional=actual_notional,
        raw_quantity=raw_notional / request.price,
        raw_notional=raw_notional,
        capped=len(cap_reasons) > 0,
        cap_reasons=cap_reasons,
        warnings=[],
        errors=[]
    )

def calculate_zero_size(request: PositionSizingRequest, reason: str) -> PositionSizingResult:
    return PositionSizingResult(
        candidate_id=request.candidate_id,
        method=PositionSizingMethod.ZERO_SIZE,
        approved_quantity=0.0,
        approved_notional=0.0,
        raw_quantity=0.0,
        raw_notional=0.0,
        capped=True,
        cap_reasons=[reason],
        warnings=[],
        errors=[]
    )

def calculate_position_size(request: PositionSizingRequest, config: PositionSizingConfig | None = None) -> PositionSizingResult:
    cfg = config or default_position_sizing_config()

    if request.price <= 0:
        return calculate_zero_size(request, f"Invalid price: {request.price}")

    if cfg.method == PositionSizingMethod.FIXED_NOTIONAL:
        return calculate_fixed_notional_size(request, cfg)
    elif cfg.method == PositionSizingMethod.FIXED_FRACTIONAL:
        return calculate_fixed_fractional_size(request, cfg)
    elif cfg.method == PositionSizingMethod.VOLATILITY_ADJUSTED:
        return calculate_volatility_adjusted_size(request, cfg)
    elif cfg.method == PositionSizingMethod.ATR_RISK:
        return calculate_atr_risk_size(request, cfg)
    elif cfg.method == PositionSizingMethod.EQUAL_WEIGHT:
        return calculate_equal_weight_size(request, 10, cfg)
    else:
        return calculate_zero_size(request, f"Unsupported sizing method: {cfg.method}")
