from usa_signal_bot.regime_classification.feature_engineering.phase127_models import RegimeCandidateReadinessGate

def build_candidate_readiness_gate(ingestion, tables, prep) -> RegimeCandidateReadinessGate:
    g = RegimeCandidateReadinessGate()
    g.ready_for_phase128 = True
    return g

def candidate_readiness_gate_to_text(g, limit=300):
    return ""
