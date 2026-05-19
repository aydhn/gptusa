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


class BacktestError(USASignalBotError):
    pass
class BacktestEventError(BacktestError):
    pass
class BacktestMarketReplayError(BacktestError):
    pass
class BacktestSignalReplayError(BacktestError):
    pass
class BacktestOrderError(BacktestError):
    pass
class BacktestFillError(BacktestError):
    pass
class BacktestPositionError(BacktestError):
    pass
class BacktestPortfolioError(BacktestError):
    pass
class BacktestValidationError(BacktestError):
    pass
class BacktestStorageError(BacktestError):
    pass
class BacktestMetricError(BacktestError):
    pass

class TransactionCostError(USASignalBotError):
    pass
class SlippageModelError(USASignalBotError):
    pass
class TradeLedgerError(USASignalBotError):
    pass
class TradeAnalyticsError(USASignalBotError):
    pass
class DrawdownAnalyticsError(USASignalBotError):
    pass
class AdvancedBacktestMetricError(USASignalBotError):
    pass

class BenchmarkError(USASignalBotError):
    pass

class BenchmarkLoaderError(BenchmarkError):
    pass

class BuyAndHoldError(BenchmarkError):
    pass

class BenchmarkComparisonError(BenchmarkError):
    pass

class PerformanceAttributionError(BenchmarkError):
    pass

class BenchmarkStorageError(BenchmarkError):
    pass


class WalkForwardError(Exception):
    """Base class for Walk Forward exceptions."""
    pass

class WalkForwardWindowError(WalkForwardError):
    """Raised when there is an issue with Walk Forward Windows."""
    pass

class WalkForwardEngineError(WalkForwardError):
    """Raised when there is an issue in the Walk Forward Engine."""
    pass

class WalkForwardMetricError(WalkForwardError):
    """Raised when there is an issue with Walk Forward Metrics."""
    pass

class WalkForwardValidationError(WalkForwardError):
    """Raised when Walk Forward validation fails."""
    pass

class WalkForwardStorageError(WalkForwardError):
    """Raised when there is an issue storing Walk Forward results."""
    pass

class OutOfSampleEvaluationError(WalkForwardError):
    """Raised when there is an issue with Out-of-Sample evaluation."""
    pass

class ParameterSensitivityError(USASignalBotError):
    pass

class ParameterGridError(ParameterSensitivityError):
    pass

class SensitivityRunnerError(ParameterSensitivityError):
    pass

class StabilityMapError(ParameterSensitivityError):
    pass

class SensitivityMetricError(ParameterSensitivityError):
    pass

class SensitivityValidationError(ParameterSensitivityError):
    pass

class SensitivityStorageError(ParameterSensitivityError):
    pass

class NonOptimizerGuardError(ParameterSensitivityError):
    pass


class RiskEngineError(USASignalBotError):
    pass

class RiskLimitError(RiskEngineError):
    pass

class PositionSizingError(RiskEngineError):
    pass

class ExposureGuardError(RiskEngineError):
    pass

class CandidateRiskError(RiskEngineError):
    pass

class RiskValidationError(RiskEngineError):
    pass

class RiskStorageError(RiskEngineError):
    pass

class RiskReportingError(RiskEngineError):
    pass

class PortfolioConstructionError(USASignalBotError):
    pass

class PortfolioCandidateError(PortfolioConstructionError):
    pass

class AllocationMethodError(PortfolioConstructionError):
    pass

class RiskBudgetingError(PortfolioConstructionError):
    pass

class ConcentrationGuardError(PortfolioConstructionError):
    pass

class PortfolioValidationError(PortfolioConstructionError):
    pass

class PortfolioStorageError(PortfolioConstructionError):
    pass

class PortfolioReportingError(PortfolioConstructionError):
    pass


class BasketReplayError(USASignalBotError):
    pass

class BasketSimulationError(USASignalBotError):
    pass

class AllocationReplayError(USASignalBotError):
    pass

class AllocationDriftError(USASignalBotError):
    pass

class BasketMetricError(USASignalBotError):
    pass

class BasketValidationError(USASignalBotError):
    pass

class BasketStorageError(USASignalBotError):
    pass

