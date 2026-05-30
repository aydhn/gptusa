import pytest
from usa_signal_bot.regime_classification.validation.regime_context_validation_report import build_regime_context_validation_context
from usa_signal_bot.regime_classification.validation.phase132_models import (
    RegimeAlignmentIngestionResult, CompatibilityValidationResult, RegimeAwareAcceptanceGate
)
from usa_signal_bot.core.enums import RegimeContextValidationQuality, RegimeContextAcceptanceStatus

def test_build_regime_context_validation_context():
    ing = RegimeAlignmentIngestionResult(
        ingestion_id="i1", created_at_utc="now", source_path=None, source_review_id=None, source_context_id=None,
        available=True, market_behavior_ingested=True, frozen_factors_loaded=True, behavior_artifacts_loaded=True,
        alignment_specs_ready=True, overlays_built=True, compatibility_computed=True, diagnostics_built=True,
        readiness_gate_ready=True, ready_for_phase132=True, metadata_only=True, research_data_only=True,
        activation_allowed=False, strategy_activation_allowed=False, deployment_allowed=False,
        active_paper_enabled=False, broker_execution_enabled=False, order_creation_enabled=False,
        paper_state_mutation_enabled=False, telegram_real_send_enabled=False, scraping_enabled=False,
        html_parse_enabled=False, paid_api_enabled=False, dashboard_enabled=False, network_default_enabled=False,
        model_training_used=False, model_prediction_used=False, heavy_ml_dependency_used=False,
        produces_trade_signal=False, produces_order_decision=False, produces_portfolio_weights=False,
        investment_advice=False, network_used=False, paid_api_used=False, scraping_used=False,
        html_parsing_used=False, broker_used=False, order_created=False, paper_state_mutated=False,
        telegram_real_sent=False, dashboard_started=False, valid_for_phase132=True, risk_flags=[], warnings=[], errors=[], metadata={}
    )
    comp = CompatibilityValidationResult(
        validation_id="v1", created_at_utc="now", rules=[], total_rules=0, passed_rules=0, warning_rules=0, failed_rules=0, blocked_rules=0,
        validation_passed=True, compatibility_result_count=0, overlay_result_count=0, diagnostics_profile_count=0,
        low_compatibility_count=0, uncertain_count=0, conflicted_count=0, data_quality_limited_count=0,
        explained_low_compatibility_count=0, explained_uncertain_count=0, explained_conflicted_count=0, explained_data_quality_limited_count=0,
        quality=RegimeContextValidationQuality.HIGH, research_metadata_only=True, activation_allowed=False,
        strategy_activation_allowed=False, deployment_allowed=False, model_training_used=False, model_prediction_used=False,
        produces_trade_signal=False, produces_order_decision=False, produces_portfolio_weights=False, investment_advice=False,
        warnings=[], errors=[], risk_flags=[], metadata={}
    )
    gate = RegimeAwareAcceptanceGate(
        gate_id="g1", created_at_utc="now", status=RegimeContextAcceptanceStatus.ACCEPTED, rules=[],
        compatibility_validation=comp, conditional_diagnostics=[], diagnostics_profiles=[],
        ready_for_phase133=True, research_data_only=True, activation_allowed=False, strategy_activation_allowed=False,
        deployment_allowed=False, model_training_used=False, model_prediction_used=False, produces_trade_signal=False,
        produces_order_decision=False, produces_portfolio_weights=False, investment_advice=False, warnings=[], errors=[], risk_flags=[], metadata={}
    )

    ctx = build_regime_context_validation_context(ing, comp, [], [], [], gate)
    assert ctx.ready_for_phase133 is True
