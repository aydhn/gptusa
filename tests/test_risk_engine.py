from usa_signal_bot.risk.risk_engine import RiskEngine
from usa_signal_bot.risk.candidate_risk import CandidateRiskInput
from usa_signal_bot.risk.exposure_guard import create_empty_exposure_snapshot
from usa_signal_bot.core.enums import SignalAction, RiskDecisionStatus

def test_risk_engine_evaluate_candidate():
    engine = RiskEngine()
    cand = CandidateRiskInput("c1", "s1", "AAPL", "1d", "strat", SignalAction.LONG, 0.8, 80.0, 100.0, {}, [])
    snap = create_empty_exposure_snapshot(100000.0, 100000.0)

    dec = engine.evaluate_candidate(cand, snap)
    assert dec.status == RiskDecisionStatus.APPROVED
    assert dec.approved_notional == 5000.0

def test_risk_engine_short_rejected():
    engine = RiskEngine()
    cand = CandidateRiskInput("c1", "s1", "AAPL", "1d", "strat", SignalAction.SHORT, 0.8, 80.0, 100.0, {}, [])
    snap = create_empty_exposure_snapshot(100000.0, 100000.0)

    dec = engine.evaluate_candidate(cand, snap)
    assert dec.status == RiskDecisionStatus.REJECTED
    assert dec.approved_notional == 0.0

def test_risk_engine_missing_price():
    engine = RiskEngine()
    cand = CandidateRiskInput("c1", "s1", "AAPL", "1d", "strat", SignalAction.LONG, 0.8, 80.0, None, {}, [])
    snap = create_empty_exposure_snapshot(100000.0, 100000.0)

    dec = engine.evaluate_candidate(cand, snap)
    assert dec.status == RiskDecisionStatus.REJECTED

def test_risk_engine_evaluate_candidates():
    engine = RiskEngine()
    cands = [
        CandidateRiskInput("c1", "s1", "AAPL", "1d", "strat", SignalAction.LONG, 0.8, 80.0, 100.0, {}, []),
        CandidateRiskInput("c2", "s2", "MSFT", "1d", "strat", SignalAction.LONG, 0.8, 80.0, 200.0, {}, [])
    ]
    snap = create_empty_exposure_snapshot(100000.0, 100000.0)

    res = engine.evaluate_candidates(cands, snap)
    assert res.total_candidates == 2
    assert res.approved_count == 2
    assert sum(d.approved_notional for d in res.decisions) == 10000.0
