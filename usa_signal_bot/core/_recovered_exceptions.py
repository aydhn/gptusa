"""Definitions recovered from git history.

They were deleted from core/exceptions.py by an accidental overwrite (commit 45faa03 and later
rewrites) while the rest of the code base still imports them.
"""

from usa_signal_bot.core.exceptions import *  # noqa: F401,F403
from usa_signal_bot.core.exceptions import USASignalBotError


class BaseProjectError(Exception):
    pass


class DryAdmissionValidationError(USASignalBotError): pass


class AdvancedTransitionValidationError(USASignalBotError):
    pass


class LifecycleStateMachineError(USASignalBotError):
    pass


class LifecycleManagerError(USASignalBotError):
    pass


class StartupCheckRegistryError(USASignalBotError):
    pass


class LifecycleStorageError(USASignalBotError):
    pass


class LifecycleValidationError(USASignalBotError):
    pass


class ConfigError(USASignalBotError):
    pass


class ProviderValidationError(Exception): pass


class ProviderGovernanceIngestionError(Exception):
    pass


class ProviderFreezeBundleError(Exception):
    pass


class ProviderFreezeValidationError(Exception):
    pass


class MultiProviderFinalReviewError(Exception):
    pass


class ProviderFreezeIngestionError(Exception): pass


class FinalAcceptanceValidationError(Exception): pass


class FactorValidationValidationError(USASignalBotError):
    pass


class MarkdownReportRendererError(BaseProjectError): pass


class JsonReportRendererError(BaseProjectError): pass


class ExplainabilityStoreError(BaseProjectError): pass


class ExplainabilityValidationError(BaseProjectError): pass


class FeatureFactorFinalClosureError(Exception): pass


class FreezePreparationIngestionError(FeatureFactorFinalClosureError): pass


class FinalArtifactChainLoaderError(FeatureFactorFinalClosureError): pass


class FinalClosureChecksError(FeatureFactorFinalClosureError): pass


class FinalSchemaLineageSafetyClosureError(FeatureFactorFinalClosureError): pass


class FreezeSealBuilderError(FeatureFactorFinalClosureError): pass


class EngineReadinessCertificateError(FeatureFactorFinalClosureError): pass


class Phase126KickoffGateError(FeatureFactorFinalClosureError): pass


class RegimeContextValidationIngestionError(Exception):
    pass


class ContextValidationArtifactLoaderError(Exception):
    pass


class RegimeMonitoringStoreError(Exception):
    pass


class RegimeMonitoringValidationError(Exception):
    pass


class RegimeResearchFreezeIngestionError(USASignalBotError):
    pass


class RuntimeInitializationError(USASignalBotError):
    pass


class AuditError(USASignalBotError):
    pass


class EnsembleScaffoldingArtifactLoaderError(USASignalBotError): pass


class BacktestMetricError(Exception): pass


class WalkForwardError(USASignalBotError): pass


class WalkForwardValidationError(WalkForwardError): pass


class PathError(USASignalBotError):
    """Raised when there is an error with file paths or directories."""
    pass


class EnvironmentConfigError(ConfigError):
    """Raised when environment variables are misconfigured."""
    pass


class HealthCheckError(USASignalBotError):
    """Raised when a health check fails."""
    pass


class StorageIntegrityError(StorageError):
    """Raised when a file's integrity check fails."""
    pass


class DataCacheError(StorageError):
    """Raised when an error occurs reading or writing to market data cache."""
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


class RuleStrategySetError(RuleStrategyError):
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


class TransactionCostError(USASignalBotError):
    pass


class TradeAnalyticsError(USASignalBotError):
    pass


class DrawdownAnalyticsError(USASignalBotError):
    pass


class AdvancedBacktestMetricError(USASignalBotError):
    pass


class WalkForwardWindowError(WalkForwardError):
    """Raised when there is an issue with Walk Forward Windows."""
    pass


class WalkForwardEngineError(WalkForwardError):
    """Raised when there is an issue in the Walk Forward Engine."""
    pass


