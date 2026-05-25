
from typing import Dict, Any
from usa_signal_bot.event_metadata.phase111_models import (
    ProviderOrchestrationIngestionResult, MacroSeriesMetadata, EconomicEventMetadata, EarningsCalendarMetadata,
    CorporateActionMetadata, NewsMetadataItem, UnifiedMarketEvent, EventSchedule, EventScheduleIndex,
    EventMetadataContext, EventMetadataFullReview
)

def provider_orchestration_ingestion_result_to_text(item: ProviderOrchestrationIngestionResult) -> str: return str(item.ingestion_id)
def macro_series_metadata_to_text(item: MacroSeriesMetadata) -> str: return str(item.series_id)
def economic_event_metadata_to_text(item: EconomicEventMetadata) -> str: return str(item.event_id)
def earnings_calendar_metadata_to_text(item: EarningsCalendarMetadata) -> str: return str(item.event_id)
def corporate_action_metadata_to_text(item: CorporateActionMetadata) -> str: return str(item.event_id)
def news_metadata_item_to_text(item: NewsMetadataItem) -> str: return str(item.news_id)
def unified_market_event_to_text(item: UnifiedMarketEvent) -> str: return str(item.unified_event_id)
def event_schedule_to_text(item: EventSchedule, limit: int = 300) -> str: return str(item.schedule_id)
def event_schedule_index_to_text(item: EventScheduleIndex, limit: int = 200) -> str: return str(item.index_id)
def event_metadata_context_to_text(item: EventMetadataContext, limit: int = 300) -> str: return str(item.context_id)
def event_metadata_full_review_to_text(item: EventMetadataFullReview, limit: int = 300) -> str: return str(item.review_id)
def event_metadata_store_summary_to_text(summary: Dict[str, Any]) -> str: return str(summary)
def event_metadata_limitations_text() -> str: return "Phase 111 limitations apply."
