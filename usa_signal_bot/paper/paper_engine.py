from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime, timezone
from dataclasses import dataclass
from pathlib import Path

from usa_signal_bot.core.enums import PaperExecutionMode, PaperOrderSide, PaperAccountStatus, PaperOrderStatus, PaperEngineStatus
from usa_signal_bot.paper.paper_models import (
    VirtualAccount, PaperOrderIntent, PaperOrder, PaperFill, PaperPosition,
    CashLedgerEntry, PaperEquitySnapshot, PaperTrade, PaperEngineRunResult,
    create_paper_run_id
)
from usa_signal_bot.paper.virtual_account import apply_cash_delta, update_account_equity
from usa_signal_bot.paper.paper_orders import create_paper_order, validate_paper_order_intent_for_account
from usa_signal_bot.paper.order_lifecycle import PaperOrderLifecycle
from usa_signal_bot.paper.price_resolver import LocalPriceResolver
from usa_signal_bot.paper.paper_fills import PaperFillConfig, simulate_paper_fill_from_bar
from usa_signal_bot.paper.paper_positions import update_paper_position_with_fill, paper_position_market_value
from usa_signal_bot.paper.cash_ledger import ledger_entries_from_fill
from usa_signal_bot.paper.equity_snapshots import create_paper_equity_snapshot
from usa_signal_bot.paper.paper_journal import build_paper_trades_from_fills, update_open_paper_trades_with_positions

@dataclass
class PaperEngineConfig:
    execution_mode: PaperExecutionMode
    starting_cash: float
    fee_bps: float
    slippage_bps: float
    allow_fractional_quantity: bool
    allow_short: bool
    max_positions: int
    max_order_notional: float
    max_total_exposure_pct: float
    reject_duplicate_symbol_position: bool
    write_outputs: bool

