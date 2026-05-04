"""The core backtest engine."""
from dataclasses import dataclass, field
from typing import Any
from pathlib import Path
from datetime import datetime, timezone
import uuid

from usa_signal_bot.core.enums import BacktestRunStatus, BacktestExitMode, BacktestOrderType, BacktestOrderSide, BacktestEventType, BacktestSignalMode
from usa_signal_bot.backtesting.order_models import BacktestOrderIntent, is_trade_order, signal_to_order_intent, SignalToOrderIntentConfig, build_exit_order_for_position
from usa_signal_bot.backtesting.transaction_costs import TransactionCostConfig
from usa_signal_bot.backtesting.slippage_models import SlippageConfig
from usa_signal_bot.backtesting.portfolio_models import BacktestPortfolio, BacktestPortfolioSnapshot, create_portfolio, apply_fill_to_portfolio, create_portfolio_snapshot
from usa_signal_bot.backtesting.order_models import BacktestOrderIntent
from usa_signal_bot.backtesting.fill_models import BacktestFill, simulate_market_fill, simulate_next_open_fill
from usa_signal_bot.backtesting.equity_curve import EquityCurve, build_equity_curve_from_snapshots
from usa_signal_bot.backtesting.backtest_metrics import BacktestMetrics, calculate_basic_backtest_metrics
from usa_signal_bot.backtesting.event_models import BacktestEvent, BacktestEventStream, sort_events_by_time_sequence
from usa_signal_bot.backtesting.market_replay import MarketReplayRequest, MarketReplayData, load_market_replay_data_from_cache, build_market_bar_events, get_next_bar_for_symbol
from usa_signal_bot.backtesting.signal_replay import SignalReplayRequest, SignalReplayData, load_signals_for_replay, build_signal_events

@dataclass
class BacktestRunConfig:
    starting_cash: float
    fee_rate: float
    slippage_bps: float
    signal_to_order: SignalToOrderIntentConfig
    exit_mode: BacktestExitMode
    hold_bars: int
    max_positions: int
    max_position_notional: float
    allow_fractional_quantity: bool
    transaction_cost_config: TransactionCostConfig | None = None
    slippage_config: SlippageConfig | None = None
    enable_advanced_metrics: bool = True
    build_trade_ledger: bool = True

@dataclass
class BacktestRunRequest:
    run_name: str
    symbols: list[str]
    timeframe: str
    provider_name: str = "yfinance"
    signal_file: str | None = None
    selected_candidates_file: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    config: BacktestRunConfig | None = None

@dataclass
class BacktestRunResult:
    run_id: str
    run_name: str
    status: BacktestRunStatus
    request: BacktestRunRequest
    portfolio: BacktestPortfolio
    snapshots: list[BacktestPortfolioSnapshot]
    fills: list[BacktestFill]
    order_intents: list[BacktestOrderIntent]
    equity_curve: EquityCurve
    metrics: BacktestMetrics
    events: list[BacktestEvent]
    warnings: list[str]
    errors: list[str]
    created_at_utc: str

