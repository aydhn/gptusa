import time
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any

from usa_signal_bot.core.enums import DataProviderName, ProviderResponseStatus
from usa_signal_bot.providers.provider_models import (
    ProviderCapabilityProfile, ProviderHealthResult, ProviderRequest,
    ProviderResponse, create_provider_response_id
)

class BaseDataProvider(ABC):
    @abstractmethod
    def name(self) -> DataProviderName:
        pass

    @abstractmethod
    def capability_profile(self) -> ProviderCapabilityProfile:
        pass

    @abstractmethod
    def fetch(self, request: ProviderRequest) -> ProviderResponse:
        pass

    @abstractmethod
    def health_check(self) -> ProviderHealthResult:
        pass

    def supports(self, request: ProviderRequest) -> bool:
        from usa_signal_bot.providers.provider_capabilities import provider_supports_request
        return provider_supports_request(self.capability_profile(), request)


def build_empty_provider_response(
    request: ProviderRequest,
    provider_name: DataProviderName,
    status: ProviderResponseStatus,
    message: str
) -> ProviderResponse:
    now_utc = datetime.now(timezone.utc).isoformat()
    return ProviderResponse(
        response_id=create_provider_response_id(),
        request_id=request.request_id,
        provider_name=provider_name,
        status=status,
        created_at_utc=now_utc,
        symbol_count=len(request.symbols),
        row_count=0,
        data={},
        latency_ms=0.0,
        warnings=[message] if status in [ProviderResponseStatus.PARTIAL, ProviderResponseStatus.STALE] else [],
        errors=[message] if status in [ProviderResponseStatus.FAILED, ProviderResponseStatus.INVALID, ProviderResponseStatus.EMPTY, ProviderResponseStatus.BLOCKED] else []
    )

def measure_provider_latency_ms(start_perf: float, end_perf: float) -> float:
    latency = (end_perf - start_perf) * 1000.0
    return max(0.0, latency)

def normalize_provider_symbols(symbols: list[str]) -> list[str]:
    return list(dict.fromkeys([s.strip().upper() for s in symbols if s and s.strip()]))