class BasketReportingError(USASignalBotError):
    pass

class RuntimeOrchestrationError(USASignalBotError):
    pass

class RuntimeLockError(RuntimeOrchestrationError):
    pass

class SafeStopError(RuntimeOrchestrationError):
    pass

class PipelineStepError(RuntimeOrchestrationError):
    pass

class MarketScanError(RuntimeOrchestrationError):
    pass

class ScheduledScanError(RuntimeOrchestrationError):
    pass

class RuntimeValidationError(RuntimeOrchestrationError):
    pass

class RuntimeStorageError(RuntimeOrchestrationError):
    pass

class RuntimeReportingError(RuntimeOrchestrationError):
    pass

class NotificationError(USASignalBotError):
    pass

class NotificationTemplateError(NotificationError):
    pass

class NotificationQueueError(NotificationError):
    pass

class NotificationDispatchError(NotificationError):
    pass

class NotificationRateLimitError(NotificationError):
    pass

class NotificationDedupError(NotificationError):
    pass

class TelegramConfigError(NotificationError):
    pass

class TelegramSendError(NotificationError):
    pass

class NotificationValidationError(NotificationError):
    pass

class NotificationStorageError(NotificationError):
    pass

class NotificationReportingError(NotificationError):
    pass

class PaperTradingError(Exception):
    pass

class VirtualAccountError(PaperTradingError):
    pass

class PaperOrderError(PaperTradingError):
    pass

class PaperOrderLifecycleError(PaperTradingError):
    pass

class PaperFillError(PaperTradingError):
    pass

class PaperPositionError(PaperTradingError):
    pass

class CashLedgerError(PaperTradingError):
    pass

class PaperJournalError(PaperTradingError):
    pass

class PaperPriceResolverError(PaperTradingError):
    pass

class PaperValidationError(PaperTradingError):
    pass

class PaperStorageError(PaperTradingError):
    pass

class PaperReportingError(PaperTradingError):
    pass

class PaperAnalyticsError(USASignalBotError):
    pass

class PaperEquityAnalyticsError(PaperAnalyticsError):
    pass

class PaperDrawdownMonitorError(PaperAnalyticsError):
    pass

class PaperTradeAnalyticsError(PaperAnalyticsError):
    pass

class PaperExposureAnalyticsError(PaperAnalyticsError):
    pass

class PaperRiskReportError(PaperAnalyticsError):
    pass

class PaperRollingMetricsError(PaperAnalyticsError):
    pass

class PaperAnalyticsStorageError(PaperAnalyticsError):
    pass

class PaperAnalyticsValidationError(PaperAnalyticsError):
    pass

class PaperAnalyticsReportingError(PaperAnalyticsError):
    pass

class ComparisonError(USASignalBotError):
    pass

class ResultLoaderError(ComparisonError):
    pass

class TradeMatchingError(ComparisonError):
    pass

class OrderFillMatchingError(ComparisonError):
    pass

class PerformanceGapError(ComparisonError):
    pass

class ExposureGapError(ComparisonError):
    pass

class TimingGapError(ComparisonError):
    pass

class SignalDriftError(ComparisonError):
    pass

class ExecutionRealismError(ComparisonError):
    pass

class ComparisonStorageError(ComparisonError):
    pass

class ComparisonValidationError(ComparisonError):
    pass

class ComparisonReportingError(ComparisonError):
    pass

class QualityScorecardError(USASignalBotError):
    """Raised when a quality scorecard operation fails."""
    pass

class QualityEvaluatorError(USASignalBotError):
    """Raised when a quality evaluator fails."""
    pass

class GateRuleError(USASignalBotError):
    """Raised when a gate rule evaluation fails."""
    pass

class ReadinessGateError(USASignalBotError):
    """Raised when a readiness gate evaluation fails."""
    pass

class AcceptanceEvaluatorError(USASignalBotError):
    """Raised when an acceptance evaluation fails."""
    pass

class QualityStorageError(USASignalBotError):
    """Raised when a quality storage operation fails."""
    pass

class QualityValidationError(USASignalBotError):
    """Raised when a quality validation fails."""
    pass

