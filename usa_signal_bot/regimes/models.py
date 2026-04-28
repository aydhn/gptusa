from dataclasses import dataclass
from typing import Optional, Any
from ..core.domain import BaseDomainModel
from ..core.enums import RegimeType
from ..core.model_validation import ensure_ratio

@dataclass
class RegimeState(BaseDomainModel):
    symbol: str = ""
    timestamp_utc: str = ""
    regime_type: RegimeType = RegimeType.UNKNOWN
    confidence: float = 0.0
    features: dict[str, Any] = None
    description: Optional[str] = None

    def __post_init__(self):
        if self.features is None:
            self.features = {}
        self.validate()

    def validate(self) -> None:
        super().validate()
        ensure_ratio(self.confidence, "confidence")

@dataclass
class MarketRegimeSnapshot(BaseDomainModel):
    timestamp_utc: str = ""
    market_proxy: str = ""
    primary_regime: RegimeType = RegimeType.UNKNOWN
    confidence: float = 0.0
    states: list[RegimeState] = None
    notes: list[str] = None

    def __post_init__(self):
        if self.states is None:
            self.states = []
        if self.notes is None:
            self.notes = []
        self.validate()

    def validate(self) -> None:
        super().validate()
        ensure_ratio(self.confidence, "confidence")
