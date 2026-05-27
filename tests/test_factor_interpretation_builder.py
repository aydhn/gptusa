import pytest
from usa_signal_bot.core.enums import FactorInterpretationKind
from usa_signal_bot.feature_engine.factor_explainability.factor_interpretation_builder import infer_factor_interpretation_kind, build_factor_interpretation_summary

def test_infer_factor_interpretation_kind():
    assert infer_factor_interpretation_kind("momentum_10") == FactorInterpretationKind.MOMENTUM_CONTEXT
    assert infer_factor_interpretation_kind("volatility_10") == FactorInterpretationKind.VOLATILITY_CONTEXT

def test_build_factor_interpretation_summary():
    summ = build_factor_interpretation_summary("AAPL", "mom_10", "mom_10")
    assert summ.produces_trade_signal is False
    assert summ.investment_advice is False
