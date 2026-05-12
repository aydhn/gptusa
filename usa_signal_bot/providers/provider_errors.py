from usa_signal_bot.core.enums import ProviderErrorType
from usa_signal_bot.providers.provider_models import ProviderResponse

class ProviderError(Exception):
    pass

class ProviderConfigError(ProviderError):
    pass

class ProviderCapabilityError(ProviderError):
    pass

class ProviderValidationError(ProviderError):
    pass

class ProviderQualityError(ProviderError):
    pass

class ProviderRoutingError(ProviderError):
    pass

class ProviderStorageError(ProviderError):
    pass

class ProviderReportingError(ProviderError):
    pass

class YFinanceProviderError(ProviderError):
    pass

class LocalCacheProviderError(ProviderError):
    pass

class LocalFixtureProviderError(ProviderError):
    pass

class ManualFileProviderError(ProviderError):
    pass

def classify_provider_exception(exc: Exception) -> ProviderErrorType:
    exc_str = str(exc).lower()
    if "timeout" in exc_str:
        return ProviderErrorType.TIMEOUT
    if "rate limit" in exc_str or "429" in exc_str:
        return ProviderErrorType.RATE_LIMIT
    if "connection" in exc_str or "network" in exc_str or "socket" in exc_str:
        return ProviderErrorType.NETWORK_ERROR
    return ProviderErrorType.UNKNOWN

def classify_provider_response_error(response: ProviderResponse) -> ProviderErrorType | None:
    if response.row_count == 0:
        return ProviderErrorType.EMPTY_RESPONSE
    # We can refine this based on the status/warnings later
    return None

def provider_error_type_to_message(error_type: ProviderErrorType) -> str:
    messages = {
        ProviderErrorType.NETWORK_ERROR: "Network connection failed",
        ProviderErrorType.TIMEOUT: "Provider request timed out",
        ProviderErrorType.RATE_LIMIT: "Provider rate limit exceeded",
        ProviderErrorType.EMPTY_RESPONSE: "Provider returned an empty response",
        ProviderErrorType.INVALID_SCHEMA: "Response failed schema validation",
        ProviderErrorType.INVALID_OHLCV: "Response failed OHLCV consistency checks",
        ProviderErrorType.STALE_DATA: "Provider returned stale data",
        ProviderErrorType.MISSING_SYMBOL: "Requested symbol not found by provider",
        ProviderErrorType.UNSUPPORTED_CAPABILITY: "Provider does not support requested capability",
        ProviderErrorType.CONFIG_ERROR: "Provider configuration error",
        ProviderErrorType.UNKNOWN: "Unknown provider error"
    }
    return messages.get(error_type, "Unknown provider error")

def provider_error_is_retryable(error_type: ProviderErrorType) -> bool:
    return error_type in [
        ProviderErrorType.NETWORK_ERROR,
        ProviderErrorType.TIMEOUT,
        ProviderErrorType.RATE_LIMIT
    ]

def provider_error_is_fallback_candidate(error_type: ProviderErrorType) -> bool:
    return error_type in [
        ProviderErrorType.NETWORK_ERROR,
        ProviderErrorType.TIMEOUT,
        ProviderErrorType.RATE_LIMIT,
        ProviderErrorType.EMPTY_RESPONSE,
        ProviderErrorType.STALE_DATA,
        ProviderErrorType.MISSING_SYMBOL,
        ProviderErrorType.INVALID_SCHEMA,
        ProviderErrorType.INVALID_OHLCV
    ]
