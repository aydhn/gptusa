"""Core custom exceptions for USA Signal Bot."""

class USASignalBotError(Exception):
    """Base exception for all USA Signal Bot errors."""
    pass

class ConfigError(USASignalBotError):
    """Raised when there is a configuration issue."""
    pass

class PathError(USASignalBotError):
    """Raised when a directory or file path issue occurs."""
    pass

class DataValidationError(USASignalBotError):
    """Raised when data fails validation rules."""
    pass

class UnsupportedOperationError(USASignalBotError):
    """Raised for general unsupported operations."""
    pass

class BrokerRoutingForbiddenError(USASignalBotError):
    """Strictly raised if broker routing is attempted."""
    pass

class WebScrapingForbiddenError(USASignalBotError):
    """Strictly raised if web scraping is attempted."""
    pass
