from usa_signal_bot.portfolio.risk_reporting.portfolio_risk_schema_validator import (
    validate_portfolio_risk_column_names
)

def test_validate_portfolio_risk_column_names():
    cols = ["good_col", "target_weight", "another_good_col"]
    forbidden = validate_portfolio_risk_column_names(cols)
    assert "target_weight" in forbidden
