from dataclasses import dataclass, field
from typing import Optional
from ..core.domain import BaseDomainModel
from ..core.enums import TimeFrame, DataQualityStatus
from ..core.model_validation import (
    ensure_non_empty_string, ensure_non_negative_number,
    validate_ohlcv_prices, ensure_list
)

@dataclass
class OHLCVBar(BaseDomainModel):
    symbol: str = ""
    timestamp_utc: str = ""
    timeframe: TimeFrame | str = ""
    open: float = 0.0
    high: float = 0.0
    low: float = 0.0
    close: float = 0.0
    volume: float = 0.0
    adjusted_close: Optional[float] = None
    source: Optional[str] = None

    def __post_init__(self):
        self.validate()

    def validate(self) -> None:
        super().validate()
        ensure_non_empty_string(self.symbol, "symbol")
        ensure_non_empty_string(self.timestamp_utc, "timestamp_utc")
        validate_ohlcv_prices(self.open, self.high, self.low, self.close)
        ensure_non_negative_number(self.volume, "volume")

@dataclass
class OHLCVSeriesMetadata(BaseDomainModel):
    symbol: str = ""
    timeframe: str = ""
    source: str = ""
    row_count: int = 0
    start_timestamp_utc: Optional[str] = None
    end_timestamp_utc: Optional[str] = None
    quality_status: DataQualityStatus = DataQualityStatus.OK
    warnings: list[str] = None

    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []

@dataclass
class DataFetchRequest(BaseDomainModel):
    symbols: list[str] = None
    timeframe: str = ""
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    source: str = ""
    adjusted: bool = True

    def __post_init__(self):
        if self.symbols is None:
            self.symbols = []

@dataclass
class DataFetchResult(BaseDomainModel):
    request: DataFetchRequest = None
    metadata: list[OHLCVSeriesMetadata] = None
    success: bool = False
    errors: list[str] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = []
        if self.errors is None:
            self.errors = []

from typing import Any

@dataclass
class MarketDataRequest(BaseDomainModel):
    symbols: list[str] = field(default_factory=list)
    timeframe: str = ""
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    provider_name: str = ""
    adjusted: bool = True
    use_cache: bool = True

    def __post_init__(self):
        super().validate()
        if not self.symbols:
            raise ValueError("MarketDataRequest requires at least one symbol.")
        for symbol in self.symbols:
            ensure_non_empty_string(symbol, "symbol in list")
        ensure_non_empty_string(self.provider_name, "provider_name")
        ensure_non_empty_string(self.timeframe, "timeframe")

@dataclass
class MarketDataResponse(BaseDomainModel):
    request: MarketDataRequest = None
    bars: list[OHLCVBar] = field(default_factory=list)
    success: bool = False
    provider_name: str = ""
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    fetched_at_utc: str = ""
    from_cache: bool = False

    def bar_count(self) -> int:
        return len(self.bars)

    def symbols_returned(self) -> list[str]:
        return list(set(bar.symbol for bar in self.bars))

    def has_errors(self) -> bool:
        return len(self.errors) > 0

@dataclass
class ProviderStatus(BaseDomainModel):
    provider_name: str = ""
    available: bool = False
    message: str = ""
    checked_at_utc: str = ""
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class ProviderFetchPlan(BaseDomainModel):
    provider_name: str = ""
    symbols: list[str] = field(default_factory=list)
    timeframe: str = ""
    batch_count: int = 0
    estimated_requests: int = 0
    cache_enabled: bool = False
    notes: list[str] = field(default_factory=list)
