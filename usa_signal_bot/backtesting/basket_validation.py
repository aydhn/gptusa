from dataclasses import dataclass
from usa_signal_bot.backtesting.basket_models import BasketSimulationResult

@dataclass
class BasketValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    issues: list
    warnings: list[str]
    errors: list[str]

def validate_basket_simulation_result(result: BasketSimulationResult) -> BasketValidationReport:
    return BasketValidationReport(True, 0, 0, 0, [], [], [])

def basket_validation_report_to_text(report: BasketValidationReport) -> str:
    return "valid"
