PROVIDER_NOT_CONFIGURED = "PROVIDER_NOT_CONFIGURED"
PROVIDER_DISABLED = "PROVIDER_DISABLED"
NETWORK_DISABLED = "NETWORK_DISABLED"
PAID_API_BLOCKED = "PAID_API_BLOCKED"
SCRAPING_BLOCKED = "SCRAPING_BLOCKED"
RATE_LIMIT_UNKNOWN = "RATE_LIMIT_UNKNOWN"
INVALID_REQUEST = "INVALID_REQUEST"
UNSUPPORTED_CAPABILITY = "UNSUPPORTED_CAPABILITY"
DATA_UNAVAILABLE = "DATA_UNAVAILABLE"
CACHE_MISS = "CACHE_MISS"
QUALITY_WARNING = "QUALITY_WARNING"
UNKNOWN_PROVIDER_ERROR = "UNKNOWN_PROVIDER_ERROR"

def provider_error_code_description(code: str) -> str:
    descriptions = {
        PROVIDER_NOT_CONFIGURED: "Provider is not fully configured.",
        PROVIDER_DISABLED: "Provider is disabled in config.",
        NETWORK_DISABLED: "Network fetch is disabled.",
        PAID_API_BLOCKED: "Paid API usage is blocked.",
        SCRAPING_BLOCKED: "Web scraping is blocked.",
        RATE_LIMIT_UNKNOWN: "Rate limit metadata is unknown.",
        INVALID_REQUEST: "The data request is invalid.",
        UNSUPPORTED_CAPABILITY: "The requested capability is not supported.",
        DATA_UNAVAILABLE: "Data is not available from this provider.",
        CACHE_MISS: "Data was not found in cache.",
        QUALITY_WARNING: "Data quality does not meet required thresholds.",
        UNKNOWN_PROVIDER_ERROR: "An unknown provider error occurred."
    }
    return descriptions.get(code, "Unknown error code")

def provider_error_is_blocking(code: str) -> bool:
    blocking_codes = [
        PAID_API_BLOCKED, SCRAPING_BLOCKED, INVALID_REQUEST, UNSUPPORTED_CAPABILITY
    ]
    return code in blocking_codes

def provider_error_taxonomy_to_text() -> str:
    return "Provider Error Taxonomy initialized."
