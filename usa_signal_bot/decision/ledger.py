"""Local simulated paper ledger. Books *simulated fills* in memory/JSONL only.

No order objects, no broker, no network. ``ORDER_ROUTING_ENABLED`` is a constant False.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Mapping, Optional

import pandas as pd

from usa_signal_bot.core.types import ExecutionMode
from usa_signal_bot.evidence.costs import CostModel
from usa_signal_bot.decision.rules import PositionState
from usa_signal_bot.paper_common.io import append_jsonl

ORDER_ROUTING_ENABLED = False
EXECUTION_MODE: ExecutionMode = "local_paper_only"


@dataclass
class SimulatedFill:
    date: str
    symbol: str
    side: str  # BUY | SELL (bookkeeping label of a simulated fill)
    quantity: float
    price: float
    cost: float
    reason: str


@dataclass
class PaperLedger:
    initial_cash: float = 100_000.0
    cost: CostModel = field(default_factory=CostModel)
    journal_path: Optional[Path] = None
    cash_rate_annual: float = 0.0  # interest on idle cash (annual, compounded by calendar days)
    interest_earned: float = 0.0
    _last_accrual: Optional[str] = None
    cash: float = 0.0
    positions: Dict[str, PositionState] = field(default_factory=dict)
    fills: List[SimulatedFill] = field(default_factory=list)
    equity_curve: Dict[str, float] = field(default_factory=dict)
    peak_equity: float = 0.0
    last_price: Dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.cash = self.initial_cash
        self.peak_equity = self.initial_cash

    def equity(self, prices: Mapping[str, float]) -> float:
        total = self.cash
        for sym, pos in self.positions.items():
            px = prices.get(sym)
            total += pos.quantity * (pos.entry_price if px is None or pd.isna(px) else px)
        return total

    def drawdown(self, prices: Mapping[str, float]) -> float:
        eq = self.equity(prices)
        return eq / self.peak_equity - 1.0 if self.peak_equity > 0 else 0.0

    def current_weights(self, prices: Mapping[str, float]) -> Dict[str, float]:
        eq = self.equity(prices)
        if eq <= 0:
            return {}
        out = {}
        for s, p in self.positions.items():
            px = prices.get(s)
            if px is not None and not pd.isna(px):
                out[s] = p.quantity * px / eq
        return out

    def _record(self, fill: SimulatedFill) -> None:
        self.fills.append(fill)
        if self.journal_path is not None:
            append_jsonl(
                self.journal_path,
                [{**fill.__dict__, "execution_mode": EXECUTION_MODE, "order_routing_enabled": ORDER_ROUTING_ENABLED}],
            )

    def close_missing(self, prices: Mapping[str, float], date: str) -> None:
        """Positions whose price disappeared (delisting/halt data gap) are closed at the last known price.

        Assumption (optimistic, documented): no recovery haircut is applied.
        """
        for sym in list(self.positions):
            px = prices.get(sym)
            if px is None or pd.isna(px):
                last = self.last_price.get(sym, self.positions[sym].entry_price)
                self._sell(sym, self.positions[sym].quantity, last, date, "DELISTED_LAST_PRICE")

    def _sell(self, sym: str, qty: float, px: float, date: str, reason: str) -> None:
        if px is None or pd.isna(px):
            raise ValueError(f"cannot book a fill for {sym} without a price")
        pos = self.positions[sym]
        qty = min(qty, pos.quantity)
        fee = qty * px * (self.cost.commission_bps + self.cost.slippage_bps) / 10_000.0
        self.cash += qty * px - fee
        pos.quantity -= qty
        if pos.quantity <= 1e-9:
            del self.positions[sym]
        self._record(SimulatedFill(date, sym, "SELL", qty, px, fee, reason))

    def rebalance_to(
        self,
        target_weights: Mapping[str, float],
        prices: Mapping[str, float],
        date: str,
        day_index: int,
        reasons: Optional[Mapping[str, str]] = None,
    ) -> None:
        """Move holdings toward ``target_weights`` at ``prices`` (simulated fills, long-only, no leverage)."""
        reasons = reasons or {}
        eq = self.equity(prices)
        # sells first so cash is available
        for sym in list(self.positions):
            px = prices.get(sym)
            if px is None or pd.isna(px):
                continue
            want = target_weights.get(sym, 0.0) * eq / px
            if self.positions[sym].quantity > want + 1e-9:
                self._sell(sym, self.positions[sym].quantity - want, px, date, reasons.get(sym, "REBALANCE"))
        rate = (self.cost.commission_bps + self.cost.slippage_bps) / 10_000.0
        for sym, w in sorted(target_weights.items()):
            px = prices.get(sym)
            if w <= 0 or px is None or pd.isna(px) or px <= 0:
                continue
            have = self.positions[sym].quantity if sym in self.positions else 0.0
            add = w * eq / px - have
            if add <= 1e-9:
                continue
            affordable = self.cash / (px * (1.0 + rate))  # never spend more cash than available
            qty = min(add, max(affordable, 0.0))
            if qty <= 1e-9:
                continue
            fee = qty * px * rate
            self.cash -= qty * px + fee
            if sym in self.positions:
                p = self.positions[sym]
                total = p.quantity + qty
                p.entry_price = (p.entry_price * p.quantity + px * qty) / total
                p.quantity = total
                p.peak_price = max(p.peak_price, px)
            else:
                self.positions[sym] = PositionState(qty, px, px, day_index)
            self._record(SimulatedFill(date, sym, "BUY", qty, px, fee, "REBALANCE"))

    def accrue_interest(self, date: str) -> float:
        """Credit interest on positive cash for the calendar days since the previous accrual (first call: none)."""
        gained = 0.0
        if self._last_accrual is not None and self.cash > 0 and self.cash_rate_annual:
            days = (pd.Timestamp(date) - pd.Timestamp(self._last_accrual)).days
            if days > 0:
                gained = self.cash * ((1.0 + self.cash_rate_annual) ** (days / 365.0) - 1.0)
                self.cash += gained
                self.interest_earned += gained
        self._last_accrual = date
        return gained

    def mark(self, prices: Mapping[str, float], date: str) -> float:
        for sym, pos in self.positions.items():
            px = prices.get(sym)
            if px is not None and not pd.isna(px):
                pos.peak_price = max(pos.peak_price, px)
                self.last_price[sym] = float(px)
        eq = self.equity(prices)
        self.peak_equity = max(self.peak_equity, eq)
        self.equity_curve[date] = eq
        return eq

    def check_invariants(self) -> None:
        assert self.cash >= -1e-6, f"negative cash {self.cash}"
        assert all(p.quantity > 0 for p in self.positions.values()), "short or empty position"
