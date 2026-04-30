from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from usa_signal_bot.core.enums import FeatureComputationStatus

@dataclass
class FeatureRow:
    timestamp_utc: str
    symbol: str
    timeframe: str
    features: Dict[str, Any]

@dataclass
class FeatureComputationRequest:
    indicator_names: List[str]
    params_by_indicator: Dict[str, Dict[str, Any]]
    symbols: List[str]
    timeframes: List[str]
    provider_name: str = "yfinance"
    universe_name: Optional[str] = None

@dataclass
class FeatureComputationResult:
    request: FeatureComputationRequest
    status: FeatureComputationStatus
    feature_rows: List[FeatureRow]
    produced_features: List[str]
    symbols_processed: List[str]
    timeframes_processed: List[str]
    warnings: List[str]
    errors: List[str]
    created_at_utc: str

    def row_count(self) -> int:
        return len(self.feature_rows)

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def is_successful(self) -> bool:
        return self.status in (FeatureComputationStatus.COMPLETED, FeatureComputationStatus.PARTIAL_SUCCESS)

@dataclass
class FeatureOutputMetadata:
    output_id: str
    provider_name: str
    universe_name: Optional[str]
    symbols: List[str]
    timeframes: List[str]
    indicators: List[str]
    produced_features: List[str]
    row_count: int
    created_at_utc: str
    storage_paths: List[str]
