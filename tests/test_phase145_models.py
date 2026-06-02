import pytest
from usa_signal_bot.ml_research.ml_governance_closure.phase145_models import (
    DriftMonitoringIngestionResult,
    ExplainabilityInputReference,
    ExplainabilityInputKind,
    FeatureAttributionProxy,
    ExplainabilityMethodKind,
    ExplanationScope,
    ExplanationStatus,
    FactorContributionSummary,
    ModelBehaviorExplanation,
    RegimeAwareExplanation,
    CalibrationAwareExplanation,
    EnsembleExplanation,
    ExplainabilityReport,
    MLGovernanceClosureResult,
    AdvancedMLArtifactLineage,
    AdvancedMLFinalAuditResult,
    NonActivationMLClosureBoundaryResult,
    FinalMLModelCardClosure,
    AdvancedMLAcceptanceGate,
    AdvancedMLClosureContext,
    AdvancedMLClosureFullReview,
    create_drift_monitoring_ingestion_id
)

def test_phase145_models_imports():
    assert create_drift_monitoring_ingestion_id().startswith("ing-")
