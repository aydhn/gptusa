
from typing import Any
from usa_signal_bot.data_providers.phase106_models import ProviderSelectionRequest, create_provider_selection_id, _now
from usa_signal_bot.core.enums import DataProviderKind, DataProviderCapability, ProviderDataDomain, ProviderSelectorMode

def build_provider_selection_request(provider_kind: DataProviderKind, capability: DataProviderCapability, domain: ProviderDataDomain, symbol: str | None = None, selector_mode: ProviderSelectorMode = ProviderSelectorMode.METADATA_ONLY) -> ProviderSelectionRequest:
    return ProviderSelectionRequest(
        selection_id=create_provider_selection_id(),
        created_at_utc=_now(),
        provider_kind=provider_kind,
        capability=capability,
        domain=domain,
        selector_mode=selector_mode,
        symbol=symbol,
        metadata_only=True,
        allow_network=False,
        allow_paid_api=False,
        allow_scraping=False,
        allow_broker=False,
        allow_order=False
    )

def build_market_data_request_plan(symbol: str, capability: DataProviderCapability = DataProviderCapability.GET_DAILY_OHLCV) -> ProviderSelectionRequest:
    return build_provider_selection_request(DataProviderKind.MARKET_DATA, capability, ProviderDataDomain.EQUITY_US, symbol)

def validate_provider_request_plan(request: ProviderSelectionRequest) -> list[str]:
    errs = []
    if not request.metadata_only: errs.append("metadata_only must be true")
    if request.allow_network: errs.append("allow_network must be false")
    return errs

def provider_request_plan_summary(request: ProviderSelectionRequest) -> dict[str, Any]:
    return {"kind": request.provider_kind}

def provider_request_plan_to_text(request: ProviderSelectionRequest) -> str:
    return f"Request {request.selection_id}"
