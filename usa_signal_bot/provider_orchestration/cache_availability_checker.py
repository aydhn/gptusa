from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.core.enums import DataAvailabilityStatus
from usa_signal_bot.provider_orchestration.phase110_models import (
    DataAvailabilityItem, create_data_availability_id
)

def check_cache_availability(symbol: str, capability: str, provider_name: str | None = None, cache_payload: dict[str, Any] | None = None) -> DataAvailabilityItem:
    # Dummy logic for Phase 110 offline cache check
    available = cache_payload is not None and cache_payload.get("status") == "AVAILABLE"

    return DataAvailabilityItem(
        availability_id=create_data_availability_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        symbol=symbol,
        capability=capability,
        interval="1d",
        provider_name=provider_name,
        status=DataAvailabilityStatus.AVAILABLE if available else DataAvailabilityStatus.MISSING,
        cache_available=available,
        cache_fresh=available,
        cache_stale=False,
        local_fixture_available=True,
        provider_quality_score=0.9 if available else None,
        source_trust_score=0.8 if available else None,
        rows_available=100 if available else 0,
        last_available_timestamp=datetime.now(timezone.utc).isoformat() if available else None,
        refresh_required_future=not available,
        risk_flags=[],
        warnings=[],
        errors=[],
        metadata={}
    )

def check_cache_availability_batch(symbols: list[str], capability: str = "GET_DAILY_OHLCV", cache_payload: dict[str, Any] | None = None) -> list[DataAvailabilityItem]:
    return [check_cache_availability(sym, capability, None, cache_payload) for sym in symbols]

def cache_availability_summary(items: list[DataAvailabilityItem]) -> dict[str, Any]:
    return {
        "total": len(items),
        "available": sum(1 for i in items if i.status == DataAvailabilityStatus.AVAILABLE),
        "missing": sum(1 for i in items if i.status == DataAvailabilityStatus.MISSING)
    }

def cache_availability_checker_to_text(items: list[DataAvailabilityItem], limit: int = 100) -> str:
    lines = ["--- Cache Availability ---"]
    for i in items[:limit]:
        lines.append(f"{i.symbol}: {i.status.value} (Rows: {i.rows_available})")
    return "\n".join(lines)
