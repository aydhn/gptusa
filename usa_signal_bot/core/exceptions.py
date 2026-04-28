"""Core exception classes for USA Signal Bot."""

class USASignalBotError(Exception):
    """Base exception for all USA Signal Bot errors."""
    pass

class ConfigError(USASignalBotError):
    """Raised when there is a configuration error."""
    pass

class PathError(USASignalBotError):
    """Raised when there is an error with file paths or directories."""
    pass

class DataValidationError(USASignalBotError):
    """Raised when data validation fails."""
    def __init__(self, message: str):
        super().__init__(f"Data validation error: {message}")

class UnsupportedOperationError(USASignalBotError):
    """Raised when an operation is not supported."""
    pass

class BrokerRoutingForbiddenError(UnsupportedOperationError):
    """Raised when an attempt is made to route orders to a live broker."""
    pass

class WebScrapingForbiddenError(UnsupportedOperationError):
    """Raised when an attempt is made to perform web scraping."""
    pass

class EnvironmentConfigError(ConfigError):
    """Raised when environment variables are misconfigured."""
    pass

class RuntimeInitializationError(USASignalBotError):
    """Raised when runtime initialization fails."""
    pass

class ValidationError(USASignalBotError):
    """Raised for general validation errors."""
    pass

class SecretHandlingError(USASignalBotError):
    """Raised when there's an error handling secrets."""
    pass

class AuditError(USASignalBotError):
    """Raised when there's an error writing to the audit trail."""
    pass

class LoggingSetupError(USASignalBotError):
    """Raised when logging configuration fails."""
    pass

class HealthCheckError(USASignalBotError):
    """Raised when a health check fails."""
    pass
