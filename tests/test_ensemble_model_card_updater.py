from usa_signal_bot.ml_research.ensemble_evaluation.ensemble_model_card_updater import update_model_card_for_ensemble_prototype
from usa_signal_bot.ml_research.ensemble_evaluation.phase143_models import OfflineEnsembleEvaluationReport, EnsemblePrototypeQuality

def test_update_model_card_for_ensemble_prototype():
    report = OfflineEnsembleEvaluationReport(
        report_id="r1", created_at_utc="", prototype_id="p1", prediction_ids=[], metric_results=[],
        blend_diagnostics=[], agreement_diagnostics=[], candidate_comparisons=[], train_metric_count=0,
        validation_metric_count=0, test_metric_count=0, report_hash=None, report_valid=True,
        quality=EnsemblePrototypeQuality.ACCEPTABLE, offline_evaluation_only=True, research_data_only=True,
        offline_ml_research_only=True, activation_allowed=False, strategy_activation_allowed=False,
        deployment_allowed=False, live_inference_enabled=False, online_inference_enabled=False,
        threshold_optimization_performed=False, produces_trade_signal=False, produces_order_decision=False,
        produces_portfolio_weights=False, investment_advice=False, warnings=[], errors=[], risk_flags=[], metadata={}
    )

    update = update_model_card_for_ensemble_prototype(None, report)
    assert update.non_activation_notice_preserved is True
    assert update.not_investment_advice is True
    assert update.not_deployment_artifact is True
