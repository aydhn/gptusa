with open('tests/test_portfolio_candidates.py', 'r') as f:
    content = f.read()

import re

# Update RiskDecision instantiation
# decision_id: str, candidate_id: str, signal_id: str | None, symbol: str, strategy_name: str | None, timeframe: str, status: RiskDecisionStatus, action: SignalAction, approved_quantity: float, approved_notional: float, sizing_method: PositionSizingMethod, checks: list[RiskCheckResult], rejection_reasons: list[RiskRejectionReason], risk_score: float, severity: RiskSeverity, notes: list[str], created_at_utc: str
new_rd = 'decision = RiskDecision("d1", "c1", "sig1", "AAPL", "Strat1", "1d", RiskDecisionStatus.APPROVED, SignalAction.LONG, 10.0, 1500.0, PositionSizingMethod.FIXED_NOTIONAL, [], [], 50.0, RiskSeverity.LOW, [], "utc")'
content = re.sub(r'decision = RiskDecision\(.*?\)', new_rd, content)

# Update SelectedCandidate instantiation
new_sc = """
    from usa_signal_bot.strategies.ranking_store import RankedSignal
    from usa_signal_bot.strategies.signal_contract import StrategySignal
    from usa_signal_bot.core.enums import CandidateSelectionStatus
    sig = StrategySignal("sig1", "Strat1", "AAPL", "1d", SignalAction.LONG, 150.0, 100.0, 0.8, [], "utc")
    rs = RankedSignal(sig, 80.0, 50.0, 0.8, [], {})
    sel = SelectedCandidate("s1", rs, CandidateSelectionStatus.SELECTED, None, 1, [], "utc")
"""
content = re.sub(r'sel = SelectedCandidate\(.*?\)', new_sc, content)

with open('tests/test_portfolio_candidates.py', 'w') as f:
    f.write(content)
