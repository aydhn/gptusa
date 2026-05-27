with open('usa_signal_bot/core/exceptions.py', 'a') as f:
    f.write('''

class FeatureFactorIntegrationFreezeError(USASignalBotError):
    """Raised when integration freeze fails."""

class ExplainabilityIngestionError(USASignalBotError):
    """Raised when explainability ingestion fails."""

class ArtifactChainLoaderError(USASignalBotError):
    """Raised when artifact chain loader fails."""

class ArtifactChainIntegrityError(USASignalBotError):
    """Raised when artifact chain integrity fails."""

class SchemaContinuityValidationError(USASignalBotError):
    """Raised when schema continuity validation fails."""

class LineageContinuityValidationError(USASignalBotError):
    """Raised when lineage continuity validation fails."""

class SafetyBoundaryContinuityError(USASignalBotError):
    """Raised when safety boundary continuity fails."""

class ReportQaAcceptanceError(USASignalBotError):
    """Raised when report QA acceptance fails."""

class ResearchReportAcceptanceError(USASignalBotError):
    """Raised when research report acceptance fails."""

class FactorStoreHardeningAcceptanceError(USASignalBotError):
    """Raised when factor store hardening acceptance fails."""

class IntegrationRehearsalRunnerError(USASignalBotError):
    """Raised when integration rehearsal runner fails."""

class FreezeCandidateManifestError(USASignalBotError):
    """Raised when freeze candidate manifest fails."""

class FreezeReadinessGateError(USASignalBotError):
    """Raised when freeze readiness gate fails."""

class FreezePreparationSafetyValidationError(USASignalBotError):
    """Raised when freeze preparation safety validation fails."""

class FreezePreparationStoreError(USASignalBotError):
    """Raised when freeze preparation store fails."""

class FreezePreparationValidationError(USASignalBotError):
    """Raised when freeze preparation validation fails."""

class FreezePreparationReportingError(USASignalBotError):
    """Raised when freeze preparation reporting fails."""

''')