class WalkForwardStorageError(WalkForwardError):
    """Raised when there is an issue storing Walk Forward results."""
    pass


class ParameterSensitivityError(USASignalBotError):
    pass


class ParameterGridError(ParameterSensitivityError):
    pass


class SensitivityValidationError(ParameterSensitivityError):
    pass


class SensitivityStorageError(ParameterSensitivityError):
    pass


class PortfolioCandidateError(PortfolioConstructionError):
    pass


class AllocationMethodError(PortfolioConstructionError):
    pass


class PortfolioStorageError(PortfolioConstructionError):
    pass


class BasketValidationError(USASignalBotError):
    pass


class BasketStorageError(USASignalBotError):
    pass


class QualityStorageError(USASignalBotError):
    """Raised when a quality storage operation fails."""
    pass


class QualityValidationError(USASignalBotError):
    """Raised when a quality validation fails."""
    pass


class ArtifactCollectionError(USASignalBotError):
    """Raised when an artifact collection operation fails."""
    pass


class RollbackSourceError(USASignalBotError): pass


class MarketCalendarError(Exception):
    """Raised for general market calendar errors."""


class HolidayStoreError(Exception):
    """Raised for manual holiday/early-close store errors."""


class CalendarStorageError(Exception):
    """Raised for calendar storage errors."""


class CalendarValidationError(Exception):
    """Raised for calendar validation constraints or assertions."""


class CorporateActionLoaderError(Exception):
    """Raised for corporate action loading errors."""


class AdjustedPriceValidationError(Exception):
    """Raised for adjusted price validation errors."""


class CorporateActionStorageError(Exception):
    """Raised for corporate action storage errors."""


class CorporateActionValidationError(Exception):
    """Raised for corporate action validation constraints or assertions."""


class LifecycleRegistryError(USASignalBotError):
    pass


class SymbolAliasError(USASignalBotError):
    pass


class UsaSignalBotError(Exception):
    pass


class PaperControlledPlanningError(Exception): pass


class PaperObserverError(Exception):
    pass


class PaperPromotionDossierError(Exception): pass


class PaperFinalHandoffError(BaseProjectError):
    pass


class PaperPreRehearsalError(USASignalBotError):
    """Base exception for pre-paper dry rehearsal errors."""
    pass


class PaperReadinessBoardError(Exception): pass


class PaperAdmissionReviewError(USASignalBotError): pass


class PaperNoWriteTransitionError(Exception):
    pass


class PaperBoundaryCertificateError(USASignalBotError):
    pass


class PaperSafeGateError(Exception): pass


class PaperSafeDossierError(USASignalBotError):
    pass


class PaperReadinessNonExecutionBoardError(USASignalBotError):
    pass


class PaperReadinessBoardDossierError(USASignalBotError):
    pass


class AcceptanceBoardSealError(PaperReadinessBoardDossierError):
    pass


class LocalPaperAdmissionSimulatorGateError(USASignalBotError):
    pass


class RuntimeServiceGraphError(USASignalBotError):
    pass


class CoreRuntimeAcceptanceError(USASignalBotError): pass


class DataProviderRuntimeError(Exception):
    pass


class ProviderCacheError(Exception): pass


class ProviderOrchestrationError(USASignalBotError):
    pass


class FeatureFoundationError(Exception):
    pass


class AdvancedFeatureError(USASignalBotError):
    pass


class FactorCompositionError(USASignalBotError):
    pass


class FactorScoringError(USASignalBotError):
    pass


class RegimeFoundationError(Exception):
    pass


class RegimeLabelingError(USASignalBotError):
    pass


class RegimeTransitionAnalyticsError(USASignalBotError):
    pass


class MarketBehaviorReportingError(USASignalBotError): pass


class RegimeAlignmentError(Exception): pass


class RegimeResearchFreezeError(Exception):
    pass


class MLGovernanceClosureError(USASignalBotError):
    pass


class BacktestFoundationError(USASignalBotError): pass


class BacktestRunError(USASignalBotError): pass


class BacktestAnalyticsError(USASignalBotError):
    pass


