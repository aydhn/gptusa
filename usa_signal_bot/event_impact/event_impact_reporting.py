
from typing import Any, Dict
from usa_signal_bot.event_impact.phase112_models import (
    EventMetadataIngestionResult, EventImpactTag, SymbolEventExposure,
    MacroRegimeMetadata, CalendarAwareAnomaly, CalendarAwareValidationResult,
    EventImpactContext, EventImpactFullReview
)
from usa_signal_bot.event_impact.event_impact_report import event_impact_limitations_text

def event_metadata_ingestion_result_to_text(item: EventMetadataIngestionResult) -> str: return f"Ingest: {item.ingestion_id}"
def event_impact_tag_to_text(item: EventImpactTag) -> str: return f"Tag: {item.event_name} ({item.impact_category.value})"
def symbol_event_exposure_to_text(item: SymbolEventExposure) -> str: return f"Exposure: {item.symbol} ({item.exposure_label})"
def macro_regime_metadata_to_text(item: MacroRegimeMetadata) -> str: return f"Regime: {item.label.value}"
def calendar_aware_anomaly_to_text(item: CalendarAwareAnomaly) -> str: return f"Anomaly: {item.anomaly_kind.value} on {item.symbol}"
def calendar_aware_validation_result_to_text(item: CalendarAwareValidationResult) -> str: return f"Validation: {item.symbol} ({item.status.value})"
def event_impact_context_to_text(item: EventImpactContext, limit: int = 300) -> str: return f"Context: {item.context_id}"
def event_impact_full_review_to_text(item: EventImpactFullReview, limit: int = 300) -> str: return f"Review: {item.review_id}"
def event_impact_store_summary_to_text(summary: Dict[str, Any]) -> str: return f"Store summary: {summary}"
