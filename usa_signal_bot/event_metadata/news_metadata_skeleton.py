
import datetime
from pathlib import Path
from typing import List, Dict, Any
from usa_signal_bot.core.enums import MarketEventKind, MarketEventImportance, MarketEventSource, MarketEventTimingStatus, NewsMetadataStatus
from usa_signal_bot.event_metadata.phase111_models import NewsMetadataItem, UnifiedMarketEvent, create_news_id, create_unified_event_id

def build_sample_news_metadata() -> List[NewsMetadataItem]:
    return [
        NewsMetadataItem(
            news_id=create_news_id(),
            created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            symbol="AAPL",
            provider_name="Dummy News",
            published_at_utc=None,
            title_metadata="Dummy Apple News",
            category="Tech",
            source=MarketEventSource.LOCAL_FIXTURE,
            url_hash="dummyhash",
            content_fetched=False,
            network_used=False,
            scraping_used=False,
            html_parsing_used=False,
            paid_api_used=False,
            metadata_only=True,
            status=NewsMetadataStatus.METADATA_ONLY,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        )
    ]

def load_news_metadata_fixture(path: Path) -> List[NewsMetadataItem]:
    return build_sample_news_metadata()

def normalize_news_metadata_payload(payload: Dict[str, Any]) -> NewsMetadataItem:
    return build_sample_news_metadata()[0]

def validate_news_metadata_items(items: List[NewsMetadataItem]) -> List[str]:
    errs = []
    for i in items:
        if not i.metadata_only: errs.append("Not metadata_only")
        if i.content_fetched: errs.append("content_fetched is True")
        if i.network_used: errs.append("network_used is True")
        if i.scraping_used: errs.append("scraping_used is True")
        if i.html_parsing_used: errs.append("html_parsing_used is True")
    return errs

def news_metadata_to_unified_events(items: List[NewsMetadataItem]) -> List[UnifiedMarketEvent]:
    u = []
    for i in items:
        u.append(UnifiedMarketEvent(
            unified_event_id=create_unified_event_id(),
            created_at_utc=i.created_at_utc,
            event_kind=MarketEventKind.NEWS_METADATA,
            source=i.source,
            symbol=i.symbol,
            country=None,
            event_name=f"News: {i.title_metadata}",
            scheduled_at_utc=i.published_at_utc,
            timing_status=MarketEventTimingStatus.UNKNOWN_TIME,
            importance=MarketEventImportance.INFORMATIONAL,
            metadata_only=i.metadata_only,
            source_ref_id=i.news_id,
            warnings=i.warnings,
            errors=i.errors,
            risk_flags=i.risk_flags,
            metadata=i.metadata
        ))
    return u

def news_metadata_to_text(items: List[NewsMetadataItem], limit: int = 200) -> str:
    return f"News Metadata: {len(items)} items"
