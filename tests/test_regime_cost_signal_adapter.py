import pytest
from usa_signal_bot.regime_costs.signal_adapter import (
    attach_regime_cost_to_signal, attach_regime_cost_to_candidate,
    regime_cost_rank_penalty, candidate_regime_cost_summary
)
from usa_signal_bot.regime_costs.combined_regime_classifier import build_cost_regime_snapshot
from usa_signal_bot.core.enums import CombinedCostRegime, AdaptiveExecutionDecision, RegimeCostAdjustmentStatus, RegimeCostCurveProfile
from usa_signal_bot.regime_costs.regime_cost_models import AdaptiveExecutionRealismDecision, get_utc_now_str

def test_signal_adapter():
    s = build_cost_regime_snapshot("SPY")
    s.combined_regime = CombinedCostRegime.HIGH_RISK
    dec = AdaptiveExecutionRealismDecision("id", "SPY", get_utc_now_str(), AdaptiveExecutionDecision.BLOCK_SIGNAL_METADATA, RegimeCostAdjustmentStatus.APPLIED, CombinedCostRegime.HIGH_RISK, RegimeCostCurveProfile.EXTREME, [], [], [], [])

    cand = attach_regime_cost_to_candidate({}, s, dec)
    assert cand["metadata"]["suppressed_by_regime"] is True

    assert regime_cost_rank_penalty(s, dec) == 0.5
    assert candidate_regime_cost_summary([cand])["suppressed_by_regime"] == 1
