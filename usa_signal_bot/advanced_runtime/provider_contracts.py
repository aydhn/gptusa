from typing import Any
from usa_signal_bot.advanced_runtime.phase102_models import (
    ProviderDataRequest, ProviderDataResponse, ProviderInterfaceKind, ProviderCapability,
    create_provider_data_request_id, create_provider_data_response_id
)

def build_provider_data_request(
    provider_name: str,
    interface_kind: ProviderInterfaceKind,
    capability: ProviderCapability,
    symbol: str | None = None,
    symbols: list[str] | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    interval: str | None = None,
    adjusted: bool = True,
    metadata_only: bool = True,
    allow_network: bool = False,
    allow_cache: bool = True,
    parameters: dict[str, Any] | None = None
) -> ProviderDataRequest:
    return ProviderDataRequest(
        request_id=create_provider_data_request_id(),
        provider_name=provider_name,
        interface_kind=interface_kind,
        capability=capability,
        symbol=symbol,
        symbols=symbols or [],
        start_date=start_date,
        end_date=end_date,
        interval=interval,
        adjusted=adjusted,
        metadata_only=metadata_only,
        allow_network=allow_network,
        allow_cache=allow_cache,
        parameters=parameters or {},
        metadata={}
    )

def build_provider_data_response(
    request: ProviderDataRequest,
    success: bool,
    data: Any | None = None,
    rows_returned: int = 0,
    from_cache: bool = False,
    network_used: bool = False,
    warnings: list[str] | None = None,
    errors: list[str] | None = None
) -> ProviderDataResponse:
    return ProviderDataResponse(
        response_id=create_provider_data_response_id(),
        request_id=request.request_id,
        provider_name=request.provider_name,
        success=success,
        rows_returned=rows_returned,
        from_cache=from_cache,
        network_used=network_used,
        data=data,
        data_quality_hints={},
        warnings=warnings or [],
        errors=errors or [],
        metadata={}
    )

def validate_provider_data_request(request: ProviderDataRequest) -> list[str]:
    errors = []
    if request.metadata_only and request.allow_network:
        errors.append("metadata_only=True conflicts with allow_network=True")
    if 'broker' in str(request.parameters).lower() or 'order' in str(request.parameters).lower():
        errors.append("Request contains broker/order parameters")
    return errors

def validate_provider_data_response(response: ProviderDataResponse) -> list[str]:
    errors = []
    if response.network_used:
        errors.append("network_used is true, which is not allowed in Phase 102")
    return errors

def provider_contract_summary(request: ProviderDataRequest, response: ProviderDataResponse | None = None) -> dict[str, Any]:
    return {
        "request_id": request.request_id,
        "provider": request.provider_name,
        "capability": request.capability.value,
        "response_present": response is not None,
        "success": response.success if response else False
    }
