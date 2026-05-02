from dataclasses import dataclass
from typing import Optional, Any
from ..core.domain import BaseDomainModel
from ..core.model_validation import ensure_non_empty_string

@dataclass
class FeatureValue(BaseDomainModel):
    symbol: str = ""
    timestamp_utc: str = ""
    timeframe: str = ""
    feature_name: str = ""
    value: float | int | str | bool | None = None
    source: Optional[str] = None

@dataclass
class FeatureRow(BaseDomainModel):
    symbol: str = ""
    timestamp_utc: str = ""
    timeframe: str = ""
    values: dict[str, float | int | str | bool | None] = None

    def __post_init__(self):
        if self.values is None:
            self.values = {}

@dataclass
class FeatureSetMetadata(BaseDomainModel):
    name: str = ""
    symbols: list[str] = None
    timeframe: str = ""
    feature_names: list[str] = None
    row_count: int = 0
    created_at_utc: str = ""

    def __post_init__(self):
        if self.symbols is None:
            self.symbols = []
        if self.feature_names is None:
            self.feature_names = []
        self.validate()

    def validate(self) -> None:
        super().validate()
        ensure_non_empty_string(self.name, "name")

@dataclass
class IndicatorSet(BaseDomainModel):
    name: str = ""
    description: str = ""
    indicators: list[str] = None
    params_by_indicator: dict[str, dict[str, Any]] = None

    def __post_init__(self):
        if self.indicators is None:
            self.indicators = []
        if self.params_by_indicator is None:
            self.params_by_indicator = {}
