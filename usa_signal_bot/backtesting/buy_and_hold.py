from dataclasses import dataclass, field
from typing import Optional

from usa_signal_bot.data.models import OHLCVBar
from usa_signal_bot.backtesting.benchmark_models import BenchmarkEquityCurve, BenchmarkSpec
from usa_signal_bot.backtesting.equity_curve import EquityCurvePoint
from usa_signal_bot.core.enums import BenchmarkType

@dataclass
class BuyAndHoldConfig:
    starting_cash: float
    symbol: str
    timeframe: str
    allow_fractional_quantity: bool = True
    fee_rate: float = 0.0
    slippage_bps: float = 0.0
    invest_at: str = "first_open"
    exit_at: str = "last_close"

@dataclass
class BuyAndHoldResult:
    symbol: str
    timeframe: str
    starting_cash: float
    quantity: float
    entry_price: Optional[float]
    exit_price: Optional[float]
    ending_equity: Optional[float]
    total_return: Optional[float]
    total_return_pct: Optional[float]
    equity_curve: BenchmarkEquityCurve
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def default_buy_and_hold_config(symbol: str = "SPY", timeframe: str = "1d", starting_cash: float = 100000.0) -> BuyAndHoldConfig:
    return BuyAndHoldConfig(
        starting_cash=starting_cash,
        symbol=symbol,
        timeframe=timeframe
    )

def validate_buy_and_hold_config(config: BuyAndHoldConfig) -> None:
    if config.starting_cash <= 0:
        raise ValueError("starting_cash must be > 0")
    if config.invest_at != "first_open":
        raise ValueError("invest_at must be 'first_open'")
    if config.exit_at != "last_close":
        raise ValueError("exit_at must be 'last_close'")

def build_cash_baseline(starting_cash: float, timestamps: list[str]) -> BenchmarkEquityCurve:
    points = []
    for ts in timestamps:
        points.append(EquityCurvePoint(
            timestamp_utc=ts,
            equity=starting_cash,
            cash=starting_cash,
            realized_pnl=0.0,
            unrealized_pnl=0.0,
            drawdown=0.0,
            drawdown_pct=0.0
        ))

    spec = BenchmarkSpec(benchmark_id="CASH", name="Cash", symbol="CASH", benchmark_type=BenchmarkType.CASH)
    return BenchmarkEquityCurve(
        benchmark=spec,
        points=points,
        starting_cash=starting_cash,
        ending_equity=starting_cash,
        total_return_pct=0.0,
        warnings=[],
        errors=[]
    )

def build_buy_and_hold_equity_curve(
    bars: list[OHLCVBar],
    quantity: float,
    starting_cash: float,
    benchmark_spec: BenchmarkSpec
) -> BenchmarkEquityCurve:
    if not bars:
        return BenchmarkEquityCurve(
            benchmark=benchmark_spec,
            points=[],
            starting_cash=starting_cash,
            ending_equity=None,
            total_return_pct=None,
            errors=["No bars provided"]
        )

    points = []
    entry_price = bars[0].open
    cash_remaining = starting_cash - (quantity * entry_price)

    max_equity = starting_cash

    for bar in bars:
        current_value = quantity * bar.close
        equity = cash_remaining + current_value
        max_equity = max(max_equity, equity)
        drawdown = max_equity - equity
        drawdown_pct = (drawdown / max_equity) if max_equity > 0 else 0.0

        points.append(EquityCurvePoint(
            timestamp_utc=bar.timestamp_utc,
            equity=equity,
            cash=cash_remaining,
            realized_pnl=0.0,
            unrealized_pnl=current_value - (quantity * entry_price),
            drawdown=drawdown,
            drawdown_pct=drawdown_pct
        ))

    ending_equity = points[-1].equity
    return_pct = ((ending_equity - starting_cash) / starting_cash) * 100.0 if starting_cash > 0 else 0.0

    return BenchmarkEquityCurve(
        benchmark=benchmark_spec,
        points=points,
        starting_cash=starting_cash,
        ending_equity=ending_equity,
        total_return_pct=return_pct
    )

