from dataclasses import dataclass
from typing import Optional, Any
from ..core.domain import BaseDomainModel
from ..core.enums import ModelRunStatus

@dataclass
class MLDatasetMetadata(BaseDomainModel):
    dataset_id: str = ""
    symbols: list[str] = None
    timeframe: str = ""
    feature_names: list[str] = None
    label_name: str = ""
    row_count: int = 0
    start_timestamp_utc: Optional[str] = None
    end_timestamp_utc: Optional[str] = None
    leakage_checked: bool = False

    def __post_init__(self):
        if self.symbols is None:
            self.symbols = []
        if self.feature_names is None:
            self.feature_names = []

@dataclass
class MLModelMetadata(BaseDomainModel):
    model_id: str = ""
    model_name: str = ""
    model_type: str = ""
    version: str = ""
    trained_at_utc: Optional[str] = None
    features: list[str] = None
    target: str = ""
    status: ModelRunStatus = ModelRunStatus.NOT_STARTED
    metrics: dict[str, Any] = None

    def __post_init__(self):
        if self.features is None:
            self.features = []
        if self.metrics is None:
            self.metrics = {}

@dataclass
class Prediction(BaseDomainModel):
    prediction_id: str = ""
    symbol: str = ""
    timestamp_utc: str = ""
    model_id: str = ""
    prediction: float | int | str = 0.0
    confidence: Optional[float] = None
    features_used: list[str] = None

    def __post_init__(self):
        if self.features_used is None:
            self.features_used = []