class QualityReportingError(USASignalBotError):
    """Raised when a quality reporting operation fails."""
    pass

class ArtifactCollectionError(USASignalBotError):
    """Raised when an artifact collection operation fails."""
    pass


class RegressionError(USASignalBotError):
    pass

class GoldenFixtureError(RegressionError):
    pass

class GoldenDatasetError(RegressionError):
    pass

class GoldenSnapshotError(RegressionError):
    pass

class RegressionHarnessError(RegressionError):
    pass

class RegressionDriftError(RegressionError):
    pass

class ReleaseRehearsalError(RegressionError):
    pass

class RegressionStorageError(RegressionError):
    pass

class RegressionValidationError(RegressionError):
    pass

class RegressionReportingError(RegressionError):
    pass

class ReleaseError(USASignalBotError):
    pass

class VersioningError(ReleaseError):
    pass

class ChangelogError(ReleaseError):
    pass

class ReleaseManifestError(ReleaseError):
    pass

class ArtifactCollectorError(ReleaseError):
    pass

class LocalPackagerError(ReleaseError):
    pass

class RunbookGeneratorError(ReleaseError):
    pass

class MaintenanceWorkflowError(ReleaseError):
    pass

class BackupRestoreError(ReleaseError):
    pass

class ConfigProfileError(ReleaseError):
    pass

class UpgradePrecheckError(ReleaseError):
    pass

class ReleaseStorageError(ReleaseError):
    pass

class ReleaseValidationError(ReleaseError):
    pass

class ReleaseReportingError(ReleaseError):
    pass

class ObservabilityError(USASignalBotError):
    pass

class LocalLoggerError(ObservabilityError):
    pass

class LogRotationError(ObservabilityError):
    pass

class MetricsCollectorError(ObservabilityError):
    pass

class OperationalHealthError(ObservabilityError):
    pass

class SafetyMonitorError(ObservabilityError):
    pass

class DiskUsageError(ObservabilityError):
    pass

class ObservabilityStorageError(ObservabilityError):
    pass

class ObservabilityValidationError(ObservabilityError):
    pass

class ObservabilityReportingError(ObservabilityError):
    pass


class IncidentError(USASignalBotError): pass
class IncidentClassifierError(IncidentError): pass
class IncidentAdapterError(IncidentError): pass
class IncidentReportError(IncidentError): pass
class RecoveryPlannerError(USASignalBotError): pass
class RecoveryActionError(RecoveryPlannerError): pass
class RollbackSourceError(USASignalBotError): pass
class RollbackPrecheckError(RollbackSourceError): pass
class RollbackExecutorError(RollbackSourceError): pass
class IncidentAuditError(IncidentError): pass
class IncidentStorageError(IncidentError): pass
class IncidentValidationError(IncidentError): pass
class IncidentReportingError(IncidentError): pass

class SchedulerError(USASignalBotError):
    pass

class RunIdentityError(SchedulerError):
    pass

class RunLockError(SchedulerError):
    pass

class LockHeartbeatError(SchedulerError):
    pass

class StaleLockError(SchedulerError):
    pass

class ConcurrencyPolicyError(SchedulerError):
    pass

class ConcurrencyGuardError(SchedulerError):
    pass

class DuplicateRunGuardError(SchedulerError):
    pass

class IdempotencyError(SchedulerError):
    pass

class AtomicIOError(SchedulerError):
    pass

class SchedulerPlanError(SchedulerError):
    pass

class SchedulerExecutorError(SchedulerError):
    pass

class LockAuditError(SchedulerError):
    pass

class SchedulerStorageError(SchedulerError):
    pass

class SchedulerValidationError(SchedulerError):
    pass

class SchedulerReportingError(SchedulerError):
    pass


class ProfilingError(USASignalBotError):
    pass

class ResourceTimerError(ProfilingError):
    pass

class MemoryProfilingError(ProfilingError):
    pass

class ArtifactGrowthError(ProfilingError):
    pass

class RunMetricsLoaderError(ProfilingError):
    pass

class ResourceProfileCollectorError(ProfilingError):
    pass

class BudgetCalibrationError(ProfilingError):
    pass

