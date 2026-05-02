from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import (
    DivergenceType,
    DivergenceSource,
    PivotType,
    DivergenceConfirmationMode,
    DivergenceStrength
)

@dataclass
class PivotPoint:
    index: int
    value: float
    pivot_type: PivotType
    timestamp_utc: Optional[str] = None
    symbol: Optional[str] = None
    timeframe: Optional[str] = None

    def __post_init__(self):
        if self.index < 0:
            raise ValueError("index cannot be negative")
        if not isinstance(self.value, (int, float)):
            raise TypeError("value must be numeric")
        if not isinstance(self.pivot_type, PivotType):
            raise TypeError("pivot_type must be a valid PivotType enum")

@dataclass
class DivergencePair:
    price_pivot_1: PivotPoint
    price_pivot_2: PivotPoint
    osc_pivot_1: PivotPoint
    osc_pivot_2: PivotPoint
    divergence_type: DivergenceType
    source: DivergenceSource
    strength_score: float
    confirmation_mode: DivergenceConfirmationMode
    details: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not (0 <= self.strength_score <= 100):
            raise ValueError("strength_score must be between 0 and 100")
        if not isinstance(self.divergence_type, DivergenceType):
            raise TypeError("divergence_type must be a valid DivergenceType enum")
        if self.price_pivot_1.index >= self.price_pivot_2.index:
            raise ValueError("price_pivot_1 must occur before price_pivot_2")
        if self.osc_pivot_1.index >= self.osc_pivot_2.index:
            raise ValueError("osc_pivot_1 must occur before osc_pivot_2")

@dataclass
class DivergenceDetectionConfig:
    source: DivergenceSource
    price_column: str
    oscillator_column: str
    left_window: int
    right_window: int
    max_pivot_distance: int
    min_price_change_pct: float
    min_osc_change_pct: float
    confirmation_mode: DivergenceConfirmationMode

@dataclass
class DivergenceDetectionResult:
    symbol: str
    timeframe: str
    source: DivergenceSource
    created_at_utc: str
    pairs: List[DivergencePair]
    latest_divergence_type: DivergenceType
    latest_strength_score: float
    feature_columns: List[str]
    warnings: List[str]
    errors: List[str]

def pivot_point_to_dict(pivot: PivotPoint) -> Dict[str, Any]:
    return {
        "index": pivot.index,
        "timestamp_utc": pivot.timestamp_utc,
        "value": pivot.value,
        "pivot_type": pivot.pivot_type.value if pivot.pivot_type else None,
        "symbol": pivot.symbol,
        "timeframe": pivot.timeframe
    }

def divergence_pair_to_dict(pair: DivergencePair) -> Dict[str, Any]:
    return {
        "price_pivot_1": pivot_point_to_dict(pair.price_pivot_1),
        "price_pivot_2": pivot_point_to_dict(pair.price_pivot_2),
        "osc_pivot_1": pivot_point_to_dict(pair.osc_pivot_1),
        "osc_pivot_2": pivot_point_to_dict(pair.osc_pivot_2),
        "divergence_type": pair.divergence_type.value if pair.divergence_type else None,
        "source": pair.source.value if pair.source else None,
        "strength_score": pair.strength_score,
        "confirmation_mode": pair.confirmation_mode.value if pair.confirmation_mode else None,
        "details": pair.details
    }

def divergence_detection_result_to_dict(result: DivergenceDetectionResult) -> Dict[str, Any]:
    return {
        "symbol": result.symbol,
        "timeframe": result.timeframe,
        "source": result.source.value if result.source else None,
        "created_at_utc": result.created_at_utc,
        "pairs": [divergence_pair_to_dict(p) for p in result.pairs],
        "latest_divergence_type": result.latest_divergence_type.value if result.latest_divergence_type else None,
        "latest_strength_score": result.latest_strength_score,
        "feature_columns": result.feature_columns,
        "warnings": result.warnings,
        "errors": result.errors
    }

def validate_divergence_config(config: DivergenceDetectionConfig) -> None:
    if config.left_window <= 0:
        raise ValueError("left_window must be positive")
    if config.right_window < 0:
        raise ValueError("right_window cannot be negative")
    if config.max_pivot_distance < 0:
        raise ValueError("max_pivot_distance cannot be negative")
