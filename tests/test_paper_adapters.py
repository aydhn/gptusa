import pytest
from usa_signal_bot.paper.paper_adapters import (
    paper_order_intent_from_risk_decision,
    paper_order_intent_from_allocation_result,
    paper_order_intent_from_selected_candidate,
    paper_order_intent_from_strategy_signal
)
from usa_signal_bot.risk.risk_models import RiskDecision
from usa_signal_bot.portfolio.portfolio_models import AllocationResult
from usa_signal_bot.strategies.candidate_selection import SelectedCandidate
from usa_signal_bot.strategies.signal_contract import StrategySignal
from usa_signal_bot.core.enums import PaperOrderSide

def test_intent_from_risk_decision():
    # Helper to mock RiskDecision
    rd = RiskDecision(
        decision_id="r1",
        candidate_id="c1",
        signal_id="s1",
        symbol="AAPL",
        strategy_name="test",
        timeframe="1d",
        status="APPROVED",
        action="BUY",
        approved_quantity=10.0,
        approved_notional=1000.0,
        sizing_method="default",
        checks=[],
        rejection_reasons=[],
        risk_score=50.0,
        severity="INFO",
        notes=[],
        created_at_utc="now"
    )

    intent = paper_order_intent_from_risk_decision(rd)
    assert intent is not None
    assert intent.symbol == "AAPL"
    assert intent.side == PaperOrderSide.BUY
    assert intent.quantity == 10.0

    # Rejected returns None
    rd_rej = RiskDecision(
        decision_id="r2",
        candidate_id="c2",
        signal_id="s2",
        symbol="MSFT",
        strategy_name="test",
        timeframe="1d",
        status="REJECTED",
        action="BUY",
        approved_quantity=0,
        approved_notional=0,
        sizing_method="default",
        checks=[],
        rejection_reasons=[],
        risk_score=50.0,
        severity="INFO",
        notes=[],
        created_at_utc="now"
    )
    assert paper_order_intent_from_risk_decision(rd_rej) is None

def test_intent_from_allocation_result():
    alloc = AllocationResult(
        candidate_id="c1",
        symbol="AAPL",
        timeframe="1d",
        method="default",
        status="ALLOCATED",
        target_weight=0.1,
        target_notional=1000.0,
        target_quantity=10.0,
        raw_weight=0.1,
        raw_notional=1000.0,
        capped=False,
        cap_reasons=[],
        warnings=[],
        errors=[]
    )

    intent = paper_order_intent_from_allocation_result(alloc)
    assert intent is not None
    assert intent.symbol == "AAPL"
    assert intent.quantity == 10.0

    alloc_rej = AllocationResult(
        candidate_id="c2",
        symbol="MSFT", timeframe="1d",
        method="default",
        status="REJECTED", target_weight=0, target_notional=0, target_quantity=0,
        raw_weight=0, raw_notional=0, capped=False, cap_reasons=[], warnings=[], errors=[]
    )
    assert paper_order_intent_from_allocation_result(alloc_rej) is None