class ThrottlingPolicyError(ProfilingError):
    pass

class ThrottlingEngineError(ProfilingError):
    pass

class ProfilingStorageError(ProfilingError):
    pass

class ProfilingValidationError(ProfilingError):
    pass

class ProfilingReportingError(ProfilingError):
    pass

class ProfilingAuditError(ProfilingError):
    pass

class PerformanceBaselineError(USASignalBotError):
    pass

class BaselineBuilderError(PerformanceBaselineError):
    pass

class BaselineCollectorError(PerformanceBaselineError):
    pass

class SLAThresholdError(PerformanceBaselineError):
    pass

class ThresholdEvaluatorError(PerformanceBaselineError):
    pass

class BaselineComparatorError(PerformanceBaselineError):
    pass

class RuntimeRegressionDetectorError(PerformanceBaselineError):
    pass

class BaselineDriftError(PerformanceBaselineError):
    pass

class PerformanceAcceptanceGateError(PerformanceBaselineError):
    pass

class PerformanceAlertRuleError(PerformanceBaselineError):
    pass

class PerformanceBaselineStorageError(PerformanceBaselineError):
    pass

class PerformanceBaselineValidationError(PerformanceBaselineError):
    pass

class PerformanceBaselineReportingError(PerformanceBaselineError):
    pass

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
class ProviderRegistryError(ProviderError):
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

class MarketCalendarError(Exception):
    """Raised for general market calendar errors."""

class SessionClassificationError(Exception):
    """Raised for session classification errors."""

class SessionValidationError(Exception):
    """Raised for session validation errors."""

class HolidayStoreError(Exception):
    """Raised for manual holiday/early-close store errors."""

class CalendarStorageError(Exception):
    """Raised for calendar storage errors."""

class CalendarValidationError(Exception):
    """Raised for calendar validation constraints or assertions."""

class CalendarReportingError(Exception):
    """Raised for calendar reporting issues."""

class CorporateActionError(Exception):
    """Raised for general corporate action errors."""

class CorporateActionLoaderError(Exception):
    """Raised for corporate action loading errors."""

class SplitDetectionError(Exception):
    """Raised for split detection errors."""

class DividendDetectionError(Exception):
    """Raised for dividend detection errors."""

class AdjustedPriceValidationError(Exception):
    """Raised for adjusted price validation errors."""

class CorporateActionGuardError(Exception):
    """Raised for corporate action guard evaluation errors."""

class CorporateActionStorageError(Exception):
    """Raised for corporate action storage errors."""

class CorporateActionValidationError(Exception):
    """Raised for corporate action validation constraints or assertions."""

class CorporateActionReportingError(Exception):
    """Raised for corporate action reporting errors."""

class UniverseLifecycleError(USASignalBotError):
    pass

class LifecycleRegistryError(USASignalBotError):
    pass

class UniverseSnapshotError(USASignalBotError):
    pass

class SymbolAliasError(USASignalBotError):
    pass

class SymbolStatusResolverError(USASignalBotError):
    pass

class DelistingAwarenessError(USASignalBotError):
    pass

class MissingHistoryError(USASignalBotError):
    pass

class StaleSymbolError(USASignalBotError):
    pass

class SurvivorshipBiasGuardError(USASignalBotError):
    pass

class LifecycleStorageError(USASignalBotError):
    pass

class LifecycleValidationError(USASignalBotError):
    pass

class LifecycleReportingError(USASignalBotError):
    pass

class ExecutionRealismError(USASignalBotError):
    pass

class LiquidityMetricError(ExecutionRealismError):
    pass

class SpreadProxyError(ExecutionRealismError):
    pass

class SlippageProxyError(ExecutionRealismError):
    pass

class VolumeParticipationError(ExecutionRealismError):
    pass

class TradabilityGuardError(ExecutionRealismError):
    pass

class BorrowabilityProxyError(ExecutionRealismError):
    pass

class ShortRealismGuardError(ExecutionRealismError):
    pass

class ExecutionStorageError(ExecutionRealismError):
    pass

class ExecutionValidationError(ExecutionRealismError):
    pass

class ExecutionReportingError(ExecutionRealismError):
    pass


