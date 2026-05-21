class PaperDryRunBridgeError(Exception): pass
class DryRunQuarantineIngestionError(Exception): pass
class DryRunTicketIngestionError(Exception): pass
class DryRunBridgePlanIngestionError(Exception): pass
class PaperSnapshotLoaderError(Exception): pass
class DryRunBridgeContextError(Exception): pass
class DryRunProposalError(Exception): pass
class DryRunRiskEvaluatorError(Exception): pass
class DryRunNotificationPreviewError(Exception): pass
class BridgeOperationMonitorError(Exception): pass
class BlockedOperationTelemetryError(Exception): pass
class HumanReviewCheckpointError(Exception): pass
class DryRunBridgeRunnerError(Exception): pass
class DryRunBridgeTelemetryError(Exception): pass
class DryRunBridgeStorageError(Exception): pass
class DryRunBridgeValidationError(Exception): pass
class DryRunBridgeReportingError(Exception): pass

class PaperObservationError(Exception): pass
class ObservationDryRunIngestionError(PaperObservationError): pass
class ObservationQuarantineIngestionError(PaperObservationError): pass
class ObservationWindowPlannerError(PaperObservationError): pass
class ObservationWindowTrackerError(PaperObservationError): pass
class CheckpointHistoryError(PaperObservationError): pass
class CheckpointTimelineError(PaperObservationError): pass
class ObservationTelemetryHistoryError(PaperObservationError): pass
class ObservationProposalHistoryError(PaperObservationError): pass
class ObservationRiskHistoryError(PaperObservationError): pass
class ObservationBlockedOperationHistoryError(PaperObservationError): pass
class ObservationNotificationSafetyError(PaperObservationError): pass
class ObservationScoringError(PaperObservationError): pass
class QuarantineExitGateError(PaperObservationError): pass
class QuarantineExitDecisionError(PaperObservationError): pass
class ObservationAuditError(PaperObservationError): pass
class ObservationStorageError(PaperObservationError): pass
class ObservationValidationError(PaperObservationError): pass
class ObservationReportingError(PaperObservationError): pass

# Phase 75: Controlled Paper-Observation Planning Exceptions
class PaperControlledPlanningError(Exception): pass
class ControlledPlanningObservationIngestionError(PaperControlledPlanningError): pass
class ControlledPlanningEligibilityError(PaperControlledPlanningError): pass
class ControlledPlanningTicketError(PaperControlledPlanningError): pass
class PaperSnapshotComparatorError(PaperControlledPlanningError): pass
class PaperAdjacentRehearsalContextError(PaperControlledPlanningError): pass
class PaperAdjacentProposalError(PaperControlledPlanningError): pass
class GuardedPaperAdjacentRehearsalError(PaperControlledPlanningError): pass
class FinalHumanApprovalQueueError(PaperControlledPlanningError): pass
class ApprovalQueueRegistryError(PaperControlledPlanningError): pass
class ApprovalQueueValidationError(PaperControlledPlanningError): pass
class ControlledPlanningSafetyError(PaperControlledPlanningError): pass
class ControlledPlanningAuditError(PaperControlledPlanningError): pass
class ControlledPlanningStorageError(PaperControlledPlanningError): pass
class ControlledPlanningValidationError(PaperControlledPlanningError): pass
class ControlledPlanningReportingError(PaperControlledPlanningError): pass

# Phase 76: Paper Observer Exceptions
class PaperObserverError(Exception):
    pass

class ObserverControlledPlanningIngestionError(PaperObserverError):
    pass

class ObserverEligibilityError(PaperObserverError):
    pass

class ObserverEnrollmentError(PaperObserverError):
    pass

class LockedObserverPolicyError(PaperObserverError):
    pass

class ObserverPaperSnapshotError(PaperObserverError):
    pass

class ObserverRuntimeContextError(PaperObserverError):
    pass

class ObserverSignalMirrorError(PaperObserverError):
    pass

class ObserverProposalError(PaperObserverError):
    pass

class ObserverRiskMirrorError(PaperObserverError):
    pass

class ObserverNotificationPreviewError(PaperObserverError):
    pass

class ObserverParallelMonitorError(PaperObserverError):
    pass

class ObserverDriftDetectionError(PaperObserverError):
    pass

class ObserverBlockedOperationError(PaperObserverError):
    pass

class ObserverRuntimeSafetyError(PaperObserverError):
    pass

class ObserverMonitoringAnalyzerError(PaperObserverError):
    pass

class ObserverSessionRegistryError(PaperObserverError):
    pass

class ObserverAuditError(PaperObserverError):
    pass

class ObserverStorageError(PaperObserverError):
    pass

class ObserverValidationError(PaperObserverError):
    pass

class ObserverReportingError(PaperObserverError):
    pass


class PaperObserverGovernanceError(Exception):
    pass

class ObserverGovernanceIngestionError(PaperObserverGovernanceError):
    pass

class ObserverPaperSnapshotIngestionError(PaperObserverGovernanceError):
    pass

class ObserverMetricExtractionError(PaperObserverGovernanceError):
    pass

class PaperMetricExtractionError(PaperObserverGovernanceError):
    pass

class ObserverPaperComparisonError(PaperObserverGovernanceError):
    pass

class ObserverSignalDeltaError(PaperObserverGovernanceError):
    pass

class ObserverProposalDeltaError(PaperObserverGovernanceError):
    pass

class ObserverRiskDeltaError(PaperObserverGovernanceError):
    pass

class ObserverDriftDeltaError(PaperObserverGovernanceError):
    pass

class ObserverSafetyComplianceError(PaperObserverGovernanceError):
    pass

class ObserverEvidenceCollectionError(PaperObserverGovernanceError):
    pass

class ObserverEvidenceFreshnessError(PaperObserverGovernanceError):
    pass

class ObserverGovernanceGateError(PaperObserverGovernanceError):
    pass

class ObserverGovernanceDecisionError(PaperObserverGovernanceError):
    pass

class ObserverGovernanceAuditError(PaperObserverGovernanceError):
    pass

class ObserverGovernanceStorageError(PaperObserverGovernanceError):
    pass

class ObserverGovernanceValidationError(PaperObserverGovernanceError):
    pass

class ObserverGovernanceReportingError(PaperObserverGovernanceError):
    pass
