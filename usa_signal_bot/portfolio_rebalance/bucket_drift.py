from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import DriftType
from usa_signal_bot.portfolio_rebalance.rebalance_models import (
    CurrentPortfolioState, TargetPortfolioState, DriftMeasurement
)
from usa_signal_bot.portfolio_rebalance.exposure_drift import drift_for_exposure, ExposureDriftParams

def group_state_by_bucket(state: CurrentPortfolioState | TargetPortfolioState, bucket: DriftType) -> Dict[str, float]:
    positions = state.positions if isinstance(state, CurrentPortfolioState) else state.target_positions
    result = {}
    for pos in positions:
        key = "UNKNOWN"
        if bucket == DriftType.SECTOR_WEIGHT:
            key = pos.sector or "UNKNOWN"
        elif bucket == DriftType.CLUSTER_WEIGHT:
            key = pos.cluster or "UNKNOWN"
        elif bucket == DriftType.STRATEGY_WEIGHT:
            key = pos.strategy_name or "UNKNOWN"
        elif bucket == DriftType.REGIME_WEIGHT:
            key = pos.regime_label or "UNKNOWN"
        elif bucket == DriftType.LIQUIDITY_BUCKET_WEIGHT:
            key = pos.liquidity_bucket or "UNKNOWN"
        elif bucket == DriftType.COST_BUCKET_WEIGHT:
            key = pos.cost_bucket or "UNKNOWN"

        result[key] = result.get(key, 0.0) + pos.market_value_usd
    return result

def calculate_bucket_drift(
    current: CurrentPortfolioState,
    target: TargetPortfolioState,
    bucket: DriftType,
    threshold_pct: float = 3.0
) -> List[DriftMeasurement]:

    current_buckets = group_state_by_bucket(current, bucket)
    target_buckets = group_state_by_bucket(target, bucket)

    all_keys = set(current_buckets.keys()).union(set(target_buckets.keys()))
    equity = current.total_equity_usd if current.total_equity_usd else target.total_equity_usd

    measurements = []
    for key in sorted(all_keys):
        curr_val = current_buckets.get(key, 0.0)
        tgt_val = target_buckets.get(key, 0.0)

        name = f"{bucket.value}_{key}"
        measurement = drift_for_exposure(ExposureDriftParams(name, curr_val, tgt_val, equity, bucket, threshold_pct))

        # Add warnings for high drift
        if measurement.absolute_drift is not None and measurement.absolute_drift > (threshold_pct * 2):
            if bucket in [DriftType.SECTOR_WEIGHT, DriftType.CLUSTER_WEIGHT]:
                measurement.warnings.append(f"Significant {bucket.value} drift detected for {key}.")
            if bucket == DriftType.COST_BUCKET_WEIGHT and measurement.pct_drift is not None and measurement.pct_drift > 0:
                if key in ["HIGH", "VERY_HIGH", "CRITICAL"]:
                    measurement.warnings.append(f"Target is significantly increasing exposure to high cost bucket: {key}.")

        measurements.append(measurement)

    return measurements

def calculate_sector_cluster_drift(current: CurrentPortfolioState, target: TargetPortfolioState) -> List[DriftMeasurement]:
    drifts = calculate_bucket_drift(current, target, DriftType.SECTOR_WEIGHT)
    drifts.extend(calculate_bucket_drift(current, target, DriftType.CLUSTER_WEIGHT))
    return drifts

def calculate_strategy_regime_drift(current: CurrentPortfolioState, target: TargetPortfolioState) -> List[DriftMeasurement]:
    drifts = calculate_bucket_drift(current, target, DriftType.STRATEGY_WEIGHT)
    drifts.extend(calculate_bucket_drift(current, target, DriftType.REGIME_WEIGHT))
    return drifts

def calculate_liquidity_cost_bucket_drift(current: CurrentPortfolioState, target: TargetPortfolioState) -> List[DriftMeasurement]:
    drifts = calculate_bucket_drift(current, target, DriftType.LIQUIDITY_BUCKET_WEIGHT)
    drifts.extend(calculate_bucket_drift(current, target, DriftType.COST_BUCKET_WEIGHT))
    return drifts

def bucket_drift_to_text(measurements: List[DriftMeasurement], limit: int = 100) -> str:
    from usa_signal_bot.portfolio_rebalance.drift_calculator import drift_measurements_to_text
    return drift_measurements_to_text(measurements, limit)
