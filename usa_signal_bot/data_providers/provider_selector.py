
from typing import Any
from usa_signal_bot.data_providers.phase106_models import (
    ProviderSelectionRequest, ProviderSelectionResult, ProviderRegistryEntry, ProviderSafetyPolicy,
    create_provider_selection_result_id, _now
)
from usa_signal_bot.core.enums import DataProviderKind, DataProviderCapability, ProviderDataDomain, ProviderSelectorMode

class ProviderSelector:
    def __init__(self, registry_entries: list[ProviderRegistryEntry] | None = None, safety_policy: ProviderSafetyPolicy | None = None):
        self.registry_entries = registry_entries or []
        self.safety_policy = safety_policy

    def select(self, request: ProviderSelectionRequest) -> ProviderSelectionResult:
        errs = self.validate_selection_request(request)
        return ProviderSelectionResult(
            result_id=create_provider_selection_result_id(),
            created_at_utc=_now(),
            selection_id=request.selection_id,
            selected_provider=None,
            selected_entry_id=None,
            fallback_providers=[],
            selection_safe=len(errs) == 0,
            metadata_only=True,
            network_used=False,
            paid_api_used=False,
            scraping_used=False,
            broker_used=False,
            order_created=False,
            errors=errs
        )

    def select_provider(self, provider_kind: DataProviderKind, capability: DataProviderCapability, domain: ProviderDataDomain, selector_mode: ProviderSelectorMode = ProviderSelectorMode.METADATA_ONLY) -> ProviderSelectionResult:
        return self.select(ProviderSelectionRequest(
            selection_id="temp", created_at_utc=_now(), provider_kind=provider_kind, capability=capability,
            domain=domain, selector_mode=selector_mode, symbol=None, metadata_only=True,
            allow_network=False, allow_paid_api=False, allow_scraping=False, allow_broker=False, allow_order=False
        ))

    def available_providers(self, provider_kind: DataProviderKind | None = None, capability: DataProviderCapability | None = None) -> list[ProviderRegistryEntry]:
        return []

    def validate_selection_request(self, request: ProviderSelectionRequest) -> list[str]:
        errs = []
        if request.allow_network: errs.append("allow_network must be false")
        if request.allow_paid_api: errs.append("allow_paid_api must be false")
        if request.allow_scraping: errs.append("allow_scraping must be false")
        return errs

    def selector_summary(self) -> dict[str, Any]:
        return {"entries": len(self.registry_entries)}
