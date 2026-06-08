import pytest
from usa_signal_bot.portfolio.optimization.phase156_models import OptimizerSafetyBoundaryResult, OptimizerPrototypeContext
from usa_signal_bot.portfolio.optimization.optimizer_safety_validator import validate_optimizer_context_safety, optimizer_text_has_trade_or_execution_language, optimizer_payload_has_forbidden_fields

def test_validate_optimizer_context_safety():
    c = OptimizerPrototypeContext()
    c.actual_target_weights_produced = True
    errs = validate_optimizer_context_safety(c)
    assert len(errs) > 0
    assert "actual_target_weights_produced" in errs

def test_optimizer_text_has_trade_or_execution_language():
    text1 = "This is a safe sandbox weight."
    assert not optimizer_text_has_trade_or_execution_language(text1)

    text2 = "Set actual target weight to 0.5 and sent_to_broker."
    assert optimizer_text_has_trade_or_execution_language(text2)

def test_optimizer_payload_has_forbidden_fields():
    payload1 = {"symbol": "AAPL", "sandbox_score": 0.8}
    assert not optimizer_payload_has_forbidden_fields(payload1)

    payload2 = {"symbol": "AAPL", "actual_allocation": 0.5}
    assert optimizer_payload_has_forbidden_fields(payload2)
