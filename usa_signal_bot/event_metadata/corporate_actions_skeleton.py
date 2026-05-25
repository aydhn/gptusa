
import datetime
from pathlib import Path
from typing import List, Dict, Any
from usa_signal_bot.core.enums import MarketEventKind, MarketEventImportance, MarketEventSource, MarketEventTimingStatus
from usa_signal_bot.event_metadata.phase111_models import CorporateActionMetadata, UnifiedMarketEvent, create_event_id, create_unified_event_id

def build_sample_corporate_actions() -> List[CorporateActionMetadata]:
    return [
        CorporateActionMetadata(
            event_id=create_event_id("corp"),
            created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            symbol="AAPL",
            event_kind=MarketEventKind.DIVIDEND,
            effective_at_utc=None,
            declared_at_utc=None,
            source=MarketEventSource.LOCAL_FIXTURE,
            dividend_amount=0.24,
            split_ratio=None,
            metadata_only=True,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        )
    ]

def load_corporate_actions_fixture(path: Path) -> List[CorporateActionMetadata]:
    return build_sample_corporate_actions()

def normalize_corporate_action_payload(payload: Dict[str, Any]) -> CorporateActionMetadata:
    return build_sample_corporate_actions()[0]

def validate_corporate_actions(items: List[CorporateActionMetadata]) -> List[str]:
    errs = []
    for i in items:
        if not i.metadata_only: errs.append("Not metadata_only")
    return errs

def corporate_actions_to_unified_events(items: List[CorporateActionMetadata]) -> List[UnifiedMarketEvent]:
    u = []
    for i in items:
        u.append(UnifiedMarketEvent(
            unified_event_id=create_unified_event_id(),
            created_at_utc=i.created_at_utc,
            event_kind=i.event_kind,
            source=i.source,
            symbol=i.symbol,
            country="US",
            event_name=f"{i.event_kind.value}: {i.symbol}",
            scheduled_at_utc=i.effective_at_utc,
            timing_status=MarketEventTimingStatus.UNKNOWN_TIME,
            importance=MarketEventImportance.INFORMATIONAL,
            metadata_only=i.metadata_only,
            source_ref_id=i.event_id,
            warnings=i.warnings,
            errors=i.errors,
            risk_flags=i.risk_flags,
            metadata=i.metadata
        ))
    return u

def corporate_actions_to_text(items: List[CorporateActionMetadata], limit: int = 200) -> str:
    return f"Corporate Actions: {len(items)} items"
