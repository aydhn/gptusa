from typing import List, Dict, Any, Tuple

def trend_strategy_required_features() -> List[str]:
    return [
        "close_ema_20",
        "close_ema_50",
        "close_price_distance_to_ma_ema_20",
        "close_ma_slope_ema_20_5",
        "close_trend_strength_basic_20"
    ]

def momentum_strategy_required_features() -> List[str]:
    return [
        "close_rsi_14",
        "close_roc_12",
        "close_momentum_10"
    ]

def mean_reversion_strategy_required_features() -> List[str]:
    return [
        "close_bb_percent_b_20_2.0",
        "close_rsi_14",
        "close_price_distance_to_ma_sma_20"
    ]

def breakout_strategy_required_features() -> List[str]:
    return [
        "breakout_distance_pct_20",
        "close_normalized_atr_14",
        "close_volatility_compression_20_100"
    ]

def volume_confirmation_required_features() -> List[str]:
    return [
        "volume_relative_volume_20",
        "dollar_volume",
        "volume_trend_strength_basic_20"
    ]

def composite_rule_required_features() -> List[str]:
    features = set()
    features.update(trend_strategy_required_features())
    features.update(momentum_strategy_required_features())
    features.update(breakout_strategy_required_features())
    features.update(volume_confirmation_required_features())
    return sorted(list(features))

def validate_required_features_available(rows: List[Dict[str, Any]], required_features: List[str]) -> Tuple[bool, List[str]]:
    if not rows:
        return False, required_features

    latest = rows[-1]
    missing = [f for f in required_features if f not in latest]

    return len(missing) == 0, missing

def feature_requirement_summary_text(strategy_name: str, required_features: List[str]) -> str:
    lines = [f"Feature Requirements for {strategy_name}:"]
    for f in required_features:
        lines.append(f"  - {f}")
    return "\n".join(lines)
