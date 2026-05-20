class PaperShadowError(Exception): pass
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

class PaperShadowGovernanceError(Exception): pass
class ShadowSessionIngestionError(PaperShadowGovernanceError): pass
class ShadowMetricExtractionError(PaperShadowGovernanceError): pass
class ShadowSessionComparisonError(PaperShadowGovernanceError): pass
class ShadowRiskDeltaError(PaperShadowGovernanceError): pass
class ShadowSafetyDeltaError(PaperShadowGovernanceError): pass
class ShadowLedgerCompletenessError(PaperShadowGovernanceError): pass
class ShadowAcceptanceGateError(PaperShadowGovernanceError): pass
class ShadowAcceptanceScoringError(PaperShadowGovernanceError): pass
class ShadowDecisionBoardError(PaperShadowGovernanceError): pass
class ShadowEvidencePackError(PaperShadowGovernanceError): pass
class ShadowGovernanceAuditError(PaperShadowGovernanceError): pass
class ShadowGovernanceStorageError(PaperShadowGovernanceError): pass
class ShadowGovernanceValidationError(PaperShadowGovernanceError): pass
class ShadowGovernanceReportingError(PaperShadowGovernanceError): pass


class PaperQuarantineError(Exception):
    pass

class ShadowGovernanceIngestionError(PaperQuarantineError):
    pass

class QuarantineEligibilityError(PaperQuarantineError):
    pass

class QuarantinePolicyError(PaperQuarantineError):
    pass

class PaperSnapshotRefError(PaperQuarantineError):
    pass

class PromotionTicketError(PaperQuarantineError):
    pass

class SupervisedDryRunBridgeError(PaperQuarantineError):
    pass

class BridgeOperationGuardError(PaperQuarantineError):
    pass

class QuarantineOutputIsolationError(PaperQuarantineError):
    pass

class ManualReviewGateError(PaperQuarantineError):
    pass

class QuarantineReviewWindowError(PaperQuarantineError):
    pass

class QuarantineRegistryError(PaperQuarantineError):
    pass

class PromotionTicketRegistryError(PaperQuarantineError):
    pass

class BridgeValidationError(PaperQuarantineError):
    pass

class QuarantineEnrollmentSafetyError(PaperQuarantineError):
    pass

class QuarantineStorageError(PaperQuarantineError):
    pass

class QuarantineValidationError(PaperQuarantineError):
    pass

class QuarantineReportingError(PaperQuarantineError):
    pass