class PaperShadowError(Exception): pass


class PaperShadowGovernanceError(Exception): pass


class PaperQuarantineError(Exception):
    pass


class FeatureError(USASignalBotError):
    pass


class DivergenceFeatureError(FeatureError):
    """Base class for divergence feature errors."""
    pass


class StrategyError(USASignalBotError):
    pass


class BacktestError(USASignalBotError):
    pass


class BenchmarkError(USASignalBotError):
    pass


class RiskEngineError(USASignalBotError):
    pass


class RuntimeOrchestrationError(USASignalBotError):
    pass


class PaperTradingError(Exception):
    pass


class PaperAnalyticsError(USASignalBotError):
    pass


class ComparisonError(USASignalBotError):
    pass


class ExecutionRealismError(ComparisonError):
    pass


class RegressionError(USASignalBotError):
    pass


class ReleaseError(USASignalBotError):
    pass


class ObservabilityError(USASignalBotError):
    pass


class IncidentError(USASignalBotError): pass


class RecoveryPlannerError(USASignalBotError): pass


class SchedulerError(USASignalBotError):
    pass


class ProfilingError(USASignalBotError):
    pass


class PerformanceBaselineError(USASignalBotError):
    pass


class CostRobustnessError(Exception): pass


class RegimeAwareCostError(USASignalBotError):
    pass


class AdaptiveAllocationError(USASignalBotError):
    pass


class PortfolioRebalanceError(USASignalBotError):
    pass


class ResearchExecutionError(USASignalBotError):
    pass


class ResearchGovernanceError(USASignalBotError):
    pass


class ReleasePackagingError(USASignalBotError):
    pass


class ReleaseSandboxError(USASignalBotError):
    """Base exception for all Release Sandbox errors."""
    pass


class ControlledPlanningObservationIngestionError(PaperControlledPlanningError): pass


class GuardedPaperAdjacentRehearsalError(PaperControlledPlanningError): pass


class ControlledPlanningValidationError(PaperControlledPlanningError): pass


class ObserverControlledPlanningIngestionError(PaperObserverError):
    pass


class ObserverBlockedOperationError(PaperObserverError):
    pass


class ObserverValidationError(PaperObserverError):
    pass


class PromotionDossierValidationError(PaperPromotionDossierError): pass


class FinalHandoffValidationError(PaperFinalHandoffError):
    pass


class PreRehearsalFinalHandoffIngestionError(PaperPreRehearsalError):
    pass


class PrePaperValidationError(PaperPreRehearsalError):
    pass


class PaperReadinessBoardConfirmationIngestionError(PaperReadinessBoardError): pass


class PaperReadinessBoardValidationError(PaperReadinessBoardError): pass


class LedgerReconciliationError(PaperAdmissionReviewError): pass


class AdmissionReviewStorageError(PaperAdmissionReviewError): pass


class AdmissionReviewValidationError(PaperAdmissionReviewError): pass


class NoWriteTransitionAdmissionIngestionError(PaperNoWriteTransitionError):
    pass


class NoWriteTransitionValidationError(PaperNoWriteTransitionError):
    pass


class BoundaryCertificateValidationError(PaperBoundaryCertificateError):
    pass


class BoundaryValidationError(PaperBoundaryCertificateError):
    pass


class PaperSafeBoundaryIngestionError(PaperSafeGateError): pass


class BoundaryReplayPlanError(PaperSafeGateError): pass


class PaperSafeGateValidationError(PaperSafeGateError): pass


class PaperSafeDossierValidationError(PaperSafeDossierError):
    pass


class NonExecutionBoardDossierIngestionError(PaperReadinessNonExecutionBoardError):
    pass


class NonExecutionBoardValidationError(PaperReadinessNonExecutionBoardError):
    pass


class AcceptanceBoardSealValidationError(AcceptanceBoardSealError):
    pass


class FinalShadowLaunchBlockerError(PaperReadinessBoardDossierError):
    pass


class BoardDossierValidationError(PaperReadinessBoardDossierError):
    pass


