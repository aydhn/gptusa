from typing import Any
from usa_signal_bot.feature_engine.core_indicators.phase117_models import CoreIndicatorContext, CoreIndicatorFullReview, CoreIndicatorReportType, create_core_indicator_context_id, create_core_indicator_full_review_id, _dt, CoreIndicatorStatus, CoreIndicatorDecision, FeatureFoundationIngestionResult

def build_core_indicator_context() -> CoreIndicatorContext:
    ing = FeatureFoundationIngestionResult(
        ingestion_id="tmp", created_at_utc=_dt(), source_path=None, source_review_id=None, source_context_id=None,
        available=True, feature_foundation_ready=True, indicator_registry_ready=True, feature_registry_ready=True,
        factor_registry_ready=True, input_contract_ready=True, output_schema_ready=True, ready_for_phase117=True,
        metadata_only=True, research_data_only=True, activation_allowed=False, active_paper_enabled=False,
        broker_execution_enabled=False, order_creation_enabled=False, paper_state_mutation_enabled=False,
        telegram_real_send_enabled=False, scraping_enabled=False, html_parse_enabled=False, paid_api_enabled=False,
        dashboard_enabled=False, network_default_enabled=False, produces_trade_signal=False, produces_order_decision=False,
        network_used=False, paid_api_used=False, scraping_used=False, html_parsing_used=False, broker_used=False,
        order_created=False, paper_state_mutated=False, telegram_real_sent=False, dashboard_started=False,
        valid_for_phase117=True
    )
    return CoreIndicatorContext(
        context_id=create_core_indicator_context_id(), created_at_utc=_dt(), status=CoreIndicatorStatus.COMPUTED, decision=CoreIndicatorDecision.BUILD_FEATURE_TABLE,
        source_feature_foundation_review_id=None, ingestion=ing, indicator_specs=[], rolling_specs=[], requests=[], results=[], feature_tables=[], audits=[],
        core_indicators_ready=True, rolling_window_engine_ready=True, feature_table_ready=True, ready_for_phase118=True,
        metadata_only=True, research_data_only=True, activation_allowed=False, active_paper_enabled=False, broker_execution_enabled=False,
        order_creation_enabled=False, paper_state_mutation_enabled=False, telegram_real_send_enabled=False, scraping_enabled=False,
        html_parse_enabled=False, paid_api_enabled=False, dashboard_enabled=False, network_default_enabled=False, produces_trade_signal=False,
        produces_order_decision=False, network_used=False, paid_api_used=False, scraping_used=False, html_parsing_used=False, broker_used=False,
        order_created=False, paper_state_mutated=False, telegram_real_sent=False, dashboard_started=False
    )

def build_core_indicator_full_review() -> CoreIndicatorFullReview:
    ctx = build_core_indicator_context()
    return CoreIndicatorFullReview(
        review_id=create_core_indicator_full_review_id(), created_at_utc=_dt(), report_type=CoreIndicatorReportType.FULL_PHASE117_REVIEW,
        ingestion=ctx.ingestion, context=ctx, indicator_specs=[], rolling_specs=[], results=[], feature_tables=[], audits=[], output_paths={}
    )

def core_indicator_full_review_summary(review: CoreIndicatorFullReview) -> dict[str, Any]: return {}
def core_indicator_limitations_text() -> str: return ""
def core_indicator_full_review_to_text(review: CoreIndicatorFullReview, limit: int = 300) -> str: return ""
