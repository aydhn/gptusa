from usa_signal_bot.feature_engine.core_indicators.phase117_models import CoreIndicatorFullReview, CoreIndicatorReportType, create_core_indicator_full_review_id, CoreIndicatorContext, FeatureFoundationIngestionResult
from usa_signal_bot.feature_engine.core_indicators.indicator_implementation_registry import build_core_indicator_computation_specs

def build_core_indicator_full_review() -> CoreIndicatorFullReview:
    specs = build_core_indicator_computation_specs()
    ing = FeatureFoundationIngestionResult("", "", "", "", "", False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, [], [], [], {})
    return CoreIndicatorFullReview(
        review_id=create_core_indicator_full_review_id(), created_at_utc="", report_type=CoreIndicatorReportType.FULL_PHASE117_REVIEW,
        ingestion=ing, context=CoreIndicatorContext("", "", None, None, None, ing, [], [], [], [], [], [], True, True, True, True, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, [], [], [], {}),
        indicator_specs=specs, rolling_specs=[], results=[], feature_tables=[], audits=[], output_paths={}, warnings=[], errors=[]
    )
def core_indicator_full_review_to_text(rev) -> str:
    return ""
