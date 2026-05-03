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

class DataRepairError(DataProviderError):
    """Raised when data repair fails."""
    pass

class CacheRefreshError(StorageError):
    """Raised when cache refresh fails."""
    pass

class CacheValidationError(StorageError):
    """Raised when cache validation fails."""
    pass

class DataAnomalyError(DataProviderError):
    """Raised when a data anomaly is detected."""
    pass

class MultiTimeframeError(USASignalBotError):
    """Raised when there is an error in multi-timeframe processing."""
    pass

class DataCoverageError(USASignalBotError):
    """Raised when there is an error calculating or verifying data coverage."""
    pass

class DataReadinessError(USASignalBotError):
    """Raised when data readiness requirements are not met."""
    pass

class DataPipelineError(USASignalBotError):
    """Raised when there is an error in the data pipeline orchestration."""
    pass

class UniverseSourceError(USASignalBotError):
    pass

class UniverseImportError(USASignalBotError):
    pass

class UniverseReconciliationError(USASignalBotError):
    pass

class UniverseSnapshotError(USASignalBotError):
    pass

class UniverseCatalogError(USASignalBotError):
    pass

class UniverseExportError(USASignalBotError):
    pass


class ActiveUniverseError(UniverseError):
    pass

class ActiveUniverseResolutionError(ActiveUniverseError):
    pass

class UniverseReadinessGateError(USASignalBotError):
    pass

class UniverseDataRunError(USASignalBotError):
    pass

class ActiveUniversePipelineError(USASignalBotError):
    pass

class FeatureError(USASignalBotError):
    pass

class IndicatorError(FeatureError):
    pass

class IndicatorRegistrationError(IndicatorError):
    pass

class IndicatorParameterError(IndicatorError):
    pass

class FeatureInputError(FeatureError):
    pass

class FeatureComputationError(FeatureError):
    pass

class FeatureValidationError(FeatureError):
    pass

class FeatureStorageError(FeatureError):
    pass

class TrendFeatureError(FeatureError):
    pass

class TrendIndicatorError(IndicatorError):
    pass

class IndicatorSetError(FeatureError):
    pass

class MomentumFeatureError(FeatureError):
    pass
class MomentumIndicatorError(IndicatorError):
    pass
class MomentumIndicatorSetError(IndicatorSetError):
    pass


class VolatilityFeatureError(FeatureComputationError):
    pass

class VolatilityIndicatorError(IndicatorError):
    pass

class VolatilityIndicatorSetError(FeatureComputationError):
    pass

class DivergenceFeatureError(FeatureError):
    """Base class for divergence feature errors."""
    pass

class DivergenceIndicatorError(DivergenceFeatureError):
    """Raised when a divergence indicator encounters an error."""
    pass

class DivergenceIndicatorSetError(DivergenceFeatureError):
    """Raised for errors related to divergence indicator sets."""
    pass

class DivergenceDetectionError(DivergenceFeatureError):
    """Raised during divergence detection failures."""
    pass

class PivotDetectionError(DivergenceFeatureError):
    """Raised during pivot point detection failures."""
    pass

class CompositeFeatureError(FeatureError):
    pass

class FeatureGroupError(CompositeFeatureError):
    pass

class FeaturePipelineError(CompositeFeatureError):
    pass

class FeatureCheckpointError(CompositeFeatureError):
    pass

class CompositeFeatureValidationError(FeatureValidationError):
    pass

class StrategyError(USASignalBotError):
    pass

class StrategyMetadataError(StrategyError):
    pass

class StrategyParameterError(StrategyError):
    pass

class StrategyRegistrationError(StrategyError):
    pass

class StrategyInputError(StrategyError):
    pass

class StrategyExecutionError(StrategyError):
    pass

class SignalContractError(StrategyError):
    pass

class SignalValidationError(StrategyError):
    pass

class SignalStorageError(StrategyError):
    pass


class SignalScoringError(USASignalBotError):
    """Raised when an error occurs during signal scoring."""
    pass

class SignalQualityError(USASignalBotError):
    """Raised when an error occurs in the signal quality guard."""
    pass

class SignalConfluenceError(USASignalBotError):
    """Raised when an error occurs in the confluence engine."""
    pass

class SignalRiskFlagError(USASignalBotError):
    """Raised when an error occurs assigning risk flags."""
    pass

class SignalQualityGuardError(USASignalBotError):
    """Raised when a critical quality guard fails."""
    pass

class RuleStrategyError(USASignalBotError):
    pass

class RuleConditionError(RuleStrategyError):
    pass

class RuleEvaluationError(RuleStrategyError):
    pass

class RuleStrategySetError(RuleStrategyError):
    pass

class RuleFeatureRequirementError(RuleStrategyError):
    pass

class SignalRankingError(USASignalBotError):
    pass

class CandidateSelectionError(USASignalBotError):
    pass

class StrategyPortfolioError(USASignalBotError):
    pass

class SignalAggregationError(USASignalBotError):
    pass

class RankingStorageError(USASignalBotError):
    pass
