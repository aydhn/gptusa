from usa_signal_bot.core.exceptions import DataProviderError

def provider_error_to_message(exc: Exception) -> str:
    if isinstance(exc, DataProviderError):
        return f"Provider Error ({exc.__class__.__name__}): {str(exc)}"
    return f"Unexpected Error: {str(exc)}"
