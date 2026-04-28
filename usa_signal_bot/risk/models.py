from dataclasses import dataclass
from typing import Any
from ..core.domain import BaseDomainModel
from ..core.model_validation import ensure_ratio, ensure_positive_number

@dataclass
class RiskLimits(BaseDomainModel):
    max_position_pct: float = 0.0
    max_total_exposure_pct: float = 0.0
    max_daily_loss_pct: float = 0.0
    max_open_positions: int = 0
    allow_short: bool = False

    def __post_init__(self):
        self.validate()

    def validate(self) -> None:
        super().validate()
        ensure_ratio(self.max_position_pct, "max_position_pct")
        ensure_ratio(self.max_total_exposure_pct, "max_total_exposure_pct")
        ensure_ratio(self.max_daily_loss_pct, "max_daily_loss_pct")
        ensure_positive_number(self.max_open_positions, "max_open_positions")

@dataclass
class RiskCheckResult(BaseDomainModel):
    passed: bool = False
    rule_name: str = ""
    message: str = ""
    severity: str = "INFO"
    details: dict[str, Any] = None

    def __post_init__(self):
        if self.details is None:
            self.details = {}

@dataclass
class RiskDecision(BaseDomainModel):
    allowed: bool = False
    checks: list[RiskCheckResult] = None
    final_message: str = ""

    def __post_init__(self):
        if self.checks is None:
            self.checks = []
