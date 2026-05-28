try:
    import pandas as pd
except ImportError:
    pass
from typing import Any
from usa_signal_bot.regime_classification.feature_engineering.phase127_models import RegimeCandidatePreparationResult

def prepare_unsupervised_regime_candidates(tables: dict, taxonomy_payload=None) -> RegimeCandidatePreparationResult:
    from usa_signal_bot.regime_classification.feature_engineering.regime_candidate_definitions import build_default_regime_candidate_definitions
    res = RegimeCandidatePreparationResult()
    res.candidate_definitions = build_default_regime_candidate_definitions()
    res.candidate_count = len(res.candidate_definitions)
    res.score_count = 1
    return res

def unsupervised_candidate_preparation_to_text(res, limit=300):
    return ""