class CostRobustnessError(Exception): pass
class CostStressScenarioError(CostRobustnessError): pass
class SlippageStressError(CostRobustnessError): pass
class SpreadStressError(CostRobustnessError): pass
class ImpactStressError(CostRobustnessError): pass
class FeeStressError(CostRobustnessError): pass
class ParticipationStressError(CostRobustnessError): pass
class LiquidityFilterStressError(CostRobustnessError): pass
class FillRealismStressError(CostRobustnessError): pass
class ExecutionSensitivityMatrixError(CostRobustnessError): pass
class WalkForwardCostRobustnessError(CostRobustnessError): pass
class CostFragilityError(CostRobustnessError): pass
class BreakevenCostError(CostRobustnessError): pass
class CostRobustnessStorageError(CostRobustnessError): pass
class CostRobustnessValidationError(CostRobustnessError): pass
class CostRobustnessReportingError(CostRobustnessError): pass

class RegimeAwareCostError(USASignalBotError):
    pass

class VolatilityRegimeCostError(RegimeAwareCostError):
    pass

class LiquidityRegimeCostError(RegimeAwareCostError):
    pass

class SpreadRegimeCostError(RegimeAwareCostError):
    pass

class SessionRegimeCostError(RegimeAwareCostError):
    pass

class LifecycleRegimeCostError(RegimeAwareCostError):
    pass

class CombinedCostRegimeError(RegimeAwareCostError):
    pass

class CostCurveSelectionError(RegimeAwareCostError):
    pass

class AdaptiveExecutionRealismError(RegimeAwareCostError):
    pass

class RegimeCostBreakdownError(RegimeAwareCostError):
    pass

class RegimeCostStorageError(RegimeAwareCostError):
    pass

class RegimeCostValidationError(RegimeAwareCostError):
    pass

class RegimeCostReportingError(RegimeAwareCostError):
    pass


class RegimeMapError(USASignalBotError):
    pass

class TimeframeResamplerError(RegimeMapError):
    pass

class TimeframeRegimeConfirmationError(RegimeMapError):
    pass

class TrendConfirmationError(RegimeMapError):
    pass

class VolatilityConfirmationError(RegimeMapError):
    pass

class MomentumConfirmationError(RegimeMapError):
    pass

class LiquidityConfirmationError(RegimeMapError):
    pass

class BreadthProxyError(RegimeMapError):
    pass

class DispersionProxyError(RegimeMapError):
    pass

class CrossSectionalRegimeMapError(RegimeMapError):
    pass

class SymbolRegimeAlignmentError(RegimeMapError):
    pass

class RegimeTransitionDetectorError(RegimeMapError):
    pass

class RegimeTransitionRiskError(RegimeMapError):
    pass

class RegimeMapStorageError(RegimeMapError):
    pass

class RegimeMapValidationError(RegimeMapError):
    pass

class RegimeMapReportingError(RegimeMapError):
    pass


class StrategyAdaptationError(USASignalBotError):
    pass

class StrategyRegimeProfileError(StrategyAdaptationError):
    pass

class StrategyCompatibilityError(StrategyAdaptationError):
    pass

class StrategyGatingError(StrategyAdaptationError):
    pass

class StrategyConflictResolutionError(StrategyAdaptationError):
    pass

class StrategyEnsembleError(StrategyAdaptationError):
    pass

class AdaptiveStrategyWeightError(StrategyAdaptationError):
    pass

class StrategyAdaptationStorageError(StrategyAdaptationError):
    pass

class StrategyAdaptationValidationError(StrategyAdaptationError):
    pass

class StrategyAdaptationReportingError(StrategyAdaptationError):
    pass


class AdaptiveAllocationError(USASignalBotError):
    pass

class CapitalStateError(AdaptiveAllocationError):
    pass

class RiskBudgetError(AdaptiveAllocationError):
    pass

class ConfidenceScalingError(AdaptiveAllocationError):
    pass

class VolatilitySizingError(AdaptiveAllocationError):
    pass

class DollarRiskSizingError(AdaptiveAllocationError):
    pass

class PositionCapsError(AdaptiveAllocationError):
    pass