class RehearsalReplayEngineError(LocalPaperAdmissionSimulatorGateError):
    pass


class RehearsalReplayAnalyzerError(LocalPaperAdmissionSimulatorGateError):
    pass


class DryAdmissionEvidenceFreezeError(LocalPaperAdmissionSimulatorGateError):
    pass


class SimulatorGateRuleError(LocalPaperAdmissionSimulatorGateError):
    pass


class SimulatorGateAssertionError(LocalPaperAdmissionSimulatorGateError):
    pass


class FinalSimulatorGateError(LocalPaperAdmissionSimulatorGateError):
    pass


class SimulatorReportingError(LocalPaperAdmissionSimulatorGateError):
    pass


class ServiceGraphStorageError(RuntimeServiceGraphError):
    pass


class ServiceGraphValidationError(RuntimeServiceGraphError):
    pass


class LifecycleReviewIngestionError(CoreRuntimeAcceptanceError): pass


class FoundationFreezeValidationError(CoreRuntimeAcceptanceError): pass


class ProviderKickoffGateValidationError(CoreRuntimeAcceptanceError): pass


class CoreRuntimeAcceptanceValidationError(CoreRuntimeAcceptanceError): pass


class ProviderAbstractionIngestionError(DataProviderRuntimeError):
    pass


class ProviderCacheKeyError(DataProviderRuntimeError):
    pass


class ProviderRuntimeValidationError(DataProviderRuntimeError):
    pass


class OhlcvSchemaValidationError(DataProviderRuntimeError):
    pass


class ProviderRuntimeIngestionError(ProviderCacheError): pass


class CachePathResolverError(ProviderCacheError): pass


class CacheStoreError(ProviderCacheError): pass


class OhlcvComparisonError(ProviderCacheError): pass


class ProviderCacheSafetyValidationError(ProviderCacheError): pass


class ProviderCacheValidationError(ProviderCacheError): pass


class ProviderQualityIngestionError(ProviderOrchestrationError):
    pass


class EventMetadataError(UsaSignalBotError): pass


class FeatureFoundationValidationError(FeatureFoundationError):
    pass


class AdvancedVolatilityFeatureError(AdvancedFeatureError):
    pass


class AdvancedMomentumFeatureError(AdvancedFeatureError):
    pass


class AdvancedTrendFeatureError(AdvancedFeatureError):
    pass


class NormalizationFeatureError(AdvancedFeatureError):
    pass


class CrossSectionalUniverseError(AdvancedFeatureError):
    pass


class CrossSectionalAlignmentError(AdvancedFeatureError):
    pass


class AdvancedFeatureValidationError(AdvancedFeatureError):
    pass


class FactorCompositionValidationError(FactorCompositionError):
    pass


class FactorTableInputLoaderError(FactorScoringError):
    pass


class FactorComputationValidationError(FactorScoringError):
    pass


class FinalClosureIngestionError(RegimeFoundationError):
    pass


class FrozenArtifactLoaderError(RegimeFoundationError):
    pass


class RegimeFoundationValidationError(RegimeFoundationError):
    pass


class RegimeFeatureEngineeringIngestionError(RegimeLabelingError):
    pass


class RegimeLabelInputLoaderError(RegimeLabelingError):
    pass


class RegimeLabelingStoreError(RegimeLabelingError):
    pass


class RegimeLabelingValidationError(RegimeLabelingError):
    pass


class RegimeLabelingIngestionError(RegimeTransitionAnalyticsError):
    pass


class RegimeSequenceInputLoaderError(RegimeTransitionAnalyticsError):
    pass


class RegimeTransitionMatrixError(RegimeTransitionAnalyticsError):
    pass


class RegimePersistenceAnalyticsError(RegimeTransitionAnalyticsError):
    pass


class RegimeDurationAnalyticsError(RegimeTransitionAnalyticsError):
    pass


class RegimeChurnDiagnosticsError(RegimeTransitionAnalyticsError):
    pass


class RegimeStabilityDiagnosticsError(RegimeTransitionAnalyticsError):
    pass


