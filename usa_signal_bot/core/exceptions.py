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