class LiquiditySizeAdjustmentError(AdaptiveAllocationError):
    pass

class CostSizeAdjustmentError(AdaptiveAllocationError):
    pass

class RegimeSizeAdjustmentError(AdaptiveAllocationError):
    pass

class DrawdownThrottleError(AdaptiveAllocationError):
    pass

class ConcentrationGuardError(AdaptiveAllocationError):
    pass

class AllocationStorageError(AdaptiveAllocationError):
    pass

class AllocationValidationError(AdaptiveAllocationError):
    pass

class AllocationReportingError(AdaptiveAllocationError):
    pass

class PortfolioRebalanceError(USASignalBotError):
    pass

class PortfolioStateError(PortfolioRebalanceError):
    pass

class TargetPortfolioStateError(PortfolioRebalanceError):
    pass

class DriftCalculationError(PortfolioRebalanceError):
    pass

class ExposureDriftError(PortfolioRebalanceError):
    pass

class BucketDriftError(PortfolioRebalanceError):
    pass

class SignalDecayError(PortfolioRebalanceError):
    pass

class RebalanceThresholdError(PortfolioRebalanceError):
    pass

class TurnoverControlError(PortfolioRebalanceError):
    pass

class TurnoverCostError(PortfolioRebalanceError):
    pass

class DustGuardError(PortfolioRebalanceError):
    pass

class CostAwareRebalanceError(PortfolioRebalanceError):
    pass

class RegimeRebalanceThrottleError(PortfolioRebalanceError):
    pass

class DrawdownRebalanceThrottleError(PortfolioRebalanceError):
    pass

class RebalancePlannerError(PortfolioRebalanceError):
    pass

class RebalanceStorageError(PortfolioRebalanceError):
    pass

class RebalanceValidationError(PortfolioRebalanceError):
    pass

class RebalanceReportingError(PortfolioRebalanceError):
    pass

class AttributionError(USASignalBotError):
    """Base exception for attribution errors."""
    pass

class TradeNormalizationError(AttributionError):
    """Raised when trade normalization fails."""
    pass

class PerformanceAttributionError(AttributionError):
    """Raised when performance attribution calculation fails."""
    pass

class CostAttributionError(AttributionError):
    """Raised when cost attribution calculation fails."""
    pass

class SignalContributionError(AttributionError):
    """Raised when signal contribution calculation fails."""
    pass

class RiskAttributionError(AttributionError):
    """Raised when risk attribution calculation fails."""
    pass

class DrawdownAttributionError(AttributionError):
    """Raised when drawdown attribution calculation fails."""
    pass

class ExposureAttributionError(AttributionError):
    """Raised when exposure attribution calculation fails."""
    pass

class TimeWindowAttributionError(AttributionError):
    """Raised when time window attribution calculation fails."""
    pass

class AttributionScorecardError(AttributionError):
    """Raised when attribution scorecard generation fails."""
    pass

class AttributionStorageError(AttributionError):
    """Raised when attribution storage operations fail."""
    pass

class AttributionValidationError(AttributionError):
    """Raised when attribution validation fails."""
    pass

class AttributionReportingError(AttributionError):
    """Raised when attribution reporting fails."""
    pass


class DiagnosticsError(Exception): pass
class DiagnosticEventNormalizationError(DiagnosticsError): pass
class LossEventAnalysisError(DiagnosticsError): pass
class FalseSignalAnalysisError(DiagnosticsError): pass
class CostDegradationAnalysisError(DiagnosticsError): pass
class RegimeFailureAnalysisError(DiagnosticsError): pass
class LiquidityExecutionFailureError(DiagnosticsError): pass
class SizingFailureAnalysisError(DiagnosticsError): pass
class RebalanceFailureAnalysisError(DiagnosticsError): pass
class DrawdownDiagnosticsError(DiagnosticsError): pass
class StrategyDiagnosticsError(DiagnosticsError): pass
class FailureSignatureMiningError(DiagnosticsError): pass
class FailureClusterRankingError(DiagnosticsError): pass
class RemediationHintError(DiagnosticsError): pass
class DiagnosticScorecardError(DiagnosticsError): pass
class DiagnosticsStorageError(DiagnosticsError): pass
class DiagnosticsValidationError(DiagnosticsError): pass
class DiagnosticsReportingError(DiagnosticsError): pass


