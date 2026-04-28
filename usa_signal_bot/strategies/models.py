from dataclasses import dataclass
from typing import Optional, Any
from ..core.domain import BaseDomainModel
from ..core.enums import SignalSide, SignalStrength
from ..core.model_validation import ensure_non_empty_string, ensure_ratio, ensure_enum_value, ensure_list

@dataclass
class StrategyConfig(BaseDomainModel):
    name: str = ""
    version: str = ""
    enabled: bool = True
    parameters: dict[str, Any] = None
    description: Optional[str] = None

    def __post_init__(self):
        if self.parameters is None:
            self.parameters = {}

@dataclass
class Signal(BaseDomainModel):
    signal_id: str = ""
    symbol: str = ""
    timestamp_utc: str = ""
    strategy_name: str = ""
    side: SignalSide = SignalSide.FLAT
    strength: SignalStrength = SignalStrength.MODERATE
    confidence: float = 0.0
    score: float = 0.0
    timeframe: str = ""
    reasons: list[str] = None
    features: dict[str, Any] = None
    regime: Optional[str] = None

    def __post_init__(self):
        if self.reasons is None:
            self.reasons = []
        if self.features is None:
            self.features = {}
        self.validate()

    def validate(self) -> None:
        super().validate()
        ensure_non_empty_string(self.symbol, "symbol")
        ensure_non_empty_string(self.strategy_name, "strategy_name")
        ensure_enum_value(self.side, SignalSide, "side")
        ensure_list(self.reasons, "reasons")
        ensure_ratio(self.confidence, "confidence")

@dataclass
class SignalBatch(BaseDomainModel):
    batch_id: str = ""
    timestamp_utc: str = ""
    signals: list[Signal] = None
    source: str = ""
    universe_name: Optional[str] = None

    def __post_init__(self):
        if self.signals is None:
            self.signals = []

    def top_signals(self, limit: int = 10) -> list[Signal]:
        return sorted(self.signals, key=lambda s: s.score, reverse=True)[:limit]
