from usa_signal_bot.regime_classification.feature_engineering.phase127_models import RegimeCandidateDefinition, RegimeCandidateKind

def build_default_regime_candidate_definitions(t=None) -> list[RegimeCandidateDefinition]:
    return [
        RegimeCandidateDefinition(candidate_name="risk_on_candidate", candidate_kind=RegimeCandidateKind.RISK_ON_CANDIDATE),
        RegimeCandidateDefinition(candidate_name="risk_off_candidate", candidate_kind=RegimeCandidateKind.RISK_OFF_CANDIDATE),
        RegimeCandidateDefinition(candidate_name="high_volatility_candidate", candidate_kind=RegimeCandidateKind.HIGH_VOLATILITY_CANDIDATE),
        RegimeCandidateDefinition(candidate_name="low_volatility_candidate", candidate_kind=RegimeCandidateKind.LOW_VOLATILITY_CANDIDATE),
        RegimeCandidateDefinition(candidate_name="trending_up_candidate", candidate_kind=RegimeCandidateKind.TRENDING_UP_CANDIDATE),
        RegimeCandidateDefinition(candidate_name="trending_down_candidate", candidate_kind=RegimeCandidateKind.TRENDING_DOWN_CANDIDATE),
        RegimeCandidateDefinition(candidate_name="range_bound_candidate", candidate_kind=RegimeCandidateKind.RANGE_BOUND_CANDIDATE),
        RegimeCandidateDefinition(candidate_name="liquidity_stress_candidate", candidate_kind=RegimeCandidateKind.LIQUIDITY_STRESS_CANDIDATE),
        RegimeCandidateDefinition(candidate_name="event_distorted_candidate", candidate_kind=RegimeCandidateKind.EVENT_DISTORTED_CANDIDATE),
        RegimeCandidateDefinition(candidate_name="data_quality_degraded_candidate", candidate_kind=RegimeCandidateKind.DATA_QUALITY_DEGRADED_CANDIDATE),
        RegimeCandidateDefinition(candidate_name="mixed_regime_candidate", candidate_kind=RegimeCandidateKind.MIXED_REGIME_CANDIDATE),
        RegimeCandidateDefinition(candidate_name="unknown_candidate", candidate_kind=RegimeCandidateKind.UNKNOWN_CANDIDATE),
    ]

def validate_regime_candidate_definitions(candidates: list[RegimeCandidateDefinition]) -> list[str]:
    return []