class PaperTradingEngine:
    def __init__(
        self,
        data_root: Path,
        account: Optional[VirtualAccount] = None,
        price_resolver: Optional[LocalPriceResolver] = None,
        config: Optional[PaperEngineConfig] = None
    ):
        self.data_root = data_root
        self.account = account
        self.price_resolver = price_resolver or LocalPriceResolver(data_root)

        self.config = config or PaperEngineConfig(
            execution_mode=PaperExecutionMode.DRY_RUN,
            starting_cash=100000.0,
            fee_bps=1.0,
            slippage_bps=2.0,
            allow_fractional_quantity=True,
            allow_short=False,
            max_positions=20,
            max_order_notional=10000.0,
            max_total_exposure_pct=0.80,
            reject_duplicate_symbol_position=True,
            write_outputs=False
        )

        self.lifecycle = PaperOrderLifecycle()
        self.fills: List[PaperFill] = []
        self.positions: Dict[str, PaperPosition] = {}
        self.ledger: List[CashLedgerEntry] = []

        self.warnings: List[str] = []
        self.errors: List[str] = []

    def _create_fallback_account(self) -> VirtualAccount:
        from usa_signal_bot.paper.virtual_account import create_virtual_account
        acct = create_virtual_account("engine_fallback", self.config.starting_cash)
        from usa_signal_bot.paper.cash_ledger import create_starting_cash_entry
        self.ledger.append(create_starting_cash_entry(acct))
        return acct

    def run_order_intents(self, intents: List[PaperOrderIntent]) -> PaperEngineRunResult:
        run_id = create_paper_run_id()

        if not self.account:
            self.account = self._create_fallback_account()

        orders = []
        fills = []

        for intent in intents:
            try:
                order = self.submit_order_intent(intent)
                orders.append(order)

                if self.config.execution_mode == PaperExecutionMode.VALIDATE_ONLY:
                    continue

                processed_order, fill = self.process_order(order)
                if fill:
                    fills.append(fill)
                    self.process_fill(fill)
            except Exception as e:
                self.errors.append(f"Error processing intent for {intent.symbol}: {e}")

        snapshot = self.mark_to_market()

        trades = build_paper_trades_from_fills(self.fills)
        update_open_paper_trades_with_positions(trades, list(self.positions.values()))

        update_account_equity(
            self.account,
            list(self.positions.values()),
            {s: p.market_price for s, p in self.positions.items() if p.market_price is not None}
        )

        result = self.build_run_result(run_id, orders, self.fills, self.warnings, self.errors)
        result.equity_snapshots = [snapshot]
        result.trades = trades
        result.cash_ledger = self.ledger

        if self.config.write_outputs:
            self.write_result(result)

        return result

    def submit_order_intent(self, intent: PaperOrderIntent) -> PaperOrder:
        if not self.account:
            self.account = self._create_fallback_account()

        order = create_paper_order(self.account, intent)
        order = self.lifecycle.validate(order)

        is_valid, reject_reason, warnings = validate_paper_order_intent_for_account(self.account, intent)
        if warnings:
            self.warnings.extend(warnings)

        if not is_valid:
            return self.lifecycle.reject(order, reject_reason)

        estimated_price = 0.0
        if self.config.execution_mode != PaperExecutionMode.VALIDATE_ONLY:
            snap = self.price_resolver.resolve_latest_price(intent.symbol, intent.timeframe)
            if snap:
                estimated_price = snap.price

        estimated_notional = intent.notional or (intent.quantity * estimated_price)

        if estimated_notional > self.config.max_order_notional:
            from usa_signal_bot.core.enums import PaperRejectReason
            return self.lifecycle.reject(order, PaperRejectReason.VALIDATION_FAILED, "Max order notional exceeded")

        if intent.side == PaperOrderSide.BUY and self.config.reject_duplicate_symbol_position:
            pos = self.positions.get(intent.symbol)
            if pos and pos.quantity > 0:
                from usa_signal_bot.core.enums import PaperRejectReason
                return self.lifecycle.reject(order, PaperRejectReason.DUPLICATE_POSITION)

        if intent.side == PaperOrderSide.SELL and not self.config.allow_short:
            pos = self.positions.get(intent.symbol)
            if not pos or pos.quantity < intent.quantity:
                from usa_signal_bot.core.enums import PaperRejectReason
                return self.lifecycle.reject(order, PaperRejectReason.SHORT_NOT_ALLOWED, "Short selling not allowed")

        return self.lifecycle.accept(order)

    def process_order(self, order: PaperOrder) -> Tuple[PaperOrder, Optional[PaperFill]]:
        if order.status != PaperOrderStatus.ACCEPTED:
            return order, None

        order = self.lifecycle.queue(order)

        intent = order.intent

        if self.config.execution_mode == PaperExecutionMode.DRY_RUN:
            order.status = PaperOrderStatus.SKIPPED
            order.message = "Dry run mode - no fill simulated"
            return order, None

        bar = self.price_resolver.resolve_bar_for_order(intent.symbol, intent.timeframe, intent.order_type)

        if not bar:
            from usa_signal_bot.core.enums import PaperRejectReason
            self.warnings.append(f"No market data found for {intent.symbol} {intent.timeframe}")
            order = self.lifecycle.reject(order, PaperRejectReason.MARKET_DATA_MISSING)
            return order, None

        fill_config = PaperFillConfig(
            fee_bps=self.config.fee_bps,
            slippage_bps=self.config.slippage_bps,
            allow_partial_fills=False
        )

        fill = simulate_paper_fill_from_bar(order, bar, fill_config)

        if fill.side == PaperOrderSide.BUY:
            if self.account.cash + fill.net_cash_impact < 0:
                from usa_signal_bot.core.enums import PaperRejectReason
                order = self.lifecycle.reject(order, PaperRejectReason.INSUFFICIENT_CASH)
                return order, None

            open_pos_count = sum(1 for p in self.positions.values() if p.quantity > 0)
            if intent.symbol not in self.positions or self.positions[intent.symbol].quantity == 0:
                if open_pos_count >= self.config.max_positions:
                    from usa_signal_bot.core.enums import PaperRejectReason
                    order = self.lifecycle.reject(order, PaperRejectReason.MAX_POSITIONS_EXCEEDED)
                    return order, None

        order = self.lifecycle.fill(order, fill)
        return order, fill

    def process_fill(self, fill: PaperFill) -> None:
        self.fills.append(fill)

        apply_cash_delta(self.account, fill.net_cash_impact, allow_negative_cash=False)

        entries = ledger_entries_from_fill(self.account, fill, self.account.cash)
        self.ledger.extend(entries)

        pos = self.positions.get(fill.symbol)
        updated_pos = update_paper_position_with_fill(pos, fill)
        self.positions[fill.symbol] = updated_pos

    def mark_to_market(self, symbols: Optional[List[str]] = None, timeframe: str = "1d") -> PaperEquitySnapshot:
        if not self.account:
            self.account = self._create_fallback_account()

        syms_to_check = symbols or list(self.positions.keys())
        prices = {}

        if syms_to_check and self.config.execution_mode != PaperExecutionMode.VALIDATE_ONLY:
            price_snaps = self.price_resolver.resolve_many_latest(syms_to_check, timeframe)
            prices = {sym: snap.price for sym, snap in price_snaps.items()}

        now_utc = datetime.now(timezone.utc).isoformat()
        return create_paper_equity_snapshot(self.account, list(self.positions.values()), prices, now_utc)

    def current_positions(self) -> List[PaperPosition]:
        return list(self.positions.values())

    def current_account(self) -> VirtualAccount:
        return self.account if self.account else self._create_fallback_account()

    def build_run_result(
        self,
        run_id: str,
        orders: List[PaperOrder],
        fills: List[PaperFill],
        warnings: List[str],
        errors: List[str]
    ) -> PaperEngineRunResult:

        if errors:
            status = PaperEngineStatus.FAILED
        elif warnings or any(o.status == PaperOrderStatus.REJECTED for o in orders):
            status = PaperEngineStatus.PARTIAL_SUCCESS
        elif not orders:
            status = PaperEngineStatus.EMPTY
        else:
            status = PaperEngineStatus.COMPLETED

        return PaperEngineRunResult(
            run_id=run_id,
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            status=status,
            account=self.current_account(),
            orders=orders,
            fills=fills,
            positions=self.current_positions(),
            cash_ledger=self.ledger,
            equity_snapshots=[],
            trades=[],
            output_paths={},
            warnings=warnings,
            errors=errors
        )

    def write_result(self, result: PaperEngineRunResult) -> List[Path]:
        from usa_signal_bot.paper.paper_store import (
            build_paper_run_dir, write_paper_engine_run_result_json,
            write_virtual_account_json, write_paper_orders_jsonl,
            write_paper_fills_jsonl, write_paper_positions_jsonl,
            write_cash_ledger_jsonl, write_paper_equity_snapshots_jsonl,
            write_paper_trades_jsonl, build_paper_account_dir
        )

        paths = []
        run_dir = build_paper_run_dir(self.data_root, result.run_id)

        p_res = write_paper_engine_run_result_json(run_dir / "result.json", result)
        paths.append(p_res)
        result.output_paths["result"] = str(p_res)

        if result.orders:
            p = write_paper_orders_jsonl(run_dir / "orders.jsonl", result.orders)
            paths.append(p)
            result.output_paths["orders"] = str(p)

        if result.fills:
            p = write_paper_fills_jsonl(run_dir / "fills.jsonl", result.fills)
            paths.append(p)
            result.output_paths["fills"] = str(p)

        if result.positions:
            p = write_paper_positions_jsonl(run_dir / "positions.jsonl", result.positions)
            paths.append(p)
            result.output_paths["positions"] = str(p)

        if result.cash_ledger:
            p = write_cash_ledger_jsonl(run_dir / "cash_ledger.jsonl", result.cash_ledger)
            paths.append(p)
            result.output_paths["cash_ledger"] = str(p)

        if result.equity_snapshots:
            p = write_paper_equity_snapshots_jsonl(run_dir / "equity_snapshots.jsonl", result.equity_snapshots)
            paths.append(p)
            result.output_paths["equity_snapshots"] = str(p)

        if result.trades:
            p = write_paper_trades_jsonl(run_dir / "trades.jsonl", result.trades)
            paths.append(p)
            result.output_paths["trades"] = str(p)

        if result.account:
            acct_dir = build_paper_account_dir(self.data_root, result.account.account_id)
            p = write_virtual_account_json(acct_dir / "account.json", result.account)
            paths.append(p)
            result.output_paths["account"] = str(p)

        return paths
