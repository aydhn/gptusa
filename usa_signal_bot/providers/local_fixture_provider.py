import json
import time
from datetime import datetime, timezone
from pathlib import Path

from usa_signal_bot.core.enums import (
    DataProviderName, ProviderRequestType, ProviderResponseStatus, ProviderQualityStatus
)
from usa_signal_bot.providers.provider_capabilities import local_fixture_capability_profile
from usa_signal_bot.providers.provider_interface import (
    BaseDataProvider, build_empty_provider_response, measure_provider_latency_ms,
    normalize_provider_symbols
)
from usa_signal_bot.providers.provider_models import (
    ProviderCapabilityProfile, ProviderHealthResult, ProviderRequest, ProviderResponse,
    create_provider_response_id, create_provider_health_id
)

class LocalFixtureDataProvider(BaseDataProvider):
    def __init__(self, fixture_root: Path):
        self.fixture_root = Path(fixture_root)

    def name(self) -> DataProviderName:
        return DataProviderName.LOCAL_FIXTURE

    def capability_profile(self) -> ProviderCapabilityProfile:
        return local_fixture_capability_profile()

    def fetch(self, request: ProviderRequest) -> ProviderResponse:
        start_time = time.perf_counter()

        if not self.supports(request):
            return build_empty_provider_response(
                request, self.name(), ProviderResponseStatus.FAILED, f"Unsupported request type: {request.request_type}"
            )

        if request.request_type == ProviderRequestType.OHLCV:
            response = self.fetch_ohlcv_fixture(request)
        else:
            response = build_empty_provider_response(
                request, self.name(), ProviderResponseStatus.FAILED, f"Unimplemented request type: {request.request_type}"
            )

        response.latency_ms = measure_provider_latency_ms(start_time, time.perf_counter())
        return response

    def fetch_ohlcv_fixture(self, request: ProviderRequest) -> ProviderResponse:
        symbols = normalize_provider_symbols(request.symbols)
        if not symbols:
            return build_empty_provider_response(request, self.name(), ProviderResponseStatus.FAILED, "No valid symbols provided")

        now_utc = datetime.now(timezone.utc).isoformat()

        data_dict = {}
        total_rows = 0

        return build_empty_provider_response(
            request, self.name(), ProviderResponseStatus.EMPTY, "Fixture read not implemented"
        )


    def health_check(self) -> ProviderHealthResult:
        now_utc = datetime.now(timezone.utc).isoformat()

        reachable = self.fixture_root.exists() and self.fixture_root.is_dir()
        status = ProviderQualityStatus.GOOD if reachable else ProviderQualityStatus.POOR

        return ProviderHealthResult(
            health_id=create_provider_health_id(),
            provider_name=self.name(),
            checked_at_utc=now_utc,
            status=status,
            reachable=reachable,
            capability_status={c.value: reachable for c in self.capability_profile().capabilities},
            warnings=[] if reachable else [f"Fixture root {self.fixture_root} does not exist"]
        )
