from typing import List, Optional
from pathlib import Path
import json

from usa_signal_bot.core.enums import PaperOrderSide, PaperOrderType, PaperOrderSource
from usa_signal_bot.paper.paper_models import PaperOrderIntent
from usa_signal_bot.paper.paper_orders import create_paper_order_intent
from usa_signal_bot.risk.risk_models import RiskDecision
from usa_signal_bot.portfolio.portfolio_models import AllocationResult
from usa_signal_bot.strategies.candidate_selection import SelectedCandidate
from usa_signal_bot.strategies.signal_contract import StrategySignal

def paper_order_intent_from_risk_decision(
    decision: RiskDecision,
    order_type: PaperOrderType = PaperOrderType.NEXT_OPEN
) -> Optional[PaperOrderIntent]:

    status = str(decision.status)
    if "REJECTED" in status:
        return None

    side_str = str(decision.action).upper() if decision.action else ""
    if "SHORT" in side_str:
        return None

    side = PaperOrderSide.BUY if "BUY" in side_str or "LONG" in side_str else PaperOrderSide.SELL if "SELL" in side_str else None
    if not side:
        side = PaperOrderSide.BUY

    qty = decision.approved_quantity or 0.0
    if qty <= 0:
        return None

    return create_paper_order_intent(
        symbol=decision.symbol,
        timeframe=decision.timeframe,
        side=side,
        quantity=qty,
        source=PaperOrderSource.RISK_DECISION,
        source_id=decision.decision_id,
        order_type=order_type,
        notional=decision.approved_notional,
        reason=None
    )

def paper_order_intent_from_allocation_result(
    allocation: AllocationResult,
    order_type: PaperOrderType = PaperOrderType.NEXT_OPEN
) -> Optional[PaperOrderIntent]:

    status = str(allocation.status)
    if "REJECTED" in status or "ZERO" in status:
        return None

    qty = allocation.target_quantity
    if qty is None or qty <= 0:
        return None

    side = PaperOrderSide.BUY

    return create_paper_order_intent(
        symbol=allocation.symbol,
        timeframe=allocation.timeframe,
        side=side,
        quantity=qty,
        source=PaperOrderSource.PORTFOLIO_ALLOCATION,
        source_id=allocation.candidate_id,
        order_type=order_type,
        notional=allocation.target_notional
    )

def paper_order_intent_from_selected_candidate(
    candidate: SelectedCandidate,
    default_quantity: float = 1.0,
    default_notional: Optional[float] = None,
    order_type: PaperOrderType = PaperOrderType.NEXT_OPEN
) -> Optional[PaperOrderIntent]:

    return create_paper_order_intent(
        symbol=candidate.symbol,
        timeframe=candidate.timeframe,
        side=PaperOrderSide.BUY,
        quantity=default_quantity,
        source=PaperOrderSource.SELECTED_CANDIDATE,
        source_id=candidate.candidate_id,
        order_type=order_type,
        notional=default_notional
    )

def paper_order_intent_from_strategy_signal(
    signal: StrategySignal,
    default_quantity: float = 1.0,
    order_type: PaperOrderType = PaperOrderType.NEXT_OPEN
) -> Optional[PaperOrderIntent]:

    action = str(signal.action).upper()
    if "SHORT" in action:
        return None

    side = PaperOrderSide.BUY if "BUY" in action or "LONG" in action or "WATCH" in action else PaperOrderSide.SELL if "SELL" in action else None

    if not side:
        return None

    return create_paper_order_intent(
        symbol=signal.symbol,
        timeframe=signal.timeframe,
        side=side,
        quantity=default_quantity,
        source=PaperOrderSource.SIGNAL,
        source_id=signal.signal_id,
        order_type=order_type
    )

def _read_jsonl(path: Path) -> List[dict]:
    res = []
    if not path.exists():
        return res
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    res.append(json.loads(line))
                except Exception:
                    pass
    return res

def load_paper_order_intents_from_risk_decisions_file(path: Path) -> List[PaperOrderIntent]:
    intents = []
    data = _read_jsonl(path)
    for d in data:
        decision = RiskDecision(**{k: v for k, v in d.items() if k in RiskDecision.__dataclass_fields__})
        intent = paper_order_intent_from_risk_decision(decision)
        if intent:
            intents.append(intent)
    return intents

def load_paper_order_intents_from_allocations_file(path: Path) -> List[PaperOrderIntent]:
    intents = []
    data = _read_jsonl(path)
    for d in data:
        allocation = AllocationResult(**{k: v for k, v in d.items() if k in AllocationResult.__dataclass_fields__})
        intent = paper_order_intent_from_allocation_result(allocation)
        if intent:
            intents.append(intent)
    return intents

def load_paper_order_intents_from_selected_candidates_file(path: Path) -> List[PaperOrderIntent]:
    intents = []
    data = _read_jsonl(path)
    for d in data:
        candidate = SelectedCandidate(**{k: v for k, v in d.items() if k in SelectedCandidate.__dataclass_fields__})
        intent = paper_order_intent_from_selected_candidate(candidate)
        if intent:
            intents.append(intent)
    return intents

def load_paper_order_intents_from_signals_file(path: Path) -> List[PaperOrderIntent]:
    intents = []
    data = _read_jsonl(path)
    for d in data:
        signal = StrategySignal(**{k: v for k, v in d.items() if k in StrategySignal.__dataclass_fields__})
        intent = paper_order_intent_from_strategy_signal(signal)
        if intent:
            intents.append(intent)
    return intents
