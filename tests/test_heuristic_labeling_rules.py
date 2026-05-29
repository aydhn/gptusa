import pandas as pd
from usa_signal_bot.regime_classification.labeling.heuristic_labeling_rules import (
    assign_heuristic_regime_labels_for_table,
    determine_label_from_candidate_scores,
    detect_label_conflicts_from_scores
)
from usa_signal_bot.regime_classification.labeling.phase128_models import RegimeLabelingSpec
from usa_signal_bot.core.enums import RegimeLabelingMethod

def test_heuristic_labeling():
    df = pd.DataFrame({
        "symbol": ["AAPL", "AAPL"],
        "timestamp": ["2023-01-01", "2023-01-02"],
        "candidate_bull_score": [80.0, 20.0],
        "candidate_bear_score": [10.0, 90.0]
    })

    spec = RegimeLabelingSpec(
        spec_id="test",
        created_at_utc="2023-01-01T00:00:00Z",
        spec_name="test",
        method=RegimeLabelingMethod.DETERMINISTIC_TOP_CANDIDATE,
        taxonomy_labels=["bull_regime", "bear_regime"],
        candidate_score_columns=["candidate_bull_score", "candidate_bear_score"],
        minimum_score_threshold=40.0,
        minimum_score_gap=5.0,
        fallback_label="unknown",
        mixed_label="mixed",
        unknown_label="unknown",
        conflict_policy="fallback",
        deterministic=True,
        research_metadata_only=True,
        model_training_used=False,
        model_prediction_used=False,
        activation_allowed=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False
    )

    out_df, results = assign_heuristic_regime_labels_for_table("AAPL", df, spec)
    assert len(results) == 2
    assert results[0].assigned_label == "bull_regime"
    assert results[1].assigned_label == "bear_regime"
    assert "regime_label_research" in out_df.columns
    assert "regime_label_confidence" in out_df.columns
