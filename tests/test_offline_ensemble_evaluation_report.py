from usa_signal_bot.ml_research.ensemble_evaluation.offline_ensemble_evaluation_report import build_offline_ensemble_evaluation_reports
from usa_signal_bot.ml_research.ensemble_evaluation.phase143_models import EnsemblePrototypeSpec, EnsemblePrototypeKind, OfflineEnsemblePredictionKind

def test_build_offline_ensemble_evaluation_reports():
    spec = EnsemblePrototypeSpec(
        prototype_id="p1", created_at_utc="", prototype_name="", prototype_kind=EnsemblePrototypeKind.COEFFICIENT_BLEND_PROTOTYPE,
        candidate_group_id="g1", blend_plan_id="bp1", candidate_ref_ids=["c1"], coefficient_by_candidate_ref_id={"c1": 1.0},
        coefficient_sum=1.0, coefficient_valid=True, output_kind=OfflineEnsemblePredictionKind.RESEARCH_ENSEMBLE_SCORE,
        offline_evaluation_only=True, live_inference_allowed=False, online_inference_allowed=False, threshold_optimization_allowed=False,
        deployment_allowed=False, broker_allowed=False, paper_mutation_allowed=False, strategy_activation_allowed=False,
        research_data_only=True, produces_trade_signal=False, produces_order_decision=False, produces_portfolio_weights=False,
        warnings=[], errors=[], risk_flags=[], metadata={}
    )
    reports = build_offline_ensemble_evaluation_reports([spec], [], [], [], [], [])
    assert len(reports) == 1
    assert reports[0].offline_evaluation_only is True
    assert reports[0].deployment_allowed is False
