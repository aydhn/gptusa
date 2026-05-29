from usa_signal_bot.regime_classification.behavior_reporting.phase130_models import (
    RegimeTransitionIngestionResult, validate_regime_transition_ingestion_result,
    MarketBehaviorProfileSpec, MarketBehaviorProfile, RegimeBehaviorSummary,
    RegimeDiagnosticsInterpretation, BehaviorReportDocument, BehaviorReportQaRuleResult,
    MarketBehaviorReadinessGate, MarketBehaviorContext, MarketBehaviorFullReview
)

def test_regime_transition_ingestion_result_defaults():
    res = RegimeTransitionIngestionResult()
    assert res.metadata_only is True
    assert res.research_data_only is True
    assert res.activation_allowed is False
    assert res.produces_trade_signal is False

def test_validate_regime_transition_ingestion_result():
    res = RegimeTransitionIngestionResult()
    res.ready_for_phase130 = True
    errs = validate_regime_transition_ingestion_result(res)
    assert not errs

    res.activation_allowed = True
    errs = validate_regime_transition_ingestion_result(res)
    assert "activation_allowed must be false" in errs

def test_models_to_dict():
    prof = MarketBehaviorProfile(symbol="AAPL")
    d = prof.to_dict()
    assert d["symbol"] == "AAPL"
    assert isinstance(d["profile_kind"], str)
