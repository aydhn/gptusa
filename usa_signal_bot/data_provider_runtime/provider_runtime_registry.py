from typing import Any, Optional, Dict, List
from datetime import datetime, timezone

from usa_signal_bot.data_provider_runtime.phase107_models import (
    ProviderRuntimeAdapterSpec,
    create_provider_runtime_adapter_id
)
from usa_signal_bot.core.enums import ProviderImplementationStatus, ProviderFetchMode


def build_provider_runtime_adapter_specs() -> List[ProviderRuntimeAdapterSpec]:
    specs = []

    yfinance = ProviderRuntimeAdapterSpec(
        runtime_adapter_id=create_provider_runtime_adapter_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        provider_name="YFINANCE",
        adapter_module="usa_signal_bot.data_providers.adapters.yfinance_adapter",
        adapter_class="YFinanceMarketDataAdapter",
        implementation_status=ProviderImplementationStatus.IMPLEMENTED_NETWORK_GUARDED,
        fetch_mode=ProviderFetchMode.NETWORK_GUARDED_DISABLED,
        supports_contract_tests=True,
        supports_cache_key=True,
        supports_cache_lookup_dry_run=True,
        supports_local_fixture=False,
        supports_ohlcv_schema=True,
        network_guarded=True,
        network_enabled_by_default=False,
        paid_api=False,
        scraping_required=False,
        html_parsing_required=False,
        credential_required_now=False,
        broker_related=False,
        order_related=False,
        paper_mutation_related=False
    )
    specs.append(yfinance)

    stooq = ProviderRuntimeAdapterSpec(
        runtime_adapter_id=create_provider_runtime_adapter_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        provider_name="STOOQ",
        adapter_module="usa_signal_bot.data_providers.adapters.stooq_adapter",
        adapter_class="StooqMarketDataAdapter",
        implementation_status=ProviderImplementationStatus.IMPLEMENTED_NETWORK_GUARDED,
        fetch_mode=ProviderFetchMode.NETWORK_GUARDED_DISABLED,
        supports_contract_tests=True,
        supports_cache_key=True,
        supports_cache_lookup_dry_run=True,
        supports_local_fixture=False,
        supports_ohlcv_schema=True,
        network_guarded=True,
        network_enabled_by_default=False,
        paid_api=False,
        scraping_required=False,
        html_parsing_required=False,
        credential_required_now=False,
        broker_related=False,
        order_related=False,
        paper_mutation_related=False
    )
    specs.append(stooq)

    local_csv = ProviderRuntimeAdapterSpec(
        runtime_adapter_id=create_provider_runtime_adapter_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        provider_name="LOCAL_CSV",
        adapter_module="usa_signal_bot.data_providers.adapters.local_csv_adapter",
        adapter_class="LocalCsvMarketDataAdapter",
        implementation_status=ProviderImplementationStatus.IMPLEMENTED_LOCAL_FIXTURE,
        fetch_mode=ProviderFetchMode.LOCAL_FIXTURE_ONLY,
        supports_contract_tests=True,
        supports_cache_key=False,
        supports_cache_lookup_dry_run=False,
        supports_local_fixture=True,
        supports_ohlcv_schema=True,
        network_guarded=False,
        network_enabled_by_default=False,
        paid_api=False,
        scraping_required=False,
        html_parsing_required=False,
        credential_required_now=False,
        broker_related=False,
        order_related=False,
        paper_mutation_related=False
    )
    specs.append(local_csv)

    return specs

def provider_runtime_spec_for_name(provider_name: str) -> Optional[ProviderRuntimeAdapterSpec]:
    specs = build_provider_runtime_adapter_specs()
    for spec in specs:
        if spec.provider_name.upper() == provider_name.upper():
            return spec
    return None

def validate_provider_runtime_registry(specs: List[ProviderRuntimeAdapterSpec]) -> List[str]:
    errors = []
    for spec in specs:
        if spec.network_enabled_by_default:
            errors.append(f"{spec.provider_name} has network_enabled_by_default=True")
        if spec.paid_api:
            errors.append(f"{spec.provider_name} has paid_api=True")
        if spec.scraping_required:
            errors.append(f"{spec.provider_name} has scraping_required=True")
        if spec.html_parsing_required:
            errors.append(f"{spec.provider_name} has html_parsing_required=True")
        if spec.credential_required_now:
            errors.append(f"{spec.provider_name} has credential_required_now=True")
        if spec.broker_related or spec.order_related or spec.paper_mutation_related:
            errors.append(f"{spec.provider_name} is broker/order/mutation related")
    return errors

def provider_runtime_registry_summary(specs: List[ProviderRuntimeAdapterSpec]) -> Dict[str, Any]:
    return {
        "count": len(specs),
        "providers": [s.provider_name for s in specs]
    }

def provider_runtime_registry_to_text(specs: List[ProviderRuntimeAdapterSpec], limit: int = 200) -> str:
    lines = [
        "=== Provider Runtime Registry ===",
        f"Count: {len(specs)}",
        ""
    ]
    for spec in specs[:limit]:
        lines.append(f"- {spec.provider_name}: {spec.implementation_status.value}")
    if len(specs) > limit:
        lines.append(f"... and {len(specs) - limit} more")
    return "\n".join(lines)
