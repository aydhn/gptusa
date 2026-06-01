import pandas as pd
from usa_signal_bot.ml_research.ensemble_evaluation.candidate_agreement_diagnostics import build_candidate_agreement_diagnostics
from usa_signal_bot.ml_research.ensemble_evaluation.phase143_models import EnsemblePrototypeSpec, EnsemblePrototypeKind, OfflineEnsemblePredictionKind

def test_build_candidate_agreement_diagnostics():
    spec = EnsemblePrototypeSpec(
        prototype_id="p1", created_at_utc="", prototype_name="", prototype_kind=EnsemblePrototypeKind.COEFFICIENT_BLEND_PROTOTYPE,
        candidate_group_id="g1", blend_plan_id="bp1", candidate_ref_ids=["c1"], coefficient_by_candidate_ref_id={"c1": 1.0},
        coefficient_sum=1.0, coefficient_valid=True, output_kind=OfflineEnsemblePredictionKind.RESEARCH_ENSEMBLE_SCORE,
        offline_evaluation_only=True, live_inference_allowed=False, online_inference_allowed=False, threshold_optimization_allowed=False,
        deployment_allowed=False, broker_allowed=False, paper_mutation_allowed=False, strategy_activation_allowed=False,
        research_data_only=True, produces_trade_signal=False, produces_order_decision=False, produces_portfolio_weights=False,
        warnings=[], errors=[], risk_flags=[], metadata={}
    )
    df = pd.DataFrame({"symbol": ["AAPL"], "timestamp": ["2023-01-01"], "score_1": [0.8], "score_2": [0.6]})
    diagnostics = build_candidate_agreement_diagnostics([spec], df)
    assert len(diagnostics) == 1
    assert diagnostics[0].investment_advice is False
