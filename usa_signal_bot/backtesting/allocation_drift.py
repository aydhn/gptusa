from dataclasses import dataclass, field
import uuid
from usa_signal_bot.backtesting.portfolio_models import BacktestPortfolio
from usa_signal_bot.backtesting.basket_models import BasketReplayItem, BasketExposureSnapshot
from usa_signal_bot.core.enums import AllocationDriftStatus

@dataclass
class AllocationDriftConfig:
    drift_warning_threshold: float
    drift_breach_threshold: float
    evaluate_by_symbol: bool = True
    evaluate_total_weight: bool = True

@dataclass
class AllocationDriftReport:
    report_id: str
    created_at_utc: str
    status: AllocationDriftStatus
    items: list
    max_abs_drift: float | None
    average_abs_drift: float | None
    warnings: list[str]
    errors: list[str]

def default_allocation_drift_config() -> AllocationDriftConfig:
    return AllocationDriftConfig(0.03, 0.05, True, True)

def calculate_allocation_drift(target_weights: dict, actual_weights: dict, config: AllocationDriftConfig | None = None) -> AllocationDriftReport:
    return AllocationDriftReport("1", "2023", AllocationDriftStatus.WITHIN_TOLERANCE, [], 0, 0, [], [])

def build_basket_exposure_snapshot(timestamp_utc: str, portfolio: BacktestPortfolio, prices: dict, target_weights: dict) -> BasketExposureSnapshot:
    return BasketExposureSnapshot(timestamp_utc, 100, 100, 0, 0, 0, 0, {}, {}, {}, 0, [])

def allocation_drift_report_to_text(report: AllocationDriftReport, limit: int = 30) -> str:
    return "drift report"


def calculate_target_weights_from_replay_items(items) -> dict:
    return {}
