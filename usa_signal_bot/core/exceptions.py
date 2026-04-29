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

class StorageError(USASignalBotError):
    """Base exception for all storage errors."""
    pass

class StorageReadError(StorageError):
    """Raised when an error occurs while reading from storage."""
    pass

class StorageWriteError(StorageError):
    """Raised when an error occurs while writing to storage."""
    pass

class StoragePathError(StorageError):
    """Raised when there is an issue with a storage path (e.g. traversal attempt)."""
    pass

class StorageIntegrityError(StorageError):
    """Raised when a file's integrity check fails."""
    pass

class UniverseError(USASignalBotError):
    """Base exception for universe operations."""
    pass

class UniverseLoadError(UniverseError):
    """Exception raised when universe data cannot be loaded."""
    pass

class UniverseValidationError(UniverseError):
    """Exception raised when a universe fails validation."""
    pass

class SymbolValidationError(UniverseError):
    """Exception raised when a symbol fails validation."""
    pass

class DataProviderError(USASignalBotError):
    pass

class ProviderNotFoundError(DataProviderError):
    pass

class ProviderRegistrationError(DataProviderError):
    pass

class ProviderCapabilityError(DataProviderError):
    pass

class ProviderPolicyError(DataProviderError):
    pass

class ProviderRequestError(DataProviderError):
    pass

class ProviderFetchError(DataProviderError):
    pass

class ForbiddenProviderError(DataProviderError):
    pass

class DataNormalizationError(DataProviderError):
    """Raised when data cannot be normalized to project standards."""
    pass

class DataQualityError(DataProviderError):
    """Raised when data fails quality checks."""
    pass

class DataCacheError(StorageError):
    """Raised when an error occurs reading or writing to market data cache."""
    pass

class MarketDataDownloadError(DataProviderError):
    """Raised when a download operation fails."""
    pass
