import datetime
from typing import Any, Dict, List, Optional
from datetime import timezone

from usa_signal_bot.core.enums import DriftType, DriftSeverity
from usa_signal_bot.portfolio_rebalance.rebalance_models import (
    CurrentPortfolioState, TargetPortfolioState, PortfolioPosition, DriftMeasurement,
    create_drift_measurement_id
)

def classify_drift_severity(
    abs_drift_pct: Optional[float],
    low: float = 1.0,
    moderate: float = 3.0,
    high: float = 5.0,
    critical: float = 10.0
) -> DriftSeverity:
    if abs_drift_pct is None:
        return DriftSeverity.INSUFFICIENT_DATA
    if abs_drift_pct < low:
        return DriftSeverity.NONE
    if abs_drift_pct < moderate:
        return DriftSeverity.LOW
    if abs_drift_pct < high:
        return DriftSeverity.MODERATE
    if abs_drift_pct < critical:
        return DriftSeverity.HIGH
    return DriftSeverity.CRITICAL

def calculate_position_weight_drift(
    current_position: Optional[PortfolioPosition],
    target_position: Optional[PortfolioPosition],
    total_equity_usd: Optional[float],
    threshold_pct: float = 1.0
) -> DriftMeasurement:

    symbol = current_position.symbol if current_position else target_position.symbol
    now_str = datetime.datetime.now(timezone.utc).isoformat()

    current_val = current_position.market_value_usd if current_position else 0.0
    target_val = target_position.market_value_usd if target_position else 0.0

    warnings = []
    pct_drift = None
    abs_drift = None
    severity = DriftSeverity.INSUFFICIENT_DATA

    if total_equity_usd and total_equity_usd > 0:
        current_weight = (current_val / total_equity_usd) * 100.0
        target_weight = (target_val / total_equity_usd) * 100.0

        pct_drift = target_weight - current_weight
        abs_drift = abs(pct_drift)
        severity = classify_drift_severity(abs_drift)
    else:
        warnings.append("Missing total_equity_usd, cannot calculate weight drift percentages.")

    return DriftMeasurement(
        drift_id=create_drift_measurement_id(symbol),
        created_at_utc=now_str,
        drift_type=DriftType.SYMBOL_WEIGHT,
        name=symbol,
        current_value=current_val,
        target_value=target_val,
        absolute_drift=abs_drift,
        pct_drift=pct_drift,
        severity=severity,
        threshold=threshold_pct,
        warnings=warnings
    )

def calculate_symbol_drift(
    current: CurrentPortfolioState,
    target: TargetPortfolioState,
    threshold_pct: float = 1.0
) -> List[DriftMeasurement]:

    current_map = {p.symbol: p for p in current.positions if p.symbol}
    target_map = {p.symbol: p for p in target.target_positions if p.symbol}

    all_symbols = set(current_map.keys()).union(set(target_map.keys()))
    measurements = []

    # We prefer the current equity for calculating current drift if available
    equity = current.total_equity_usd if current.total_equity_usd else target.total_equity_usd

    for symbol in sorted(all_symbols):
        curr_pos = current_map.get(symbol)
        tgt_pos = target_map.get(symbol)

        measurement = calculate_position_weight_drift(curr_pos, tgt_pos, equity, threshold_pct)
        measurements.append(measurement)

    return measurements

def aggregate_drift_score(measurements: List[DriftMeasurement]) -> Optional[float]:
    valid_drifts = [m.absolute_drift for m in measurements if m.absolute_drift is not None]
    if not valid_drifts:
        return None
    return sum(valid_drifts) / len(valid_drifts)

def drift_measurements_to_text(measurements: List[DriftMeasurement], limit: int = 100) -> str:
    lines = [f"Drift Measurements ({len(measurements)}):"]
    for idx, m in enumerate(measurements[:limit]):
        current = f"${m.current_value:.2f}" if m.current_value is not None else "N/A"
        target = f"${m.target_value:.2f}" if m.target_value is not None else "N/A"
        pct = f"{m.pct_drift:.2f}%" if m.pct_drift is not None else "N/A"
        lines.append(f"  - {m.name} ({m.drift_type.value}): Current {current} -> Target {target} | Drift: {pct} [{m.severity.value}]")

    if len(measurements) > limit:
        lines.append(f"  ... and {len(measurements) - limit} more.")

    return "\n".join(lines)
