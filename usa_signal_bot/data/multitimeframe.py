from dataclasses import dataclass, field
from typing import Optional, Any
from ..core.domain import BaseDomainModel
from ..core.enums import TimeframeRole, PipelineRunStatus
from .models import MarketDataRequest

@dataclass
class TimeframeSpec(BaseDomainModel):
    timeframe: str = ""
    role: TimeframeRole = TimeframeRole.PRIMARY
    enabled: bool = True
    lookback_days: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    max_symbols: Optional[int] = None

    def __post_init__(self):
        super().validate()
        from .timeframes import validate_timeframe_for_yfinance
        validate_timeframe_for_yfinance(self.timeframe)

        if self.lookback_days is not None and self.lookback_days < 0:
            raise ValueError("lookback_days must be non-negative")
        if self.max_symbols is not None and self.max_symbols < 0:
            raise ValueError("max_symbols must be non-negative")

@dataclass
class MultiTimeframeDataRequest(BaseDomainModel):
    symbols: list[str] = field(default_factory=list)
    provider_name: str = "yfinance"
    timeframe_specs: list[TimeframeSpec] = field(default_factory=list)
    adjusted: bool = True
    use_cache: bool = True
    force_refresh: bool = False

    def __post_init__(self):
        super().validate()
        if not self.symbols:
            raise ValueError("symbols cannot be empty")
        if not self.provider_name:
            raise ValueError("provider_name cannot be empty")

        enabled_specs = [s for s in self.timeframe_specs if s.enabled]
        if not enabled_specs:
            raise ValueError("at least one enabled timeframe_spec is required")

@dataclass
class TimeframeDownloadResult(BaseDomainModel):
    timeframe: str = ""
    response_bar_count: int = 0
    symbols_requested: list[str] = field(default_factory=list)
    symbols_returned: list[str] = field(default_factory=list)
    cache_paths: list[str] = field(default_factory=list)
    success: bool = False
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

@dataclass
class MultiTimeframeDataResult(BaseDomainModel):
    request: MultiTimeframeDataRequest = None
    status: PipelineRunStatus = PipelineRunStatus.NOT_STARTED
    results: list[TimeframeDownloadResult] = field(default_factory=list)
    created_at_utc: str = ""
    total_bars: int = 0
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def successful_timeframes(self) -> list[str]:
        return [r.timeframe for r in self.results if r.success]

    def failed_timeframes(self) -> list[str]:
        return [r.timeframe for r in self.results if not r.success]

    def symbols_with_any_data(self) -> list[str]:
        syms = set()
        for r in self.results:
            syms.update(r.symbols_returned)
        return list(syms)

    def is_usable(self) -> bool:
        return self.status in [PipelineRunStatus.COMPLETED, PipelineRunStatus.PARTIAL_SUCCESS] and self.total_bars > 0

def default_timeframe_specs() -> list[TimeframeSpec]:
    return [
        TimeframeSpec(timeframe="1d", role=TimeframeRole.PRIMARY),
        TimeframeSpec(timeframe="1h", role=TimeframeRole.CONFIRMATION),
        TimeframeSpec(timeframe="15m", role=TimeframeRole.INTRADAY)
    ]

def normalize_timeframe_specs(specs: list[TimeframeSpec]) -> list[TimeframeSpec]:
    # Ensure primary exists if specs are provided, otherwise just return as is (validation handles rules later)
    # Could also deduplicate
    unique = {}
    for spec in specs:
        if spec.timeframe not in unique:
            unique[spec.timeframe] = spec
    return list(unique.values())

def parse_timeframe_list(value: str) -> list[str]:
    if not value:
        return []
    return [v.strip() for v in value.split(",") if v.strip()]

def build_timeframe_specs_from_list(timeframes: list[str]) -> list[TimeframeSpec]:
    if not timeframes:
        return default_timeframe_specs()
    specs = []
    for i, tf in enumerate(timeframes):
        if i == 0:
            role = TimeframeRole.PRIMARY
        elif "m" in tf and "mo" not in tf:
            role = TimeframeRole.INTRADAY
        elif "h" in tf:
            role = TimeframeRole.CONFIRMATION
        else:
            role = TimeframeRole.DAILY
        specs.append(TimeframeSpec(timeframe=tf, role=role))
    return specs
