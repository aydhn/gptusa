class BacktestClosureError(Exception): pass
class StressRobustnessIngestionError(BacktestClosureError): pass
class CrossPhaseArtifactLoaderError(BacktestClosureError): pass
class ArtifactLineageManifestError(BacktestClosureError): pass
class ArtifactAvailabilityAuditError(BacktestClosureError): pass
class DeterminismComplianceAuditError(BacktestClosureError): pass
class SafetyComplianceAuditError(BacktestClosureError): pass
class ResearchBoundaryAuditError(BacktestClosureError): pass
class MetricInventoryError(BacktestClosureError): pass
class RiskNoteInventoryError(BacktestClosureError): pass
class RobustnessEvidenceTableError(BacktestClosureError): pass
class AcceptanceSummaryError(BacktestClosureError): pass
class ClosureBlockerDetectorError(BacktestClosureError): pass
class ClosureWarningCollectorError(BacktestClosureError): pass
class BacktestFinalAuditReportError(BacktestClosureError): pass
class BacktestBandClosureCertificateError(BacktestClosureError): pass
class Phase153HandoffContractError(BacktestClosureError): pass
class Phase153HandoffPackageError(BacktestClosureError): pass
class HandoffSafetyBoundaryError(BacktestClosureError): pass
class Phase153ReadinessGateError(BacktestClosureError): pass
class ClosureSchemaValidationError(BacktestClosureError): pass
class ClosureSafetyValidationError(BacktestClosureError): pass
class BacktestClosureStoreError(BacktestClosureError): pass
class BacktestClosureValidationError(BacktestClosureError): pass
class BacktestClosureReportingError(BacktestClosureError): pass


class PortfolioFoundationError(Exception):
    pass

class BacktestClosureIngestionError(PortfolioFoundationError):
    pass

class Phase153HandoffLoaderError(PortfolioFoundationError):
    pass

class PortfolioInputResolverError(PortfolioFoundationError):
    pass

class CandidateUniverseContractError(PortfolioFoundationError):
    pass

class PortfolioEligibilityRulesError(PortfolioFoundationError):
    pass

class PortfolioConstraintCatalogError(PortfolioFoundationError):
    pass

class RiskBudgetContractError(PortfolioFoundationError):
    pass

class PositionSizingBoundaryError(PortfolioFoundationError):
    pass

class PortfolioConstructionBoundaryError(PortfolioFoundationError):
    pass

class CandidateUniverseDiagnosticsError(PortfolioFoundationError):
    pass

class ConstraintValidationReportError(PortfolioFoundationError):
    pass

class RiskBudgetValidationReportError(PortfolioFoundationError):
    pass

class SizingBoundaryValidationReportError(PortfolioFoundationError):
    pass

class PortfolioFoundationSafetyBoundaryError(PortfolioFoundationError):
    pass

class Phase154ReadinessGateError(PortfolioFoundationError):
    pass

class PortfolioFoundationSchemaValidationError(PortfolioFoundationError):
    pass

class PortfolioFoundationSafetyValidationError(PortfolioFoundationError):
    pass

class PortfolioFoundationStoreError(PortfolioFoundationError):
    pass

class PortfolioFoundationValidationError(PortfolioFoundationError):
    pass

class PortfolioFoundationReportingError(PortfolioFoundationError):
    pass
class EnsembleScaffoldingIngestionError(Exception):
    pass

class SizingPrototypeError(AppError):
    pass

class PortfolioFoundationIngestionError(SizingPrototypeError):
    pass

class PortfolioFoundationArtifactLoaderError(SizingPrototypeError):
    pass

class SizingInputResolverError(SizingPrototypeError):
    pass

class SizingPolicyError(SizingPrototypeError):
    pass

class SizingMethodContractError(SizingPrototypeError):
    pass

class FixedFractionalSizingError(SizingPrototypeError):
    pass

class VolatilityAdjustedSizingError(SizingPrototypeError):
    pass

class DrawdownAdjustedSizingError(SizingPrototypeError):
    pass

class CostAwareSizingError(SizingPrototypeError):
    pass

class LiquidityAwareSizingError(SizingPrototypeError):
    pass

class RobustnessAdjustedSizingError(SizingPrototypeError):
    pass

class SizingCapFloorRulesError(SizingPrototypeError):
    pass

class SizingComparisonMatrixError(SizingPrototypeError):
    pass

class SizingDiagnosticsError(SizingPrototypeError):
    pass

class SizingSensitivityReportError(SizingPrototypeError):
    pass

class RiskBudgetAdherenceReportError(SizingPrototypeError):
    pass

class SizingSafetyBoundaryError(SizingPrototypeError):
    pass

class Phase155ReadinessGateError(SizingPrototypeError):
    pass

class SizingSchemaValidationError(SizingPrototypeError):
    pass

class SizingSafetyValidationError(SizingPrototypeError):
    pass

class SizingPrototypeStoreError(SizingPrototypeError):
    pass

class SizingPrototypeValidationError(SizingPrototypeError):
    pass

class SizingPrototypeReportingError(SizingPrototypeError):
    pass
