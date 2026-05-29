from usa_signal_bot.regime_classification.behavior_reporting.phase130_models import (
    RegimeTransitionIngestionResult, MarketBehaviorProfile, RegimeBehaviorSummary
)
from usa_signal_bot.regime_classification.behavior_reporting.behavior_report_sections import (
    build_behavior_executive_summary_section, build_behavior_data_scope_section
)

def test_build_sections():
    ing = RegimeTransitionIngestionResult(ingestion_id="test")
    p = MarketBehaviorProfile(symbol="AAPL")
    s = RegimeBehaviorSummary(title="Test")

    sec1 = build_behavior_executive_summary_section([p], [s])
    assert sec1.title == "Executive Summary"

    sec2 = build_behavior_data_scope_section(ing)
    assert sec2.title == "Data Scope"
    assert "test" in sec2.body