class CrossSymbolRegimeTransitionError(RegimeTransitionAnalyticsError):
    pass


class RollingTransitionAnalyticsError(RegimeTransitionAnalyticsError):
    pass


class TransitionConcentrationMetricsError(RegimeTransitionAnalyticsError):
    pass


class RegimeDiagnosticsReadinessGateError(RegimeTransitionAnalyticsError):
    pass


class RegimeDiagnosticsSchemaValidationError(RegimeTransitionAnalyticsError):
    pass


class RegimeDiagnosticsSafetyValidationError(RegimeTransitionAnalyticsError):
    pass


class RegimeTransitionStoreError(RegimeTransitionAnalyticsError):
    pass


class RegimeTransitionValidationError(RegimeTransitionAnalyticsError):
    pass


class RegimeTransitionIngestionError(MarketBehaviorReportingError): pass


class DiagnosticsArtifactLoaderError(MarketBehaviorReportingError): pass


class RegimeAlignmentValidationError(RegimeAlignmentError): pass


class MonitoringArtifactLoaderError(RegimeResearchFreezeError):
    pass


class ResearchFreezeValidationError(RegimeResearchFreezeError):
    pass


class DriftMonitoringIngestionError(MLGovernanceClosureError):
    pass


class DriftMonitoringArtifactLoaderError(MLGovernanceClosureError):
    pass


class MLClosureSchemaValidationError(MLGovernanceClosureError):
    pass


class SlippageModelError(BacktestFoundationError): pass


class BacktestFoundationValidationError(BacktestFoundationError): pass


class BacktestFoundationIngestionError(BacktestRunError): pass


class BacktestRunIngestionError(BacktestAnalyticsError):
    pass


class BacktestRunArtifactLoaderError(BacktestAnalyticsError):
    pass


class AnalyticsInputResolverError(BacktestAnalyticsError):
    pass


class ReturnSeriesBuilderError(BacktestAnalyticsError):
    pass


class RollingAnalyticsError(BacktestAnalyticsError):
    pass


class AdvancedPerformanceMetricsError(BacktestAnalyticsError):
    pass


class TradeDiagnosticsError(BacktestAnalyticsError):
    pass


class FillDiagnosticsError(BacktestAnalyticsError):
    pass


class CostDiagnosticsError(BacktestAnalyticsError):
    pass


class ExposureDiagnosticsError(BacktestAnalyticsError):
    pass


class DrawdownDiagnosticsError(BacktestAnalyticsError):
    pass


class DeterminismValidationError(BacktestAnalyticsError):
    pass


class RunValidationReportError(BacktestAnalyticsError):
    pass


class BacktestAnalyticsReportError(BacktestAnalyticsError):
    pass


class PerformanceAnalyticsSafetyBoundaryError(BacktestAnalyticsError):
    pass


class Phase149ReadinessGateError(BacktestAnalyticsError):
    pass


class BacktestAnalyticsSchemaValidationError(BacktestAnalyticsError):
    pass


class BacktestAnalyticsSafetyValidationError(BacktestAnalyticsError):
    pass


class BacktestAnalyticsStoreError(BacktestAnalyticsError):
    pass


class BacktestAnalyticsValidationError(BacktestAnalyticsError):
    pass


class BacktestAnalyticsReportingError(BacktestAnalyticsError):
    pass


class ShadowSafetyError(PaperShadowError): pass


class ShadowValidationError(PaperShadowError): pass


class ShadowGovernanceValidationError(PaperShadowGovernanceError): pass


class ShadowGovernanceIngestionError(PaperQuarantineError):
    pass


class QuarantineOutputIsolationError(PaperQuarantineError):
    pass


class QuarantineStorageError(PaperQuarantineError):
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


class IndicatorSetError(FeatureError):
    pass


class MomentumIndicatorSetError(IndicatorSetError):
    pass


class VolatilityIndicatorSetError(FeatureComputationError):
    pass


class DivergenceIndicatorSetError(DivergenceFeatureError):
    """Raised for errors related to divergence indicator sets."""
    pass


