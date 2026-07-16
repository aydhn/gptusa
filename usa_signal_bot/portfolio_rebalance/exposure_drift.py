import datetime
from typing import Any, Dict, List, Optional
from datetime import timezone

from usa_signal_bot.core.enums import DriftType
from usa_signal_bot.portfolio_rebalance.rebalance_models import (
    CurrentPortfolioState, TargetPortfolioState, DriftMeasurement, create_drift_measurement_id
)
from usa_signal_bot.portfolio_rebalance.drift_calculator import classify_drift_severity

from dataclasses import dataclass

@dataclass
class ExposureDriftParams:
    name: str
    current_value: Optional[float]
    target_value: Optional[float]
    total_equity_usd: Optional[float]
    drift_type: DriftType
    threshold: float = 3.0

def drift_for_exposure(params: ExposureDriftParams) -> DriftMeasurement:

    now_str = datetime.datetime.now(timezone.utc).isoformat()
    pct_drift = None
    abs_drift = None
    severity = classify_drift_severity(None)
    warnings = []

    if params.total_equity_usd and params.total_equity_usd > 0 and params.current_value is not None and params.target_value is not None:
        curr_pct = (params.current_value / params.total_equity_usd) * 100.0
        tgt_pct = (params.target_value / params.total_equity_usd) * 100.0
        pct_drift = tgt_pct - curr_pct
        abs_drift = abs(pct_drift)
        severity = classify_drift_severity(abs_drift, low=params.threshold/3, moderate=params.threshold, high=params.threshold*2, critical=params.threshold*3)
    else:
        warnings.append(f"Insufficient data to calculate drift percentage for {params.name}")

    return DriftMeasurement(
        drift_id=create_drift_measurement_id(params.name),
        created_at_utc=now_str,
        drift_type=params.drift_type,
        name=params.name,
        current_value=params.current_value,
        target_value=params.target_value,
        pct_drift=pct_drift,
        absolute_drift=abs_drift,
        severity=severity,
        threshold=params.threshold,
        warnings=warnings
    )

def calculate_gross_exposure_drift(current: CurrentPortfolioState, target: TargetPortfolioState, threshold: float = 3.0) -> DriftMeasurement:
    equity = current.total_equity_usd if current.total_equity_usd else target.total_equity_usd
    return drift_for_exposure(ExposureDriftParams(
        name="Gross Exposure",
        current_value=current.gross_exposure_usd,
        target_value=target.target_gross_exposure_usd,
        total_equity_usd=equity,
        drift_type=DriftType.GROSS_EXPOSURE,
        threshold=threshold
    ))

def calculate_net_exposure_drift(current: CurrentPortfolioState, target: TargetPortfolioState, threshold: float = 3.0) -> DriftMeasurement:
    equity = current.total_equity_usd if current.total_equity_usd else target.total_equity_usd
    return drift_for_exposure(ExposureDriftParams(
        name="Net Exposure",
        current_value=current.net_exposure_usd,
        target_value=target.target_net_exposure_usd,
        total_equity_usd=equity,
        drift_type=DriftType.NET_EXPOSURE,
        threshold=threshold
    ))

def calculate_long_short_exposure_drift(current: CurrentPortfolioState, target: TargetPortfolioState, threshold: float = 3.0) -> List[DriftMeasurement]:
    equity = current.total_equity_usd if current.total_equity_usd else target.total_equity_usd

    current_long = sum(p.market_value_usd for p in current.positions if p.side == "LONG" or p.side is None)
    current_short = sum(p.market_value_usd for p in current.positions if p.side == "SHORT")

    target_long = sum(p.market_value_usd for p in target.target_positions if p.side == "LONG" or p.side is None)
    target_short = sum(p.market_value_usd for p in target.target_positions if p.side == "SHORT")

    return [
        drift_for_exposure(ExposureDriftParams("Long Exposure", current_long, target_long, equity, DriftType.LONG_EXPOSURE, threshold)),
        drift_for_exposure(ExposureDriftParams("Short Exposure", current_short, target_short, equity, DriftType.SHORT_EXPOSURE, threshold))
    ]

def calculate_exposure_drift(current: CurrentPortfolioState, target: TargetPortfolioState, threshold: float = 3.0) -> List[DriftMeasurement]:
    measurements = []
    measurements.append(calculate_gross_exposure_drift(current, target, threshold))
    measurements.append(calculate_net_exposure_drift(current, target, threshold))
    measurements.extend(calculate_long_short_exposure_drift(current, target, threshold))
    return measurements

def exposure_drift_to_text(measurements: List[DriftMeasurement]) -> str:
    from usa_signal_bot.portfolio_rebalance.drift_calculator import drift_measurements_to_text
    return drift_measurements_to_text(measurements)
