from usa_signal_bot.portfolio.risk_reporting.sandbox_exposure_governance import (
    validate_sandbox_exposure_governance_records
)
from usa_signal_bot.portfolio.risk_reporting.phase157_models import (
    SandboxExposureGovernanceRecord
)
from usa_signal_bot.core.enums import ExposureGovernanceKind

def test_validate_sandbox_exposure_governance_records():
    # Valid
    r1 = SandboxExposureGovernanceRecord(
        exposure_id="1", created_at_utc="", symbol="A", method_name="m",
        exposure_kind=ExposureGovernanceKind.SANDBOX_WEIGHT_EXPOSURE,
        sandbox_optimizer_weight=0.1, normalized_sandbox_optimizer_weight=0.1,
        group_name=None, group_sandbox_exposure=None, exposure_valid=True,
        research_exposure_only=True, actual_target_weight=None,
        actual_portfolio_weight=None, actual_allocation=None,
        actual_position_size=None, order_size=None, capital_allocation=None,
        not_investment_advice=True, warnings=[], errors=[], risk_flags=[], metadata={}
    )
    # Invalid
    r2 = SandboxExposureGovernanceRecord(
        exposure_id="2", created_at_utc="", symbol="B", method_name="m",
        exposure_kind=ExposureGovernanceKind.SANDBOX_WEIGHT_EXPOSURE,
        sandbox_optimizer_weight=0.1, normalized_sandbox_optimizer_weight=0.1,
        group_name=None, group_sandbox_exposure=None, exposure_valid=True,
        research_exposure_only=True, actual_target_weight=0.1,
        actual_portfolio_weight=None, actual_allocation=None,
        actual_position_size=None, order_size=None, capital_allocation=None,
        not_investment_advice=True, warnings=[], errors=[], risk_flags=[], metadata={}
    )

    assert len(validate_sandbox_exposure_governance_records([r1])) == 0
    errs = validate_sandbox_exposure_governance_records([r2])
    assert len(errs) > 0