class ResearchWorkflowError(USASignalBotError):
    """Base exception for research workflow errors."""
    pass


class RepairQueueError(ResearchWorkflowError):
    """Raised when a repair queue operation fails."""
    pass


class HypothesisTrackerError(ResearchWorkflowError):
    """Raised when a hypothesis tracker operation fails."""
    pass


class ControlledExperimentPlanningError(ResearchWorkflowError):
    """Raised when a controlled experiment planning operation fails."""
    pass


class ExperimentScopeError(ResearchWorkflowError):
    """Raised when an experiment scope operation fails."""
    pass


class AcceptanceGateError(ResearchWorkflowError):
    """Raised when an acceptance gate operation fails."""
    pass


class ParameterChangeProposalError(ResearchWorkflowError):
    """Raised when a parameter change proposal operation fails."""
    pass


class ValidationPlanError(ResearchWorkflowError):
    """Raised when a validation plan operation fails."""
    pass


class SampleSizeGuardError(ResearchWorkflowError):
    """Raised when a sample size guard operation fails."""
    pass


class LeakageOverfitGuardError(ResearchWorkflowError):
    """Raised when a leakage/overfit guard operation fails."""
    pass


class ResearchPriorityScoringError(ResearchWorkflowError):
    """Raised when a research priority scoring operation fails."""
    pass


class DependencyGraphError(ResearchWorkflowError):
    """Raised when a dependency graph operation fails."""
    pass


class RollbackPlanError(ResearchWorkflowError):
    """Raised when a rollback plan operation fails."""
    pass


class ResearchDecisionLogError(ResearchWorkflowError):
    """Raised when a research decision log operation fails."""
    pass


class ResearchWorkflowStorageError(ResearchWorkflowError):
    """Raised when a research workflow storage operation fails."""
    pass


class ResearchWorkflowValidationError(ResearchWorkflowError):
    """Raised when a research workflow validation operation fails."""
    pass


class ResearchWorkflowReportingError(ResearchWorkflowError):
    """Raised when a research workflow reporting operation fails."""
    pass


class ResearchExecutionError(USASignalBotError):
    pass

class ExperimentPlanLoadError(ResearchExecutionError):
    pass

class ConfigSnapshotError(ResearchExecutionError):
    pass

class CandidateOverlayError(ResearchExecutionError):
    pass

class ExperimentRunContextError(ResearchExecutionError):
    pass

class LocalExperimentHarnessError(ResearchExecutionError):
    pass

class BacktestExperimentRunnerError(ResearchExecutionError):
    pass

class WalkForwardExperimentRunnerError(ResearchExecutionError):
    pass

class MockExperimentRunnerError(ResearchExecutionError):
    pass

class RunRegistryError(ResearchExecutionError):
    pass

class ExperimentArtifactError(ResearchExecutionError):
    pass

class MetricsExtractionError(ResearchExecutionError):
    pass

class ResultComparisonError(ResearchExecutionError):
    pass

class GateEvaluationError(ResearchExecutionError):
    pass

class ResearchExecutionStorageError(ResearchExecutionError):
    pass

class ResearchExecutionValidationError(ResearchExecutionError):
    pass

class ResearchExecutionReportingError(ResearchExecutionError):
    pass


class ResearchGovernanceError(USASignalBotError):
    pass
class GovernanceEvidencePackError(ResearchGovernanceError):
    pass
class PromotionReviewError(ResearchGovernanceError):
    pass
class ReleaseCandidateError(ResearchGovernanceError):
    pass
class GovernanceDecisionBoardError(ResearchGovernanceError):
    pass
class GovernanceRiskRegressionError(ResearchGovernanceError):
    pass
class GovernanceChecklistError(ResearchGovernanceError):
    pass
class PromotionDecisionLogError(ResearchGovernanceError):
    pass
class GovernanceAuditTrailError(ResearchGovernanceError):
    pass
class GovernanceStorageError(ResearchGovernanceError):
    pass
class GovernanceValidationError(ResearchGovernanceError):
    pass
