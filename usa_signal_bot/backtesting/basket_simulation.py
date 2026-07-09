from pathlib import Path
from datetime import datetime
from usa_signal_bot.backtesting.basket_models import (
    BasketSimulationResult,
    BasketReplayRequest,
    BasketSimulationConfig,
    BasketReplayData,
    create_basket_simulation_run_id,
)
from usa_signal_bot.backtesting.basket_replay import load_basket_replay_data
from usa_signal_bot.core.enums import (
    BasketSimulationStatus,
    BasketReviewStatus,
    BasketEntryMode,
    BasketExitMode,
)
from usa_signal_bot.data.cache import read_cached_bars_for_symbols_timeframe
from usa_signal_bot.data.models import OHLCVBar, MarketDataRequest, MarketDataResponse
from usa_signal_bot.backtesting.order_models import (
    BacktestOrderIntent,
    BacktestOrderType,
)
from usa_signal_bot.backtesting.portfolio_models import BacktestPortfolio
from usa_signal_bot.backtesting.trade_ledger import (
    TradeLedger,
    build_trade_ledger_from_fills,
)
from usa_signal_bot.backtesting.allocation_adapter import (
    default_allocation_to_order_config,
    replay_item_to_order_intent,
    build_exit_order_for_basket_position,
)
from usa_signal_bot.backtesting.basket_metrics import (
    calculate_basket_metrics,
    basket_metrics_to_dict,
)
from usa_signal_bot.backtesting.allocation_drift import (
    build_basket_exposure_snapshot,
    calculate_target_weights_from_replay_items,
)
from usa_signal_bot.core.exceptions import BasketSimulationError