def run_buy_and_hold_baseline(
    bars: list[OHLCVBar],
    config: BuyAndHoldConfig,
    benchmark_spec: Optional[BenchmarkSpec] = None
) -> BuyAndHoldResult:
    warnings = []
    errors = []

    try:
        validate_buy_and_hold_config(config)
    except ValueError as e:
        errors.append(str(e))
        return BuyAndHoldResult(
            symbol=config.symbol,
            timeframe=config.timeframe,
            starting_cash=config.starting_cash,
            quantity=0.0, entry_price=None, exit_price=None,
            ending_equity=None, total_return=None, total_return_pct=None,
            equity_curve=BenchmarkEquityCurve(
                benchmark=benchmark_spec or BenchmarkSpec(benchmark_id="ERR", name="ERR", symbol="ERR", benchmark_type=BenchmarkType.CUSTOM_SYMBOL),
                points=[], starting_cash=config.starting_cash, ending_equity=None, total_return_pct=None
            ),
            warnings=warnings,
            errors=errors
        )

    if not bars:
        errors.append("No bars provided")
        return BuyAndHoldResult(
            symbol=config.symbol, timeframe=config.timeframe, starting_cash=config.starting_cash,
            quantity=0.0, entry_price=None, exit_price=None,
            ending_equity=None, total_return=None, total_return_pct=None,
            equity_curve=BenchmarkEquityCurve(
                benchmark=benchmark_spec or BenchmarkSpec(benchmark_id="ERR", name="ERR", symbol="ERR", benchmark_type=BenchmarkType.CUSTOM_SYMBOL),
                points=[], starting_cash=config.starting_cash, ending_equity=None, total_return_pct=None
            ),
            warnings=warnings, errors=errors
        )

    entry_price = bars[0].open
    exit_price = bars[-1].close

    if entry_price <= 0:
        errors.append(f"Invalid entry price: {entry_price}")

    quantity = config.starting_cash / entry_price if entry_price > 0 else 0.0
    if not config.allow_fractional_quantity:
        quantity = float(int(quantity))

    spec = benchmark_spec or BenchmarkSpec(
        benchmark_id=config.symbol,
        name=config.symbol,
        symbol=config.symbol,
        benchmark_type=BenchmarkType.CUSTOM_SYMBOL
    )

    curve = build_buy_and_hold_equity_curve(bars, quantity, config.starting_cash, spec)

    ending_equity = curve.ending_equity
    total_return = ending_equity - config.starting_cash if ending_equity is not None else None

    return BuyAndHoldResult(
        symbol=config.symbol,
        timeframe=config.timeframe,
        starting_cash=config.starting_cash,
        quantity=quantity,
        entry_price=entry_price,
        exit_price=exit_price,
        ending_equity=ending_equity,
        total_return=total_return,
        total_return_pct=curve.total_return_pct,
        equity_curve=curve,
        warnings=warnings,
        errors=errors
    )

def buy_and_hold_result_to_dict(result: BuyAndHoldResult) -> dict:
    from usa_signal_bot.backtesting.benchmark_models import benchmark_equity_curve_to_dict
    return {
        "symbol": result.symbol,
        "timeframe": result.timeframe,
        "starting_cash": result.starting_cash,
        "quantity": result.quantity,
        "entry_price": result.entry_price,
        "exit_price": result.exit_price,
        "ending_equity": result.ending_equity,
        "total_return": result.total_return,
        "total_return_pct": result.total_return_pct,
        "equity_curve": benchmark_equity_curve_to_dict(result.equity_curve),
        "warnings": result.warnings,
        "errors": result.errors
    }

def buy_and_hold_result_to_text(result: BuyAndHoldResult) -> str:
    lines = [
        f"Buy and Hold Baseline for {result.symbol} ({result.timeframe})",
        f"Starting Cash: ${result.starting_cash:.2f}",
    ]
    if result.errors:
        lines.append(f"Errors: {result.errors}")
    else:
        lines.append(f"Quantity: {result.quantity:.4f}")
        lines.append(f"Entry Price: ${result.entry_price:.2f}")
        lines.append(f"Exit Price: ${result.exit_price:.2f}")
        lines.append(f"Ending Equity: ${result.ending_equity:.2f}")
        lines.append(f"Total Return: ${result.total_return:.2f} ({result.total_return_pct:.2f}%)")
    return "\n".join(lines)