class GovernanceReportingError(ResearchGovernanceError):
    pass

class ReleasePackagingError(USASignalBotError):
    pass

class GovernanceIngestionError(ReleasePackagingError):
    pass

class BundleVersioningError(ReleasePackagingError):
    pass

class ArtifactCollectionError(ReleasePackagingError):
    pass

class ArtifactFreezingError(ReleasePackagingError):
    pass

class BundleManifestError(ReleasePackagingError):
    pass

class BundleChecksumError(ReleasePackagingError):
    pass

class BundleSafetyScannerError(ReleasePackagingError):
    pass

class BundleCompatibilityError(ReleasePackagingError):
    pass

class BundleValidationError(ReleasePackagingError):
    pass

class BundleReadmeError(ReleasePackagingError):
    pass

class BundleWriterError(ReleasePackagingError):
    pass

class BundleReaderError(ReleasePackagingError):
    pass

class BundleRegistryError(ReleasePackagingError):
    pass

class BundleDiffError(ReleasePackagingError):
    pass

class RestorePreviewError(ReleasePackagingError):
    pass

class ReleasePackagingStorageError(ReleasePackagingError):
    pass

class ReleasePackagingValidationError(ReleasePackagingError):
    pass

class ReleasePackagingReportingError(ReleasePackagingError):
    pass

class ReleaseSandboxError(USASignalBotError):
    """Base exception for all Release Sandbox errors."""
    pass

class SandboxBundleLoaderError(ReleaseSandboxError):
    """Raised when the bundle loader fails to read or parse files."""
    pass

class ReadOnlyVerifierError(ReleaseSandboxError):
    """Raised when read-only verification fails."""
    pass

class SandboxActivationPlannerError(ReleaseSandboxError):
    """Raised when there is an error in activation planning."""
    pass

class SandboxMountPlannerError(ReleaseSandboxError):
    """Raised when there is an error in mount planning."""
    pass

class SandboxOverlayResolverError(ReleaseSandboxError):
    """Raised when the candidate overlay cannot be resolved safely."""
    pass

class SandboxOutputIsolationError(ReleaseSandboxError):
    """Raised when sandbox output isolation fails."""
    pass

class BlockedOperationGuardError(ReleaseSandboxError):
    """Raised when a blocked operation is attempted in the sandbox."""
    pass

class SandboxRuntimeContextError(ReleaseSandboxError):
    """Raised when there is an error with the sandbox runtime context."""
    pass

class SandboxPreviewRunnerError(ReleaseSandboxError):
    """Raised when the preview runner encounters an error."""
    pass

class SandboxSafetyValidationError(ReleaseSandboxError):
    """Raised when sandbox safety validation fails."""
    pass

class SandboxSessionRegistryError(ReleaseSandboxError):
    """Raised when there is an error with the sandbox session registry."""
    pass

class ReleaseSandboxStorageError(ReleaseSandboxError):
    """Raised when there is an error reading or writing sandbox data."""
    pass

class ReleaseSandboxValidationError(ReleaseSandboxError):
    """Raised when overall sandbox validation fails."""
    pass

class ReleaseSandboxReportingError(ReleaseSandboxError):
    """Raised when there is an error generating sandbox reports."""
    pass

class PaperShadowError(USASignalBotError): pass
class ShadowSimulationContextError(PaperShadowError): pass
class ShadowPortfolioError(PaperShadowError): pass
class ShadowSignalRehearsalError(PaperShadowError): pass
class ShadowOrderIntentError(PaperShadowError): pass
class ShadowRiskGateError(PaperShadowError): pass
class ShadowFillSimulationError(PaperShadowError): pass
class ShadowLedgerError(PaperShadowError): pass
class ShadowPnLError(PaperShadowError): pass
class ShadowRebalanceError(PaperShadowError): pass
class ShadowSafetyError(PaperShadowError): pass
class ShadowValidationError(PaperShadowError): pass
class ShadowRehearsalRunnerError(PaperShadowError): pass
class ShadowSessionRegistryError(PaperShadowError): pass
class ShadowStorageError(PaperShadowError): pass
class ShadowReportingError(PaperShadowError): pass
