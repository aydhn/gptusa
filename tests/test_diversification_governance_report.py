from usa_signal_bot.portfolio.risk_reporting.diversification_governance_report import (
    calculate_effective_name_count_from_exposures,
    calculate_herfindahl_from_exposures
)
from usa_signal_bot.portfolio.risk_reporting.phase157_models import (
    SandboxExposureGovernanceRecord
)
from usa_signal_bot.core.enums import ExposureGovernanceKind

def test_diversification_metrics():
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
        sandbox_optimizer_weight=0.5, normalized_sandbox_optimizer_weight=0.5,
        group_name=None, group_sandbox_exposure=None, exposure_valid=True,
        research_exposure_only=True, actual_target_weight=None,
        actual_portfolio_weight=None, actual_allocation=None,
        actual_position_size=None, order_size=None, capital_allocation=None,
        not_investment_advice=True, warnings=[], errors=[], risk_flags=[], metadata={}
    )

    # Herfindahl = 0.5^2 + 0.5^2 = 0.5
    assert calculate_herfindahl_from_exposures([r1, r2]) == 0.5
    # ENC = 1 / 0.5 = 2.0
    assert calculate_effective_name_count_from_exposures([r1, r2]) == 2.0
