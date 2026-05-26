import pytest
from usa_signal_bot.feature_engine.advanced_features.phase118_models import AdvancedFeatureComputationResult, AdvancedFeatureQuality
from usa_signal_bot.feature_engine.advanced_features.advanced_feature_computation_validator import validate_advanced_feature_computation_result

def test_comp_validator():
    r = AdvancedFeatureComputationResult(
        result_id="1", created_at_utc="1", request_id=None, symbols=[],
        computed_feature_columns=[], computed_family_counts={},
        input_rows_by_symbol={}, output_rows_by_symbol={}, normalization_results=[],
        cross_sectional_alignment=None, quality=AdvancedFeatureQuality.HIGH,
        output_paths={}, metadata_only=False, dry_run_only=True, research_data_only=True,
        computed_values=True, produced_trade_signal=False, produced_order_decision=False,
        produced_portfolio_weights=False, network_used=False, paid_api_used=False,
        scraping_used=False, html_parsing_used=False, broker_used=False, order_created=False,
        paper_state_mutated=False, telegram_real_sent=False, dashboard_started=False,
        passed=True, warnings=[], errors=[], risk_flags=[], metadata={}
    )
    assert len(validate_advanced_feature_computation_result(r)) == 0
    r.produced_trade_signal = True
    assert len(validate_advanced_feature_computation_result(r)) == 1
