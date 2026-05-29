from usa_signal_bot.regime_classification.labeling.candidate_validation_runner import run_candidate_validation
from usa_signal_bot.regime_classification.labeling.phase128_models import HeuristicRegimeLabelResult
from usa_signal_bot.core.enums import RegimeLabelingMethod, RegimeLabelConfidenceKind

def test_validation_runner():
    res1 = HeuristicRegimeLabelResult(
        label_result_id="res1",
        created_at_utc="2023-01-01T00:00:00Z",
        symbol="AAPL",
        timestamp="2023-01-01",
        assigned_label="bull_regime",
        assigned_label_kind="top_candidate",
        method=RegimeLabelingMethod.DETERMINISTIC_TOP_CANDIDATE,
        top_candidate_name="bull",
        top_candidate_score=80.0,
        second_candidate_name="bear",
        second_candidate_score=20.0,
        score_gap=60.0,
        confidence_score=100.0,
        confidence_kind=RegimeLabelConfidenceKind.SCORE_GAP_CONFIDENCE,
        conflict_kinds=[],
        fallback_used=False,
        mixed_label_used=False,
        unknown_label_used=False,
        validation_status="NOT_CHECKED",
        research_metadata_only=True,
        model_prediction=False,
        model_training_used=False,
        activation_allowed=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False
    )

    validation = run_candidate_validation([{"name": "bull"}, {"name": "bear"}], [{"bull": 80.0, "bear": 20.0}], [res1])
    assert validation.validation_passed is True
    assert validation.no_model_training is True
    assert validation.no_model_prediction is True
    assert validation.produces_trade_signal is False
