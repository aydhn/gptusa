import datetime
from typing import Dict, Any, List
import pandas as pd
from .phase147_models import PriceEvent, PriceEventStream, PriceEventKind, create_price_event_id, create_price_event_stream_id

def build_price_event_from_row(row: Dict[str, Any]) -> PriceEvent:
    return PriceEvent(
        event_id=create_price_event_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        symbol=row["symbol"],
        timestamp=row["timestamp"],
        event_kind=PriceEventKind.BAR_CLOSE,
        open_price=row.get("open"),
        high_price=row.get("high"),
        low_price=row.get("low"),
        close_price=row.get("close"),
        adjusted_close=row.get("adjusted_close"),
        volume=row.get("volume"),
        event_valid=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_price_event_stream(price_bars: pd.DataFrame) -> PriceEventStream:
    events = [build_price_event_from_row(r) for r in price_bars.to_dict('records')]
    symbols = list(price_bars["symbol"].unique()) if not price_bars.empty else []
    timestamps = sorted(price_bars["timestamp"].unique()) if not price_bars.empty else []

    return PriceEventStream(
        stream_id=create_price_event_stream_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        events=events,
        row_count=len(events),
        symbols=symbols,
        start_timestamp=timestamps[0] if timestamps else None,
        end_timestamp=timestamps[-1] if timestamps else None,
        stream_hash=None,
        stream_valid=True,
        deterministic=True,
        research_data_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def validate_price_event_stream(stream: PriceEventStream) -> List[str]:
    return []

def compute_price_event_stream_hash(stream: PriceEventStream) -> str:
    import hashlib
    data = "".join([f"{e.symbol}{e.timestamp}{e.close_price}" for e in stream.events])
    return hashlib.sha256(data.encode()).hexdigest()

def price_event_stream_summary(stream: PriceEventStream) -> Dict[str, Any]:
    return {"event_count": stream.row_count}

def price_event_stream_to_text(stream: PriceEventStream, limit: int = 300) -> str:
    return f"PriceEventStream {stream.stream_id} with {stream.row_count} events"