class BacktestEngine:
    def __init__(self, data_root: Path):
        self.data_root = data_root

    def run(self, request: BacktestRunRequest) -> BacktestRunResult:
        run_id = str(uuid.uuid4())
        created_at_utc = datetime.now(timezone.utc).isoformat()
        warnings = []
        errors = []

        if not request.config:
            request.config = BacktestRunConfig(
                starting_cash=100000.0,
                fee_rate=0.0,
                slippage_bps=0.0,
                signal_to_order=SignalToOrderIntentConfig(allow_short=False),
                exit_mode=BacktestExitMode.HOLD_N_BARS,
                hold_bars=5,
                max_positions=10,
                max_position_notional=10000.0,
                allow_fractional_quantity=True
            )

        config = request.config

        market_data = self.prepare_market_replay(request)
        if market_data.warnings:
            warnings.extend(market_data.warnings)
        if market_data.errors:
            errors.extend(market_data.errors)

        signal_data = self.prepare_signal_replay(request)
        if signal_data.warnings:
            warnings.extend(signal_data.warnings)
        if signal_data.errors:
            errors.extend(signal_data.errors)

        stream = self.build_event_stream(market_data, signal_data)

        try:
            portfolio, snapshots, order_intents, fills = self.process_event_stream(
                stream, market_data, signal_data, config
            )
        except Exception as e:
            errors.append(f"Engine failure during process_event_stream: {e}")
            portfolio = create_portfolio(config.starting_cash)
            snapshots = []
            order_intents = []
            fills = []

        equity_curve = build_equity_curve_from_snapshots(snapshots, config.starting_cash)
        metrics = calculate_basic_backtest_metrics(config.starting_cash, equity_curve, fills)

        if portfolio.warnings:
            warnings.extend(portfolio.warnings)

        status = BacktestRunStatus.COMPLETED if not errors else BacktestRunStatus.FAILED
        if errors and fills:
            status = BacktestRunStatus.PARTIAL_SUCCESS

        return BacktestRunResult(
            run_id=run_id,
            run_name=request.run_name,
            status=status,
            request=request,
            portfolio=portfolio,
            snapshots=snapshots,
            fills=fills,
            order_intents=order_intents,
            equity_curve=equity_curve,
            metrics=metrics,
            events=stream.events,
            warnings=warnings,
            errors=errors,
            created_at_utc=created_at_utc
        )

    def prepare_market_replay(self, request: BacktestRunRequest) -> MarketReplayData:
        req = MarketReplayRequest(
            symbols=request.symbols,
            timeframe=request.timeframe,
            provider_name=request.provider_name,
            start_date=request.start_date,
            end_date=request.end_date
        )
        return load_market_replay_data_from_cache(self.data_root, req)

    def prepare_signal_replay(self, request: BacktestRunRequest) -> SignalReplayData:
        req = SignalReplayRequest(
            signal_file=request.signal_file,
            selected_candidates_file=request.selected_candidates_file,
            symbols=request.symbols,
            timeframe=request.timeframe,
            start_date=request.start_date,
            end_date=request.end_date,
            signal_mode=request.config.signal_to_order.signal_mode if request.config else BacktestSignalMode.WATCH_AS_LONG_CANDIDATE
        )
        return load_signals_for_replay(self.data_root, req)

    def build_event_stream(self, market_data: MarketReplayData, signal_data: SignalReplayData) -> BacktestEventStream:
        market_events = build_market_bar_events(market_data)
        signal_events = build_signal_events(signal_data)

        all_events = market_events + signal_events
        all_events = sort_events_by_time_sequence(all_events)

        return BacktestEventStream(
            stream_id=str(uuid.uuid4()),
            events=all_events,
            created_at_utc=datetime.now(timezone.utc).isoformat()
        )


    def process_event_stream(
        self,
        stream: BacktestEventStream,
        market_data: MarketReplayData,
        signal_data: SignalReplayData,
        config: BacktestRunConfig
    ) -> tuple[BacktestPortfolio, list[BacktestPortfolioSnapshot], list[BacktestOrderIntent], list[BacktestFill]]:

        portfolio = create_portfolio(config.starting_cash)
        snapshots = []
        order_intents = []
        fills = []

        current_prices: dict[str, float] = {}
        position_bars_held: dict[str, int] = {}
        signals_by_id = {s.signal_id: s for s in signal_data.signals}

        for event in stream.events:
            if event.event_type == BacktestEventType.MARKET_BAR:
                symbol = event.symbol
                if symbol:
                    current_prices[symbol] = event.payload["close"]

                for pos_symbol, position in portfolio.positions.items():
                    if position.side.value != "FLAT" and symbol == pos_symbol:
                        position_bars_held[pos_symbol] = position_bars_held.get(pos_symbol, 0) + 1

                        if config.exit_mode == BacktestExitMode.HOLD_N_BARS:
                            if position_bars_held[pos_symbol] >= config.hold_bars:
                                exit_order = build_exit_order_for_position(
                                    position,
                                    event.timestamp_utc,
                                    event.timeframe or "1d",
                                    f"Exit after {config.hold_bars} bars"
                                )
                                if exit_order:
                                    order_intents.append(exit_order)
                                    next_bar = get_next_bar_for_symbol(market_data, pos_symbol, event.timestamp_utc)
                                    if next_bar:
                                        fill = simulate_next_open_fill(exit_order, next_bar, config.fee_rate, config.slippage_bps)
                                    else:
                                        from usa_signal_bot.data.models import OHLCVBar
                                        mock_bar = OHLCVBar(symbol=pos_symbol, timestamp_utc=event.timestamp_utc, timeframe=event.timeframe or '1d', open=event.payload["open"], high=event.payload["high"], low=event.payload["low"], close=event.payload["close"], volume=100)
                                        fill = simulate_market_fill(exit_order, mock_bar, config.fee_rate, config.slippage_bps)

                                    fills.append(fill)
                                    portfolio = apply_fill_to_portfolio(portfolio, fill, current_prices.get(pos_symbol, 0.0))
                                    position_bars_held[pos_symbol] = 0

                snapshot = create_portfolio_snapshot(portfolio, current_prices, event.timestamp_utc)
                if snapshots and snapshots[-1].timestamp_utc == event.timestamp_utc:
                    snapshots[-1] = snapshot
                else:
                    snapshots.append(snapshot)

            elif event.event_type == BacktestEventType.SIGNAL:
                sig_id = event.payload.get("signal_id")
                if not sig_id or sig_id not in signals_by_id:
                    continue

                signal = signals_by_id[sig_id]

                open_pos_count = sum(1 for p in portfolio.positions.values() if p.side.value != "FLAT")

                if signal.symbol in portfolio.positions and portfolio.positions[signal.symbol].side.value != "FLAT":
                    continue

                if open_pos_count >= config.max_positions:
                    continue

                from usa_signal_bot.data.models import OHLCVBar
                price = current_prices.get(signal.symbol, 0.0)
                if price <= 0:
                    continue
                mock_bar = OHLCVBar(symbol=signal.symbol, timestamp_utc=event.timestamp_utc, timeframe=event.timeframe or '1d', open=price, high=price, low=price, close=price, volume=100)

                intent = signal_to_order_intent(signal, mock_bar, config.signal_to_order)
                if intent:
                    if config.max_position_notional and (intent.quantity * mock_bar.close) > config.max_position_notional:
                        if mock_bar.close > 0:
                            intent.quantity = config.max_position_notional / mock_bar.close

                    if not config.allow_fractional_quantity:
                        intent.quantity = int(intent.quantity)

                    if intent.quantity <= 0:
                        continue

                    order_intents.append(intent)

                    next_bar = get_next_bar_for_symbol(market_data, signal.symbol, event.timestamp_utc)
                    if next_bar:
                        fill = simulate_next_open_fill(intent, next_bar, config.fee_rate, config.slippage_bps)
                        fills.append(fill)
                        portfolio = apply_fill_to_portfolio(portfolio, fill, current_prices.get(signal.symbol, 0.0))
                        position_bars_held[signal.symbol] = 0

        return portfolio, snapshots, order_intents, fills


    def write_result(self, result: BacktestRunResult) -> list[Path]:
        from usa_signal_bot.backtesting.backtest_store import write_backtest_result_json, build_backtest_run_dir, write_backtest_events_jsonl, write_backtest_fills_jsonl, write_backtest_orders_jsonl, write_backtest_snapshots_jsonl, write_equity_curve_jsonl, write_backtest_metrics_json

        run_dir = build_backtest_run_dir(self.data_root, result.run_id)
        paths = []
        paths.append(write_backtest_result_json(run_dir / "result.json", result))
        paths.append(write_backtest_events_jsonl(run_dir / "events.jsonl", result.events))
        paths.append(write_backtest_fills_jsonl(run_dir / "fills.jsonl", result.fills))
        paths.append(write_backtest_orders_jsonl(run_dir / "orders.jsonl", result.order_intents))
        paths.append(write_backtest_snapshots_jsonl(run_dir / "snapshots.jsonl", result.snapshots))
        paths.append(write_equity_curve_jsonl(run_dir / "equity_curve.jsonl", result.equity_curve))
        paths.append(write_backtest_metrics_json(run_dir / "metrics.json", result.metrics))

        return paths
