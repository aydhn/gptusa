
from typing import Any
from usa_signal_bot.core.enums import DataProviderName, DataProviderKind

def build_free_provider_candidate_catalog() -> list[dict[str, Any]]:
    return [
        {
            "name": DataProviderName.YFINANCE,
            "kind": DataProviderKind.MARKET_DATA,
            "free_candidate": True,
            "scraping_required": False,
            "paid_api": False,
            "requires_api_key": False,
            "network_future_possible": True,
        },
        {
            "name": DataProviderName.STOOQ,
            "kind": DataProviderKind.MARKET_DATA,
            "free_candidate": True,
            "scraping_required": False,
            "paid_api": False,
            "requires_api_key": False,
            "csv_download_style": True,
            "network_future_possible": True,
        },
        {
            "name": DataProviderName.NASDAQ_DATA_LINK_FREE,
            "kind": DataProviderKind.FUNDAMENTAL_DATA,
            "free_candidate": True,
            "scraping_required": False,
            "paid_api": False,
            "credential_required_now": False,
            "network_future_possible": True,
        },
        {
            "name": DataProviderName.FRED_COMPATIBLE,
            "kind": DataProviderKind.MACRO_DATA,
            "free_candidate": True,
            "scraping_required": False,
            "paid_api": False,
            "credential_required_now": False,
            "network_future_possible": True,
        },
        {
            "name": DataProviderName.SEC_COMPANY_FACTS,
            "kind": DataProviderKind.FUNDAMENTAL_DATA,
            "free_candidate": True,
            "scraping_required": False,
            "html_parse_required": False,
            "paid_api": False,
            "requires_api_key": False,
            "network_future_possible": True,
        },
        {
            "name": DataProviderName.LOCAL_CSV,
            "kind": DataProviderKind.LOCAL_FIXTURE,
            "free_candidate": True,
            "local_fixture": True,
            "network_future_possible": False,
        }
    ]

def provider_catalog_entry(provider_name: DataProviderName) -> dict[str, Any] | None:
    for entry in build_free_provider_candidate_catalog():
        if entry["name"] == provider_name:
            return entry
    return None

def validate_provider_catalog_safety(catalog: list[dict[str, Any]]) -> list[str]:
    errs = []
    for entry in catalog:
        if entry.get("paid_api", False): errs.append(f"{entry['name']} paid_api=True")
        if entry.get("scraping_required", False): errs.append(f"{entry['name']} scraping_required=True")
        if entry.get("html_parse_required", False): errs.append(f"{entry['name']} html_parse_required=True")
    return errs

def provider_catalog_summary(catalog: list[dict[str, Any]]) -> dict[str, Any]:
    return {"count": len(catalog), "safe": len(validate_provider_catalog_safety(catalog)) == 0}

def provider_catalog_to_text(catalog: list[dict[str, Any]], limit: int = 200) -> str:
    return str(catalog)[:limit]
