from usa_signal_bot.regime_classification.behavior_reporting.phase130_models import (
    RegimeTransitionIngestionResult, BehaviorReportDocument, BehaviorReportQaRuleResult
)
from usa_signal_bot.regime_classification.behavior_reporting.behavior_report_readiness_gate import (
    build_market_behavior_readiness_gate, market_behavior_readiness_passed
)

def test_build_market_behavior_readiness_gate():
    ing = RegimeTransitionIngestionResult(valid_for_phase130=True)
    doc = BehaviorReportDocument()
    qa_res = BehaviorReportQaRuleResult(passed=True)
    # Using an empty profile list will fail the gate since DIAGNOSTICS_ARTIFACTS_AVAILABLE requires len(profiles) > 0
    gate = build_market_behavior_readiness_gate(ing, [], [], doc, [qa_res])
    assert not market_behavior_readiness_passed(gate)
    assert gate.ready_for_phase131 is False
