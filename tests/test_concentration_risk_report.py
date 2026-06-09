from usa_signal_bot.portfolio.risk_reporting.concentration_risk_report import (
    calculate_max_sandbox_weight,
    calculate_top_n_sandbox_concentration
)
from usa_signal_bot.portfolio.risk_reporting.phase157_models import (
    SandboxExposureGovernanceRecord
)
from usa_signal_bot.core.enums import ExposureGovernanceKind

def test_concentration_metrics():
    r1 = SandboxExposureGovernanceRecord(
        exposure_id="1", created_at_utc="", symbol="A", method_name="m",
        exposure_kind=ExposureGovernanceKind.SANDBOX_WEIGHT_EXPOSURE,
        sandbox_optimizer_weight=0.5, normalized_sandbox_optimizer_weight=0.5,
        group_name=None, group_sandbox_exposure=None, exposure_valid=True,
        research_exposure_only=True, actual_target_weight=None,
        actual_portfolio_weight=None, actual_allocation=None,
        actual_position_size=None, order_size=None, capital_allocation=None,
        not_investment_advice=True, warnings=[], errors=[], risk_flags=[], metadata={}
    )
    r2 = SandboxExposureGovernanceRecord(
        exposure_id="2", created_at_utc="", symbol="B", method_name="m",
        exposure_kind=ExposureGovernanceKind.SANDBOX_WEIGHT_EXPOSURE,
        sandbox_optimizer_weight=0.3, normalized_sandbox_optimizer_weight=0.3,
        group_name=None, group_sandbox_exposure=None, exposure_valid=True,
        research_exposure_only=True, actual_target_weight=None,
        actual_portfolio_weight=None, actual_allocation=None,
        actual_position_size=None, order_size=None, capital_allocation=None,
        not_investment_advice=True, warnings=[], errors=[], risk_flags=[], metadata={}
    )

    assert calculate_max_sandbox_weight([r1, r2]) == 0.5
    assert calculate_top_n_sandbox_concentration([r1, r2], 1) == 0.5
    assert calculate_top_n_sandbox_concentration([r1, r2], 2) == 0.8