class BasketSimulationEngine:
    def __init__(self, data_root: Path):
        self.data_root = data_root

    def run(
        self, request: BasketReplayRequest, config: BasketSimulationConfig
    ) -> BasketSimulationResult:
        run_id = create_basket_simulation_run_id()
        created_at_utc = datetime.utcnow().isoformat()

        try:
            replay_data = self.prepare_replay_data(request)
            result = self.process_basket_simulation(
                run_id, created_at_utc, replay_data, config
            )
            return result
        except Exception as e:
            return BasketSimulationResult(
                run_id=run_id,
                created_at_utc=created_at_utc,
                status=BasketSimulationStatus.FAILED,
                request=request,
                config=config,
                replay_data=BasketReplayData(
                    request, [], [], request.timeframe, [], []
                ),
                portfolio=BacktestPortfolio(
                    config.starting_cash,
                    config.starting_cash,
                    {},
                    0.0,
                    0.0,
                    config.starting_cash,
                    created_at_utc,
                ),
                snapshots=[],
                basket_exposure_snapshots=[],
                order_intents=[],
                fills=[],
                trade_ledger=TradeLedger(
                    trades=[], closed_pnl=0.0, win_count=0, loss_count=0
                ),
                basket_metrics={},
                benchmark_summary={},
                review_status=BasketReviewStatus.FAILED,
                warnings=[],
                errors=[str(e)],
            )

    def prepare_replay_data(self, request: BasketReplayRequest) -> BasketReplayData:
        return load_basket_replay_data(self.data_root, request)

    def prepare_market_data(
        self, replay_data: BasketReplayData, request: BasketReplayRequest
    ) -> dict[str, list[OHLCVBar]]:
        bars_by_symbol = {}
        for symbol in replay_data.symbols:
            bars = read_cached_bars_for_symbols_timeframe(
                self.data_root, [symbol], request.timeframe, request.provider_name
            )
            bars_by_symbol[symbol] = bars
        return bars_by_symbol

    def process_basket_simulation(
        self,
        run_id: str,
        created_at_utc: str,
        replay_data: BasketReplayData,
        config: BasketSimulationConfig,
    ) -> BasketSimulationResult:
        if not replay_data.items:
            raise BasketSimulationError("No replay items found to simulate.")

        bars_by_symbol = self.prepare_market_data(replay_data, replay_data.request)
        sorted_timestamps = self._extract_sorted_timestamps(bars_by_symbol)

        portfolio = BacktestPortfolio(
            config.starting_cash,
            config.starting_cash,
            {},
            0.0,
            0.0,
            config.starting_cash,
            None,
        )

        simulation_state = {
            "portfolio": portfolio,
            "order_intents": [],
            "fills": [],
            "exposure_snapshots": [],
            "warnings": list(replay_data.warnings),
            "errors": list(replay_data.errors),
            "pending_orders": [],
            "items_to_process": list(replay_data.items),
        }

        target_weights = calculate_target_weights_from_replay_items(replay_data.items)
        alloc_config = default_allocation_to_order_config()
        alloc_config.replay_mode = config.allocation_replay_mode
        alloc_config.allow_fractional_quantity = config.allow_fractional_quantity

        self._run_simulation_loop(
            sorted_timestamps,
            bars_by_symbol,
            simulation_state,
            config,
            replay_data,
            alloc_config,
            target_weights,
        )

        return self._build_simulation_result(
            run_id, created_at_utc, replay_data, config, simulation_state
        )

    def _run_simulation_loop(
        self,
        sorted_timestamps: list[str],
        bars_by_symbol: dict[str, list[OHLCVBar]],
        state: dict,
        config: BasketSimulationConfig,
        replay_data: BasketReplayData,
        alloc_config: "AllocationConfig",
        target_weights: dict,
    ) -> None:
        for t_idx, ts in enumerate(sorted_timestamps):
            state["portfolio"].timestamp_utc = ts
            current_prices = self._get_current_prices(bars_by_symbol, ts)

            state["pending_orders"] = self._process_pending_orders(
                state["portfolio"],
                state["pending_orders"],
                current_prices,
                ts,
                state["fills"],
            )

            self._process_hold_n_bars_exits(
                config,
                t_idx,
                state["portfolio"],
                ts,
                replay_data,
                state["order_intents"],
                state["pending_orders"],
            )

            eligible_items, state["items_to_process"] = (
                self._get_eligible_items_and_update_queue(
                    config, t_idx, ts, state["items_to_process"]
                )
            )

            self._process_entries(
                eligible_items,
                current_prices,
                state["portfolio"],
                config,
                state["warnings"],
                ts,
                alloc_config,
                state["order_intents"],
                state["pending_orders"],
            )

            self._process_end_of_data_exits(
                config,
                t_idx,
                sorted_timestamps,
                state["portfolio"],
                ts,
                replay_data,
                current_prices,
                state["fills"],
            )

            if current_prices:
                snap = build_basket_exposure_snapshot(
                    ts, state["portfolio"], current_prices, target_weights
                )
                state["exposure_snapshots"].append(snap)

    def _build_simulation_result(
        self,
        run_id: str,
        created_at_utc: str,
        replay_data: BasketReplayData,
        config: BasketSimulationConfig,
        state: dict,
    ) -> BasketSimulationResult:
        trade_ledger = build_trade_ledger_from_fills(state["fills"])

        res = BasketSimulationResult(
            run_id=run_id,
            created_at_utc=created_at_utc,
            status=BasketSimulationStatus.COMPLETED,
            request=replay_data.request,
            config=config,
            replay_data=replay_data,
            portfolio=state["portfolio"],
            snapshots=[],
            basket_exposure_snapshots=state["exposure_snapshots"],
            order_intents=state["order_intents"],
            fills=state["fills"],
            trade_ledger=trade_ledger,
            basket_metrics={},
            benchmark_summary={},
            review_status=BasketReviewStatus.ACCEPTABLE,
            warnings=state["warnings"],
            errors=state["errors"],
        )

        m = calculate_basket_metrics(res)
        res.basket_metrics = basket_metrics_to_dict(m)

        return res

    def _extract_sorted_timestamps(self, bars_by_symbol):
        all_timestamps = set()
        for bars in bars_by_symbol.values():
            for b in bars:
                all_timestamps.add(b.timestamp_utc)
        return sorted(list(all_timestamps))

    def _get_current_prices(self, bars_by_symbol, ts):
        current_prices = {}
        for sym, bars in bars_by_symbol.items():
            bar_match = [b for b in bars if b.timestamp_utc == ts]
            if bar_match:
                current_prices[sym] = bar_match[0].close
        return current_prices

    def _process_pending_orders(
        self, portfolio, pending_orders, current_prices, ts, fills
    ):
        still_pending = []
        for order in pending_orders:
            sym = order.symbol
            if sym in current_prices:
                fill = portfolio.process_fill(
                    order, current_prices[sym], ts, fees=0.0, slippage_cost=0.0
                )
                if fill:
                    fills.append(fill)
            else:
                still_pending.append(order)
        return still_pending

    def _process_hold_n_bars_exits(
        self, config, t_idx, portfolio, ts, replay_data, order_intents, pending_orders
    ):
        if config.exit_mode == BasketExitMode.HOLD_N_BARS:
            for sym, pos in list(portfolio.positions.items()):
                if t_idx >= config.hold_bars:
                    exit_order = build_exit_order_for_basket_position(
                        pos, ts, replay_data.timeframe, "hold_n_bars"
                    )
                    if exit_order:
                        order_intents.append(exit_order)
                        pending_orders.append(exit_order)

    def _get_eligible_items_and_update_queue(self, config, t_idx, ts, items_to_process):
        eligible_items = []
        if config.entry_mode == BasketEntryMode.ENTER_ALL_AT_START:
            if t_idx == 0:
                eligible_items = items_to_process
                items_to_process = []
        elif config.entry_mode == BasketEntryMode.ENTER_ON_SIGNAL_TIME:
            eligible_items = [
                i for i in items_to_process if i.timestamp_utc and i.timestamp_utc <= ts
            ]
            items_to_process = [
                i
                for i in items_to_process
                if not i.timestamp_utc or i.timestamp_utc > ts
            ]
        return eligible_items, items_to_process

    def _process_entries(
        self,
        eligible_items,
        current_prices,
        portfolio,
        config,
        warnings,
        ts,
        alloc_config,
        order_intents,
        pending_orders,
    ):
        for item in eligible_items:
            if item.symbol in current_prices:
                if (
                    len(portfolio.positions) >= config.max_positions
                    and item.symbol not in portfolio.positions
                ):
                    warnings.append(
                        f"Max positions {config.max_positions} reached, skipping {item.symbol}"
                    )
                    continue
                bar = OHLCVBar(
                    symbol=item.symbol,
                    timestamp_utc=ts,
                    close=current_prices[item.symbol],
                )
                intent = replay_item_to_order_intent(
                    item, bar, portfolio.calculate_equity(current_prices), alloc_config
                )
                if intent:
                    order_intents.append(intent)
                    pending_orders.append(intent)

    def _process_end_of_data_exits(
        self,
        config,
        t_idx,
        sorted_timestamps,
        portfolio,
        ts,
        replay_data,
        current_prices,
        fills,
    ):
        if (
            config.exit_mode == BasketExitMode.END_OF_DATA
            and t_idx == len(sorted_timestamps) - 1
        ):
            for sym, pos in list(portfolio.positions.items()):
                exit_order = build_exit_order_for_basket_position(
                    pos, ts, replay_data.timeframe, "end_of_data"
                )
                if exit_order:
                    if sym in current_prices:
                        fill = portfolio.process_fill(
                            exit_order,
                            current_prices[sym],
                            ts,
                            fees=0.0,
                            slippage_cost=0.0,
                        )
                        if fill:
                            fills.append(fill)
