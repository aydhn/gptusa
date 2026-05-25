
from typing import List, Dict, Any
from usa_signal_bot.event_metadata.phase111_models import (
    MacroSeriesMetadata, EconomicEventMetadata, EarningsCalendarMetadata, CorporateActionMetadata, NewsMetadataItem
)

def validate_all_event_metadata(
    macro_series: List[MacroSeriesMetadata],
    economic_events: List[EconomicEventMetadata],
    earnings_events: List[EarningsCalendarMetadata],
    corporate_actions: List[CorporateActionMetadata],
    news_metadata: List[NewsMetadataItem]
) -> List[str]:
    errs = []
    for x in macro_series:
        if not x.metadata_only: errs.append(f"Macro {x.series_id} not metadata_only")
    for x in economic_events:
        if not x.metadata_only: errs.append(f"Eco {x.event_id} not metadata_only")
    for x in earnings_events:
        if not x.metadata_only: errs.append(f"Earn {x.event_id} not metadata_only")
    for x in corporate_actions:
        if not x.metadata_only: errs.append(f"Corp {x.event_id} not metadata_only")
    for x in news_metadata:
        if not x.metadata_only: errs.append(f"News {x.news_id} not metadata_only")
        if x.content_fetched: errs.append(f"News {x.news_id} content_fetched")
        if x.network_used: errs.append(f"News {x.news_id} network_used")
        if x.scraping_used: errs.append(f"News {x.news_id} scraping_used")
        if x.html_parsing_used: errs.append(f"News {x.news_id} html_parsing_used")
    return errs

def validate_no_network_or_scraping_in_events(payload: Dict[str, Any]) -> List[str]:
    errs = []
    for k in ["network_used", "scraping_used", "html_parsing_used", "paid_api_used"]:
        if payload.get(k, False):
            errs.append(f"{k} is true")
    return errs

def validate_no_trade_signal_in_events_text(text: str) -> List[str]:
    errs = []
    lower_text = text.lower()
    for w in ["buy signal", "sell signal", "emir gönder", "garanti kâr", "kesin al", "kesin sat", "aktif trading", "paper'a alındı"]:
        if w in lower_text:
            errs.append(f"Found execution language: {w}")
    return errs

def event_metadata_validator_summary(errors: List[str]) -> Dict[str, Any]:
    return {"error_count": len(errors)}

def event_metadata_validator_to_text(errors: List[str]) -> str:
    if not errors: return "All valid"
    return "Errors: " + ", ".join(errors)
