
from typing import Any
from usa_signal_bot.data_providers.phase106_models import ProviderAdapterSpec, ProviderRegistryEntry

def validate_provider_adapter_spec(spec: ProviderAdapterSpec) -> list[str]:
    errs = []
    if spec.paid_api: errs.append("paid_api true")
    if spec.scraping_required: errs.append("scraping_required true")
    if spec.html_parsing_required: errs.append("html_parsing_required true")
    if spec.broker_related: errs.append("broker_related true")
    if spec.order_related: errs.append("order_related true")
    if spec.network_fetch_enabled_now: errs.append("network_fetch_enabled_now true")
    if spec.credential_required_now: errs.append("credential_required_now true")
    return errs

def validate_provider_adapter_class(adapter: Any) -> list[str]:
    errs = []
    unsafe_words = ["order", "broker", "trade", "scrape", "html", "selenium", "playwright", "live", "paper_order"]
    for attr_name in dir(adapter):
        if any(w in attr_name.lower() for w in unsafe_words):
            errs.append(f"Unsafe method: {attr_name}")
    return errs

def validate_all_provider_adapters(entries: list[ProviderRegistryEntry]) -> list[str]:
    return []

def provider_adapter_validator_summary(errors: list[str]) -> dict[str, Any]:
    return {"errors": len(errors)}

def provider_adapter_validator_to_text(errors: list[str]) -> str:
    return str(errors)
