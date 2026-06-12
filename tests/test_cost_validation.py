import sys
from unittest.mock import MagicMock
sys.modules['usa_signal_bot.core.enums'] = MagicMock()

import pytest
from usa_signal_bot.transaction_costs.cost_validation import validate_no_live_execution_language_in_cost, validate_no_sensitive_data_in_cost_payload

def test_no_live_execution_language():
    rep = validate_no_live_execution_language_in_cost("This is guaranteed fill")
    assert rep.valid is False
    assert rep.blocked_count > 0

def test_no_sensitive_data():
    rep = validate_no_sensitive_data_in_cost_payload({"api_key": "12345"})
    assert rep.valid is False
    assert rep.blocked_count > 0

def test_validate_slippage_curve_report_error():
    import sys
    from unittest.mock import MagicMock
    sys.modules['usa_signal_bot.core.enums'] = MagicMock()
    from usa_signal_bot.transaction_costs.cost_models import SlippageCurve, SlippageCurvePoint
    from usa_signal_bot.transaction_costs.cost_validation import validate_slippage_curve_report

    # Create a point that triggers ValueError in validate_slippage_curve
    point = SlippageCurvePoint(participation_rate_pct=-10.0, slippage_bps=5.0)

    curve = SlippageCurve(
        curve_id="test_curve_123",
        symbol="AAPL",
        curve_type="EMPIRICAL", # using string to bypass enum import issues
        created_at_utc="2024-01-01T00:00:00Z",
        points=[point],
        base_spread_bps=2.0,
        volatility_multiplier=1.0,
        liquidity_multiplier=1.0,
        warnings=[],
        errors=[]
    )

    report = validate_slippage_curve_report(curve)

    assert report.valid is False
    assert report.error_count == 1
    assert "participation_rate_pct cannot be negative" in report.errors[0]

def test_validate_slippage_curve_report_error_slippage():
    import sys
    from unittest.mock import MagicMock
    sys.modules['usa_signal_bot.core.enums'] = MagicMock()
    from usa_signal_bot.transaction_costs.cost_models import SlippageCurve, SlippageCurvePoint
    from usa_signal_bot.transaction_costs.cost_validation import validate_slippage_curve_report

    # Create a point that triggers ValueError in validate_slippage_curve
    point = SlippageCurvePoint(participation_rate_pct=10.0, slippage_bps=-5.0)

    curve = SlippageCurve(
        curve_id="test_curve_123",
        symbol="AAPL",
        curve_type="EMPIRICAL",
        created_at_utc="2024-01-01T00:00:00Z",
        points=[point],
        base_spread_bps=2.0,
        volatility_multiplier=1.0,
        liquidity_multiplier=1.0,
        warnings=[],
        errors=[]
    )

    report = validate_slippage_curve_report(curve)

    assert report.valid is False
    assert report.error_count == 1
    assert "slippage_bps cannot be negative" in report.errors[0]

def test_validate_market_impact_report_error_empty_symbol():
    import sys
    from unittest.mock import MagicMock
    sys.modules['usa_signal_bot.core.enums'] = MagicMock()
    from usa_signal_bot.transaction_costs.cost_models import MarketImpactEstimate
    from usa_signal_bot.transaction_costs.cost_validation import validate_market_impact_report

    item = MarketImpactEstimate(
        estimate_id="est_123",
        symbol="",
        created_at_utc="2024-01-01T00:00:00Z",
        side="BUY",
        notional_usd=1000.0,
        participation_rate_pct=10.0,
        impact_bps=5.0,
        impact_usd=50.0,
        status="SUCCESS",
        order_size_class="NORMAL", warnings=[], errors=[]
    )

    report = validate_market_impact_report(item)
    assert report.valid is False
    assert report.error_count == 1
    assert "symbol cannot be empty" in report.errors[0]

def test_validate_market_impact_report_error_negative_bps():
    import sys
    from unittest.mock import MagicMock
    sys.modules['usa_signal_bot.core.enums'] = MagicMock()
    from usa_signal_bot.transaction_costs.cost_models import MarketImpactEstimate
    from usa_signal_bot.transaction_costs.cost_validation import validate_market_impact_report

    item = MarketImpactEstimate(
        estimate_id="est_123",
        symbol="AAPL",
        created_at_utc="2024-01-01T00:00:00Z",
        side="BUY",
        notional_usd=1000.0,
        participation_rate_pct=10.0,
        impact_bps=-5.0,
        impact_usd=50.0,
        status="SUCCESS",
        order_size_class="NORMAL", warnings=[], errors=[]
    )

    report = validate_market_impact_report(item)
    assert report.valid is False
    assert report.error_count == 1
    assert "impact_bps cannot be negative" in report.errors[0]

def test_validate_market_impact_report_error_negative_usd():
    import sys
    from unittest.mock import MagicMock
    sys.modules['usa_signal_bot.core.enums'] = MagicMock()
    from usa_signal_bot.transaction_costs.cost_models import MarketImpactEstimate
    from usa_signal_bot.transaction_costs.cost_validation import validate_market_impact_report

    item = MarketImpactEstimate(
        estimate_id="est_123",
        symbol="AAPL",
        created_at_utc="2024-01-01T00:00:00Z",
        side="BUY",
        notional_usd=1000.0,
        participation_rate_pct=10.0,
        impact_bps=5.0,
        impact_usd=-50.0,
        status="SUCCESS",
        order_size_class="NORMAL", warnings=[], errors=[]
    )

    report = validate_market_impact_report(item)
    assert report.valid is False
    assert report.error_count == 1
    assert "impact_usd cannot be negative" in report.errors[0]