class CompositeFeatureError(FeatureError):
    pass


class FeatureGroupError(CompositeFeatureError):
    pass


class FeaturePipelineError(CompositeFeatureError):
    pass


class FeatureCheckpointError(CompositeFeatureError):
    pass


class StrategyMetadataError(StrategyError):
    pass


class StrategyParameterError(StrategyError):
    pass


class StrategyRegistrationError(StrategyError):
    pass


class StrategyExecutionError(StrategyError):
    pass


class SignalValidationError(StrategyError):
    pass


class SignalStorageError(StrategyError):
    pass


class BacktestEventError(BacktestError):
    pass


class BacktestMarketReplayError(BacktestError):
    pass


class BacktestSignalReplayError(BacktestError):
    pass


class BacktestValidationError(BacktestError):
    pass


class BacktestStorageError(BacktestError):
    pass


class BenchmarkLoaderError(BenchmarkError):
    pass


class BenchmarkStorageError(BenchmarkError):
    pass


class RiskLimitError(RiskEngineError):
    pass


class PositionSizingError(RiskEngineError):
    pass


class RiskValidationError(RiskEngineError):
    pass


class RiskStorageError(RiskEngineError):
    pass


class RuntimeLockError(RuntimeOrchestrationError):
    pass


class SafeStopError(RuntimeOrchestrationError):
    pass


class RuntimeValidationError(RuntimeOrchestrationError):
    pass


class PaperValidationError(PaperTradingError):
    pass


class PaperAnalyticsStorageError(PaperAnalyticsError):
    pass


class PaperAnalyticsValidationError(PaperAnalyticsError):
    pass


class ResultLoaderError(ComparisonError):
    pass


class ComparisonStorageError(ComparisonError):
    pass


class ComparisonValidationError(ComparisonError):
    pass


class GoldenFixtureError(RegressionError):
    pass


class GoldenDatasetError(RegressionError):
    pass


class RegressionValidationError(RegressionError):
    pass


class ReleaseValidationError(ReleaseError):
    pass


class ObservabilityValidationError(ObservabilityError):
    pass


class RecoveryActionError(RecoveryPlannerError): pass


class IncidentValidationError(IncidentError): pass


class SchedulerValidationError(SchedulerError):
    pass


class ThrottlingPolicyError(ProfilingError):
    pass


class ProfilingValidationError(ProfilingError):
    pass


class PerformanceBaselineValidationError(PerformanceBaselineError):
    pass


class ExecutionValidationError(ExecutionRealismError):
    pass


class CostRobustnessValidationError(CostRobustnessError): pass


class RegimeCostValidationError(RegimeAwareCostError):
    pass


class CapitalStateError(AdaptiveAllocationError):
    pass


class RiskBudgetError(AdaptiveAllocationError):
    pass


class AllocationStorageError(AdaptiveAllocationError):
    pass


class AllocationValidationError(AdaptiveAllocationError):
    pass


class RebalanceValidationError(PortfolioRebalanceError):
    pass


class ExperimentPlanLoadError(ResearchExecutionError):
    pass


class CandidateOverlayError(ResearchExecutionError):
    pass


class LocalExperimentHarnessError(ResearchExecutionError):
    pass


class MetricsExtractionError(ResearchExecutionError):
    pass


class ResearchExecutionValidationError(ResearchExecutionError):
    pass


class GovernanceValidationError(ResearchGovernanceError):
    pass


class ReleasePackagingValidationError(ReleasePackagingError):
    pass


class SandboxOutputIsolationError(ReleaseSandboxError):
    """Raised when sandbox output isolation fails."""
    pass


class BlockedOperationGuardError(ReleaseSandboxError):
    """Raised when a blocked operation is attempted in the sandbox."""
    pass


class ReleaseSandboxStorageError(ReleaseSandboxError):
    """Raised when there is an error reading or writing sandbox data."""
    pass


class ReleaseSandboxValidationError(ReleaseSandboxError):
    """Raised when overall sandbox validation fails."""
    pass
