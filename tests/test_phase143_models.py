from usa_signal_bot.ml_research.ensemble_evaluation.phase143_models import (
    EnsemblePrototypeStatus,
    EnsemblePrototypeDecision,
    EnsemblePrototypeKind,
    OfflineEnsemblePredictionKind,
    BlendDiagnosticKind,
    CandidateAgreementKind,
    EnsembleCandidateComparisonKind,
    OfflineEnsembleEvaluationMetricKind,
    OfflineEnsembleEvaluationStatus,
    NonActivationEnsembleRegistryStatus,
    EnsembleRegistryEntryStatus,
    EnsemblePrototypeBoundaryRuleKind,
    EnsemblePrototypeReadinessStatus,
    EnsemblePrototypeReadinessRuleKind,
    EnsemblePrototypeQuality,
    EnsemblePrototypeRiskFlag,
    EnsemblePrototypeReportType
)

def test_enums_exist():
    assert hasattr(EnsemblePrototypeStatus, 'DRAFT')
    assert hasattr(EnsemblePrototypeDecision, 'BUILD_READINESS_GATE')
    assert hasattr(EnsemblePrototypeKind, 'COEFFICIENT_BLEND_PROTOTYPE')
    assert hasattr(OfflineEnsemblePredictionKind, 'RESEARCH_ENSEMBLE_SCORE')
