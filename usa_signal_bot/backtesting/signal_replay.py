"""Historical signal replay for the backtest engine."""
from dataclasses import dataclass, field
from typing import Any
from pathlib import Path
from datetime import datetime

from usa_signal_bot.core.enums import BacktestEventType, BacktestSignalMode, SignalAction
from usa_signal_bot.core.exceptions import BacktestSignalReplayError
import json
def load_jsonl(path):
    with open(path, 'r') as f:
        return [json.loads(line) for line in f if line.strip()]
from usa_signal_bot.strategies.signal_contract import StrategySignal
from usa_signal_bot.backtesting.event_models import BacktestEvent, create_backtest_event

@dataclass
class SignalReplayRequest:
    signal_file: str | None = None
    selected_candidates_file: str | None = None
    symbols: list[str] | None = None
    timeframe: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    signal_mode: BacktestSignalMode = BacktestSignalMode.WATCH_AS_LONG_CANDIDATE

@dataclass
class SignalReplayData:
    request: SignalReplayRequest
    signals: list[StrategySignal]
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def load_strategy_signals_from_file(path: Path) -> list[StrategySignal]:
    if not path.exists():
        raise BacktestSignalReplayError(f"Signal file not found: {path}")

    dicts = load_jsonl(path)
    signals = []
    for d in dicts:
        if "action" in d and isinstance(d["action"], str):
            d["action"] = SignalAction(d["action"])
        signals.append(StrategySignal(**d))
    return signals

def load_selected_candidates_as_signals(path: Path) -> list[StrategySignal]:
    if not path.exists():
        raise BacktestSignalReplayError(f"Selected candidates file not found: {path}")

    dicts = load_jsonl(path)
    signals = []
    for d in dicts:
        if "ranked_signal" in d and "signal" in d["ranked_signal"]:
            sig_dict = d["ranked_signal"]["signal"]
            if "action" in sig_dict and isinstance(sig_dict["action"], str):
                sig_dict["action"] = SignalAction(sig_dict["action"])
            signals.append(StrategySignal(**sig_dict))
    return signals

def filter_signals_for_replay(
    signals: list[StrategySignal],
    symbols: list[str] | None,
    timeframe: str | None,
    start_date: str | None,
    end_date: str | None
) -> list[StrategySignal]:
    filtered = []
    for sig in signals:
        if symbols and sig.symbol not in symbols:
            continue
        if timeframe and sig.timeframe != timeframe:
            continue

        dt = datetime.fromisoformat(sig.timestamp_utc.replace('Z', '+00:00'))
        if start_date:
            sd = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            if dt < sd:
                continue
        if end_date:
            ed = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            if dt > ed:
                continue
        filtered.append(sig)
    return filtered

def load_signals_for_replay(data_root: Path, request: SignalReplayRequest) -> SignalReplayData:
    signals = []
    warnings = []
    errors = []

    try:
        if request.signal_file:
            path = Path(request.signal_file)
            if not path.is_absolute():
                path = data_root.parent / path

            raw_signals = load_strategy_signals_from_file(path)
            signals = filter_signals_for_replay(
                raw_signals, request.symbols, request.timeframe, request.start_date, request.end_date
            )

        elif request.selected_candidates_file:
            path = Path(request.selected_candidates_file)
            if not path.is_absolute():
                path = data_root.parent / path

            raw_signals = load_selected_candidates_as_signals(path)
            signals = filter_signals_for_replay(
                raw_signals, request.symbols, request.timeframe, request.start_date, request.end_date
            )
        else:
            warnings.append("No signal file or candidates file provided.")

    except Exception as e:
        errors.append(f"Failed to load signals: {e}")

    if not signals and not errors and (request.signal_file or request.selected_candidates_file):
        warnings.append("No signals matched the filter criteria.")

    signals.sort(key=lambda s: s.timestamp_utc)

    return SignalReplayData(
        request=request,
        signals=signals,
        warnings=warnings,
        errors=errors
    )

def build_signal_events(data: SignalReplayData) -> list[BacktestEvent]:
    events = []
    for i, sig in enumerate(data.signals):
        payload = {
            "signal_id": sig.signal_id,
            "strategy_name": getattr(sig, 'strategy_name', ''),
            "action": sig.action.value,
            "confidence": sig.confidence,
            "score": sig.score,
            "signal_mode": data.request.signal_mode.value
        }
        event = create_backtest_event(
            event_type=BacktestEventType.SIGNAL,
            timestamp_utc=sig.timestamp_utc,
            symbol=sig.symbol,
            timeframe=sig.timeframe,
            payload=payload,
            sequence=10
        )
        events.append(event)
    return events

def validate_signal_replay_data(data: SignalReplayData) -> None:
    if data.errors:
        raise BacktestSignalReplayError(f"Errors loading signals: {data.errors}")
